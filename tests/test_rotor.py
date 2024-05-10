import pytest
from pyenigma import Rotor
from pyenigma.exceptions import (
    RotorWiringWrongLengthException,
    RotorWiringDuplicateLettersException,
    RotorInvalidLetterException,
    RotorInvalidModelException
)

#### Test sub functions ####


def test_shift_alphabet():
    assert Rotor._shift_alphabet("A") == "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    assert Rotor._shift_alphabet("B") == "BCDEFGHIJKLMNOPQRSTUVWXYZA"
    assert Rotor._shift_alphabet("C") == "CDEFGHIJKLMNOPQRSTUVWXYZAB"
    assert Rotor._shift_alphabet("D") == "DEFGHIJKLMNOPQRSTUVWXYZABC"
    assert Rotor._shift_alphabet("E") == "EFGHIJKLMNOPQRSTUVWXYZABCD"
    assert Rotor._shift_alphabet("F") == "FGHIJKLMNOPQRSTUVWXYZABCDE"
    assert Rotor._shift_alphabet("G") == "GHIJKLMNOPQRSTUVWXYZABCDEF"
    assert Rotor._shift_alphabet("H") == "HIJKLMNOPQRSTUVWXYZABCDEFG"
    assert Rotor._shift_alphabet("I") == "IJKLMNOPQRSTUVWXYZABCDEFGH"
    assert Rotor._shift_alphabet("J") == "JKLMNOPQRSTUVWXYZABCDEFGHI"
    assert Rotor._shift_alphabet("K") == "KLMNOPQRSTUVWXYZABCDEFGHIJ"
    assert Rotor._shift_alphabet("L") == "LMNOPQRSTUVWXYZABCDEFGHIJK"
    assert Rotor._shift_alphabet("M") == "MNOPQRSTUVWXYZABCDEFGHIJKL"
    assert Rotor._shift_alphabet("N") == "NOPQRSTUVWXYZABCDEFGHIJKLM"
    assert Rotor._shift_alphabet("O") == "OPQRSTUVWXYZABCDEFGHIJKLMN"
    assert Rotor._shift_alphabet("P") == "PQRSTUVWXYZABCDEFGHIJKLMNO"
    assert Rotor._shift_alphabet("Q") == "QRSTUVWXYZABCDEFGHIJKLMNOP"
    assert Rotor._shift_alphabet("R") == "RSTUVWXYZABCDEFGHIJKLMNOPQ"
    assert Rotor._shift_alphabet("S") == "STUVWXYZABCDEFGHIJKLMNOPQR"
    assert Rotor._shift_alphabet("T") == "TUVWXYZABCDEFGHIJKLMNOPQRS"
    assert Rotor._shift_alphabet("U") == "UVWXYZABCDEFGHIJKLMNOPQRST"
    assert Rotor._shift_alphabet("V") == "VWXYZABCDEFGHIJKLMNOPQRSTU"
    assert Rotor._shift_alphabet("W") == "WXYZABCDEFGHIJKLMNOPQRSTUV"
    assert Rotor._shift_alphabet("X") == "XYZABCDEFGHIJKLMNOPQRSTUVW"
    assert Rotor._shift_alphabet("Y") == "YZABCDEFGHIJKLMNOPQRSTUVWX"
    assert Rotor._shift_alphabet("Z") == "ZABCDEFGHIJKLMNOPQRSTUVWXY"


def test_get_ring_setting_offset():
    rotor1 = Rotor.get_rotor_I("A", "A")
    assert rotor1._get_ring_setting_offset("A") == "A"

    rotor2 = Rotor.get_rotor_I("B", "A")
    assert rotor2._get_ring_setting_offset("A") == "Z"

    rotor3 = Rotor.get_rotor_I("C", "A")
    assert rotor3._get_ring_setting_offset("A") == "Y"

    rotor4 = Rotor.get_rotor_I("A", "B")
    assert rotor4._get_ring_setting_offset("A") == "B"


def test_get_ring_setting_offset_reversed():
    rotor1 = Rotor.get_rotor_I("A", "A")
    assert rotor1._get_ring_setting_offset_reversed("A") == "A"

    rotor2 = Rotor.get_rotor_I("B", "A")
    assert rotor2._get_ring_setting_offset_reversed("A") == "B"

    rotor3 = Rotor.get_rotor_I("C", "A")
    assert rotor3._get_ring_setting_offset_reversed("A") == "C"

    rotor4 = Rotor.get_rotor_I("A", "B")
    assert rotor4._get_ring_setting_offset_reversed("A") == "Z"

#### Test rotor forward pass functions ####


def test_pass_forward_rotor_I_A_A():
    rotor = Rotor.get_rotor_I("A", "A")
    assert rotor.pass_forward("A") == "E"
    assert rotor.pass_forward("B") == "K"
    assert rotor.pass_forward("C") == "M"
    assert rotor.pass_forward("D") == "F"
    assert rotor.pass_forward("E") == "L"
    assert rotor.pass_forward("F") == "G"
    assert rotor.pass_forward("G") == "D"
    assert rotor.pass_forward("H") == "Q"
    assert rotor.pass_forward("I") == "V"
    assert rotor.pass_forward("J") == "Z"
    assert rotor.pass_forward("K") == "N"
    assert rotor.pass_forward("L") == "T"
    assert rotor.pass_forward("M") == "O"
    assert rotor.pass_forward("N") == "W"
    assert rotor.pass_forward("O") == "Y"
    assert rotor.pass_forward("P") == "H"
    assert rotor.pass_forward("Q") == "X"
    assert rotor.pass_forward("R") == "U"
    assert rotor.pass_forward("S") == "S"
    assert rotor.pass_forward("T") == "P"
    assert rotor.pass_forward("U") == "A"
    assert rotor.pass_forward("V") == "I"
    assert rotor.pass_forward("W") == "B"
    assert rotor.pass_forward("X") == "R"
    assert rotor.pass_forward("Y") == "C"
    assert rotor.pass_forward("Z") == "J"


def test_pass_forward_rotor_I_A_B():
    # Known permutation of Rotor I from https://www.ciphermachinesandcryptology.com/en/enigmatech.htm#rotorencryption
    rotor = Rotor.get_rotor_I("A", "B")
    assert rotor.pass_forward("A") == "J"


def test_pass_forward_rotor_I_B_A():
    # Known permutation of Rotor I from https://www.ciphermachinesandcryptology.com/en/enigmatech.htm#rotorencryption
    rotor = Rotor.get_rotor_I("B", "A")
    assert rotor.pass_forward("A") == "K"


def test_pass_forward_rotor_I_F_Y():
    # Known permutation of Rotor I from https://www.ciphermachinesandcryptology.com/en/enigmatech.htm#rotorencryption
    rotor = Rotor.get_rotor_I("F", "Y")
    assert rotor.pass_forward("A") == "W"


def test_pass_forward_rotor_II_A_A():
    rotor = Rotor.get_rotor_II("A", "A")
    assert rotor.pass_forward("A") == "A"
    assert rotor.pass_forward("B") == "J"
    assert rotor.pass_forward("C") == "D"
    assert rotor.pass_forward("D") == "K"
    assert rotor.pass_forward("E") == "S"
    assert rotor.pass_forward("F") == "I"
    assert rotor.pass_forward("G") == "R"
    assert rotor.pass_forward("H") == "U"
    assert rotor.pass_forward("I") == "X"
    assert rotor.pass_forward("J") == "B"
    assert rotor.pass_forward("K") == "L"
    assert rotor.pass_forward("L") == "H"
    assert rotor.pass_forward("M") == "W"
    assert rotor.pass_forward("N") == "T"
    assert rotor.pass_forward("O") == "M"
    assert rotor.pass_forward("P") == "C"
    assert rotor.pass_forward("Q") == "Q"
    assert rotor.pass_forward("R") == "G"
    assert rotor.pass_forward("S") == "Z"
    assert rotor.pass_forward("T") == "N"
    assert rotor.pass_forward("U") == "P"
    assert rotor.pass_forward("V") == "Y"
    assert rotor.pass_forward("W") == "F"
    assert rotor.pass_forward("X") == "V"
    assert rotor.pass_forward("Y") == "O"
    assert rotor.pass_forward("Z") == "E"


def test_pass_forward_rotor_III_A_A():
    rotor = Rotor.get_rotor_III("A", "A")
    assert rotor.pass_forward("A") == "B"
    assert rotor.pass_forward("B") == "D"
    assert rotor.pass_forward("C") == "F"
    assert rotor.pass_forward("D") == "H"
    assert rotor.pass_forward("E") == "J"
    assert rotor.pass_forward("F") == "L"
    assert rotor.pass_forward("G") == "C"
    assert rotor.pass_forward("H") == "P"
    assert rotor.pass_forward("I") == "R"
    assert rotor.pass_forward("J") == "T"
    assert rotor.pass_forward("K") == "X"
    assert rotor.pass_forward("L") == "V"
    assert rotor.pass_forward("M") == "Z"
    assert rotor.pass_forward("N") == "N"
    assert rotor.pass_forward("O") == "Y"
    assert rotor.pass_forward("P") == "E"
    assert rotor.pass_forward("Q") == "I"
    assert rotor.pass_forward("R") == "W"
    assert rotor.pass_forward("S") == "G"
    assert rotor.pass_forward("T") == "A"
    assert rotor.pass_forward("U") == "K"
    assert rotor.pass_forward("V") == "M"
    assert rotor.pass_forward("W") == "U"
    assert rotor.pass_forward("X") == "S"
    assert rotor.pass_forward("Y") == "Q"
    assert rotor.pass_forward("Z") == "O"


def test_pass_forward_rotor_IV_A_A():
    rotor = Rotor.get_rotor_IV("A", "A")
    assert rotor.pass_forward("A") == "E"
    assert rotor.pass_forward("B") == "S"
    assert rotor.pass_forward("C") == "O"
    assert rotor.pass_forward("D") == "V"
    assert rotor.pass_forward("E") == "P"
    assert rotor.pass_forward("F") == "Z"
    assert rotor.pass_forward("G") == "J"
    assert rotor.pass_forward("H") == "A"
    assert rotor.pass_forward("I") == "Y"
    assert rotor.pass_forward("J") == "Q"
    assert rotor.pass_forward("K") == "U"
    assert rotor.pass_forward("L") == "I"
    assert rotor.pass_forward("M") == "R"
    assert rotor.pass_forward("N") == "H"
    assert rotor.pass_forward("O") == "X"
    assert rotor.pass_forward("P") == "L"
    assert rotor.pass_forward("Q") == "N"
    assert rotor.pass_forward("R") == "F"
    assert rotor.pass_forward("S") == "T"
    assert rotor.pass_forward("T") == "G"
    assert rotor.pass_forward("U") == "K"
    assert rotor.pass_forward("V") == "D"
    assert rotor.pass_forward("W") == "C"
    assert rotor.pass_forward("X") == "M"
    assert rotor.pass_forward("Y") == "W"
    assert rotor.pass_forward("Z") == "B"


def test_pass_forward_rotor_V_A_A():
    rotor = Rotor.get_rotor_V("A", "A")
    assert rotor.pass_forward("A") == "V"
    assert rotor.pass_forward("B") == "Z"
    assert rotor.pass_forward("C") == "B"
    assert rotor.pass_forward("D") == "R"
    assert rotor.pass_forward("E") == "G"
    assert rotor.pass_forward("F") == "I"
    assert rotor.pass_forward("G") == "T"
    assert rotor.pass_forward("H") == "Y"
    assert rotor.pass_forward("I") == "U"
    assert rotor.pass_forward("J") == "P"
    assert rotor.pass_forward("K") == "S"
    assert rotor.pass_forward("L") == "D"
    assert rotor.pass_forward("M") == "N"
    assert rotor.pass_forward("N") == "H"
    assert rotor.pass_forward("O") == "L"
    assert rotor.pass_forward("P") == "X"
    assert rotor.pass_forward("Q") == "A"
    assert rotor.pass_forward("R") == "W"
    assert rotor.pass_forward("S") == "M"
    assert rotor.pass_forward("T") == "J"
    assert rotor.pass_forward("U") == "Q"
    assert rotor.pass_forward("V") == "O"
    assert rotor.pass_forward("W") == "F"
    assert rotor.pass_forward("X") == "E"
    assert rotor.pass_forward("Y") == "C"
    assert rotor.pass_forward("Z") == "K"

#### Test rotor backward pass functions ####


def test_pass_backward_rotor_I_A_A():
    rotor = Rotor.get_rotor_I("A", "A")
    assert rotor.pass_backward("A") == "U"
    assert rotor.pass_backward("B") == "W"
    assert rotor.pass_backward("C") == "Y"
    assert rotor.pass_backward("D") == "G"
    assert rotor.pass_backward("E") == "A"
    assert rotor.pass_backward("F") == "D"
    assert rotor.pass_backward("G") == "F"
    assert rotor.pass_backward("H") == "P"
    assert rotor.pass_backward("I") == "V"
    assert rotor.pass_backward("J") == "Z"
    assert rotor.pass_backward("K") == "B"
    assert rotor.pass_backward("L") == "E"
    assert rotor.pass_backward("M") == "C"
    assert rotor.pass_backward("N") == "K"
    assert rotor.pass_backward("O") == "M"
    assert rotor.pass_backward("P") == "T"
    assert rotor.pass_backward("Q") == "H"
    assert rotor.pass_backward("R") == "X"
    assert rotor.pass_backward("S") == "S"
    assert rotor.pass_backward("T") == "L"
    assert rotor.pass_backward("U") == "R"
    assert rotor.pass_backward("V") == "I"
    assert rotor.pass_backward("W") == "N"
    assert rotor.pass_backward("X") == "Q"
    assert rotor.pass_backward("Y") == "O"
    assert rotor.pass_backward("Z") == "J"


def test_pass_backward_rotor_I_A_B():
    # Known permutation of Rotor I from https://www.ciphermachinesandcryptology.com/en/enigmatech.htm#rotorencryption
    rotor = Rotor.get_rotor_I("A", "B")
    assert rotor.pass_backward("J") == "A"


def test_pass_backward_rotor_I_B_A():
    # Known permutation of Rotor I from https://www.ciphermachinesandcryptology.com/en/enigmatech.htm#rotorencryption
    rotor = Rotor.get_rotor_I("B", "A")
    assert rotor.pass_backward("K") == "A"


def test_pass_backward_rotor_I_F_Y():
    # Known permutation of Rotor I from https://www.ciphermachinesandcryptology.com/en/enigmatech.htm#rotorencryption
    rotor = Rotor.get_rotor_I("F", "Y")
    assert rotor.pass_backward("W") == "A"


def test_pass_backward_rotor_II_A_A():
    rotor = Rotor.get_rotor_II("A", "A")
    assert rotor.pass_backward("A") == "A"
    assert rotor.pass_backward("B") == "J"
    assert rotor.pass_backward("C") == "P"
    assert rotor.pass_backward("D") == "C"
    assert rotor.pass_backward("E") == "Z"
    assert rotor.pass_backward("F") == "W"
    assert rotor.pass_backward("G") == "R"
    assert rotor.pass_backward("H") == "L"
    assert rotor.pass_backward("I") == "F"
    assert rotor.pass_backward("J") == "B"
    assert rotor.pass_backward("K") == "D"
    assert rotor.pass_backward("L") == "K"
    assert rotor.pass_backward("M") == "O"
    assert rotor.pass_backward("N") == "T"
    assert rotor.pass_backward("O") == "Y"
    assert rotor.pass_backward("P") == "U"
    assert rotor.pass_backward("Q") == "Q"
    assert rotor.pass_backward("R") == "G"
    assert rotor.pass_backward("S") == "E"
    assert rotor.pass_backward("T") == "N"
    assert rotor.pass_backward("U") == "H"
    assert rotor.pass_backward("V") == "X"
    assert rotor.pass_backward("W") == "M"
    assert rotor.pass_backward("X") == "I"
    assert rotor.pass_backward("Y") == "V"
    assert rotor.pass_backward("Z") == "S"


def test_pass_backward_rotor_III_A_A():
    rotor = Rotor.get_rotor_III("A", "A")
    assert rotor.pass_backward("A") == "T"
    assert rotor.pass_backward("B") == "A"
    assert rotor.pass_backward("C") == "G"
    assert rotor.pass_backward("D") == "B"
    assert rotor.pass_backward("E") == "P"
    assert rotor.pass_backward("F") == "C"
    assert rotor.pass_backward("G") == "S"
    assert rotor.pass_backward("H") == "D"
    assert rotor.pass_backward("I") == "Q"
    assert rotor.pass_backward("J") == "E"
    assert rotor.pass_backward("K") == "U"
    assert rotor.pass_backward("L") == "F"
    assert rotor.pass_backward("M") == "V"
    assert rotor.pass_backward("N") == "N"
    assert rotor.pass_backward("O") == "Z"
    assert rotor.pass_backward("P") == "H"
    assert rotor.pass_backward("Q") == "Y"
    assert rotor.pass_backward("R") == "I"
    assert rotor.pass_backward("S") == "X"
    assert rotor.pass_backward("T") == "J"
    assert rotor.pass_backward("U") == "W"
    assert rotor.pass_backward("V") == "L"
    assert rotor.pass_backward("W") == "R"
    assert rotor.pass_backward("X") == "K"
    assert rotor.pass_backward("Y") == "O"
    assert rotor.pass_backward("Z") == "M"


def test_pass_backward_rotor_IV_A_A():
    rotor = Rotor.get_rotor_IV("A", "A")
    assert rotor.pass_backward("A") == "H"
    assert rotor.pass_backward("B") == "Z"
    assert rotor.pass_backward("C") == "W"
    assert rotor.pass_backward("D") == "V"
    assert rotor.pass_backward("E") == "A"
    assert rotor.pass_backward("F") == "R"
    assert rotor.pass_backward("G") == "T"
    assert rotor.pass_backward("H") == "N"
    assert rotor.pass_backward("I") == "L"
    assert rotor.pass_backward("J") == "G"
    assert rotor.pass_backward("K") == "U"
    assert rotor.pass_backward("L") == "P"
    assert rotor.pass_backward("M") == "X"
    assert rotor.pass_backward("N") == "Q"
    assert rotor.pass_backward("O") == "C"
    assert rotor.pass_backward("P") == "E"
    assert rotor.pass_backward("Q") == "J"
    assert rotor.pass_backward("R") == "M"
    assert rotor.pass_backward("S") == "B"
    assert rotor.pass_backward("T") == "S"
    assert rotor.pass_backward("U") == "K"
    assert rotor.pass_backward("V") == "D"
    assert rotor.pass_backward("W") == "Y"
    assert rotor.pass_backward("X") == "O"
    assert rotor.pass_backward("Y") == "I"
    assert rotor.pass_backward("Z") == "F"


def test_pass_backward_rotor_V_A_A():
    rotor = Rotor.get_rotor_V("A", "A")
    assert rotor.pass_backward("A") == "Q"
    assert rotor.pass_backward("B") == "C"
    assert rotor.pass_backward("C") == "Y"
    assert rotor.pass_backward("D") == "L"
    assert rotor.pass_backward("E") == "X"
    assert rotor.pass_backward("F") == "W"
    assert rotor.pass_backward("G") == "E"
    assert rotor.pass_backward("H") == "N"
    assert rotor.pass_backward("I") == "F"
    assert rotor.pass_backward("J") == "T"
    assert rotor.pass_backward("K") == "Z"
    assert rotor.pass_backward("L") == "O"
    assert rotor.pass_backward("M") == "S"
    assert rotor.pass_backward("N") == "M"
    assert rotor.pass_backward("O") == "V"
    assert rotor.pass_backward("P") == "J"
    assert rotor.pass_backward("Q") == "U"
    assert rotor.pass_backward("R") == "D"
    assert rotor.pass_backward("S") == "K"
    assert rotor.pass_backward("T") == "G"
    assert rotor.pass_backward("U") == "I"
    assert rotor.pass_backward("V") == "A"
    assert rotor.pass_backward("W") == "R"
    assert rotor.pass_backward("X") == "P"
    assert rotor.pass_backward("Y") == "H"
    assert rotor.pass_backward("Z") == "B"


### Test rotate ###


def test_rotate_rotor_I_A_A():
    rotor = Rotor.get_rotor_I("A", "A")
    assert rotor.rotor_position == "A"
    assert rotor.pass_forward("A") == "E"
    rotor.rotate()
    assert rotor.rotor_position == "B"
    assert rotor.pass_forward("A") == "J"


def test_rotate_rotor_I_A_B():
    rotor = Rotor.get_rotor_I("A", "B")
    assert rotor.rotor_position == "B"
    assert rotor.pass_forward("A") == "J"
    rotor.rotate()
    assert rotor.rotor_position == "C"
    assert rotor.pass_forward("A") == "K"

## Test rotor reset ##


def test_reset_rotor_I_A_A():
    rotor = Rotor.get_rotor_I("A", "A")
    assert rotor.rotor_position == "A"
    rotor.rotate()
    assert rotor.rotor_position == "B"
    rotor.reset()
    assert rotor.rotor_position == "A"

## Test rotor creation ##


def test_get_rotor_I_A_A():
    rotor = Rotor.get_rotor_I("A", "A")
    assert rotor._rotor_model == "I"
    assert rotor.rotor_position == "A"
    assert rotor._ring_setting == "A"
    assert rotor._wiring == "EKMFLGDQVZNTOWYHXUSPAIBRCJ"


def test_get_rotor_II_A_A():
    rotor = Rotor.get_rotor_II("A", "A")
    assert rotor._rotor_model == "II"
    assert rotor.rotor_position == "A"
    assert rotor._ring_setting == "A"
    assert rotor._wiring == "AJDKSIRUXBLHWTMCQGZNPYFVOE"


def test_get_rotor_III_A_A():
    rotor = Rotor.get_rotor_III("A", "A")
    assert rotor._rotor_model == "III"
    assert rotor.rotor_position == "A"
    assert rotor._ring_setting == "A"
    assert rotor._wiring == "BDFHJLCPRTXVZNYEIWGAKMUSQO"


def test_get_rotor_IV_A_A():
    rotor = Rotor.get_rotor_IV("A", "A")
    assert rotor._rotor_model == "IV"
    assert rotor.rotor_position == "A"
    assert rotor._ring_setting == "A"
    assert rotor._wiring == "ESOVPZJAYQUIRHXLNFTGKDCMWB"


def test_get_rotor_V_A_A():
    rotor = Rotor.get_rotor_V("A", "A")
    assert rotor._rotor_model == "V"
    assert rotor.rotor_position == "A"
    assert rotor._ring_setting == "A"
    assert rotor._wiring == "VZBRGITYUPSDNHLXAWMJQOFECK"


def test_get_rotor_by_name_A_A():
    rotor = Rotor.get_rotor("I", "A", "A")
    assert rotor._rotor_model == "I"
    assert rotor.rotor_position == "A"
    assert rotor._ring_setting == "A"
    assert rotor._wiring == "EKMFLGDQVZNTOWYHXUSPAIBRCJ"


def test_get_rotor_invalid_model():
    with pytest.raises(RotorInvalidModelException):
        Rotor.get_rotor("VI", "A", "A")

## Test rotor exceptions ##


def test_rotor_wiring_wrong_length_exception():
    with pytest.raises(RotorWiringWrongLengthException):
        Rotor("ABC", "A")


def test_rotor_wiring_duplicate_letters_exception():
    with pytest.raises(RotorWiringDuplicateLettersException):
        Rotor("AACDEFGHIJKLMNOPQRSTUVWXYZ", "A")


def test_rotor_invalid_letter_exception():
    with pytest.raises(RotorInvalidLetterException):
        Rotor("ABCDEF5HIJKLMNOPQRSTUVWXYZ", "A")

    with pytest.raises(RotorInvalidLetterException):
        Rotor("ABCDEF HIJKLMNOPQRSTUVWXYZ", "A")

    with pytest.raises(RotorInvalidLetterException):
        Rotor("ABCDEFgHIJKLMNOPQRSTUVWXYZ", "A")
