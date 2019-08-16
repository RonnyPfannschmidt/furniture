import attr
import enum
from collections import Counter


class MaterialTyp(enum.Enum):
    BRETT = enum.auto()
    SCHREINERPLATTE = enum.auto()
    SPERRHOLZ = enum.auto()


class MagicalListMixin:
    def __mul__(self, number):
        return [self] * number

    def __add__(self, other):
        return [self] + other

    def __radd___(self, other):
        return other * [self]

@attr.s(frozen=True)
class Material:
    name = attr.ib(cmp=False)
    dick = attr.ib()
    breit = attr.ib()
    typ = attr.ib()

    def brett(self, lang):
        return Brett(self, lang)


@attr.s(frozen=True)
class Brett(MagicalListMixin):
    material = attr.ib()
    lang = attr.ib()

    def __str__(self):
        return f"{self.material.name}-{self.breit}x{self.lang}"

    @property
    def breit(self):
        return self.material.breit

    @property
    def dick(self):
        return self.material.dick


@attr.s(frozen=True)
class StückGut(MagicalListMixin):
    name = attr.ib()

    def __str__(self):
        return self.name


SPIEL = 5
ELEMENT = 1000
WANDÜBERSTAND = 30
FRONTÜBERSTAND = 10
HÖHE = 400

KORPUS_DÜBEL = StückGut("Holzdübel_Korpus")
FACH_DÜBEL = StückGut("Holzdübel_Fach")
VERBINDUNGS_BOLZEN = StückGut("Schraubverbindung")
FACH_SCHRAUBE = StückGut("Fachschraube")  # sollen auch front an fach bringen
KORPUS_SCHRAUBE = StückGut("Korpusschraube")  # bringen seitenteile an front
ELEMENT_VERBINDER = StückGut("ElementVerbinder")


def teileliste(*, korpus, fach_kanten, deck, front, seitentbreite, füll):

    hinterwand = korpus.brett(ELEMENT)
    deckteil = deck.brett(ELEMENT)

    seitenteil = korpus.brett(seitentbreite)

    front_teil = front.brett(hinterwand.lang - SPIEL // 2)

    breite_ausspaarung = (ELEMENT - 3 * korpus.dick) // 2 - SPIEL

    schublade_breite = fach_kanten.brett(breite_ausspaarung)
    schublade_seite = fach_kanten.brett(seitenteil.lang - 2 * fach_kanten.dick - SPIEL)

    # todo: schublade brett
    schublade = (
        front_teil + FACH_SCHRAUBE * 3 +
        schublade_breite * 2 +
        FACH_SCHRAUBE * 2 * 2 + FACH_DÜBEL * 2 * 2 +
        schublade_seite * 2
    )

    element = (
        hinterwand + VERBINDUNGS_BOLZEN * 2 + KORPUS_DÜBEL * 1 + deckteil * 2 +
        seitenteil * 3 + VERBINDUNGS_BOLZEN * 2 * 3 + schublade * 2
    )
    seitenfüller = füll.brett(korpus.breit) + KORPUS_SCHRAUBE * 3
    dekenfüller = füll.brett(deck.breit) + KORPUS_SCHRAUBE * 2 + KORPUS_DÜBEL * 1
    # SEITENFUELLER = aussen(lang=BASIS_HOCH, breit=DICKE)
    # DECKENFUELLER = aussen(lang=DECKBREITE, breit=DICKE)
    füller = (seitenfüller + dekenfüller) * 2

    return element * 2 + ELEMENT_VERBINDER * 3 + füller


SCHICHTHOLZ_27_KORPUS = Material(
    name="Schichtholz_27",
    dick=27,
    breit=HÖHE,
    typ=MaterialTyp.SCHREINERPLATTE,
)
SCHICHTHOLZ_27_DECK = attr.evolve(SCHICHTHOLZ_27_KORPUS, breit=ELEMENT // 2)

SCHICHTHOLZ_27_FRONT = attr.evolve(SCHICHTHOLZ_27_KORPUS, breit=HÖHE - SPIEL)
SCHICHTHOLZ_27_FÜLL = attr.evolve(SCHICHTHOLZ_27_KORPUS, breit=WANDÜBERSTAND)

FICHTE_200_18 = Material(
    name="Fichtenbrett_200x18",
    dick=18,
    breit=200,
    typ=MaterialTyp.BRETT,
)


counted = Counter(teileliste(
    korpus=SCHICHTHOLZ_27_KORPUS,
    deck=SCHICHTHOLZ_27_DECK,
    front=SCHICHTHOLZ_27_FRONT,
    füll=SCHICHTHOLZ_27_FÜLL,
    fach_kanten=FICHTE_200_18,
    seitentbreite=800,  # TODO: ausrechnen
))
teile = counted.most_common()

# teile.sort(key=lambda x: x[0.])

for item, count in counted.most_common():
    print(item, "x", count)
