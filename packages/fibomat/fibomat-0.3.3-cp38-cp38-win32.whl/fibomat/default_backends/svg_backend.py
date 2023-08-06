from typing import Optional, Dict
import io

import PIL.Image

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
from fibomat.linalg import DimBoundingBox, scale, translate, Vector


class SVGBackend(BackendBase):
    def __init__(self, pixel_scale: Q_ = Q_('0.01 µm'), stroke_width: float = 0.1, description: Optional[str] = None):
        super().__init__()

        self._description = description
        self._pixel_scale = pixel_scale
        self._stroke_width = stroke_width

        # sites are mapped to svg groups
        self._layers = []
        self._current_layer: Optional[Dict] = None
        self._current_layer_center: Optional[Vector] = None

        self._total_bounding_box = None

    def process_site(self, new_site: Site) -> None:
        self._current_layer = {'id': new_site.description or None, 'elements': []}
        self._current_layer_center = new_site.center.vector_as(self._pixel_scale.u)
        self._layers.append(self._current_layer)

        if not self._total_bounding_box:
            self._total_bounding_box = new_site.fov_bounding_box
        else:
            self._total_bounding_box = self._total_bounding_box.extended(new_site.fov_bounding_box)

        super().process_site(new_site)

    # def process_pattern(self, ptn: Pattern) -> None:
    #     super().process_pattern(ptn)

    def _fill_or_stroke(self, svg_elem, raster_style):
        if raster_style.dimension == 2:
            svg_elem.fill('black')
        elif raster_style.dimension == 1:
            svg_elem.stroke('black', width=self._stroke_width)
            svg_elem['style'] = 'fill:none'
        else:
            raise RuntimeError('Only raster styles with dimension 1 or 2 are supported.')

    def _pixel_scale_factor(self, other_unit):
        return scale_factor(self._pixel_scale, other_unit) / self._pixel_scale.m

    def _scale_and_shift_shape(self, ptn: Pattern):
        fak = self._pixel_scale_factor(ptn.dim_shape.unit)

        return ptn.dim_shape.shape.transformed(scale(fak) | translate(self._current_layer_center))

    def rect(self, ptn: Pattern[Rect]) -> None:
        scale = self._pixel_scale_factor(ptn.dim_shape.unit)

        scaled_rect: Rect = self._scale_and_shift_shape(ptn)

        svg_rect = svgwrite.shapes.Rect(
            insert=scaled_rect.center + (-scaled_rect.width/2, -scaled_rect.height/2),
            size=(scaled_rect.width, scaled_rect.height)
        )

        svg_rect.rotate(np.rad2deg(scaled_rect.theta), center=scaled_rect.center)

        self._fill_or_stroke(svg_rect, ptn.raster_style)

        self._current_layer['elements'].append(svg_rect)

    def polygon(self, ptn: Pattern[Polygon]) -> None:
        scaled_polygon: Polygon = self._scale_and_shift_shape(ptn)

        svg_poly = svgwrite.shapes.Polygon(scaled_polygon.points)

        self._fill_or_stroke(svg_poly, ptn.raster_style)

        self._current_layer['elements'].append(svg_poly)

    def circle(self, ptn: Pattern[Circle]) -> None:
        scaled_circle: Circle = self._scale_and_shift_shape(ptn)

        svg_circle = svgwrite.shapes.Circle(center=scaled_circle.center, r=scaled_circle.r)

        self._fill_or_stroke(svg_circle, ptn.raster_style)

        self._current_layer['elements'].append(svg_circle)

    def _to_svg(self) -> svgwrite.Drawing:
        if not self._total_bounding_box:
            raise RuntimeError('Site may not be empty.')

        total_width = self._total_bounding_box.width
        total_height = self._total_bounding_box.height

        total_width_scaled = self._pixel_scale_factor(total_width.u) * total_width.m
        total_height_scaled = self._pixel_scale_factor(total_height.u) * total_height.m

        center = self._total_bounding_box.center

        shift_x = self._pixel_scale_factor(center.x.u) * center.x.m
        shift_y = self._pixel_scale_factor(center.y.u) * center.y.m

        svg = svgwrite.Drawing(size=(total_width_scaled, total_height_scaled))
        inkscape_svg = svgwrite.extensions.Inkscape(svg)

        for layer in self._layers:
            svg_layer = inkscape_svg.layer(label=layer['id'] or 'Layer')
            svg.add(svg_layer)
            svg_layer.translate(total_width_scaled/2 - shift_x, total_height_scaled/2 - shift_y)
            svg_layer.scale(sx=1, sy=-1)

            for elem in layer['elements']:
                svg_layer.add(elem)

        return svg

    def save(self, filename: PathLike) -> None:
        self._to_svg().saveas(filename, pretty=True)

    def to_pillow_image(self, background_color=(255, 255, 255, 255)):
        # https://github.com/manatools/dnfdragora/blob/acaa41e511c3ce026a9123fe494bd017cbfb99db/dnfdragora/updater.py

        try:
            import cairosvg
        except Exception as e:
            raise RuntimeError('Please install cairosvg manually') from e

        rendered_svg = PIL.Image.open(io.BytesIO(cairosvg.svg2png(bytestring=self._to_svg().tostring())))

        image = PIL.Image.new('RGBA', size=rendered_svg.size, color=background_color)
        image.paste(rendered_svg, None, rendered_svg)
        image.convert('RGB')

        return image
