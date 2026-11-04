# जिनागम सहायक — public version

Koi bhi link khol ke sawaal pooch sakta hai, bina claude.ai account ke. Frontend static
(`index.html` + `search_corpus.json`) hai; AI call ek Cloudflare Pages Function
(`functions/api/ask.js`) ke through hoti hai jahaan Anthropic API key chhupi rehti hai.

**Protection**: ek shared access-code (password nahi, bas ek phrase — jaise WiFi password)
+ per-IP aur daily rate limit, taaki link kahin aur leak ho jaaye to bill na badh jaaye.

**Cost**: hosting (Cloudflare Pages + Functions + KV) free tier me free hai. Har "poochein"
click Anthropic API credits kharch karta hai (~$0.003-0.01/sawaal, Sonnet model se, context
+ 700-token jawaab ke hisaab se) — yeh claude.ai subscription se bilkul alag billing hai,
console.anthropic.com pe apna balance dekhiye.

## Ek baar ka setup

1. **Cloudflare account** (free) — https://dash.cloudflare.com/sign-up
2. **Anthropic API key** — https://console.anthropic.com/settings/keys se banaiye (ek naya
   "API key" — yeh claude.ai login se alag hai, isme credits daalne padte hain, shuru me
   kuch free credit milta hai)
3. Yahi folder se, Cloudflare se login:
   ```
   npx wrangler login
   ```
   (browser khulega, apne Cloudflare account se login kar lijiye)

4. KV namespace banaiye (rate-limit counters yahin rehte hain):
   ```
   npx wrangler kv namespace create jinagam_rate_limit
   ```
   Yeh ek `id` dega — use agle step me chahiye.

5. `wrangler.toml` banaiye (isी folder me), aur upar wale `id` ko bhar dijiye:
   ```toml
   name = "jinagam-sahayak"
   pages_build_output_dir = "."

   [[kv_namespaces]]
   binding = "RATE_LIMIT_KV"
   id = "<yahan wo id paste karo>"
   ```

6. Deploy:
   ```
   npx wrangler pages deploy . --project-name=jinagam-sahayak
   ```
   Yeh ek URL dega jaisे `https://jinagam-sahayak.pages.dev` — yahi link sabko bhejna hai.

7. Secrets set karo (dashboard se karna aasaan hai — https://dash.cloudflare.com →
   Workers & Pages → jinagam-sahayak → Settings → Environment variables → "Add secret"):
   - `ANTHROPIC_API_KEY` = apni Anthropic key
   - `ACCESS_CODE` = jo bhi phrase chaahiye (jaise `jinagam2026`) — yahi sabko batana hai

   Ya CLI se:
   ```
   npx wrangler pages secret put ANTHROPIC_API_KEY --project-name=jinagam-sahayak
   npx wrangler pages secret put ACCESS_CODE --project-name=jinagam-sahayak
   ```

8. Dobara deploy karo taaki naye settings lagoo ho jaayen:
   ```
   npx wrangler pages deploy . --project-name=jinagam-sahayak
   ```

Ab link + access-code jisko bhi bhejo, wo bina login ke khol sakta hai aur sawaal pooch sakta hai.

## Baad me content update karna ho

`search_corpus.json` naya banwana ho (naya granth add hua ho) to `encyclopedia/` folder me
`build_search_corpus.py` chalaiye, phir file yahan copy karke `wrangler pages deploy . --project-name=jinagam-sahayak` dobara chalaiye.

## Rate-limit numbers badalne hon

`functions/api/ask.js` ke top pe `DEFAULT_PER_IP_LIMIT` (abhi 6/minute) aur
`DEFAULT_DAILY_LIMIT` (abhi 250/din) hai — ya environment variables `PER_IP_LIMIT` /
`DAILY_LIMIT` set kar dijiye dashboard se, code badalne ki zaroorat nahi.
