"""
tests/test_tools.py – Tests for individual tools.
"""
import pytest
from app.tools.calculator import calculator
from app.tools.file_reader import file_reader


def test_calculator_basic():
    assert calculator.invoke("1 + 1") == "2"


def test_calculator_power():
    assert calculator.invoke("2 ** 8") == "256"


def test_calculator_division():
    result = calculator.invoke("10 / 4")
    assert result == "2.5"


def test_calculator_invalid():
    result = calculator.invoke("import os")
    assert "Error" in result


def test_file_reader_missing_file():
    result = file_reader.invoke("/nonexistent/path/file.txt")
    assert "Error" in result


def test_file_reader_disallowed_extension():
    result = file_reader.invoke("/some/path/file.exe")
    assert "Error" in result
