from typing import Union, Callable, Optional, Tuple, List

from fibomat.shapes import DimShape
from fibomat.linalg import Transformable, DimTransformable, Vector, DimVector, VectorLike
from fibomat.units import U_, scale_factor
from fibomat.layout.lattices.lattice_base import LatticeBaseMixin
from fibomat.layout.groups.dim_group import DimGroup


class DimLattice(DimGroup, LatticeBaseMixin):
    def __init__(self, elements: List[DimTransformable], description: Optional[str] = None):
        super().__init__(elements, description=description)

    @classmethod
    def generate(
        cls,
        dim_boundary: DimShape,
        dim_u: VectorLike, dim_v: VectorLike,
        dim_element: Union[Transformable, Callable[[Tuple[float, float], Tuple[int, int]], Optional[DimTransformable]]],
        dim_center: Optional[VectorLike] = None,
        predicate: Optional[Union[Callable, List[Callable]]] = None,
        explode: bool = False,
        remove_outliers: bool = False,
        # break_layouts: bool = False
    ):
        """
        predicate get its coordinates in µm

        Args:
            dim_boundary:
            dim_u:
            dim_v:
            dim_element:
            dim_center:
            predicate:
            explode:
            remove_outliers:

        Returns:

        """
        base_unit = U_('µm')

        def dim_vec_to_vec(dim_vec: DimVector) -> Vector:
            return scale_factor(base_unit, dim_vec.unit) * dim_vec.vector

        def vec_to_dim_vec(vec: Vector) -> DimVector:
            return vec * base_unit

        u = dim_vec_to_vec(DimVector(dim_u))
        v = dim_vec_to_vec(DimVector(dim_v))

        center = dim_vec_to_vec(DimVector(dim_center))

        boundary = dim_boundary.scaled(scale_factor(base_unit, dim_boundary.unit), 'pivot').shape

        if callable(dim_element):
            element_gen = dim_element
        else:
            def element_gen(*args):
                return dim_element

        elements = cls._generate_impl(
            boundary, u, v, center, element_gen, predicate, explode, remove_outliers, dim_vec_to_vec, vec_to_dim_vec
        )

        return cls(elements)
