import copy as _copy
from enum import Enum, IntEnum
from json import dumps as _dumps, loads as _loads
from typing import *
from typing import BinaryIO

from PIL.Image import Image as _Image

from .Keys import Keys
from .MixIns import *
from ..debug import *




BinaryIO = BinaryIO

_T = TypeVar("_T")
_KT = TypeVar("_KT")
_VT = TypeVar("_VT")


@overload
def Assert(d: Any, t: Type): ...
@overload
def Assert(d: Any, *types: Type): ...
def Assert(d: Any, *t: type):
    if not isinstance(d, t): throw(d, *t)

@overload
def throw(d: Any, t: Type): ...
@overload
def throw(d: Any, *types: Type): ...
def throw(d: Any, *types: Type):
    if not types: raise ValueError('expected types must be provided')

    if len(types) == 1: raise TypeError(f'Expecting {types[0]}   got type {type(d)}')

    raise TypeError(f'Expecting one of {types}   got type {type(d)}')

def AssertKeys(d: Dict, *args):
    for key in args:
        if key not in d: RaiseKeyError(key, d)

def ConvertBool(o: Union[bool, str]) -> bool:
    if isinstance(o, bool): return o
    if isinstance(o, str): return o.lower() == 'true'

    throw(o, bool)

def RaiseKeyError(key, d: Dict): raise KeyError(f'{key} not in {d.keys()}')



# noinspection DuplicatedCode
def _serialize(o):
    if isinstance(o, Enum): return o.value

    if isinstance(o, BaseSetModel): return o.ToList()

    if isinstance(o, BaseListModel): return o

    if isinstance(o, BaseDictModel): return o.ToDict()

    if hasattr(o, 'ToList') and callable(o.ToList): return o.ToList()

    if hasattr(o, 'ToDict') and callable(o.ToDict): return o.ToDict()

    return o


# noinspection DuplicatedCode
def _ToDict(o: Dict) -> Dict[_KT, Union[_VT, Dict, str]]:
    d = { }
    for key, value in o.items():
        if isinstance(value, Enum): d[key] = value.value

        elif isinstance(value, BaseListModel): d[key] = value

        elif isinstance(value, BaseSetModel): d[key] = value.ToList()

        elif isinstance(value, BaseDictModel): d[key] = value.ToDict()

        elif hasattr(value, 'ToList') and callable(value.ToList): d[key] = value.ToList()

        elif hasattr(value, 'ToDict') and callable(value.ToDict): d[key] = value.ToDict()

        elif hasattr(value, 'ToString') and callable(value.ToString): d[key] = value.ToString()

        else: d[key] = value
    return d



class BaseModel(object):
    def Clone(self): return _copy.deepcopy(self)
    def ToString(self) -> str:
        # try: return f'<{self.__class__.__qualname__} Object. State: {self.__dict__}>'
        # except AttributeError: return f'<{self.__class__.__name__} Object. State: {self.__dict__}>'
        try:
            return f'<{self.__class__.__qualname__} Object() [ {self.ToJsonString()} ]'
        except AttributeError:
            return f'<{self.__class__.__name__} Object() [ {self.ToJsonString()} ]'
    def _Filter(self, func: callable): raise NotImplementedError()
    def ToDict(self): raise NotImplementedError()
    def ToList(self): raise NotImplementedError()
    def enumerate(self): raise NotImplementedError()
    def Count(self) -> int: raise NotImplementedError()
    def Empty(self) -> bool: raise NotImplementedError()


    @classmethod
    def Parse(cls, d): return cls()
    @classmethod
    def FromJson(cls, string: Union[str, bytes, bytearray], **kwargs): return cls.Parse(_loads(string, **kwargs))
    def ToJsonString(self) -> str: return _dumps(self, indent=4, default=_serialize)  # , cls=JsonEncoder)



class BaseListModel(list, BaseModel, List[_T]):
    def __init__(self, source: Union[List, Iterable] = None):
        super().__init__(source or [])
    def __str__(self): return self.ToString()

    def __contains__(self, item: _T): return super().__contains__(item)
    def __setitem__(self, key: int, value: _T): return super().__setitem__(key, value)
    def __getitem__(self, key: int) -> Optional[_T]:
        try: return super().__getitem__(key)
        except KeyError: return None
    def __iter__(self) -> Iterable[_T]: return super().__iter__()
    def enumerate(self) -> Iterable[Tuple[int, _T]]: return enumerate(self)

    @property
    def Count(self) -> int: return len(self)
    @property
    def Empty(self) -> bool: return self.Count == 0

    def Iter(self) -> Iterable[int]: return range(len(self))

    def _Filter(self, func: callable) -> List[_T]: return list(filter(func, self))
    def ToList(self) -> List[_T]: return list(self)


    def ToDict(self) -> Dict[int, _T]:
        d = { }
        for key, value in self.enumerate():
            if hasattr(value, 'ToDict') and callable(value.ToDict):
                d[key] = value.ToDict()
            else:
                d[key] = value
        return d

    @classmethod
    def Parse(cls, d):
        if isinstance(d, list):
            return cls(d)

        throw(d, list)

    @classmethod
    def Create(cls, *args: _T):
        return cls(args)



class BaseSetModel(set, BaseModel, Set[_T]):
    def __str__(self): return self.ToString()
    def __contains__(self, item: _T): return super().__contains__(item)
    def __delitem__(self, item: _T): return self.discard(item)
    # def __isub__(self, item: _T): return self.discard(item)
    def __iadd__(self, item: _T): return self.add(item)
    def __iter__(self) -> Iterable[_T]: return super().__iter__()
    def enumerate(self) -> Iterable[Tuple[int, _T]]: return enumerate(self)

    @property
    def Count(self) -> int: return len(self)
    @property
    def Empty(self) -> bool: return self.Count == 0

    def _Filter(self, func: callable): return filter(func, self)
    def extend(self, items: Union[List[_T], Set[_T]]):
        return self.update(items)
        # for _item in items: self.add(_item)

    def ToList(self) -> List[_T]: return [i for i in self]
    def ToDict(self) -> Dict[int, _T]: return dict(self.enumerate())

    @staticmethod
    def FromArgs(*items: _T): return BaseSetModel.Parse(items)

    @classmethod
    def Parse(cls, d):
        if isinstance(d, list):
            return cls(d)

        throw(d, list)

    @classmethod
    def Create(cls, *args: _T):
        return cls(args)



class BaseDictModel(dict, BaseModel, Dict[_KT, _VT]):
    def __init__(self, source: dict = None, **kwargs):
        if source is not None: super().__init__(source, **kwargs)
        else: super().__init__(**kwargs)
    def __str__(self): return self.ToString()

    def __delitem__(self, item: Union[_KT, _VT]): return super().__delitem__(item)
    def __contains__(self, item: Union[_KT, _VT]): return super().__contains__(item)
    def __setitem__(self, key: _KT, value: _VT): return super().__setitem__(key, value)
    def __getitem__(self, key: _KT) -> _VT: return super().__getitem__(key)
    def __iter__(self) -> Iterable[_VT]: return super().__iter__()

    def values(self) -> Iterable[_VT]: return super().values()
    def items(self) -> Iterable[Tuple[_KT, _VT]]: return super().items()
    def keys(self) -> Iterable[_KT]: return super().keys()
    def enumerate(self) -> Iterable[Tuple[int, _T]]: return enumerate(self)

    @property
    def Count(self) -> int: return len(self)
    @property
    def Empty(self) -> bool: return self.Count == 0

    def _Filter(self, func: callable) -> List[_VT]: return list(filter(func, self.values()))

    def ToList(self) -> List[_T]: return list(self.items())
    def ToDict(self) -> Dict[_KT, Union[_VT, Dict, str]]: return _ToDict(self)

    @classmethod
    def Parse(cls, d):
        if isinstance(d, dict):
            return cls(d)

        throw(d, dict)

    @classmethod
    def Create(cls, **kwargs: _VT):
        return cls(kwargs)


class RotationAngle(IntEnum):
    none = 0
    right = 90
    upside_down = 180
    left = 270

    def Rotate(self, angle: int = -90):
        return RotationAngle((self.value + angle) % 360)


# noinspection DuplicatedCode
class Size(BaseDictModel[str, int]):
    __slots__ = []
    @property
    def width(self) -> int: return self[Keys.width]
    @property
    def height(self) -> int: return self[Keys.height]

    def ToTuple(self) -> Tuple[int, int]: return int(self.width), int(self.height)
    def __iter__(self) -> Iterable[int]: return iter(self.ToTuple())

    def __eq__(self, other: Union[Tuple[int, int], List[int], 'Size']):
        if isinstance(other, (tuple, list)):
            other = Size.FromTuple(other)
        if isinstance(other, Size):
            return self.width == other.width and self.height == other.height

        raise TypeError(type(other), (Size, tuple, list))
    def __ne__(self, other: Union[Tuple[int, int], List[int], 'Size']): return not self.__eq__(other)

    def __gt__(self, other: Union[Tuple[int, int], List[int], 'Size']):
        if isinstance(other, (tuple, list)):
            other = Size.FromTuple(other)
        if isinstance(other, Size):
            return self.width > other.width and self.height > other.height

        raise TypeError(type(other), (Size, tuple, list))
    def __lt__(self, other: Union[Tuple[int, int], List[int], 'Size']):
        if isinstance(other, (tuple, list)):
            other = Size.FromTuple(other)
        if isinstance(other, Size):
            return self.width < other.width and self.height < other.height

        raise TypeError(type(other), (Size, tuple, list))
    def __ge__(self, other: Union[Tuple[int, int], List[int], 'Size']):
        if isinstance(other, (tuple, list)):
            other = Size.FromTuple(other)
        if isinstance(other, Size):
            return self.width >= other.width and self.height >= other.height

        raise TypeError(type(other), (Size, tuple, list))
    def __le__(self, other: Union[Tuple[int, int], List[int], 'Size']):
        if isinstance(other, (tuple, list)):
            other = Size.FromTuple(other)
        if isinstance(other, Size):
            return self.width <= other.width and self.height <= other.height

        raise TypeError(type(other), (Size, tuple, list))


    @staticmethod
    def convert(o: Union['Size', _Image, Tuple[int, int]]) -> Tuple[int, int]:
        if isinstance(o, Size): return o.ToTuple()
        elif isinstance(o, _Image): return o.size
        elif isinstance(o, tuple): return o
        throw(o, Size, _Image, tuple)

    def Factors(self, widthMax: int, heightMax: int) -> Tuple[float, float]:
        # if widthMax > self.width or heightMax > self.height:
        #     return self.width / widthMax , self.height / heightMax

        return widthMax / self.width, heightMax / self.height

    def MinScalingFactor(self, widthMax: int, heightMax: int) -> float: return min(self.Factors(widthMax, heightMax))
    def MaxScalingFactor(self, widthMax: int, heightMax: int) -> float: return max(self.Factors(widthMax, heightMax))


    @overload
    def Scale(self, size: Union['Size', _Image, Tuple[int, int]], AsSize: bool) -> 'Size': ...
    @overload
    def Scale(self, size: Union['Size', _Image, Tuple[int, int]]) -> Tuple[int, int]: ...

    def Scale(self, size: Union['Size', _Image, Tuple[int, int]], AsSize: bool = False) -> Union['Size', tuple[int, int]]:
        w, h = self.convert(size)
        factor = self.MinScalingFactor(w, h)
        result = Size.Create(self.width * factor, self.height * factor)
        if AsSize: return result

        return result.ToTuple()

    @staticmethod
    def FromTuple(v: Tuple[int, int]): return Size.Create(*v)
    @classmethod
    def Create(cls, width: Union[int, float], height: Union[int, float]): return cls({ Keys.width: int(width), Keys.height: int(height) })
    @classmethod
    def Parse(cls, d):
        if d is None: return None
        if isinstance(d, dict):
            AssertKeys(d, Keys.width, Keys.height)
            return cls(d)

        throw(d, dict)
class Ratios(Size):
    @property
    def LANDSCAPE(self) -> float: return self.width / self.height
    @property
    def PORTRAIT(self) -> float: return self.height / self.width



# noinspection DuplicatedCode
class Point(BaseDictModel[str, int]):
    __slots__ = []
    @property
    def y(self) -> int: return self[Keys.y]
    @property
    def x(self) -> int: return self[Keys.x]

    def ToTuple(self) -> Tuple[int, int]: return int(self.x), int(self.y)
    def __iter__(self) -> Iterable[int]: return iter(self.ToTuple())

    def __eq__(self, other: Union[Tuple[int, int], List[int], 'Point']):
        if isinstance(other, (tuple, list)):
            other = Point.FromTuple(other)
        if isinstance(other, Point):
            return self.x == other.y and self.y == other.y

        raise TypeError(type(other), (Point, tuple, list))
    def __ne__(self, other: Union[Tuple[int, int], List[int], 'Size']): return not self.__eq__(other)

    def __gt__(self, other: Union[Tuple[int, int], List[int], 'Point']):
        if isinstance(other, (tuple, list)):
            other = Point.FromTuple(other)
        if isinstance(other, Point):
            return self.x > other.x and self.y > other.y

        raise TypeError(type(other), (Size, tuple, list))
    def __lt__(self, other: Union[Tuple[int, int], List[int], 'Point']):
        if isinstance(other, (tuple, list)):
            other = Point.FromTuple(other)
        if isinstance(other, Point):
            return self.x < other.x and self.y < other.y

        raise TypeError(type(other), (Size, tuple, list))
    def __ge__(self, other: Union[Tuple[int, int], List[int], 'Point']):
        if isinstance(other, (tuple, list)):
            other = Point.FromTuple(other)
        if isinstance(other, Point):
            return self.x >= other.x and self.y >= other.y

        raise TypeError(type(other), (Size, tuple, list))
    def __le__(self, other: Union[Tuple[int, int], List[int], 'Point']):
        if isinstance(other, (tuple, list)):
            other = Point.FromTuple(other)
        if isinstance(other, Point):
            return self.x <= other.x and self.y <= other.y

        raise TypeError(type(other), (Size, tuple, list))

    @staticmethod
    def FromTuple(v: Tuple[int, int]): return Point.Create(*v)
    @classmethod
    def Create(cls, x: int, y: int): return cls({ Keys.x: x, Keys.y: y })
    @classmethod
    def Parse(cls, d):
        if d is None: return None
        if isinstance(d, dict):
            AssertKeys(d, Keys.x, Keys.y)
            return cls(d)

        throw(d, dict)


class CropBox(BaseDictModel[str, int]):
    """  Adjusted box (x, y, width, height), ensuring that all dimensions resides within the boundaries. """
    __slots__ = []
    @property
    def y(self) -> int: return self[Keys.y]
    @property
    def x(self) -> int: return self[Keys.x]

    def Set(self, x: int, y: int):
        self[Keys.x] = x
        self[Keys.y] = y
        return self

    @property
    def width(self) -> int: return self[Keys.width]
    @property
    def height(self) -> int: return self[Keys.height]

    def Resize(self, width: int, height: int):
        self[Keys.width] = width
        self[Keys.height] = height
        return self

    def __iter__(self) -> Iterable[int]: return iter(self.ToTuple())

    def IsAllVisible(self, pic: Point, img: Size) -> bool:
        return (pic.x >= 0 and
                pic.y >= 0 and
                (pic.y + img.height) <= self.height and
                (pic.x + img.width) <= self.width)

    @overload
    def Update(self, pic: Point, img: Size, view: Size): ...
    @overload
    def Update(self, pic: Point, img: Size, view: Size, OnlyZero: Any): ...
    @overload
    def Update(self, pic: Point, img: Size, view: Size, ZeroOrMore: Any): ...
    @overload
    def Update(self, pic: Point, img: Size, view: Size, ZeroOrLess: Any): ...
    @overload
    def Update(self, pic: Point, img: Size, view: Size, KeepInView: Any): ...

    def Update(self, pic: Point, img: Size, view: Size, **kwargs):
        """
            The goal is to find the area of the object that is visible, and return it's coordinates.

            x, y: root left point of the box, in (x, y) format.
            : bottom right point of the box, in (x, y) format.

        :param view: size of the view where the photo/object is displayed
        :param pic:  where the photo is placed, in (x, y) format. For Example: Canvas placements. This can be any integer
        :param img:  size of the photo, in (Width, Height) format.
        :return: True if all of the object will be visible, otherwise false.
        """
        def XY(_v: int, _img: int, _edit: int, args: KeysView) -> int:
            if 'OnlyZero' in args:
                return 0

            if 'ZeroOrMore' in args:
                return _v if _v >= 0 else 0

            if 'ZeroOrLess' in args:
                return _v if _v <= 0 else 0

            if 'KeepInView' in args:
                if _v == 0:
                    if _img < _edit:
                        return 0

                    if _img >= _edit:
                        return _v

                    return _v

                elif _v > 0:
                    if _v + _img >= _edit:
                        return 0

                    if _v + _img < _edit:
                        return _v

                    return _v

                else:  # _y < 0
                    if _v + _img <= _edit:
                        return - abs(_img - _edit)

                    if _v + _img > _edit:
                        return _v

                    return _v

            return _v

        self[Keys.x] = XY(pic.x, img.width, view.width, kwargs.keys())
        self[Keys.y] = XY(pic.y, img.height, view.height, kwargs.keys())


        @Debug()
        def Width(_v: int, _img: int, _edit: int) -> int:
            if _v == 0:
                if _img < _edit:
                    return _img

                # img_h >= edit_h:
                return _edit

            elif _v > 0:
                if _v + _img >= _edit:
                    return _edit - _v

                if _v + _img < _edit:
                    return _img

                return _img

            else:  # _y < 0
                if _v + _img < _edit:
                    # print('__Width__', _v, _img, _edit)
                    return _img + _v

                # _y + img_h >= edit_h
                return _edit
        self[Keys.width] = Width(self.x, img.width, view.width)


        @Debug()
        def Height(_v: int, _img: int, _edit: int) -> int:
            if _v == 0:
                if _img < _edit:
                    return _img

                # img_h >= edit_h:
                return _edit

            elif _v > 0:
                if _v + _img >= _edit:
                    return _edit - _v

                if _v + _img < _edit:
                    return _img

                return _img

            else:  # _y < 0
                if _v + _img < _edit:
                    # print('__Height__', _v, _img, _edit)
                    return _img + _v

                # _y + img_h >= edit_h
                return _edit
        self[Keys.height] = Height(self.y, img.height, view.height)

    def Scale(self, image_size: Union[Size, _Image, Tuple[int, int]]) -> Size: return self.ToPointSize()[1].Scale(image_size, AsSize=True)
    def EnforceBounds(self, image_size: Union[Size, _Image, Tuple[int, int]]) -> Tuple[int, int, int, int]:
        img_w, img_h = Size.convert(image_size)
        self.Set(int(self.x if self.x >= 0 else 0),
                 int(self.y if self.y >= 0 else 0))
        self.Resize(int(self.width if self.width <= img_w else img_w),
                    int(self.height if self.height <= img_h else img_h))

        return self.ToTuple()


    def Right(self, amount: int):
        self[Keys.x] += amount
        return self.TopLeft
    def Left(self, amount: int):
        self[Keys.x] -= amount
        return self.TopLeft
    def Up(self, amount: int):
        self[Keys.y] -= amount
        return self.TopLeft
    def Down(self, amount: int):
        self[Keys.y] += amount
        return self.TopLeft



    def ToTuple(self) -> Tuple[int, int, int, int]: return self.x, self.y, self.width, self.height
    def ToPointSize(self) -> Tuple[Point, Size]: return self.TopLeft, Size.Create(self.width, self.height)
    def ToPoints(self) -> Tuple[Point, Point]: return self.TopLeft, self.BottomRight
    def BoundaryPoints(self) -> Tuple[Point, Point, Point, Point]: return self.TopLeft, self.TopRight, self.BottomLeft, self.BottomRight

    @property
    def TopLeft(self) -> Point: return Point.Create(self.x, self.y)
    @property
    def TopRight(self) -> Point: return Point.Create(self.x + self.width, self.y)
    @property
    def BottomLeft(self) -> Point: return Point.Create(self.x, self.y + self.height)
    @property
    def BottomRight(self) -> Point: return Point.Create(self.x + self.width, self.y + self.height)

    # noinspection PyMethodOverriding
    @classmethod
    def Create(cls, x: int, y: int, width: int, height: int):
        return cls({
            Keys.x:      int(x),
            Keys.y:      int(y),
            Keys.width:  int(width),
            Keys.height: int(height),
            })
    @classmethod
    def Crop(cls, x: int, y: int, width: int, height: int, *, pic: Point, img: Size, edit: Size):
        o = cls.Create(x, y, width, height)
        o.Update(pic, img, edit)
        return o
    @classmethod
    def FromPoints(cls, start: Point, end: Point):
        x1, y1 = start
        x2, y2 = end
        return cls.Create(x1, y1, x2 - x1, y2 - y1)
    @classmethod
    def FromPointSize(cls, start: Point, size: Size):
        x1, y1 = start
        w, h = size
        return cls.Create(x1, y1, w, h)

    @classmethod
    def Box(cls, start: Point, end: Point, pic: Point, img: Size):
        """
        :param start: root start point of the box, in (x, y) format.
        :param end: root end point of the box, in (x, y) format.
        :param pic:  root left point of the photo, in (x, y) format.
        :param img:  size of the photo, in (width, height) format.
        :return: adjusted box dimensions, ensuring that it resides within the photo.
        """

        x1, y1 = start
        x2, y2 = end

        # going right
        x1 = x1 if x1 > pic.x else pic.x
        y1 = y1 if y1 > pic.y else pic.y

        # going left
        x1 = x1 if x1 < pic.x + img.width else pic.x + img.width
        y1 = y1 if y1 < pic.y + img.height else pic.y + img.height

        # going right
        x2 = x2 if x2 < pic.x + img.width else pic.x + img.width
        y2 = y2 if y2 < pic.y + img.height else pic.y + img.height

        # going left
        x2 = x2 if x2 > pic.x else pic.x
        y2 = y2 if y2 > pic.y else pic.y

        return cls.Create(int(x1), int(y1), int(x2 - x1), int(y2 - y1))
    @classmethod
    def BoxSize(cls, start: Point, end: Size, pic: Point, img: Size):
        """
        :param start: root start point of the box, in (x, y) format.
        :param end: root end point of the box, in (x, y) format.
        :param pic:  root left point of the photo, in (x, y) format.
        :param img:  size of the photo, in (width, height) format.
        :return: adjusted box dimensions, ensuring that it resides within the photo.
        """
        return cls.Box(start, Point.Create(start.x + end.width, start.y + end.height), pic, img)
    @classmethod
    def BoxDimensions(cls, x: int, y: int, width: int, height: int, pic: Point, img: Size):
        """
        :param x: root start point of the box, in (x, y) format.
        :param y: root start point of the box, in (x, y) format.
        :param width: root end point of the box, in (x, y) format.
        :param height: root end point of the box, in (x, y) format.
        :param pic:  root left point of the photo, in (x, y) format.
        :param img:  size of the photo, in (width, height) format.
        :return: adjusted box dimensions, ensuring that it resides within the photo.
        """
        return cls.Box(Point.Create(x, y), Point.Create(x + width, y + height), pic, img)


    @classmethod
    def Parse(cls, d):
        if isinstance(d, dict):
            AssertKeys(d, Keys.width, Keys.height, Keys.x, Keys.y)
            for k, v in d.items():
                d[k] = int(v)

            return cls(d)

        throw(d, dict)
