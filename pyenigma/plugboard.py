import logging
from .constants import ALPHABET
from .exceptions import (
    PlugboardConnectionExistsException,
    PlugboardConnectionToItselfException,
    PlugboardInvalidLetterException,
    PlugboardTooManyConnectionsException,
    PlugboardStringOddNumberOfLettersException
)

logger = logging.getLogger(__name__)


class Plugboard():
    def __init__(self) -> None:
        self.connections: dict[str, str] = {}
        logger.debug("Initialized Plugboard")

    def add_connection(self, letter1: str, letter2: str) -> None:
        self._validate_plugboard_connection(letter1, letter2)

        # Add the connection
        self.connections[letter1] = letter2
        self.connections[letter2] = letter1

    def add_connection_from_map(self, connection_map: dict[str, str]) -> None:
        for letter1, letter2 in connection_map.items():
            self.add_connection(letter1, letter2)

    def add_connection_from_string(self, connection_string: str) -> None:
        connection_string = connection_string.upper().replace(" ", "")

        if len(connection_string) % 2 != 0:
            raise PlugboardStringOddNumberOfLettersException("Plugboard connection string must have an even number of characters")

        for i in range(0, len(connection_string), 2):
            letter1 = connection_string[i]
            letter2 = connection_string[i + 1]
            self.add_connection(letter1, letter2)

    def translate(self, letter: str) -> str:
        val = self.connections.get(letter, letter)
        logger.debug(f"Plugboard translated letter {letter} to {val}")
        return val

    def _validate_plugboard_connection(self, letter1: str, letter2: str) -> None:
        # Check if a connection for either letter already exists
        if letter1 in self.connections or letter2 in self.connections:
            raise PlugboardConnectionExistsException(f"Connection for letter {letter1} or {letter2} already exists")

        # Check that the connection is not to itself
        if letter1 == letter2:
            raise PlugboardConnectionToItselfException("Cannot connect a letter to itself")

        # Check that the connection is not to an invalid letter
        if letter1 not in ALPHABET or letter2 not in ALPHABET:
            raise PlugboardInvalidLetterException(f"Letter {letter1} or {letter2} is not a valid letter in the alphabet")

        # Check that there are not more than 10 connections (20 letters in total)
        if len(self.connections) >= 20:
            raise PlugboardTooManyConnectionsException("Cannot have more than 10 connections")
