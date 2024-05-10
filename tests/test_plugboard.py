import pytest
from pyenigma import Plugboard
from pyenigma.exceptions import PlugboardConnectionExistsException, PlugboardConnectionToItselfException, PlugboardInvalidLetterException, PlugboardStringOddNumberOfLettersException, PlugboardTooManyConnectionsException


def test_plugboard_translates_first_letter():
    plugboard = Plugboard()
    plugboard.add_connection("A", "B")
    assert plugboard.translate("A") == "B"


def test_plugboard_translates_second_letter():
    plugboard = Plugboard()
    plugboard.add_connection("A", "B")
    assert plugboard.translate("B") == "A"


def test_plugboard_translates_unconnected_letter():
    plugboard = Plugboard()
    plugboard.add_connection("A", "B")
    assert plugboard.translate("C") == "C"


def test_plugboard_cannot_make_connection_to_same_letter_twice():
    plugboard = Plugboard()
    plugboard.add_connection("A", "B")
    plugboard.add_connection("Z", "Y")
    with pytest.raises(PlugboardConnectionExistsException):
        plugboard.add_connection("A", "C")

    with pytest.raises(PlugboardConnectionExistsException):
        plugboard.add_connection("X", "Y")


def test_plugboard_cannot_make_connection_to_itself():
    plugboard = Plugboard()
    with pytest.raises(PlugboardConnectionToItselfException):
        plugboard.add_connection("A", "A")


def test_plugboard_cannot_make_connection_to_invalid_letter():
    plugboard = Plugboard()
    with pytest.raises(PlugboardInvalidLetterException):
        plugboard.add_connection("A", "1")

    with pytest.raises(PlugboardInvalidLetterException):
        plugboard.add_connection("1", "A")

    with pytest.raises(PlugboardInvalidLetterException):
        plugboard.add_connection("a", "B")

    with pytest.raises(PlugboardInvalidLetterException):
        plugboard.add_connection("A", "b")


def test_plugboard_too_many_connections():
    plugboard = Plugboard()
    for i in range(10):
        plugboard.add_connection(chr(65 + i), chr(75 + i))

    with pytest.raises(PlugboardTooManyConnectionsException):
        plugboard.add_connection("U", "Z")


def test_plugboard_add_connections_from_map():
    plugboard = Plugboard()
    plugboard.add_connection_from_map({"A": "B", "C": "D"})
    assert plugboard.translate("A") == "B"
    assert plugboard.translate("B") == "A"
    assert plugboard.translate("C") == "D"
    assert plugboard.translate("D") == "C"


def test_plugboard_add_connections_from_string():
    plugboard = Plugboard()
    plugboard.add_connection_from_string("AB CD EF")
    assert plugboard.translate("A") == "B"
    assert plugboard.translate("B") == "A"
    assert plugboard.translate("C") == "D"
    assert plugboard.translate("D") == "C"
    assert plugboard.translate("E") == "F"
    assert plugboard.translate("F") == "E"


def test_plugboard_add_connections_from_string_with_odd_number_of_characters():
    plugboard = Plugboard()
    with pytest.raises(PlugboardStringOddNumberOfLettersException):
        plugboard.add_connection_from_string("ABC")
