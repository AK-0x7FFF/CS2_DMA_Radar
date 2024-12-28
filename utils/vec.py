from array import ArrayType
from copy import copy
from dataclasses import dataclass
from math import sqrt, atan2, degrees
from typing import Iterable, Any

from numpy import array, ndarray, dtype, float64


@dataclass
class Vec2:
    x: float = .0
    y: float = .0

    def __repr__(self):
        return "Vec2(%f, %f)" % (self.x, self.y)

    def __iter__(self):
        return iter((self.x, self.y))

    def __getitem__(self, item: int | str) -> float:
        if isinstance(item, int): return (self.x, self.y)[item]
        elif isinstance(item, str): return dict(x=self.x, y=self.y)[item]
        else: raise ValueError()

    def __hash__(self) -> int:
        return hash((self.x, self.y))

    def __round__(self, ndigits: int | None = None) -> "Vec2":
        return Vec2(
            round(self.x, ndigits),
            round(self.y, ndigits)
        )

    def __add__(self, other) -> "Vec2":
        if not isinstance(other, Vec2): return NotImplemented

        return Vec2(
            self.x + other.x,
            self.y + other.y
        )

    def __sub__(self, other) -> "Vec2":
        if not isinstance(other, Vec2): return NotImplemented

        return Vec2(
            self.x - other.x,
            self.y - other.y
        )

    def __mul__(self, other: "Vec2") -> "Vec2":
        return Vec2(
            self.x * other.x,
            self.y * other.y,
        )

    def __truediv__ (self, other: "Vec2") -> "Vec2":
        return Vec2(
            self.x / other.x,
            self.y / other.y,
        )

    @classmethod
    def from_dict(cls, dict: dict[str, float | None]) -> "Vec2":
        x: float = dict.get("x", None)
        y: float = dict.get("y", None)
        if None in (x, y): raise ValueError()

        return Vec2(x, y)

    def copy(self) -> "Vec2":
        return copy(self)

    def numpy_array(self) -> ndarray[Any, dtype[Any]]:
        return array((self.x, self.y), dtype=float64)

    def distance(self, vec2: "Vec2") -> float:
        opp_pos = self - vec2

        distance = sqrt(sum((
            opp_pos.x ** 2,
            opp_pos.y ** 2
        )))
        return distance

    def angle(self, vec2: "Vec2") -> float:
        opp_pos = self - vec2

        angle = atan2(opp_pos.y, opp_pos.x)
        return degrees(angle)

    def min(self, vec2: "Vec2"):
        return Vec2(min(self.x, vec2.x), min(self.y, vec2.y))

    def max(self, vec2: "Vec2"):
        return Vec2(max(self.x, vec2.x), max(self.y, vec2.y))


@dataclass
class Vec3:
    x: float = .0
    y: float = .0
    z: float = .0

    def __repr__(self):
        return "Vec3(%f, %f, %f)" % (self.x, self.y, self.z)

    def __iter__(self) -> Iterable:
        return iter((self.x, self.y, self.z))

    def __getitem__(self, item: int | str) -> float:
        if isinstance(item, int): return (self.x, self.y, self.z)[item]
        elif isinstance(item, str): return dict(x=self.x, y=self.y, z=self.z)[item]
        else: raise ValueError()

    def __hash__(self) -> int:
        return hash((self.x, self.y, self.z))

    def __add__(self, other) -> "Vec3":
        if not isinstance(other, Vec3): return NotImplemented

        return Vec3(
            self.x + other.x,
            self.y + other.y,
            self.z + other.z
        )

    def __sub__(self, other) -> "Vec3":
        if not isinstance(other, Vec3): return NotImplemented

        return Vec3(
            self.x - other.x,
            self.y - other.y,
            self.z - other.z
        )

    def __floordiv__(self, other: "Vec3") -> "Vec3":
        return Vec3(
            self.x * other.x,
            self.y * other.y,
            self.z * other.z,
        )

    def __truediv__(self, other: "Vec3") -> "Vec3":
        return Vec3(
            self.x / other.x,
            self.y / other.y,
            self.z / other.z,
        )

    @classmethod
    def from_dict(cls, dict: dict[str, float | None]) -> "Vec3":
        x: float = dict.get("x", None)
        y: float = dict.get("y", None)
        z: float = dict.get("z", None)
        if None in (x, y, z): raise ValueError()

        return Vec3(x, y, z)

    def copy(self) -> "Vec3":
        return copy(self)

    def numpy_array(self) -> ndarray[Any, dtype[Any]]:
        return array((self.x, self.y, self.z), dtype=float64)

    def distance(self, vec3: "Vec3") -> float:
        opp_pos = self - vec3

        distance = sqrt(sum((
            opp_pos.x ** 2,
            opp_pos.y ** 2,
            opp_pos.z ** 2
        )))
        return distance

    def normalize(self) -> "Vec3":
        length = sqrt(sum((self.x ** 2, self.y ** 2, self.z ** 2)))
        return Vec3(
            self.x / length,
            self.y / length,
            self.z / length
        )

    def cross(self, other: "Vec3") -> "Vec3":
        return Vec3(
            self.y * other.z - self.z * other.y,
            self.z * other.x - self.x * other.z,
            self.x * other.y - self.y * other.x
        )

    def dot(self, other: "Vec3") -> float:
        return sum((
            self.x * other.x,
            self.y * other.y,
            self.z * other.z,
        ))


@dataclass
class Vec4:
    x: float = .0
    y: float = .0
    z: float = .0
    w: float = .0