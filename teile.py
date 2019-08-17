import attr
from collections import Counter
from picocam import MaterialTyp, Material, StückGut


SPIEL = 5
ELEMENT = 1000
ÜBERSTAND = SPIEL
ÜBERSTAND = SPIEL

ÜBERSTAND_WAND = 30
HÖHE_SEITENLEISTEN_WAND = 20
HÖHE = 400

KORPUS_DÜBEL = StückGut("Holzdübel_Korpus")
FACH_DÜBEL = StückGut("Holzdübel_Fach")
VERBINDUNGS_BOLZEN = StückGut("Schraubverbindung")
FACH_SCHRAUBE = StückGut("Fachschraube")  # sollen auch front an fach bringen
KORPUS_SCHRAUBE = StückGut("Korpusschraube")  # bringen seitenteile an front
ELEMENT_VERBINDER = StückGut("ElementVerbinder")

ROLLE = StückGut("BodenRolleWeich")

def teileliste(
    *, korpus_seite, korpus_hinten, fach_kanten, deck, front, fuell, mat_fachboden
):

    hinterwand = korpus_hinten.brett(ELEMENT)
    deckteil = deck.brett(ELEMENT)

    seitentbreite = ELEMENT - ÜBERSTAND - korpus_hinten.dick - ÜBERSTAND - front.dick

    seitenteil = korpus_seite.brett(seitentbreite)

    front_teil = front.brett(hinterwand.lang - SPIEL // 2)

    breite_ausspaarung = (ELEMENT - 3 * korpus_seite.dick) // 2 - SPIEL

    schublade_breite = fach_kanten.brett(breite_ausspaarung)
    schublade_seite = fach_kanten.brett(seitenteil.lang - 2 * fach_kanten.dick - SPIEL)

    XXX: hack

    schublade_innenbreite = breite_ausspaarung - 2 * fach_kanten.dick
    mat_innenboden = attr.evolve(mat_fachboden, breit=schublade_innenbreite + 2 * SPIEL)

    innenboden = mat_innenboden.brett(lang=schublade_seite.lang + 2 * SPIEL)

    # todo: schublade brett
    schublade = (
        front_teil
        + FACH_SCHRAUBE * 3
        + schublade_breite * 2
        + FACH_SCHRAUBE * 2 * 2
        + FACH_DÜBEL * 2 * 2
        + schublade_seite * 2
        + ROLLE * 3 * 2
        + innenboden * 1
    )

    verbindung = VERBINDUNGS_BOLZEN * 2 + KORPUS_DÜBEL * 1

    element = (
        hinterwand
        + verbindung
        + deckteil * 2
        + seitenteil * 3
        + verbindung * 3 * 3
        + schublade * 2
    )

    seitenfueller = (
        fuell.brett(korpus_seite.breit + ÜBERSTAND_WAND) + KORPUS_SCHRAUBE * 3
    )
    dekenfueller = fuell.brett(deck.breit) + KORPUS_SCHRAUBE * 2 + KORPUS_DÜBEL * 1
    # SEITENFUELLER = aussen(lang=BASIS_HOCH, breit=DICKE)
    # DECKENFUELLER = aussen(lang=DECKBREITE, breit=DICKE)
    fueller = seitenfueller + dekenfueller * 2

    return element * 2 + ELEMENT_VERBINDER * 3 + fueller


SCHICHTHOLZ_27 = Material(
    name="Schichtholz_27", dick=27, breit=None, typ=MaterialTyp.SCHREINERPLATTE
)


SCHICHTHOLZ_27_KORPUS_SEITE = attr.evolve(SCHICHTHOLZ_27, breit=HÖHE)
SCHICHTHOLZ_27_KORPUS_HINTEN = attr.evolve(
    SCHICHTHOLZ_27, breit=HÖHE - HÖHE_SEITENLEISTEN_WAND
)
SCHICHTHOLZ_27_DECK = attr.evolve(SCHICHTHOLZ_27, breit=ELEMENT // 2)

SCHICHTHOLZ_27_FRONT = attr.evolve(SCHICHTHOLZ_27, breit=HÖHE - SPIEL)
SCHICHTHOLZ_27_FUELL = attr.evolve(SCHICHTHOLZ_27, breit=ÜBERSTAND_WAND)

FICHTE_200_18 = Material(
    name="Fichtenbrett_200x18", dick=18, breit=200, typ=MaterialTyp.BRETT
)
SPERRHOLZ_6 = Material(name="Sperrholz_6", dick=5, breit=None, typ=MaterialTyp.SPERRHOLZ)

counted = Counter(
    teileliste(
        korpus_seite=SCHICHTHOLZ_27_KORPUS_SEITE,
        korpus_hinten=SCHICHTHOLZ_27_KORPUS_HINTEN,
        deck=SCHICHTHOLZ_27_DECK,
        front=SCHICHTHOLZ_27_FRONT,
        fuell=SCHICHTHOLZ_27_FUELL,
        fach_kanten=FICHTE_200_18,
        mat_fachboden=SPERRHOLZ_6,
    )
)
teile = counted.most_common()

# teile.sort(key=lambda x: x[0.])

for item, count in counted.most_common():
    print(item, "x", count)
