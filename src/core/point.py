from __future__ import annotations
from dataclasses import dataclass
from typing import Union, Optional, Tuple
import math
import numpy as np

from .interfaces.i_point import IPoint

Number = Union[int, float, np.integer, np.floating]

@dataclass(frozen=True, slots=True)
class Point:
    x: Number
    y: Number

    # Immutable methods returning new Points
    def with_x(self, new_x: Number) -> Point:
        return Point(new_x, self.y)

    def with_y(self, new_y: Number) -> Point:
        return Point(self.x, new_y)

    def translate(self, dx: Number, dy: Number) -> Point:
        return Point(self.x + dx, self.y + dy)

    def scale(self, sx: Number, sy: Optional[Number] = None) -> Point:
        if sy is None: sy = sx
        return Point(self.x * sx, self.y * sy)

    def rotate(self, angle_deg: Number, origin: Optional[IPoint] = None) -> Point:
        if origin is None: ox, oy = 0.0, 0.0
        else: ox, oy = origin.x, origin.y
        theta = math.radians(angle_deg)
        cos_t, sin_t = math.cos(theta), math.sin(theta)
        tx, ty = self.x - ox, self.y - oy
        rx = tx * cos_t - ty * sin_t
        ry = tx * sin_t + ty * cos_t
        return Point(rx + ox, ry + oy)

    # Utilities
    def to_int(self) -> Point:
        return Point(int(self.x), int(self.y))

    def to_tuple_x_y(self) -> Tuple[Number, Number]:
        return (self.x, self.y)
    
    def to_tuple_y_x(self) -> Tuple[Number, Number]:
        return (self.y, self.x)
    
    def to_int_tuple_x_y(self) -> Tuple[int, int]:
        return (int(self.x), int(self.y))

    def to_int_tuple_y_x(self) -> Tuple[int, int]:
        return (int(self.y), int(self.x))