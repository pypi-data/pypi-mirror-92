from typing import Optional, Dict

import numpy as np

import svgwrite
import svgwrite.container
import svgwrite.shapes
import svgwrite.extensions

from fibomat.backend import BackendBase
from fibomat.site import Site
from fibomat.units import U_, Q_, scale_factor
from fibomat.utils import PathLike
from fibomat.pattern import Pattern
from fibomat.shapes import Rect, Polygon, Circle


class SVGBackend(BackendBase):
    def __init__(self, pixel_scale: Q_ = Q_('0.01 µm'), stroke_width: float = 0.1, description: Optional[str] = None):
        super().__init__()

        self._description = description
        self._pixel_scale = pixel_scale
        self._stroke_width = stroke_width

        # sites are mapped to svg groups
        self._layers = []
        self._current_layer: Optional[Dict] = None

        self._total_bounding_box = None

    def process_site(self, new_site: Site) -> None:
        self._current_layer = {'id': new_site.description or None, 'elements': []}
        self._layers.append(self._current_layer)
        super().process_site(new_site)

    def process_pattern(self, ptn: Pattern) -> None:
        if not self._total_bounding_box:
            self._total_bounding_box = ptn.bounding_box
        else:
            self._total_bounding_box = self._total_bounding_box.extended(ptn.bounding_box)

        super().process_pattern(ptn)

    def _fill_or_stroke(self, svg_elem, raster_style):
        if raster_style.dimension == 2:
            svg_elem.fill('black')
        elif raster_style.dimension == 1:
            svg_elem.stroke('black', width=self._stroke_width)
            svg_elem['style'] = 'fill:none'
        else:
            raise RuntimeError('Only raster styles with dimension 1 or 2 are supported.')

    def _pixel_scale_factor(self, other_unit):
        return self._pixel_scale.m * scale_factor(self._pixel_scale, other_unit)

    def rect(self, ptn: Pattern[Rect]) -> None:
        scale = self._pixel_scale_factor(ptn.dim_shape.unit)

        scaled_rect: Rect = ptn.dim_shape.shape.scaled(scale)

        svg_rect = svgwrite.shapes.Rect(
            insert=scaled_rect.center + (-scaled_rect.width/2, -scaled_rect.height/2),
            size=(scaled_rect.width, scaled_rect.height)
        )

        svg_rect.rotate(np.rad2deg(scaled_rect.theta), center=scaled_rect.center)

        self._fill_or_stroke(svg_rect, ptn.raster_style)

        self._current_layer['elements'].append(svg_rect)

    def polygon(self, ptn: Pattern[Polygon]) -> None:
        scaled_polygon: Polygon = ptn.dim_shape.shape.scaled(self._pixel_scale_factor(ptn.dim_shape.unit))

        svg_poly = svgwrite.shapes.Polygon(scaled_polygon.points)

        self._fill_or_stroke(svg_poly, ptn.raster_style)

        self._current_layer['elements'].append(svg_poly)

    def circle(self, ptn: Pattern[Circle]) -> None:
        scaled_circle: Circle = ptn.dim_shape.shape.scaled(self._pixel_scale_factor(ptn.dim_shape.unit))

        svg_circle = svgwrite.shapes.Circle(center=scaled_circle.center, r=scaled_circle.r)

        self._fill_or_stroke(svg_circle, ptn.raster_style)

        self._current_layer['elements'].append(svg_circle)

    def save(self, filename: PathLike) -> None:

        total_width = self._total_bounding_box.width
        total_height = self._total_bounding_box.height

        total_width_scaled = self._pixel_scale_factor(total_width.u) * total_width.m
        total_height_scaled = self._pixel_scale_factor(total_height.u) * total_height.m

        svg = svgwrite.Drawing(size=(total_width_scaled, total_height_scaled))
        inkscape_svg = svgwrite.extensions.Inkscape(svg)

        for layer in self._layers:
            svg_layer = inkscape_svg.layer(label=layer['id'] or 'Layer')
            svg.add(svg_layer)
            svg_layer.translate(total_width_scaled/2, total_height_scaled/2)
            svg_layer.scale(sx=1, sy=-1)

            for elem in layer['elements']:
                svg_layer.add(elem)

        svg.saveas(filename, pretty=True)
