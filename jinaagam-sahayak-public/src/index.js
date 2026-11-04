// Cloudflare Worker — serves the static site (via the ASSETS binding) and handles POST /api/ask.
//
// The Anthropic API key never reaches the browser; two independent cost guards sit in front of
// the call: a shared access code (not a real login — one phrase everyone with the link types
// once), and per-IP + whole-site rate limits tracked in KV (Workers run on many edge nodes with
// no shared memory, so KV is the only place a count survives between requests).
//
// Required bindings (set via `wrangler.toml` / dashboard):
//   env.ANTHROPIC_API_KEY  — secret, from console.anthropic.com
//   env.ACCESS_CODE        — secret, the shared phrase (pick anything, e.g. "jinagam2026")
//   env.RATE_LIMIT_KV      — KV namespace binding
//   env.ASSETS             — static assets binding (set automatically by the [assets] config)
//
// Optional: env.PER_IP_LIMIT (default 6/min), env.DAILY_LIMIT (default 250/day), env.MODEL.

const DEFAULT_PER_IP_LIMIT = 6;
const DEFAULT_DAILY_LIMIT = 250;
const DEFAULT_MODEL = "claude-sonnet-5-5";
const MAX_TOKENS = 700;
const MAX_CONTEXT_CHARS = 6000;

function json(data, status) {
  return new Response(JSON.stringify(data), {
    status: status || 200,
    headers: { "content-type": "application/json; charset=utf-8" },
  });
}

async function kvIncr(kv, key, ttlSeconds) {
  const current = parseInt((await kv.get(key)) || "0", 10);
  const next = current + 1;
  await kv.put(key, String(next), { expirationTtl: ttlSeconds });
  return next;
}

async function handleAsk(request, env) {
  const code = request.headers.get("x-access-code") || "";
  if (!env.ACCESS_CODE || code !== env.ACCESS_CODE) {
    return json({ error: "bad_code", message: "एक्सेस-कोड गलत है।" }, 401);
  }
  if (!env.RATE_LIMIT_KV || !env.ANTHROPIC_API_KEY) {
    return json({ error: "misconfigured", message: "सर्वर अभी सही से सेटअप नहीं है — ANTHROPIC_API_KEY या RATE_LIMIT_KV बाइंडिंग गायब है।" }, 500);
  }

  const ip = request.headers.get("cf-connecting-ip") || "unknown";
  const now = new Date();
  const minuteBucket = Math.floor(now.getTime() / 60000);
  const dayBucket = now.toISOString().slice(0, 10);

  const perIpLimit = parseInt(env.PER_IP_LIMIT || "", 10) || DEFAULT_PER_IP_LIMIT;
  const dailyLimit = parseInt(env.DAILY_LIMIT || "", 10) || DEFAULT_DAILY_LIMIT;

  const ipCount = await kvIncr(env.RATE_LIMIT_KV, `ip:${ip}:${minuteBucket}`, 70);
  if (ipCount > perIpLimit) {
    return json({ error: "rate_limited", message: "थोड़ा धीरे — एक मिनट में सीमा पार हो गई। कुछ देर बाद फिर कोशिश करें।" }, 429);
  }
  const dayCount = await kvIncr(env.RATE_LIMIT_KV, `day:${dayBucket}`, 60 * 60 * 25);
  if (dayCount > dailyLimit) {
    return json({ error: "daily_limit", message: "आज की कुल सीमा पूरी हो गई है — कल फिर कोशिश करें।" }, 429);
  }

  let body;
  try {
    body = await request.json();
  } catch (e) {
    return json({ error: "bad_request", message: "अनुरोध पढ़ा नहीं जा सका।" }, 400);
  }
  const question = (body && body.question || "").toString().trim().slice(0, 600);
  let contextText = (body && body.context || "").toString();
  if (contextText.length > MAX_CONTEXT_CHARS) contextText = contextText.slice(0, MAX_CONTEXT_CHARS);
  if (!question) {
    return json({ error: "bad_request", message: "प्रश्न खाली है।" }, 400);
  }

  const prompt = `आप "जिनागम कोश" के एक सहायक हैं — जैन-दर्शन के ग्रन्थों (अष्टसहस्री, न्यायकुमुदचन्द्र, ` +
    `सिद्धिविनिश्चयटीका, प्रमेयकमल आदि) की आधुनिक हिन्दी व्याख्या पर आधारित। नीचे दिए गए ग्रन्थ-अंश ` +
    `ही आपका प्रमुख आधार हैं।\n\nग्रन्थ-अंश:\n${contextText || "(कोई सीधा मिलान नहीं मिला)"}\n\n` +
    `प्रश्न: ${question}\n\n` +
    `निर्देश: ऊपर के अंशों के आधार पर स्पष्ट, संक्षिप्त उत्तर हिन्दी में दीजिए (लगभग 100-180 शब्द)। ` +
    `जहाँ किसी अंश का प्रयोग करें वहाँ [1], [2] जैसे अंक से सन्दर्भ दें। अंशों में सीधा उत्तर न मिले तो ` +
    `अपने सामान्य ज्ञान से बताएं, पर स्पष्ट कहें कि यह किसी विशेष उद्धृत ग्रन्थ-अंश पर आधारित नहीं है। ` +
    `सम्प्रदाय/उप-सम्प्रदाय के नाम (जैसे दिगम्बर, श्वेताम्बर आदि) मत लिखिए — केवल दार्शनिक सिद्धान्त की बात कीजिए।`;

  let resp;
  try {
    resp = await fetch("https://api.anthropic.com/v1/messages", {
      method: "POST",
      headers: {
        "content-type": "application/json",
        "x-api-key": env.ANTHROPIC_API_KEY,
        "anthropic-version": "2023-06-01",
      },
      body: JSON.stringify({
        model: env.MODEL || DEFAULT_MODEL,
        max_tokens: MAX_TOKENS,
        messages: [{ role: "user", content: prompt }],
      }),
    });
  } catch (e) {
    return json({ error: "upstream_unreachable", message: "Claude API से सम्पर्क नहीं हो पाया।" }, 502);
  }

  if (!resp.ok) {
    const detail = await resp.text().catch(() => "");
    return json({ error: "upstream_error", message: "Claude API ने त्रुटि दी।", status: resp.status, detail: detail.slice(0, 300) }, 502);
  }

  const data = await resp.json();
  const text = (data.content || []).map((b) => b.text || "").join("");
  return json({ text });
}

export default {
  async fetch(request, env, ctx) {
    const url = new URL(request.url);
    if (url.pathname === "/api/ask") {
      if (request.method !== "POST") {
        return json({ error: "method_not_allowed", message: "सिर्फ़ POST चलता है।" }, 405);
      }
      return handleAsk(request, env);
    }
    return env.ASSETS.fetch(request);
  },
};
