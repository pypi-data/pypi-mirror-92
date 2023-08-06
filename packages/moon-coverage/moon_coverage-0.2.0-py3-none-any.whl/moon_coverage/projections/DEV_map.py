"""Map projection module."""

from .axes import ProjAxes
from .equi import Equirectangular
from .equi_gc import Equirectangular as EquirectangularGC


class ProjMap:
    """Projection map for matplotlib.

    Parameters
    ----------
    proj: str
        Projection name (default: `equirectangular`).

    bg: str, pathlib.Path
        Background base map. If no :py:attr:`bg_extent`,
        the projection will assume that the image is
        centered at 180° and cover the entire globe.

    bg_extent: floats (left, right, bottom, top), optional
        Background image extent (default: ``[0, 360, -90, 90]``).

    Raises
    ------
    AttributeError:
        If the provided projection is unknown.

    """

    BG = None
    BG_EXTENT = [0, 360, -90, 90]

    def __init__(self, proj='equirectangular', bg=None, bg_extent=False, **kwargs):
        if proj.lower() in ['eq', 'eqc', 'equi', 'equirectangular', 'platecarree']:
            self.proj = Equirectangular(**kwargs)

        elif proj.lower() in ['eq-gc', 'eq_gc', 'equirectangular-great-circle']:
            self.proj = EquirectangularGC(**kwargs)

        else:
            raise AttributeError(f'Unknown projection: `{proj}`')

        self.bg = bg if bg else self.BG
        self.bg_extent = bg_extent if bg_extent else self.BG_EXTENT

    def _as_mpl_axes(self):
        return ProjAxes, self.attrs

    @property
    def attrs(self):
        """Axes attributes."""
        return {
            'proj': self.proj,
            'bg': self.bg,
            'bg_extent': self.bg_extent,
        }
