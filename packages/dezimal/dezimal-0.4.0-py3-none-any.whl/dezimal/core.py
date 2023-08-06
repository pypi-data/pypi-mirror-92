import math
import re
from decimal import Decimal
from typing import Union, Callable
from numbers import Number


class Dezimal(tuple, Number):
    __slots__ = []

    def __new__(cls, value: Union[bool, int, float, str, 'Dezimal', Decimal], scale: int = None):
        if scale is None:
            scale = 0
        else:
            if not isinstance(scale, int):
                raise TypeError(scale)
            if scale < 0:
                raise ValueError(scale)
        if isinstance(value, Dezimal):
            return value
        if isinstance(value, Decimal):
            value = str(value)
        if isinstance(value, bool):
            return Dezimal(1) if value else Dezimal(0)
        if isinstance(value, float):
            value = str(value)
        if isinstance(value, str):
            return Dezimal.from_string(value)
        if not isinstance(value, int):
            raise TypeError(f"when scale is given, value must be an int, but is {type(value)}: {value}")
        while scale > 0 and value % 10 == 0:
            scale -= 1
            value //= 10
        # noinspection PyTypeChecker
        return tuple.__new__(cls, (value, scale))

    @staticmethod
    def from_string(value: str) -> 'Dezimal':
        sign = 1
        if not value:
            raise ValueError(value)
        elif value[0] == '+':
            value = value[1:]
        elif value[0] == '-':
            value = value[1:]
            sign = -1
        if re.match(r"^[0-9]+$", value):
            value = int(value)
            scale = 0
            return Dezimal(sign * value, scale)
        m = re.match(r"^([0-9]+)\.([0-9]+)$", value)
        if m:
            frac = m.group(2)
            value = int(m.group(1)) * (10 ** len(frac)) + int(frac)
            scale = len(frac)
            return Dezimal(sign * value, scale)
        m = re.match(r"^([0-9]+)[eE]([+-]?[0-9]+)$", value)
        if m:
            value = int(m.group(1))
            scale = int(m.group(2))
            if scale < 0:
                return Dezimal(sign * value, -scale)
            return Dezimal(sign * value * 10 ** scale)
        m = re.match(r"^([0-9]+)\.([0-9]+)[eE]([+-]?[0-9]+)$", value)
        if m:
            frac = m.group(2)
            value = int(m.group(1)) * (10 ** len(frac)) + int(frac)
            scale = len(frac) - int(m.group(3))
            if scale < 0:
                return Dezimal(sign * value * (10 ** -scale))
            return Dezimal(sign * value, scale)

        raise ValueError(value)

    @property
    def value(self):
        return tuple.__getitem__(self, 0)

    @property
    def scale(self):
        return tuple.__getitem__(self, 1)

    def __getitem__(self, key):
        raise TypeError

    def __repr__(self) -> str:
        return f"Dezimal({repr(str(self))})"

    def __str__(self) -> str:
        if self.scale > 0:
            if self.value < 0:
                sign = "-"
                value = -self.value
            else:
                sign = ""
                value = self.value
            str_value = str(value).zfill(self.scale)
            a = str_value[:-self.scale]
            if not a:
                a = "0"
            b = str_value[-self.scale:]
            return f"{sign}{a}.{b}"
        else:
            return str(self.value)

    def __int__(self) -> int:
        if self.scale == 0:
            return self.value
        return self.value // (10 ** self.scale)

    def __float__(self) -> float:
        if self.scale == 0:
            return float(self.value)
        return self.value / 10 ** self.scale

    def __bool__(self) -> bool:
        return self.value != 0

    @staticmethod
    def _scaled(this, that,
                func: Callable[[int, int], int],
                scale_func: Callable[[int, int], int] = max,
                rescale: bool = True,
                result_constructor=None):
        if not isinstance(this, Dezimal):
            this = Dezimal(this)
        if not isinstance(that, Dezimal):
            that = Dezimal(that)
        target_scale = scale_func(this.scale, that.scale)
        if rescale:
            this_diff = target_scale - this.scale
            that_diff = target_scale - that.scale
            this_value = this.value * (10 ** this_diff) if this_diff > 0 else this.value
            that_value = that.value * (10 ** that_diff) if that_diff > 0 else that.value
        else:
            this_value = this.value
            that_value = that.value
        result = func(this_value, that_value)
        if result_constructor is not None:
            return result_constructor(result, target_scale)
        return Dezimal(result, target_scale)

    def truncate(self, scale: int) -> 'Dezimal':
        if scale < 0:
            raise ValueError(scale)
        if scale >= self.scale:
            return self
        scale_diff = self.scale - scale
        target_value = self.value // (10 ** scale_diff)
        return Dezimal(target_value, scale)

    def __eq__(self, other) -> bool:
        if not isinstance(other, Dezimal):
            try:
                other = Dezimal(other)
            except TypeError:
                return False
        return self.value == other.value and self.scale == other.scale

    def __ne__(self, other) -> bool:
        try:
            other = Dezimal(other)
        except TypeError:
            return False
        return self.value != other.value or self.scale != other.scale

    def __lt__(self, other) -> bool:
        return self._scaled(self, other, lambda a, b: a < b, result_constructor=lambda a, _: bool(a))

    def __gt__(self, other) -> bool:
        return self._scaled(self, other, lambda a, b: a > b, result_constructor=lambda a, _: bool(a))

    def __le__(self, other) -> bool:
        return self._scaled(self, other, lambda a, b: a <= b, result_constructor=lambda a, _: bool(a))

    def __ge__(self, other) -> bool:
        return self._scaled(self, other, lambda a, b: a >= b, result_constructor=lambda a, _: bool(a))

    def __neg__(self) -> 'Dezimal':
        return Dezimal(-self.value, self.scale)

    def __abs__(self) -> 'Dezimal':
        return Dezimal(abs(self.value), self.scale)

    def __pos__(self) -> 'Dezimal':
        return self

    def __add__(self, other) -> 'Dezimal':
        return self._scaled(self, other, lambda a, b: a + b)

    def __radd__(self, other) -> 'Dezimal':
        return Dezimal(other) + self

    def __sub__(self, other) -> 'Dezimal':
        return self._scaled(self, other, lambda a, b: a - b)

    def __rsub__(self, other) -> 'Dezimal':
        return Dezimal(other) - self

    def __mul__(self, other) -> 'Dezimal':
        return self._scaled(self, other, lambda a, b: a * b, lambda a, b: a + b, rescale=False)

    def __rmul__(self, other) -> 'Dezimal':
        return Dezimal(other) * self

    def __floordiv__(self, other) -> 'Dezimal':
        return Dezimal(int(self) // int(other))

    def __rfloordiv__(self, other) -> 'Dezimal':
        return Dezimal(other) // self

    @staticmethod
    def div(this: 'Dezimal', that: 'Dezimal', maxscale: Union[int, type(None)] = None, minscale: int = 17) -> 'Dezimal':
        d1 = 10 ** this.scale
        d2 = 10 ** that.scale
        n = this.value * d2
        d = that.value * d1
        gcd = math.gcd(n, d)
        n //= gcd
        d //= gcd
        if d == 1:
            return Dezimal(n)

        matches = set()
        scale = 0
        value = 0
        while n != 0 and ((n, d) not in matches or scale < minscale) and (not maxscale or scale < maxscale):
            matches.add((n, d))
            value *= 10
            scale += 1
            n *= 10
            value += n // d
            n = n % d

        return Dezimal(value, scale)

    def __truediv__(self, other) -> 'Dezimal':
        return Dezimal.div(self, Dezimal(other))

    def __rtruediv__(self, other) -> 'Dezimal':
        return Dezimal.div(Dezimal(other), self)
