from collections import namedtuple
from collections import Counter

Brett = namedtuple("Brett", "dick breit lang")


def aussen(lang, breit):
    return Brett(lang=max(lang, breit), breit=min(lang, breit), dick=DICKE)


def innen(lang):
    return Brett(lang=lang, breit=BREITE_INNEN, dick=DICKE_INNEN)


SPIEL = 5

DICKE = 24

DICKE_INNEN = 22
BREITE_INNEN = 150

ELEMENTBREITE = 1000
BASIS_HOCH = 400
SEITENBREITE = 800

DECKBREITE = ELEMENTBREITE // 2


HINTERWAND = aussen(breit=ELEMENTBREITE, lang=BASIS_HOCH)
DECKTEIL = aussen(breit=DECKBREITE, lang=ELEMENTBREITE)
SEITENTEIL = aussen(breit=SEITENBREITE, lang=BASIS_HOCH)

FRONTWAND = aussen(breit=HINTERWAND.breit - SPIEL // 2, lang=HINTERWAND.lang - SPIEL)

AUSSPAARUNGSBREITE = (ELEMENTBREITE - 3 * DICKE) // 2 - SPIEL

HINTEN_SCHUBLADE = innen(AUSSPAARUNGSBREITE)
SEITE_SCHUBLADE = innen(SEITENBREITE - DICKE_INNEN - SPIEL)


SCHUBLADE = [HINTEN_SCHUBLADE, FRONTWAND] + [SEITE_SCHUBLADE] * 2


ELEMENT = [HINTERWAND] + [DECKTEIL] * 2 + [SEITENTEIL] * 3 + SCHUBLADE * 2


SEITENFUELLER = aussen(lang=BASIS_HOCH, breit=DICKE)

DECKENFUELLER = aussen(lang=DECKBREITE, breit=DICKE)


ALLES = ELEMENT * 2 + [SEITENFUELLER, DECKENFUELLER] * 2


counted = Counter(ALLES)
teile = counted.most_common()

#teile.sort(key=lambda x: x[0.])

for item, count in counted.most_common():
    print(item, "x", count)
