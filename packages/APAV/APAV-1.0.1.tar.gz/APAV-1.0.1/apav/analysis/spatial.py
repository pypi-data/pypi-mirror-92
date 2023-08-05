"""
This file is part of APAV.

APAV is a python package for performing analysis and visualization on
atom probe tomography data sets.

Copyright (C) 2018 Jesse Smith

APAV is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 2 of the License, or
(at your option) any later version.

APAV is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with APAV.  If not, see <http://www.gnu.org/licenses/>.
"""

from apav.analysis.base import AnalysisBase
from apav.utils import validate
from apav import Roi
from apav.core.histogram import histogram2d_binwidth
from apav.core.multipleevent import get_mass_indices


class DensityHistogram(AnalysisBase):
    """
    Compute density histograms on an Roi
    """
    def __init__(self,
                 roi: Roi,
                 bin_width=0.3,
                 axis="z",
                 multiplicity="all"):
        """
        :param roi: region of interest
        :param bin_width: width of the bin size in Daltons
        :param axis: which axis the histogram should be computed on ("x", "y", or "z")
        :param multiplicity: the multiplicity order to compute histogram with
        """
        super().__init__(roi)
        self.bin_width = validate.positive_nonzero_number(bin_width)
        self._multiplicity = validate.multiplicity_any(multiplicity)
        if multiplicity != "all":
            roi.require_multihit_info()

        self._histogram = None
        self._histogram_extents = None
        self._axis = validate.choice(axis, ("x", "y", "z"))
        self._bin_vol = None
        self._calculate_histogram()

    @property
    def multiplicity(self):
        return self._multiplicity

    @property
    def bin_vol(self):
        return self._bin_vol

    @property
    def axis(self):
        return self._axis

    @property
    def histogram(self):
        return self._histogram

    @property
    def histogram_extents(self):
        return self._histogram_extents

    def _calculate_histogram(self):
        orient_map = {"x": 0, "y": 1, "z": 2}
        ax1, ax2 = (self.roi.xyz[:, val] for key, val in orient_map.items() if key != self.axis)
        ext_ax1, ext_ax2 = (self.roi.xyz_extents[val] for key, val in orient_map.items() if key != self.axis)
        ext = (ext_ax1, ext_ax2)

        if self.multiplicity == "all":
            self._histogram = histogram2d_binwidth(ax1, ax2, ext, self.bin_width)
        else:
            idx = get_mass_indices(self.roi.misc["ipp"], self.multiplicity)
            self._histogram = histogram2d_binwidth(ax1[idx], ax2[idx], ext, self.bin_width)

        self._histogram_extents = ext
