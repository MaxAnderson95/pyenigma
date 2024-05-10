import argparse
from .machine import EnigmaMachine
from .rotor import Rotor
from .reflector import Reflector
from .plugboard import Plugboard
from .constants import ALPHABET


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Encrypt or decrypt a message using the Enigma machine")
    parser.add_argument("--rotors", nargs=3, help="The rotors to use", required=True, choices=["I", "II", "III", "IV", "V"])
    parser.add_argument("--reflector", help="The reflector to use", required=True, choices=["B", "C"])
    parser.add_argument("--ring-settings", nargs=3, help="The ring settings for the rotors",
                        required=False, default=["A", "A", "A"], choices=[l for l in ALPHABET])
    parser.add_argument("--initial-rotor-positions", nargs=3, help="The initial rotor positions",
                        required=False, default=["A", "A", "A"], choices=[l for l in ALPHABET])
    parser.add_argument("--plugboard", help="The plugboard settings", required=False, default="")
    parser.add_argument("--message", help="The message to encrypt or decrypt")
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    first_rotor = Rotor.get_rotor(
        args.rotors[0],
        ring_setting=args.ring_settings[0],
        initial_rotor_position=args.initial_rotor_positions[0]
    )
    second_rotor = Rotor.get_rotor(
        args.rotors[1],
        ring_setting=args.ring_settings[1],
        initial_rotor_position=args.initial_rotor_positions[1]
    )
    third_rotor = Rotor.get_rotor(
        args.rotors[2],
        ring_setting=args.ring_settings[2],
        initial_rotor_position=args.initial_rotor_positions[2]
    )

    reflector = Reflector.get_reflector(args.reflector)

    plugboard_settings = Plugboard()
    plugboard_settings.add_connection_from_string(args.plugboard)

    enigma = EnigmaMachine()
    enigma.set_rotors([first_rotor, second_rotor, third_rotor])
    enigma.set_reflector(reflector)
    enigma.set_plugboard(plugboard_settings)

    print(enigma.encipher(args.message))


if __name__ == "__main__":
    main()
