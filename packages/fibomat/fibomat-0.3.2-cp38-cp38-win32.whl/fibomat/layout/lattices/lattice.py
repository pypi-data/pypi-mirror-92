from typing import Iterable, Union, Callable, Optional, Tuple, List

from fibomat.shapes import HollowArcSpline, ArcSplineCompatible, Rect
from fibomat.linalg import Transformable, Vector, VectorLike
from fibomat.layout.lattices.lattice_base import LatticeBaseMixin
from fibomat.layout.groups.group import Group
from fibomat.units import U_


class Lattice(Group, LatticeBaseMixin):
    def __init__(self, elements: List[Transformable], description: Optional[str] = None):
        super().__init__(elements, description)

    @classmethod
    def generate_rect(
        cls,
        nu: int, nv: int,
        du: float, dv: float,
        element: Union[Transformable, Callable],
        center: Optional[VectorLike] = None,
        predicate: Optional[Union[Callable, List[Callable]]] = None,
        explode: bool = False,
        remove_outliers: bool = False,
    ):
        nu = int(nu)
        nv = int(nv)

        if nu < 1 or nv < 1:
            raise ValueError('nu and nv must be at least 1.')

        du = float(du)
        dv = float(dv)

        return cls.generate(
            Rect(width=du*nu, height=dv*nv), (du, 0), (0, -dv), element, center, predicate, explode, remove_outliers
        )

    @classmethod
    def generate(
        cls,
        boundary: Union[HollowArcSpline, ArcSplineCompatible],
        u: VectorLike, v: VectorLike,
        element: Union[Transformable, Callable[[Tuple[float, float], Tuple[int, int]], Optional[Transformable]]],
        center: Optional[VectorLike] = None,
        predicate: Optional[Union[Callable, List[Callable]]] = None,
        explode: bool = False,
        remove_outliers: bool = False,
        # break_layouts: bool = False
    ):
        u = Vector(u)
        v = Vector(v)

        center = Vector(center)

        if callable(element):
            element_gen = element
        else:
            def element_gen(*args):
                return element

        elements = cls._generate_impl(
            boundary, u, v, center, element_gen, predicate, explode, remove_outliers, lambda x: x, lambda x: x
        )

        return cls(elements)

    def __mul__(self, other):
        if isinstance(other, U_):
            from fibomat.layout.lattices.dim_lattice import DimLattice
            return DimLattice([elem * other for elem in self.elements], description=self.description)
        raise NotImplementedError

