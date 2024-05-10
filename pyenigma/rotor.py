import logging
from math import e
from pyenigma.constants import ALPHABET, ROTOR_WIRING, ROTOR_NOTCHES
from pyenigma.exceptions import (
    RotorWiringWrongLengthException,
    RotorWiringDuplicateLettersException,
    RotorInvalidLetterException,
    RotorInvalidModelException
)


logger = logging.getLogger(__name__)


class Rotor():
    def __init__(self, rotor_wiring: str, rotor_notch: str, ring_setting: str = "A", initial_rotor_position: str = "A", rotor_model: str = "Custom") -> None:
        self._validate_rotor_wiring(rotor_wiring)
        self._wiring = rotor_wiring
        self.notch = rotor_notch
        self._ring_setting = ring_setting
        self.rotor_position = initial_rotor_position
        self._original_rotor_position = initial_rotor_position
        self._wiring_map = {k: v for k, v in zip(ALPHABET, rotor_wiring)}
        self._reverse_wiring_map = {v: k for k, v in zip(ALPHABET, rotor_wiring)}
        self._rotor_model = rotor_model
        logger.debug(f"Rotor model {self._rotor_model} initialized")

    @staticmethod
    def _shift_alphabet(letter: str) -> str:
        # Shift the alphabet so that the input letter is at the beginning and handles wrap around
        return ALPHABET[ALPHABET.index(letter):] + ALPHABET[:ALPHABET.index(letter)]

    def _get_ring_setting_offset(self, letter: str) -> str:
        # Get the offset of the ring setting for a given letter based on the rotor position and ring setting combined.
        # Function output letter is used to determine the new translated entry position of the rotor.
        # Used for the forward pass of the rotor.
        # Ex. Input of A, ring setting of A, rotor position of A, function output is A
        # Ex. Input of A, ring setting of B, rotor position of A, function output is Z
        # Ex. Input of A, ring setting of C, rotor position of A, function output is Y
        # Ex. Input of A, ring setting of A, rotor position of B, function output is B
        alphabet = self._shift_alphabet(self.rotor_position)
        return alphabet[(alphabet.index(letter) - alphabet.index(self._ring_setting)) % len(alphabet)]

    def _get_ring_setting_offset_reversed(self, letter: str) -> str:
        # Get the offset of the ring setting for a given letter based on the rotor position and ring setting combined.
        # Function output letter is used to determine the new translated entry position of the rotor.
        # Used for the backward pass of the rotor.
        # Ex. Input of A, ring setting of A, rotor position of A, function output is A
        # Ex. Input of A, ring setting of B, rotor position of A, function output is B
        # Ex. Input of A, ring setting of C, rotor position of A, function output is C
        # Ex. Input of A, ring setting of A, rotor position of B, function output is Z
        alphabet = self._shift_alphabet(self.rotor_position)
        return alphabet[(alphabet.index(letter) + alphabet.index(self._ring_setting)) % len(alphabet)]

    def pass_forward(self, letter: str) -> str:
        # Pass the letter through the rotor from right to left and return the translated letter
        logger.debug(f"Passing letter {letter} forward through rotor {self._rotor_model} from right to left. Current rotor position is {
            self.rotor_position}, ring setting is {self._ring_setting}")
        entry_position = self._get_ring_setting_offset(letter)
        logger.debug(f"Rotor adjusted entry position is {entry_position}")
        translated_letter = self._wiring_map[entry_position]
        logger.debug(f"Rotor translated letter is {translated_letter}")
        exit_position = self._get_ring_setting_offset_reversed(translated_letter)
        logger.debug(f"Rotor adjusted exit position is {exit_position}")
        return exit_position

    def pass_backward(self, letter: str) -> str:
        # Pass the letter through the rotor from left to right and return the translated letter
        logger.debug(f"Passing letter {letter} backward through rotor {self._rotor_model} from left to right. Current rotor position is {
            self.rotor_position}, ring setting is {self._ring_setting}")
        entry_position = self._get_ring_setting_offset(letter)
        logger.debug(f"Rotor adjusted entry position is {entry_position}")
        translated_letter = self._reverse_wiring_map[entry_position]
        logger.debug(f"Rotor translated letter is {translated_letter}")
        exit_position = self._get_ring_setting_offset_reversed(translated_letter)
        logger.debug(f"Rotor adjusted exit position is {exit_position}")
        return exit_position

    def rotate(self) -> None:
        # Rotate the rotor by one position by setting the rotor position to the next letter in the alphabet
        new_position = ALPHABET[(ALPHABET.index(self.rotor_position) + 1) % len(ALPHABET)]
        logger.debug(f"Rotating rotor {self._rotor_model} from position {self.rotor_position} to position {new_position}")
        self.rotor_position = new_position

    def reset(self) -> None:
        # Reset the rotor position to the initial position
        logger.debug(f"Resetting rotor {self._rotor_model} from position {
            self.rotor_position} to original position {self._original_rotor_position}")
        self.rotor_position = self._original_rotor_position

    @staticmethod
    def _validate_rotor_wiring(rotor_wiring: str) -> None:
        if len(rotor_wiring) != 26:
            raise RotorWiringWrongLengthException(f"Rotor wiring must be 26 characters long. Got {
                len(rotor_wiring)} characters.")

        if len(set(rotor_wiring)) != len(rotor_wiring):
            raise RotorWiringDuplicateLettersException("Rotor wiring must contain each letter exactly once")

        for letter in rotor_wiring:
            if letter not in ALPHABET:
                raise RotorInvalidLetterException(f"Rotor wiring contains invalid letter {letter}")

    @staticmethod
    def get_rotor_I(ring_setting: str = "A", initial_rotor_position: str = "A") -> "Rotor":
        return Rotor(ROTOR_WIRING["I"], ROTOR_NOTCHES["I"], ring_setting, initial_rotor_position, "I")

    @staticmethod
    def get_rotor_II(ring_setting: str = "A", initial_rotor_position: str = "A") -> "Rotor":
        return Rotor(ROTOR_WIRING["II"], ROTOR_NOTCHES["II"], ring_setting, initial_rotor_position, "II")

    @staticmethod
    def get_rotor_III(ring_setting: str = "A", initial_rotor_position: str = "A") -> "Rotor":
        return Rotor(ROTOR_WIRING["III"], ROTOR_NOTCHES["III"], ring_setting, initial_rotor_position, "III")

    @staticmethod
    def get_rotor_IV(ring_setting: str = "A", initial_rotor_position: str = "A") -> "Rotor":
        return Rotor(ROTOR_WIRING["IV"], ROTOR_NOTCHES["IV"], ring_setting, initial_rotor_position, "IV")

    @staticmethod
    def get_rotor_V(ring_setting: str = "A", initial_rotor_position: str = "A") -> "Rotor":
        return Rotor(ROTOR_WIRING["V"], ROTOR_NOTCHES["V"], ring_setting, initial_rotor_position, "V")

    @staticmethod
    def get_rotor(rotor_model: str, ring_setting: str = "A", initial_rotor_position: str = "A") -> "Rotor":
        try:
            return Rotor(ROTOR_WIRING[rotor_model], ROTOR_NOTCHES[rotor_model], ring_setting, initial_rotor_position, rotor_model)
        except KeyError:
            raise RotorInvalidModelException(f"Invalid rotor model {rotor_model}")
