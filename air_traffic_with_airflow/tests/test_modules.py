import datetime
import pytest
from packages import modules


def test_unix_time_to_datetime_int():
    result = modules.unix_time_to_datetime(1661245198)
    assert result == datetime.datetime(2022, 8, 23, 10, 59, 58)


def test_unix_time_to_datetime_str():
    result = modules.unix_time_to_datetime('1661245198')
    assert result == datetime.datetime(2022, 8, 23, 10, 59, 58)


def test_unix_time_to_datetime_empty():
    assert modules.unix_time_to_datetime('') is None


def test_unix_time_to_datetime_none():
    assert modules.unix_time_to_datetime(None) is None


def test_string_to_boolean_false_string():
    assert modules.string_to_boolean('False') is False


def test_string_to_boolean_true_string():
    assert modules.string_to_boolean('True') is True


def test_string_to_boolean_none_string():
    assert modules.string_to_boolean('None') is None


def test_string_to_boolean_other_string():
    assert modules.string_to_boolean('iubfr876!') is None


def test_string_to_boolean_empty():
    assert modules.string_to_boolean("") is None


def test_string_to_boolean_int():
    assert modules.string_to_boolean(5) is None


def test_string_to_boolean_true():
    assert modules.string_to_boolean(True) is True


def test_string_to_boolean_false():
    assert modules.string_to_boolean(False) is False
