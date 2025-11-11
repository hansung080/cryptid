from __future__ import annotations

from unittest import mock
from unittest.mock import MagicMock

import mod1
import mod2


def test_summer() -> None:
    assert mod2.summer(5, 6) == "The sum is 11"


def test_summer_mock1() -> None:
    with mock.patch("mod1.preamble", return_value=""):
        assert mod2.summer(5, 6) == "11"


def test_summer_mock2() -> None:
    with mock.patch("mod1.preamble") as mock_preamble:
        mock_preamble.return_value = ""
        assert mod2.summer(5, 6) == "11"


@mock.patch("mod1.preamble", return_value="")
def test_summer_mock3(mock_preamble: MagicMock) -> None:
    assert mod2.summer(5, 6) == "11"


@mock.patch("mod1.preamble")
def test_summer_mock4(mock_preamble: MagicMock) -> None:
    mock_preamble.return_value = ""
    assert mod2.summer(5, 6) == "11"
