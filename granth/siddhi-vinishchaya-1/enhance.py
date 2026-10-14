# -*- coding: utf-8 -*-
"""धुँधले पन्ने को पढ़ने लायक़ बनाने के लिए — काटिए, साफ़ कीजिए, बड़ा कीजिए।

चलाइए:
    python enhance.py 45                 # पूरा पृष्ठ, तीन पट्टियों में
    python enhance.py 45 --from .62 --to .90   # केवल यह हिस्सा (पाद-टिप्पणी)
    python enhance.py 45 --scale 3       # और बड़ा

मुद्रित पृष्ठ-संख्या दीजिए, स्कैन की नहीं — pagemap.json से अपने आप बैठ जाएगी।
बनी हुई छवियाँ scratchpad में जाती हैं, ग्रन्थ-फ़ोल्डर में नहीं, और उनका पथ
छप जाता है; उसी को Read से खोलिए।

## यह क्यों

कुछ पन्नों पर स्याही फैली है और टाइप भर गया है — मुद्रित 41 से 45 तक विशेषकर।
सीधे पढ़ने पर वहाँ बहुत कुछ [अस्पष्ट] रह जाता है, जबकि विषमता सुधारकर और
किनारे तीखे करके वही अक्षर पढ़े जा सकते हैं। मुद्रित 45 की टिप्पणी (4) पूरी
अपठनीय मानी गई थी; इस उपचार के बाद वह पढ़ी गई।

**फिर भी जो न पढ़ा जाए, वह [अस्पष्ट] ही रहे।** यह उपकरण अनुमान लगाने की छूट
नहीं देता — केवल आँख को वह दिखाता है जो स्याही में दबा रह गया था।
"""
import pathlib
import sys

from PIL import Image, ImageFilter, ImageOps

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import page as pagemap  # noqa: E402

try:
    sys.stdout.reconfigure(encoding="utf-8")
except (AttributeError, OSError):
    pass

HERE = pathlib.Path(__file__).resolve().parent
OUT = pathlib.Path(
    r"C:\Users\naman\AppData\Local\Temp\claude"
    r"\e--Projects-JinAagam\c18ad576-4dee-4fdc-b3a1-a26b5766fd13\scratchpad")


def enhance(img, scale):
    img = ImageOps.autocontrast(img, cutoff=2)
    img = img.filter(ImageFilter.UnsharpMask(radius=3, percent=180, threshold=2))
    return img.resize((int(img.width * scale), int(img.height * scale)), Image.LANCZOS)


def main(argv):
    if not argv:
        print(__doc__)
        return 1
    printed = int(argv[0])
    g = lambda k, d: (float(argv[argv.index(k) + 1]) if k in argv else d)
    lo, hi, scale = g("--from", 0.0), g("--to", 1.0), g("--scale", 2.2)

    scan = pagemap.printed_to_scan.get(printed)
    if not scan:
        print(f"  मुद्रित {printed}: सारणी में नहीं — pagemap.json देखिए")
        return 1
    im = Image.open(HERE / f"img/p{scan:03d}.png").convert("L")
    W, H = im.size
    band = im.crop((0, int(H * lo), W, int(H * hi)))

    OUT.mkdir(parents=True, exist_ok=True)
    # एक साथ बहुत ऊँची पट्टी पढ़ने में कठिन होती है, इसलिए तीन टुकड़े
    n = 1 if (hi - lo) <= 0.30 else 3
    step = band.height // n
    for i in range(n):
        part = band.crop((0, i * step, band.width,
                          band.height if i == n - 1 else (i + 1) * step))
        p = OUT / f"enh_p{printed}_{i + 1}.png"
        enhance(part, scale).save(p)
        print(f"  {p}")
    print(f"  (मुद्रित {printed} = स्कैन {scan}; {n} टुकड़े, {scale}x)")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
