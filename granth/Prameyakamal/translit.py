# -*- coding: utf-8 -*-
"""देवनागरी → IAST और मिलान के लिए 'ढाँचा' (skeleton)।

GRETIL के मुद्रित-संस्करण-आधारित पाठ IAST में हैं और हमारा लिप्यन्तरण देवनागरी में,
इसलिए उद्धरणों का मिलान करने से पहले दोनों को एक ही लिपि में लाना पड़ता है।
"""
import re
import unicodedata

V = {'अ':'a','आ':'ā','इ':'i','ई':'ī','उ':'u','ऊ':'ū','ऋ':'ṛ','ॠ':'ṝ','ऌ':'ḷ','ॡ':'ḹ',
     'ए':'e','ऐ':'ai','ओ':'o','औ':'au','ऍ':'e','ऎ':'e','ऒ':'o','ऑ':'o'}
M = {'ा':'ā','ि':'i','ी':'ī','ु':'u','ू':'ū','ृ':'ṛ','ॄ':'ṝ','ॢ':'ḷ','ॣ':'ḹ',
     'े':'e','ै':'ai','ो':'o','ौ':'au','ॅ':'e','ॆ':'e','ॊ':'o','ॉ':'o'}
C = {'क':'k','ख':'kh','ग':'g','घ':'gh','ङ':'ṅ','च':'c','छ':'ch','ज':'j','झ':'jh','ञ':'ñ',
     'ट':'ṭ','ठ':'ṭh','ड':'ḍ','ढ':'ḍh','ण':'ṇ','त':'t','थ':'th','द':'d','ध':'dh','न':'n',
     'प':'p','फ':'ph','ब':'b','भ':'bh','म':'m','य':'y','र':'r','ल':'l','व':'v',
     'श':'ś','ष':'ṣ','स':'s','ह':'h','ळ':'ḷ','ऴ':'ḷ','ऩ':'n','ऱ':'r',
     'क़':'k','ख़':'kh','ग़':'g','ज़':'z','ड़':'ṛ','ढ़':'ṛh','फ़':'f','य़':'y'}
VIRAMA = '्'


def dev2iast(s):
    s = unicodedata.normalize('NFC', s)
    out, i, n = [], 0, len(s)
    while i < n:
        ch = s[i]
        if ch in C:
            out.append(C[ch])
            j = i + 1
            if j < n and s[j] == VIRAMA:
                i = j + 1
                continue
            if j < n and s[j] in M:
                out.append(M[s[j]])
                i = j + 1
            else:
                out.append('a')
                i += 1
            # अनुस्वार/विसर्ग स्वर के बाद आते हैं
            while i < n and s[i] in ('ं', 'ः', 'ँ'):
                out.append('ṃ' if s[i] != 'ः' else 'ḥ')
                i += 1
            continue
        if ch in V:
            out.append(V[ch]); i += 1
            while i < n and s[i] in ('ं', 'ः', 'ँ'):
                out.append('ṃ' if s[i] != 'ः' else 'ḥ')
                i += 1
            continue
        if ch == 'ऽ':
            out.append("'"); i += 1; continue
        if ch in ('ं', 'ँ'):
            out.append('ṃ'); i += 1; continue
        if ch == 'ः':
            out.append('ḥ'); i += 1; continue
        if ch in ('।', '॥'):
            out.append(' '); i += 1; continue
        if ch == VIRAMA:
            i += 1; continue
        out.append(ch); i += 1
    return ''.join(out)


_PUNCT = re.compile(r"[^a-zāīūṛṝḷḹṅñṭḍṇśṣḥṃ'\s]")


def words(iast):
    """मिलान-योग्य शब्द-सूची — विराम, अंक, कोष्ठक सब हटाकर।"""
    t = iast.lower().replace('|', ' ').replace('॥', ' ')
    t = _PUNCT.sub(' ', t)
    return t.split()


_SKEL = str.maketrans({'b': 'v', 'ṣ': 'ś', 'ṇ': 'n', 'ṭ': 't', 'ḍ': 'd',
                       'ṅ': 'n', 'ñ': 'n', 'ṃ': '', 'ḥ': '', "'": '',
                       'ā': 'a', 'ī': 'i', 'ū': 'u', 'ṝ': 'ṛ', 'ḹ': 'ḷ'})


def skel(w):
    """छपाई-भेद मिटाया हुआ ढाँचा — ब/व, ष/श, मूर्धन्य/दन्त्य, दीर्घ/लघु एक समान।

    इस 1941 के संस्करण में ब और व एक ही टाइप से छपे हैं, और उद्धरणों में
    सन्धि-वर्तनी संस्करण-दर-संस्करण बदलती है; इसलिए खोज के समय ढाँचा देखा जाता है,
    पर भेद दिखाते समय असली रूप।
    """
    return w.translate(_SKEL)
