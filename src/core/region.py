from dataclasses import dataclass
from typing import Tuple
from .point import Point

@dataclass(frozen=True, slots=True)
class Region:
    corner1: Point
    corner2: Point

    def __post_init__(self):
        if self.corner1 == self.corner2:
            raise ValueError("corner1 and corner2 must not be identical")

    def width(self) -> float:
        return float(abs(self.corner2.x - self.corner1.x))

    def height(self) -> float:
        return float(abs(self.corner2.y - self.corner1.y))

    def center(self) -> Point:
        return Point((self.corner1.x + self.corner2.x) / 2,
                     (self.corner1.y + self.corner2.y) / 2)

    def normalize(self) -> "Region":
        x1, y1 = min(self.corner1.x, self.corner2.x), min(self.corner1.y, self.corner2.y)
        x2, y2 = max(self.corner1.x, self.corner2.x), max(self.corner1.y, self.corner2.y)
        return Region(Point(x1, y1), Point(x2, y2))

    def clamp(self, max_width: int, max_height: int) -> "Region":
        r = self.normalize()
        x1 = min(max(r.corner1.x, 0), max_width - 1)
        y1 = min(max(r.corner1.y, 0), max_height - 1)
        x2 = min(max(r.corner2.x, 0), max_width - 1)
        y2 = min(max(r.corner2.y, 0), max_height - 1)
        return Region(Point(x1, y1), Point(x2, y2))

    def contains(self, pt: Point) -> bool:
        left, right = min(self.corner1.x, self.corner2.x), max(self.corner1.x, self.corner2.x)
        top, bottom = min(self.corner1.y, self.corner2.y), max(self.corner1.y, self.corner2.y)
        return bool(left <= pt.x <= right and top <= pt.y <= bottom)

    def to_tuple_x1_y1_x2_y2(self) -> Tuple[int, int, int, int]:
        r = self.normalize()
        return int(r.corner1.x), int(r.corner1.y), int(r.corner2.x), int(r.corner2.y)
