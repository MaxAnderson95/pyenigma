import logging
import re
from pyenigma.constants import ALPHABET, REFLECTOR_WIRING
from pyenigma.exceptions import (
    ReflectorWiringWrongLengthException,
    ReflectorWiringDuplicateLettersException,
    ReflectorInvalidLetterException,
    ReflectorInvalidModelException
)

logger = logging.getLogger(__name__)


class Reflector():
    def __init__(self, reflector_wiring: str, reflector_model: str = "Custom") -> None:
        self._validate_reflector_wiring(reflector_wiring)
        self._wiring = reflector_wiring
        self._wiring_map = {k: v for k, v in zip(ALPHABET, reflector_wiring)}
        logger.debug(f"Initialized Reflector model {reflector_model} with wiring {reflector_wiring}")

    def reflect(self, letter: str) -> str:
        val = self._wiring_map[letter]
        logger.debug(f"Reflector reflected letter {letter} to {val}")
        return val

    @staticmethod
    def _validate_reflector_wiring(reflector_wiring: str) -> None:
        if len(reflector_wiring) != 26:
            raise ReflectorWiringWrongLengthException(f"Reflector wiring must be 26 characters long. Got {
                len(reflector_wiring)} characters.")

        if len(set(reflector_wiring)) != len(reflector_wiring):
            raise ReflectorWiringDuplicateLettersException("Reflector wiring must contain each letter exactly once")

        for letter in reflector_wiring:
            if letter not in ALPHABET:
                raise ReflectorInvalidLetterException(f"Reflector wiring contains invalid letter {letter}")

    @staticmethod
    def get_reflector_B() -> "Reflector":
        return Reflector(REFLECTOR_WIRING["B"], "B")

    @staticmethod
    def get_reflector_C() -> "Reflector":
        return Reflector(REFLECTOR_WIRING["C"], "C")

    @staticmethod
    def get_reflector(reflector_model: str) -> "Reflector":
        try:
            return Reflector(REFLECTOR_WIRING[reflector_model], reflector_model)
        except KeyError:
            raise ReflectorInvalidModelException(f"Invalid reflector model {reflector_model}")
