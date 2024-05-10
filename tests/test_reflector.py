import pytest
from pyenigma import Reflector
from pyenigma.exceptions import (
    ReflectorInvalidModelException,
    ReflectorWiringWrongLengthException,
    ReflectorWiringDuplicateLettersException,
    ReflectorInvalidLetterException
)


def test_reflector_B():
    reflector = Reflector.get_reflector_B()
    assert reflector.reflect("A") == "Y"
    assert reflector.reflect("B") == "R"
    assert reflector.reflect("C") == "U"
    assert reflector.reflect("D") == "H"
    assert reflector.reflect("E") == "Q"
    assert reflector.reflect("F") == "S"
    assert reflector.reflect("G") == "L"
    assert reflector.reflect("H") == "D"
    assert reflector.reflect("I") == "P"
    assert reflector.reflect("J") == "X"
    assert reflector.reflect("K") == "N"
    assert reflector.reflect("L") == "G"
    assert reflector.reflect("M") == "O"
    assert reflector.reflect("N") == "K"
    assert reflector.reflect("O") == "M"
    assert reflector.reflect("P") == "I"
    assert reflector.reflect("Q") == "E"
    assert reflector.reflect("R") == "B"
    assert reflector.reflect("S") == "F"
    assert reflector.reflect("T") == "Z"
    assert reflector.reflect("U") == "C"
    assert reflector.reflect("V") == "W"
    assert reflector.reflect("W") == "V"
    assert reflector.reflect("X") == "J"
    assert reflector.reflect("Y") == "A"
    assert reflector.reflect("Z") == "T"


def test_reflector_C():
    reflector = Reflector.get_reflector_C()
    assert reflector.reflect("A") == "F"
    assert reflector.reflect("B") == "V"
    assert reflector.reflect("C") == "P"
    assert reflector.reflect("D") == "J"
    assert reflector.reflect("E") == "I"
    assert reflector.reflect("F") == "A"
    assert reflector.reflect("G") == "O"
    assert reflector.reflect("H") == "Y"
    assert reflector.reflect("I") == "E"
    assert reflector.reflect("J") == "D"
    assert reflector.reflect("K") == "R"
    assert reflector.reflect("L") == "Z"
    assert reflector.reflect("M") == "X"
    assert reflector.reflect("N") == "W"
    assert reflector.reflect("O") == "G"
    assert reflector.reflect("P") == "C"
    assert reflector.reflect("Q") == "T"
    assert reflector.reflect("R") == "K"
    assert reflector.reflect("S") == "U"
    assert reflector.reflect("T") == "Q"
    assert reflector.reflect("U") == "S"
    assert reflector.reflect("V") == "B"
    assert reflector.reflect("W") == "N"
    assert reflector.reflect("X") == "M"
    assert reflector.reflect("Y") == "H"
    assert reflector.reflect("Z") == "L"


def test_reflector_wiring_wrong_length_exception():
    with pytest.raises(ReflectorWiringWrongLengthException):
        Reflector("ABC")


def test_reflector_wiring_duplicate_letters_exception():
    with pytest.raises(ReflectorWiringDuplicateLettersException):
        Reflector("AACDEFGHIJKLMNOPQRSTUVWXYZ")


def test_reflector_invalid_letter_exception():
    with pytest.raises(ReflectorInvalidLetterException):
        Reflector("ABCDEF5HIJKLMNOPQRSTUVWXYZ")

    with pytest.raises(ReflectorInvalidLetterException):
        Reflector("ABCDEF HIJKLMNOPQRSTUVWXYZ")

    with pytest.raises(ReflectorInvalidLetterException):
        Reflector("ABCDEFgHIJKLMNOPQRSTUVWXYZ")


def test_get_reflector_B():
    reflector = Reflector.get_reflector_B()
    assert reflector.reflect("A") == "Y"


def test_get_reflector_C():
    reflector = Reflector.get_reflector_C()
    assert reflector.reflect("A") == "F"


def test_get_reflector_by_name():
    reflector = Reflector.get_reflector("B")
    assert reflector.reflect("A") == "Y"

    reflector = Reflector.get_reflector("C")
    assert reflector.reflect("A") == "F"


def test_get_reflector_invalid_model():
    with pytest.raises(ReflectorInvalidModelException):
        Reflector.get_reflector("D")
