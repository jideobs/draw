import uuid

import pytest

from shape import Canvas, ShapeType, Coordinate, Size


@pytest.fixture
def canvas():
    canvas = Canvas()
    size = Size(10, 10)

    # Act:
    canvas.add(shape_type=ShapeType.Rectangle, 
               coordinate=Coordinate(1.0, 2.0), 
               size=size)
    canvas.add(shape_type=ShapeType.Rectangle, 
               coordinate=Coordinate(3.2, 4.1), 
               size=size)
    canvas.add(shape_type=ShapeType.Rectangle, 
               coordinate=Coordinate(5.2, 6.1), 
               size=size)
    
    return canvas


def test_add_objects():
    # Arrange:
    canvas = Canvas()
    coordinate = Coordinate(1.0, 2.0)
    size = Size(10, 10)

    # Act:
    shape_id = canvas.add(shape_type=ShapeType.Rectangle, 
               coordinate=coordinate, 
               size=size)

    # Assert:
    assert shape_id is not None

    assert len(canvas.objects.values()) == 1

    shape = list(canvas.objects.values())[0]
    assert coordinate.x == shape.x_coordinate
    assert coordinate.y == shape.y_coordinate 
    assert size.width == shape.width
    assert size.height == shape.height


def test_delete_object__object_does_not_exist(canvas):
    # Arrange:
    shape_id = uuid.uuid4()

    # Act:
    deleted = canvas.delete(shape_id)

    # Assert:
    assert not deleted
    assert 3 == len(canvas.objects.values())


def test_delete_object__object_exists(canvas):
    # Arrange:
    shape = list(canvas.objects.values())[0]
    shape_id = shape._id

    # Act:
    deleted = canvas.delete(shape_id)

    # Assert:
    assert deleted
    assert len(canvas.objects.values()) == 2
    assert shape_id not in canvas.objects


def test_move_object__object_does_not_exist(canvas):
    # Arrange:
    shape_id = uuid.uuid4()

    # Act:
    moved = canvas.delete(shape_id)

    # Assert:
    assert not moved


def test_move_object__object_exists(canvas):
    # Arrange:
    shape = list(canvas.objects.values())[0]
    shape_id = shape._id
    new_coordinate = Coordinate(5.0, 7.0)

    # Act:
    moved = canvas.move(shape_id, new_coordinate)

    # Assert:
    assert moved

    moved_shape = canvas.objects[shape_id]
    assert new_coordinate.x == moved_shape.x_coordinate
    assert new_coordinate.y == moved_shape.y_coordinate


def test_resize_object__object_does_not_exist(canvas):
    # Arrange:
    shape_id = uuid.uuid4()
    new_size = Size(30, 50)

    # Act:
    resized = canvas.resize(shape_id, new_size)

    # Assert:
    assert not resized


def test_resize_object__object_exists(canvas):
    # Arrange:
    shape = list(canvas.objects.values())[0]
    shape_id = shape._id
    new_size = Size(5.0, 7.0)

    # Act:
    resized = canvas.resize(shape_id, new_size)

    # Assert:
    assert resized

    resized_shape = canvas.objects[shape_id]
    assert new_size.height == resized_shape.height
    assert new_size.width == resized_shape.width


def test_multi_select__select_2_objects(canvas):
    # Arrange:
    start_coordinate = Coordinate(2.1, 3.2)
    stop_coordinate = Coordinate(6.2, 7.2)

    # Act:
    canvas.multi_select(start_coordinate, stop_coordinate)

    # Assert:
    assert 2 == len(canvas.selected)


def test_move_selection(canvas):
    # Arrange:
    start_coordinate = Coordinate(2.1, 3.2)
    stop_coordinate = Coordinate(6.2, 7.2)
    canvas.multi_select(start_coordinate, stop_coordinate)

    new_coordinate = Coordinate(6.2, 7.2)

    # Act:
    moved = canvas.move_selection(new_coordinate)

    # Assert:
    assert moved


def test_delete_selection(canvas):
    # Arrange:
    start_coordinate = Coordinate(2.1, 3.2)
    stop_coordinate = Coordinate(6.2, 7.2)
    canvas.multi_select(start_coordinate, stop_coordinate)

    # Act:
    deleted = canvas.delete_selection()

    # Assert:
    assert deleted
    assert 1 == len(canvas.objects)


def test_resize_selection(canvas):
    # Arrange:
    start_coordinate = Coordinate(2.1, 3.2)
    stop_coordinate = Coordinate(6.2, 7.2)
    canvas.multi_select(start_coordinate, stop_coordinate)

    new_size = Size(30, 40)

    # Act:
    resized = canvas.resize_selection(new_size)

    # Assert:
    assert resized
