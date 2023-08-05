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

from apav import Roi, RangeCollection
from apav.utils.helpers import data_path
from apav.utils import validate

import numpy as n
from pytest import raises


def test_args():
    with raises(TypeError):
        Roi((1, 0, 0), n.array([1]))
    with raises(TypeError):
        Roi(n.array([[1, 0, 0]]), [1])
    with raises(ValueError):
        Roi(n.array([[1, 0, 0], [0, 2, 0]]), n.array([1]))
    with raises(ValueError):
        Roi(n.array([[1, 0, 0], [0, 2, 0]]), n.array([[1, 2]]))
    with raises(ValueError):
        Roi(n.array([[[1, 0, 0], [0, 2, 0]]]), n.array([[1, 2]]))


class TestRoi:
    @classmethod
    def setup_class(cls):
        cls.xyz = n.array([[0,   0,  0],
                           [1,   1,  1],
                           [-1,  1,  1],
                           [1,  -1,  1],
                           [1,   1, -1],
                           [-1, -1,  1],
                           [-1,  1, -1],
                           [1,  -1, -1],
                           [-1, -1, -1]])

        cls.mass = n.array([1, 2, 2, 3, 3, 3, 5, 5, 4])
        cls.ipp = n.array([1, 2, 0, 4, 0, 0, 0, 2, 0])
        cls.det_x = n.array([1, 2, 3, 4, 5, 6, 7, 8, 9])
        cls.det_y = n.array([10, 20, 30, 40, 50, 60, 70, 80, 90])
        cls.tof = n.array([1.5, 1.5, 2.5, 5.5, 2.5, 3.5, 3.5, 3.5, 3.5])
        cls.aptrun = Roi(cls.xyz,
                         cls.mass,
                         misc={"ipp": cls.ipp, "det_x": cls.det_x, "det_y": cls.det_y, "tof": cls.tof})

    def test_xyz(self):
        assert n.allclose(self.aptrun.xyz, self.xyz)

    def test_mass(self):
        assert n.allclose(self.aptrun.mass, self.mass)

    def test_misc(self):
        assert n.allclose(self.aptrun.misc["ipp"], self.ipp)
        assert n.allclose(self.aptrun.misc["det_x"], self.det_x)
        assert n.allclose(self.aptrun.misc["det_y"], self.det_y)

    def test_nhits(self):
        assert self.aptrun.counts == 9

    def test_dimensions(self):
        assert n.allclose(self.aptrun.dimensions, (2, 2, 2))

    def test_mass_extents(self):
        assert n.allclose(self.aptrun.mass_extents, (1, 5))

    def test_xyz_extents(self):
        assert n.allclose(self.aptrun.xyz_extents, ((-1, 1), (-1, 1), (-1, 1)))

    def test_detector_extents(self):
        assert n.allclose(self.aptrun.detector_extents, ((1, 9), (10, 90)))

    def test_multiplicity_info(self):
        assert self.aptrun.has_multiplicity_info()

    def test_tof_info(self):
        assert self.aptrun.has_tof_info()

    def test_multiplicities(self):
        # Run twice since the multiplicities only get calculated the first property call
        assert n.allclose(self.aptrun.multiplicities, [1, 2, 4])
        assert n.allclose(self.aptrun.multiplicities, [1, 2, 4])

    def test_xyz_center(self, singles_roi):
        cen = singles_roi.xyz_center
        assert n.isclose(cen[0], 4.42857)
        assert n.isclose(cen[1], 3.285714)
        assert n.isclose(cen[2], 2.57142)

    def test_from_pos(self):
        fpos = data_path("Si.pos")
        posrun = Roi.from_pos(fpos)
        assert not posrun.has_multiplicity_info()
        assert not posrun.has_detailed_info()
        assert not posrun.has_tof_info()

        with raises(validate.NoMultiEventError):
            posrun.multiplicity_counts()
        with raises(validate.NoMultiEventError):
            posrun.multiplicity_fraction()
        with raises(validate.NoMultiEventError):
            posrun.multiplicity_percentage()

        with raises(validate.NoDetectorInfoError):
            posrun.detector_extents()

        with raises(validate.NoTOFError):
            posrun.tof_histogram()

    def test_from_epos(self):
        fepos = data_path("Si.epos")
        eposrun = Roi.from_epos(fepos)
        assert eposrun.has_multiplicity_info()
        assert eposrun.has_detailed_info()
        assert eposrun.has_tof_info()

        eposrun.multiplicity_counts()
        eposrun.multiplicity_percentage()
        eposrun.multiplicity_fraction()

    def test_multiplicity_counts(self):
        assert n.allclose(self.aptrun.multiplicity_counts(),
                          (n.array([1, 2, 4]), n.array([1, 4, 4])))

    def test_multiplicity_fraction(self):
        assert n.allclose(self.aptrun.multiplicity_fraction(),
                          (n.array([1, 2, 4]), n.array([1/9, 4/9, 4/9])))

    def test_multiplicity_percentage(self):
        assert n.allclose(self.aptrun.multiplicity_percentage(),
                          (n.array([1, 2, 4]), n.array([1/9*100, 4/9*100, 4/9*100])))

    def test_tof_histogram(self):
        hist = self.aptrun.tof_histogram(1, "all", norm=False, cutoff=5)
        assert n.allclose(hist[1], n.array([0, 2, 2, 4, 0]))

        hist = self.aptrun.tof_histogram(1, "multiples", norm=False, cutoff=5)
        assert n.allclose(hist[1], n.array([0, 1, 2, 4, 0]))

        hist = self.aptrun.tof_histogram(1, 2, norm=False, cutoff=5)
        assert n.allclose(hist[1], n.array([0, 1, 1, 2, 0]))

        hist = self.aptrun.tof_histogram(1, 2, norm=True, cutoff=5)
        assert n.allclose(hist[1], n.array([0, 1/2, 1/2, 1, 0]))

    def test_mass_histogram(self):
        hist = self.aptrun.mass_histogram(1, 0, 5, multiplicity="all", norm=False)
        assert n.allclose(hist[1], n.array([0, 1, 2, 3, 1]))

        hist = self.aptrun.mass_histogram(1, 0, 5, multiplicity="multiples", norm=False)
        assert n.allclose(hist[1], n.array([0, 0, 2, 3, 1]))

        hist = self.aptrun.mass_histogram(1, 0, 5, multiplicity=2, norm=False)
        assert n.allclose(hist[1], n.array([0, 0, 2, 0, 1]))

        hist = self.aptrun.mass_histogram(1, 0, 5, multiplicity="all", norm=True)
        assert n.allclose(hist[1], n.array([0, 1/3, 2/3, 3/3, 1/3]))

    def test_plotting(self, qtbot):
        # very basic plot testing
        plot = self.aptrun.plot_mass_spectrum()
        plot.show()
        qtbot.addWidget(plot)

        # bin
        plot.bin_width.setValue(0)
        plot.bin_width.editingFinished.emit()
        assert plot.bin_width.value() != 0

        # min
        plot.lower.setValue(2.5)
        plot.lower.editingFinished.emit()
        assert plot.data[1].sum() == 6

        # max
        plot.upper.setValue(3.5)
        plot.upper.editingFinished.emit()
        assert plot.data[1].sum() == 3

        # norm
        plot.lower.setValue(0)
        plot.upper.setValue(200)
        plot.upper.editingFinished.emit()
        assert plot.data[1].max() == 3
