"""A package for using complex numbers as 2D vectors."""
from __future__ import annotations

import cmath
from dataclasses import dataclass
from typing import Any, Optional, SupportsIndex


def convert_angle(angle: float, /, unit: str):
    """Convert an angle to radians."""
    unit = unit.lower()
    if unit in {"d", "deg", "degrees", "degree", "°"}:
        return angle * cmath.tau / 360
    if unit in {"r", "", None, "rad", "radian", "radians"}:
        return angle
    if unit in {"g", "grad", "gradians", "gradian", "gons", "gon", "grades", "grade"}:
        return angle * cmath.tau / 400
    if unit in {"mins", "min", "minutes", "minute", "'", "′"}:
        return angle * cmath.tau / 21600
    if unit in {"secs", "sec", "seconds", "seconds", '"', "″"}:
        return angle * cmath.tau / 1296000
    if unit in {"turn", "turns"}:
        return angle * cmath.tau
    raise ValueError(f"Invalid angle unit: '{unit}'")


def _object_to_xy(obj: Any, /) -> tuple:
    """Convert an object to an (x, y) tuple."""
    # Deal with objects with x and y attributes
    try:
        return (obj.x, obj.y)
    except AttributeError:
        pass
    # Deal with iterables
    try:
        iterable = iter(obj)
        try:
            x = next(iterable)
            y = next(iterable)
        except StopIteration:
            raise ValueError("Iterable is too short to create Vector")
        try:
            next(iterable)
            raise ValueError("Iterable is too long to create Vector")
        except StopIteration:
            return (x, y)
    except TypeError:
        raise TypeError(
            "Single argument Vector must be Vector, complex, iterable or have x and y attributes"
        )


@dataclass(frozen=True, init=False, repr=False)
class Vector:
    """A two-dimensional vector."""

    _complex: complex

    def __init__(
        self,
        x: Any = None,
        y: Optional[float] = None,
        *,
        r: Optional[float] = None,
        theta: Optional[float] = None,
        angle_unit: str = "rad",
    ):
        if r is None and theta is None:
            if y is None:
                if isinstance(x, complex):
                    object.__setattr__(self, "_complex", x)
                else:
                    # Create Vector from a single argument using the
                    # implementation _complex provides
                    try:
                        object.__setattr__(self, "_complex", complex(x))
                    except TypeError:
                        # Get x and y values using our implementation
                        object.__setattr__(self, "_complex", complex(*_object_to_xy(x)))
            else:
                if x is None:
                    raise ValueError("Must give x to create Vector if y is given")
                # Create Vector from x and y
                try:
                    object.__setattr__(self, "_complex", complex(x, y))
                except TypeError:
                    raise TypeError("x and y values must be numeric to create Vector")
            return

        if x is not None or y is not None:
            raise ValueError(
                "Cannot create Vector from mixed rectangular and polar arguments"
            )

        # Create Vector from polar arguments
        if r == 0:
            return Vector(0)
        if r is None or theta is None:
            raise ValueError(
                "must provide both r and theta to create Vector from polar"
            )
        object.__setattr__(
            self, "_complex", cmath.rect(r, convert_angle(theta, angle_unit))
        )

    def dot(self, other: Vector, /) -> float:
        """Return the dot product of self and other."""
        return (
            self._complex.real * other._complex.real
            + self._complex.imag * other._complex.imag
        )

    def perp_dot(self, other: Vector, /) -> float:
        """
        Return the perp dot product of self and other.

        This is the signed area of the parallelogram they define. It is
        also one of the 'cross products' that can be defined on 2D
        vectors.
        """
        return (
            self._complex.real * other._complex.imag
            - self._complex.imag * other._complex.real
        )

    def perp(self, /) -> Vector:
        """
        Return the Vector, rotated anticlockwise by pi / 2.

        This is one of the 'cross products' that can be defined on 2D
        vectors. Use -Vector.perp() for a clockwise rotation.
        """
        return Vector(complex(-self._complex.imag, self._complex.real))

    def rotate(self, angle: float, /, unit="rad") -> Vector:
        """
        Return a self, rotated by angle anticlockwise.

        Use negative angles for a clockwise rotation.
        """
        angle = convert_angle(angle, unit)
        return Vector(cmath.rect(self.r, self.theta + angle))

    def hat(self, /) -> Vector:
        """Return a Vector with the same direction, but unit length."""
        return self / abs(self)

    def rec(self, /) -> tuple[float, float]:
        """Get the vector as (x, y)."""
        return (self._complex.real, self._complex.imag)

    def pol(self, /) -> tuple[float, float]:
        """Get the vector as (r, theta)."""
        return cmath.polar(self._complex)

    def round(self, ndigits: int = 0, /) -> tuple:
        return (round(self._complex.real, ndigits), round(self._complex.imag, ndigits))

    def __str__(self, /):
        return f"({self._complex.real} {self._complex.imag})"

    def __repr__(self, /):
        return (
            f"{self.__class__.__qualname__}({self._complex.real}, {self._complex.imag})"
        )

    def __len__(self, /):
        return 2

    def __getitem__(self, key: SupportsIndex, /) -> float:
        return self.rec()[key]

    def __contains__(self, item: float, /):
        return item == self._complex.real or item == self._complex.imag

    def __iter__(self, /):
        yield self._complex.real
        yield self._complex.imag

    def __reversed__(self, /):
        yield self._complex.imag
        yield self._complex.real

    def __neg__(self, /):
        return Vector(-self._complex)

    def __add__(self, other: Vector, /) -> Vector:
        return Vector(self._complex + other._complex)

    def __sub__(self, other: Vector, /) -> Vector:
        return Vector(self._complex - other._complex)

    def __mul__(self, value: float, /) -> Vector:
        return Vector(self._complex * value)

    def __truediv__(self, value: float, /) -> Vector:
        return Vector(self._complex / value)

    __rmul__ = __mul__

    def __abs__(self) -> float:
        return abs(self._complex)

    @property
    def x(self) -> float:
        """The horizontal component of the vector."""
        return self._complex.real

    @property
    def y(self) -> float:
        """The vertical component of the vector."""
        return self._complex.imag

    @property
    def r(self) -> float:
        """The radius of the vector."""
        return abs(self)

    @property
    def theta(self) -> float:
        """
        The angle of the vector, anticlockwise from the horizontal.

        Negative values are clockwise. Returns values in the range
        [-pi, pi]. See documentation of cmath.phase for details.
        """
        return cmath.phase(self._complex)
