"""BadgeGeneration Module."""
import argparse
import svgwrite
from svgwrite.shapes import Line

def points_to_pixels(pts):
    """Approximate the number of pixels if given pts.

    :param float pts: the measure in points to convert
    :returns: number of pixels
    """
    return 4.0 * pts / 3.0

class BadgeGenerator:
    """Badge Generator."""
    def __init__(self, left_width=None, right_width=None, left_text='test',
                 right_text='100%', height=None, radius=5, left_stroke='#000000',
                 left_fill='#000000', left_text_color='#FFFFFF',
                 right_stroke='#000000', right_fill='#FFFFFF',
                 right_text_color='#000000',
                 font_size=16):
        """Initialize the badge generator and write out the outline.
        
        :param float left_width: The width in pts of the left cell of the
            rectangle. If ``None``, then estimates the width of the left text
            and pads.
        :param float right_width: The width in pts of the right cell of the
            rectangle. If ``None``, then estimates the width of the right text
            and pads.
        :param str left_text: Text in the left cell. Default ``'test'``.
        :param str right_text: Text in the right cell. Default ``'100%'``.
        :param float height: The height in pts of both cells. If ``None``, then
            estimates the width of the text and pads.
        :param float radius: The rounded corner radius in pts. Default ``5``.
        :param str left_stroke: The color of the outline of the left cell.
            Default ``'#000000'``.
        :param str left_fill: The color of the fill of the left cell. Default
            ``'#000000'``.
        :param str left_text_color: The color of the left text. Default
            ``'#FFFFFF'``.
        :param str right_stroke: The color of the outline of the right cell.
            Default ``'#000000'``.
        :param str right_fill: The color of the fill of the right cell. Default
            ``'#FFFFFF'``.
        :param str right_text_color: The color of the right text. Default
            ``'#000000'``.
        :param int font_size: The size of the font in pts. Default ``16``.
        """
        self.dwg = svgwrite.Drawing('badge.svg', profile='tiny')
        if left_width is None:
            left_width = len(left_text) * 3/4 * font_size
        if right_width is None:
            right_width = len(right_text) * 3/4 * font_size
        if height is None:
            height = font_size * 1.5
        self.left_rectangle(left_width, height, radius, left_stroke, left_fill)
        self.right_rectangle(right_width, height, radius, left_width,
                             right_stroke, right_fill)
        font_size = 16
        text = self.dwg.add(self.dwg.text("", insert=(left_width/2.0,height/2.0 + points_to_pixels(font_size)/4.0)))
        text.add(self.dwg.tspan(left_text, fill=left_text_color, text_anchor="middle", font_size=font_size))
        text = self.dwg.add(self.dwg.text("", insert=(left_width + right_width/2.0, height/2.0 + points_to_pixels(font_size)/4.0)))
        text.add(self.dwg.tspan(right_text, fill=right_text_color, text_anchor="middle", font_size=font_size))
        
    def __call__(self):
        self.dwg.save()

    def left_rectangle(self, width=75.0, height=25.0, radius=5.0,
                       stroke='#000000', fill='#000000'):
        """"Creates a rectangle with rounded left corners.

        :param float width: width of the rectangle in pts. Default ``75.0``
        :param float height: height of the rectangle in pts. Default ``25.0``
        :param float radius: radius of rounded corners in pts. Default ``5.0``
        :param str stroke: color of the rectangle outline. Default ``#000000``
        :param str fill: color of the rectangle fill. Default ``#FFFFFF``.
        """
        path = svgwrite.path.Path(stroke=stroke, fill=fill)
        path.push(f'M 0.0,{height - radius} C 0.0,{height - radius/2} ' +
                  f'{radius/2.0},{height} {radius},{height}')
        path.push(f'L {radius},{height} {width},{height}')
        path.push(f'L {width},{height} {width},0.0')
        path.push(f'L {width},0 {radius},0')
        path.push(f'C {radius/2.0},0 0,{radius/2.0} 0,{radius}')
        path.push('Z')
        self.dwg.add(path)

    def right_rectangle(self, width=150.0, height=25.0, radius=5.0,
                        corner=75.0, stroke='#000000', fill='#000000'):
        """"Creates a rectangle with rounded right corners.

        :param float width: width of the rectangle in pts. Default ``150.0``
        :param float height: height of the rectangle in pts. Default ``25.0``
        :param float radius: radius of rounded corners in pts. Default ``5.0``
        :param float corner: x-coordinate of the left corner in pts. Default
            ``75.0``
        :param str stroke: color of the rectangle outline. Default ``#000000``
        :param str fill: color of the rectangle fill. Default ``#FFFFFF``.
        """
        path = svgwrite.path.Path(stroke=stroke, fill=fill)
        path.push(f'M {corner + width - radius},{height} ' +
                  f'C {corner + width - radius/2.0},{height} ' +
                  f'{corner + width},{height - radius/2.0} ' +
                  f'{corner + width},{height - radius}')
        path.push(f'L {corner + width},{height - radius} ' +
                  f'{corner + width},{radius}')
        path.push(f'C {corner + width},{radius/2.0} ' +
                  f'{corner + width - radius/2.0},0 ' +
                  f'{corner + width - radius},0')
        path.push(f'L {corner + width - radius},0 {corner},0')
        path.push(f'L {corner},0 {corner},{height}')
        path.push('Z')
        self.dwg.add(path)

def _get_argparser():
    parser = argparse.ArgumentParser()
    parser.add_argument('--left-width', default=None, nargs='?',
                        help='Width of the left cell, ``None`` if fit to text')
    parser.add_argument('--right-width', default=None, nargs='?',
                        help='Width of the left cell, ``None`` if fit to text')
    parser.add_argument('--left-text', default='test', nargs='?',
                        help='Text for the left cell. Can be python format ' +
                        'string')
    parser.add_argument('--left-stroke', default='#000000', nargs='?',
                        help='Outline color for left cell.')
    parser.add_argument('--left-fill', default='#000000', nargs='?',
                        help='Fill color for left cell.')
    parser.add_argument('--left-text-color', default='#FFFFFF', nargs='?',
                        help='Text color for left cell.')
    parser.add_argument('--right-text', default='100%', nargs='?',
                        help='Text for the right cell.  Can be python format ' +
                        'string')
    parser.add_argument('--right-stroke', default='#000000', nargs='?',
                        help='Outline color for right cell.')
    parser.add_argument('--right-fill', default='#FFFFFF', nargs='?',
                        help='Fill color for right cell.')
    parser.add_argument('--right-text-color', default='#000000', nargs='?',
                        help='Text color for right cell.')
    return parser

def _run_cli():
    args = _get_argparser().parse_args()
    badge_generator = BadgeGenerator(**vars(args))
    badge_generator()

if __name__ == "__main__":
    _run_cli()
