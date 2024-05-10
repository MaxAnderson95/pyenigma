import logging
from .rotor import Rotor
from .reflector import Reflector
from .plugboard import Plugboard
from .constants import ALPHABET


logger = logging.getLogger(__name__)


class EnigmaMachine():
    def __init__(self) -> None:
        logger.debug("Initialized Enigma Machine")

    def set_rotors(self, rotors: list[Rotor]) -> None:
        logger.debug("Setting rotors")
        self.rotors = rotors

    def set_reflector(self, reflector: Reflector) -> None:
        logger.debug("Setting reflector")
        self.reflector = reflector

    def set_plugboard(self, plugboard: Plugboard) -> None:
        logger.debug("Setting plugboard")
        self.plugboard = plugboard

    def _encipher_letter(self, letter: str) -> str:
        original_letter = letter
        logger.debug(f"Starting encryption of letter {original_letter}")

        # Pass the letter through the plugboard
        letter = self.plugboard.translate(letter)

        # Pass the letter through the 3 rotors (left<-right)
        for rotor in reversed(self.rotors):
            letter = rotor.pass_forward(letter)

        # Pass the letter through the reflector
        letter = self.reflector.reflect(letter)

        # Pass the letter back through the 3 rotors (left->right)
        for rotor in self.rotors:
            letter = rotor.pass_backward(letter)

        # Pass the letter back through the plugboard
        letter = self.plugboard.translate(letter)

        logger.debug(f"Encrypted letter {original_letter} to {letter}")
        return letter

    @staticmethod
    def _next_letter(letter: str) -> str:
        letter.upper()
        if letter == 'Z':
            return 'A'
        else:
            return chr(ord(letter) + 1)  # Gets the next letter

    def _normalize_message(self, message: str) -> str:
        message = message.upper().replace(" ", "")
        for letter in message:
            if letter not in ALPHABET:
                logger.warning(f"Removing invalid character {letter} from message")
                message = message.replace(letter, "")
        return message

    def encipher(self, message: str) -> str:
        message = self._normalize_message(message)
        encrypted_message = ""

        for letter in message:
            # Rotate the rightmost rotor before encrypting the letter
            self.rotors[2].rotate()

            # Rotate the middle rotor if the rightmost rotor is at the notch
            if self.rotors[2].notch == self.rotors[2].rotor_position:
                self.rotors[1].rotate()
            # Handle the double stepping of the Enigma Machine. See: https://www.ciphermachinesandcryptology.com/en/enigmatech.htm#steppingmechanism
            elif self.rotors[1].notch == self._next_letter(self.rotors[1].rotor_position):
                self.rotors[1].rotate()
                self.rotors[0].rotate()

                # Encrypt the letter and append it to the encrypted message
            encrypted_message += self._encipher_letter(letter)
        return encrypted_message

    def decipher(self, message: str) -> str:
        return self.encipher(message)  # Deciphering is the same as enciphering in the Enigma Machine

    def reset(self) -> None:
        for rotor in self.rotors:
            rotor.reset()
        logger.debug("Reset Enigma Machine")
