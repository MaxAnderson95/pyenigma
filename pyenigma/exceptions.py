class EnigmaException(Exception):
    """Base class for exceptions in the Enigma module."""
    pass


class PlugboardException(EnigmaException):
    """Base class for exceptions related to the Plugboard"""
    pass


class PlugboardConnectionExistsException(PlugboardException):
    """Occurs when a connection already exists for one or both of the letters"""
    pass


class PlugboardConnectionToItselfException(PlugboardException):
    """Occurs when a connection is made to itself"""
    pass


class PlugboardInvalidLetterException(PlugboardException):
    """Occurs when a letter is not in the alphabet"""
    pass


class PlugboardTooManyConnectionsException(PlugboardException):
    """Occurs when there are more than 10 connections"""
    pass


class PlugboardStringOddNumberOfLettersException(PlugboardException):
    """Occurs when the connection string has ana odd number of letters"""
    pass


class ReflectorException(EnigmaException):
    """Base class for exceptions related to the Reflector"""
    pass


class ReflectorWiringWrongLengthException(ReflectorException):
    """Occurs when the reflector wiring is not 26 characters long"""
    pass


class ReflectorWiringDuplicateLettersException(ReflectorException):
    """Occurs when the reflector wiring contains duplicate letters"""
    pass


class ReflectorInvalidLetterException(ReflectorException):
    """Occurs when a letter is not in the alphabet"""
    pass


class ReflectorInvalidModelException(ReflectorException):
    """Occurs when an invalid reflector model is provided"""
    pass


class RotorException(EnigmaException):
    """Base class for exceptions related to the Rotors"""
    pass


class RotorWiringWrongLengthException(RotorException):
    """Occurs when the rotor wiring is not 26 characters long"""
    pass


class RotorWiringDuplicateLettersException(RotorException):
    """Occurs when the rotor wiring contains duplicate letters"""
    pass


class RotorInvalidLetterException(RotorException):
    """Occurs when a letter is not in the alphabet"""
    pass


class RotorInvalidModelException(RotorException):
    """Occurs when an invalid rotor model is provided"""
    pass
