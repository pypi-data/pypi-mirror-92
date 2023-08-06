# dbnomics-data-model -- Define, validate and transform DBnomics data.
# By: Christophe Benz <christophe.benz@cepremap.org>
#
# Copyright (C) 2017-2021 Cepremap
# https://git.nomics.world/dbnomics/dbnomics-data-model
#
# dbnomics-data-model is free software; you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# dbnomics-data-model is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.


"""Tests for the observations module."""


from datetime import date

import pytest

from dbnomics_data_model.observations import align_series_list


@pytest.fixture
def series_1():
    return ([date(2000, 1, 1), date(2001, 1, 1)], [10, 11])


@pytest.fixture
def series_2():
    return ([date(2000, 1, 1), date(2001, 1, 1)], [100, 110])


@pytest.fixture
def series_3():
    return ([date(2001, 1, 1), date(2002, 1, 1)], [21, 22])


def test_empty_series_list_returns_empty_list():
    assert align_series_list([]) == []


def test_one_series_is_returned_as_is(series_1):
    assert align_series_list([series_1]) == [series_1]


def test_two_series_with_same_periods_succeed(series_1, series_2):
    assert align_series_list([series_1, series_2]) == [series_1, series_2]


def test_two_series_with_different_periods_succeed(series_1, series_3):
    assert align_series_list([series_1, series_3]) == [
        ([date(2000, 1, 1), date(2001, 1, 1), date(2002, 1, 1)], [10, 11, "NA"]),
        ([date(2000, 1, 1), date(2001, 1, 1), date(2002, 1, 1)], ["NA", 21, 22]),
    ]
