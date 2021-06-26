import attr
import enum


class MaterialTyp(enum.Enum):
    BRETT = enum.auto()
    SCHREINERPLATTE = enum.auto()
    SPERRHOLZ = enum.auto()
    Balken = enum.auto()


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

    def __str__(self):
        if self.typ == MaterialTyp.BRETT:
            return f"{self.name}-"
        else:
            return f"{self.name}-{self.breit}x"

    def brett(self, lang):
        return Brett(self, lang)


@attr.s(frozen=True)
class Brett(MagicalListMixin):
    material = attr.ib()
    lang = attr.ib()

    def __str__(self):
        return f"{self.material}{self.lang}"

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
