from typing import List
from dataclasses import dataclass
import uuid
import enum
import bisect


class ShapeType(enum.Enum):
    Triangle = 1
    Circle = 2
    Rectangle = 3


class MultiSelectionOperation(enum.Enum):
    Move = 1
    Resize = 2
    Delete = 3


@dataclass
class Coordinate:
    x: float
    y: float


@dataclass
class Size:
    width: float
    height: float


# We might want to make this an abstract then have a concrete class 
# of Triangle, Rectangle and Circle beign child class of Shape, after 
# careful consideration its better since each have different properties
# like circle having radius and triangle having length of each of its 3 sides, 
# the angles within it e.tc.
class Shape:
    _id: uuid.UUID

    x_coordinate: float
    y_coordinate: float

    width: float
    height: float

    def __init__(self, _id: uuid.UUID, shape_type: ShapeType, coordinate: Coordinate, size: Size) -> None:
        self._id = _id
        self.shape_type = shape_type

        self.x_coordinate = coordinate.x
        self.y_coordinate = coordinate.y

        self.width = size.width
        self.height = size.height

    def move(self, coordinate: Coordinate) -> None:
        self.x_coordinate = coordinate.x
        self.y_coordinate = coordinate.y

    def resize(self, size: Size) -> None:
        self.height = size.height
        self.width = size.width


class Connector:
    def __init__(self, shape_a: Shape, shape_b: Shape) -> None:
        self._shape_a = shape_a
        self._shape_b = shape_b


class Line(Connector):
    pass


class Arrow(Connector):
    pass


class Collection:
    def __init__(self, *args: List[Shape]):
        pass


class Canvas:
    def __init__(self):
        self.objects = {}
        self.sorted_objects = []
        self.selected = []

    def add(self, shape_type: ShapeType, coordinate: Coordinate, size: Size) -> uuid.UUID:
        shape_id = uuid.uuid4()
        shape = Shape(shape_id, shape_type, coordinate, size)
        self.objects[shape_id] = shape
        bisect.insort_left(self.sorted_objects, shape, key=lambda s: s.x_coordinate)

        return shape_id
    
    def delete(self, shape_id: uuid.UUID) -> bool:
        if shape_id in self.objects:
            del self.objects[shape_id]

            # Todo: update self.sorted_objects to remove deleted shape.
            return True
        return False

    def move(self, shape_id: uuid.UUID, coordinate: Coordinate) -> bool:
        if shape_id in self.objects:
            shape = self.objects[shape_id]
            shape.move(coordinate)

            return True
        return False
    
    def resize(self, shape_id: uuid.UUID, size: Size) -> bool:
        if shape_id in self.objects:
            shape = self.objects[shape_id]
            shape.resize(size)

            return True
        return False

    def multi_select_V1(self, start_coordinate: Coordinate, stop_coordinate: Coordinate) -> None:
        self.selected = []  # Reset the selection
        for shape_id, shape in self.objects.items():
            if ((start_coordinate.x <= shape.x_coordinate and start_coordinate.y <= shape.y_coordinate) and 
                    (stop_coordinate.x >= shape.x_coordinate and stop_coordinate.y >= shape.y_coordinate)):
                self.selected.append(shape_id)

    # this finds the start_index and stop_index in O(log n) and searches on shapes that fall within this range
    # of category.
    def multi_select(self, start_coordinate: Coordinate, stop_coordinate: Coordinate) -> None:
        start_index = bisect.bisect_left(self.sorted_objects, start_coordinate.x, key=lambda s: s.x_coordinate)
        stop_index = bisect.bisect_right(self.sorted_objects, stop_coordinate.x, key=lambda s: s.x_coordinate)
        for shape in self.sorted_objects[start_index:stop_index]:
            if start_coordinate.y <= shape.y_coordinate <= stop_coordinate.y:
                self.selected.append(shape._id)

    # Todo: each shape's position within the selection should be moved relative to its previous position and the
    # selection new position.
    def move_selection(self, coordinate: Coordinate) -> bool:
        return all([self.move(shape_id, coordinate)  for shape_id in self.selected])
    
    def delete_selection(self) -> bool:
        return all([self.delete(shape_id) for shape_id in self.selected])

    # Todo: this needs to be resized relative to the selection size and each shape's size.
    def resize_selection(self, size: Size) -> bool:
        return all([self.resize(shape_id, size) for shape_id in self.selected])
    

