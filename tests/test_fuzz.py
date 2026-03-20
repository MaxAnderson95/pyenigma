"""
Property-based fuzz tests for pyenigma using hypothesis.

Tests invariants that must hold for ALL inputs, not just specific examples.
"""

import string
import random as random_module

from hypothesis import given, settings, assume, HealthCheck
from hypothesis import strategies as st

from pyenigma.rotor import Rotor
from pyenigma.reflector import Reflector
from pyenigma.plugboard import Plugboard
from pyenigma.machine import EnigmaMachine
from pyenigma.constants import ALPHABET, ROTOR_WIRING, ROTOR_NOTCHES, REFLECTOR_WIRING
from pyenigma.exceptions import (
    RotorWiringWrongLengthException,
    RotorWiringDuplicateLettersException,
    RotorInvalidLetterException,
    RotorInvalidModelException,
    ReflectorWiringWrongLengthException,
    ReflectorWiringDuplicateLettersException,
    ReflectorInvalidLetterException,
    ReflectorInvalidModelException,
    PlugboardConnectionExistsException,
    PlugboardConnectionToItselfException,
    PlugboardInvalidLetterException,
    PlugboardTooManyConnectionsException,
    PlugboardStringOddNumberOfLettersException,
)

import pytest


# ============================================================
# Strategies (reusable hypothesis generators)
# ============================================================

# A single uppercase letter
uppercase_letter = st.sampled_from(list(ALPHABET))

# A valid rotor model name
rotor_model = st.sampled_from(["I", "II", "III", "IV", "V"])

# A valid reflector model name
reflector_model = st.sampled_from(["B", "C"])

# A random permutation of the alphabet (valid wiring)
@st.composite
def valid_wiring(draw: st.DrawFn) -> str:
    letters = list(ALPHABET)
    draw(st.randoms().map(lambda r: r.shuffle(letters)))
    return "".join(letters)


# A message of uppercase letters only
alpha_message = st.text(alphabet=string.ascii_uppercase, min_size=1, max_size=200)

# A message with mixed content (for normalization testing)
mixed_message = st.text(
    alphabet=string.ascii_letters + string.digits + " !@#$%^&*()",
    min_size=1,
    max_size=200,
)


# ============================================================
# Rotor Fuzz Tests
# ============================================================


class TestRotorFuzz:
    """Fuzz tests for the Rotor class."""

    @given(model=rotor_model, letter=uppercase_letter, position=uppercase_letter, ring=uppercase_letter)
    @settings(max_examples=500)
    def test_rotor_forward_produces_valid_letter(self, model: str, letter: str, position: str, ring: str) -> None:
        """Forward pass through any rotor at any setting must produce a valid uppercase letter."""
        rotor = Rotor.get_rotor(model, ring_setting=ring, initial_rotor_position=position)
        result = rotor.pass_forward(letter)
        assert result in ALPHABET, f"Forward pass produced invalid letter: {result}"

    @given(model=rotor_model, letter=uppercase_letter, position=uppercase_letter, ring=uppercase_letter)
    @settings(max_examples=500)
    def test_rotor_backward_produces_valid_letter(self, model: str, letter: str, position: str, ring: str) -> None:
        """Backward pass through any rotor at any setting must produce a valid uppercase letter."""
        rotor = Rotor.get_rotor(model, ring_setting=ring, initial_rotor_position=position)
        result = rotor.pass_backward(letter)
        assert result in ALPHABET, f"Backward pass produced invalid letter: {result}"

    @given(model=rotor_model, position=uppercase_letter, ring=uppercase_letter)
    @settings(max_examples=200)
    def test_rotor_forward_is_bijection(self, model: str, position: str, ring: str) -> None:
        """Forward pass must be a bijection (permutation) — no two inputs map to the same output."""
        rotor = Rotor.get_rotor(model, ring_setting=ring, initial_rotor_position=position)
        outputs = [rotor.pass_forward(letter) for letter in ALPHABET]
        assert len(set(outputs)) == 26, f"Forward pass is not a bijection: {outputs}"

    @given(model=rotor_model, position=uppercase_letter, ring=uppercase_letter)
    @settings(max_examples=200)
    def test_rotor_backward_is_bijection(self, model: str, position: str, ring: str) -> None:
        """Backward pass must be a bijection (permutation) — no two inputs map to the same output."""
        rotor = Rotor.get_rotor(model, ring_setting=ring, initial_rotor_position=position)
        outputs = [rotor.pass_backward(letter) for letter in ALPHABET]
        assert len(set(outputs)) == 26, f"Backward pass is not a bijection: {outputs}"

    @given(model=rotor_model, position=uppercase_letter, ring=uppercase_letter)
    @settings(max_examples=200)
    def test_rotor_forward_backward_inverse(self, model: str, position: str, ring: str) -> None:
        """Forward then backward pass (or vice versa) should recover the original letter.
        
        This is the core correctness property: the rotor must be reversible.
        """
        rotor = Rotor.get_rotor(model, ring_setting=ring, initial_rotor_position=position)
        for letter in ALPHABET:
            forward_result = rotor.pass_forward(letter)
            backward_of_forward = rotor.pass_backward(forward_result)
            assert backward_of_forward == letter, (
                f"Rotor {model} pos={position} ring={ring}: "
                f"backward(forward({letter})) = backward({forward_result}) = {backward_of_forward}, expected {letter}"
            )

    @given(model=rotor_model, position=uppercase_letter, ring=uppercase_letter)
    @settings(max_examples=200)
    def test_rotor_backward_forward_inverse(self, model: str, position: str, ring: str) -> None:
        """Backward then forward pass should also recover the original letter."""
        rotor = Rotor.get_rotor(model, ring_setting=ring, initial_rotor_position=position)
        for letter in ALPHABET:
            backward_result = rotor.pass_backward(letter)
            forward_of_backward = rotor.pass_forward(backward_result)
            assert forward_of_backward == letter, (
                f"Rotor {model} pos={position} ring={ring}: "
                f"forward(backward({letter})) = forward({backward_result}) = {forward_of_backward}, expected {letter}"
            )

    @given(model=rotor_model, position=uppercase_letter, ring=uppercase_letter)
    @settings(max_examples=200)
    def test_rotor_rotate_full_cycle_returns_to_start(self, model: str, position: str, ring: str) -> None:
        """Rotating a rotor 26 times should return it to its original position."""
        rotor = Rotor.get_rotor(model, ring_setting=ring, initial_rotor_position=position)
        for _ in range(26):
            rotor.rotate()
        assert rotor.rotor_position == position, (
            f"After 26 rotations, position is {rotor.rotor_position}, expected {position}"
        )

    @given(model=rotor_model, position=uppercase_letter, ring=uppercase_letter)
    def test_rotor_reset_restores_position(self, model: str, position: str, ring: str) -> None:
        """Reset should always restore the original position."""
        rotor = Rotor.get_rotor(model, ring_setting=ring, initial_rotor_position=position)
        # Rotate some random number of times
        for _ in range(13):
            rotor.rotate()
        rotor.reset()
        assert rotor.rotor_position == position

    @given(wiring=st.text(min_size=0, max_size=100))
    @settings(max_examples=300)
    def test_rotor_rejects_invalid_wiring_length(self, wiring: str) -> None:
        """Any wiring that isn't exactly 26 chars should be rejected."""
        assume(len(wiring) != 26)
        with pytest.raises(RotorWiringWrongLengthException):
            Rotor(wiring, "R")

    @given(data=st.data())
    @settings(max_examples=200)
    def test_rotor_rejects_duplicate_letters_in_wiring(self, data: st.DataObject) -> None:
        """26-char wiring with duplicates should be rejected."""
        # Create a 26-char string with at least one duplicate uppercase letter
        base = list(ALPHABET)
        idx1 = data.draw(st.integers(min_value=0, max_value=25))
        idx2 = data.draw(st.integers(min_value=0, max_value=25))
        assume(idx1 != idx2)
        base[idx2] = base[idx1]  # Force a duplicate
        wiring = "".join(base)
        assume(len(set(wiring)) != 26)  # Ensure it actually has duplicates
        with pytest.raises(RotorWiringDuplicateLettersException):
            Rotor(wiring, "R")

    @given(model_name=st.text(min_size=1, max_size=20))
    @settings(max_examples=200)
    def test_rotor_rejects_invalid_model(self, model_name: str) -> None:
        """Unknown model names should raise RotorInvalidModelException."""
        assume(model_name not in ROTOR_WIRING)
        with pytest.raises(RotorInvalidModelException):
            Rotor.get_rotor(model_name)


# ============================================================
# Reflector Fuzz Tests
# ============================================================


class TestReflectorFuzz:
    """Fuzz tests for the Reflector class."""

    @given(model=reflector_model, letter=uppercase_letter)
    @settings(max_examples=200)
    def test_reflector_produces_valid_letter(self, model: str, letter: str) -> None:
        """Reflection must always produce a valid uppercase letter."""
        reflector = Reflector.get_reflector(model)
        result = reflector.reflect(letter)
        assert result in ALPHABET

    @given(model=reflector_model, letter=uppercase_letter)
    @settings(max_examples=200)
    def test_reflector_is_involution(self, model: str, letter: str) -> None:
        """A reflector must be an involution: reflect(reflect(x)) == x."""
        reflector = Reflector.get_reflector(model)
        result = reflector.reflect(reflector.reflect(letter))
        assert result == letter, (
            f"Reflector {model}: reflect(reflect({letter})) = {result}, expected {letter}"
        )

    @given(model=reflector_model, letter=uppercase_letter)
    @settings(max_examples=200)
    def test_reflector_never_maps_letter_to_itself(self, model: str, letter: str) -> None:
        """A real Enigma reflector never maps a letter to itself (a key Enigma weakness)."""
        reflector = Reflector.get_reflector(model)
        result = reflector.reflect(letter)
        assert result != letter, (
            f"Reflector {model} mapped {letter} to itself"
        )

    @given(model=reflector_model)
    @settings(max_examples=10)
    def test_reflector_is_bijection(self, model: str) -> None:
        """Reflector must be a bijection (permutation)."""
        reflector = Reflector.get_reflector(model)
        outputs = [reflector.reflect(letter) for letter in ALPHABET]
        assert len(set(outputs)) == 26

    @given(wiring=st.text(min_size=0, max_size=100))
    @settings(max_examples=300)
    def test_reflector_rejects_invalid_wiring_length(self, wiring: str) -> None:
        """Wiring that isn't 26 chars should be rejected."""
        assume(len(wiring) != 26)
        with pytest.raises(ReflectorWiringWrongLengthException):
            Reflector(wiring)

    @given(model_name=st.text(min_size=1, max_size=20))
    @settings(max_examples=200)
    def test_reflector_rejects_invalid_model(self, model_name: str) -> None:
        """Unknown model names should raise ReflectorInvalidModelException."""
        assume(model_name not in REFLECTOR_WIRING)
        with pytest.raises(ReflectorInvalidModelException):
            Reflector.get_reflector(model_name)


# ============================================================
# Plugboard Fuzz Tests
# ============================================================


class TestPlugboardFuzz:
    """Fuzz tests for the Plugboard class."""

    @given(letter=uppercase_letter)
    def test_empty_plugboard_is_identity(self, letter: str) -> None:
        """An empty plugboard should return the input letter unchanged."""
        pb = Plugboard()
        assert pb.translate(letter) == letter

    @given(l1=uppercase_letter, l2=uppercase_letter)
    def test_plugboard_connection_is_involution(self, l1: str, l2: str) -> None:
        """translate(translate(x)) must always equal x."""
        assume(l1 != l2)
        pb = Plugboard()
        pb.add_connection(l1, l2)
        for letter in ALPHABET:
            assert pb.translate(pb.translate(letter)) == letter

    @given(l1=uppercase_letter)
    def test_plugboard_rejects_self_connection(self, l1: str) -> None:
        """Connecting a letter to itself must raise an exception."""
        pb = Plugboard()
        with pytest.raises(PlugboardConnectionToItselfException):
            pb.add_connection(l1, l1)

    @given(data=st.data())
    @settings(max_examples=200)
    def test_plugboard_rejects_duplicate_connection(self, data: st.DataObject) -> None:
        """Adding a connection for an already-connected letter must raise an exception."""
        l1 = data.draw(uppercase_letter)
        l2 = data.draw(uppercase_letter)
        l3 = data.draw(uppercase_letter)
        assume(l1 != l2 and l1 != l3 and l2 != l3)
        pb = Plugboard()
        pb.add_connection(l1, l2)
        # Try to reuse l1 in another connection
        with pytest.raises(PlugboardConnectionExistsException):
            pb.add_connection(l1, l3)

    @given(l1=st.text(alphabet=string.ascii_lowercase + string.digits + "!@#$%", min_size=1, max_size=1),
           l2=uppercase_letter)
    def test_plugboard_rejects_invalid_letters(self, l1: str, l2: str) -> None:
        """Non-uppercase-alpha characters must be rejected."""
        assume(l1 not in ALPHABET)
        pb = Plugboard()
        with pytest.raises(PlugboardInvalidLetterException):
            pb.add_connection(l1, l2)

    def test_plugboard_rejects_more_than_10_connections(self) -> None:
        """The 11th connection must be rejected."""
        pb = Plugboard()
        # Use all 26 letters as 13 pairs, but only 10 should be allowed
        pairs = list(zip(ALPHABET[::2], ALPHABET[1::2]))  # 13 pairs
        for i, (a, b) in enumerate(pairs):
            if i < 10:
                pb.add_connection(a, b)
            else:
                with pytest.raises(PlugboardTooManyConnectionsException):
                    pb.add_connection(a, b)
                break

    @given(s=st.text(alphabet=string.ascii_uppercase, min_size=1, max_size=21))
    def test_plugboard_string_odd_length_rejected(self, s: str) -> None:
        """Odd-length connection strings must be rejected."""
        assume(len(s.replace(" ", "")) % 2 != 0)
        pb = Plugboard()
        with pytest.raises(PlugboardStringOddNumberOfLettersException):
            pb.add_connection_from_string(s)


# ============================================================
# EnigmaMachine Fuzz Tests
# ============================================================


def build_machine(
    rotor_models: tuple[str, str, str] = ("I", "II", "III"),
    reflector_model: str = "B",
    ring_settings: tuple[str, str, str] = ("A", "A", "A"),
    positions: tuple[str, str, str] = ("A", "A", "A"),
    plugboard_pairs: list[tuple[str, str]] | None = None,
) -> EnigmaMachine:
    """Helper to build a fully configured EnigmaMachine."""
    machine = EnigmaMachine()
    rotors = [
        Rotor.get_rotor(rotor_models[i], ring_setting=ring_settings[i], initial_rotor_position=positions[i])
        for i in range(3)
    ]
    machine.set_rotors(rotors)
    machine.set_reflector(Reflector.get_reflector(reflector_model))
    pb = Plugboard()
    if plugboard_pairs:
        for a, b in plugboard_pairs:
            pb.add_connection(a, b)
    machine.set_plugboard(pb)
    return machine


class TestEnigmaMachineFuzz:
    """Fuzz tests for the EnigmaMachine class — the core Enigma properties."""

    @given(
        r1=rotor_model, r2=rotor_model, r3=rotor_model,
        ref=reflector_model,
        rs1=uppercase_letter, rs2=uppercase_letter, rs3=uppercase_letter,
        p1=uppercase_letter, p2=uppercase_letter, p3=uppercase_letter,
        message=alpha_message,
    )
    @settings(max_examples=500, deadline=None, suppress_health_check=[HealthCheck.too_slow])
    def test_encipher_decipher_reciprocal(
        self, r1: str, r2: str, r3: str, ref: str,
        rs1: str, rs2: str, rs3: str,
        p1: str, p2: str, p3: str,
        message: str,
    ) -> None:
        """THE fundamental Enigma property: enciphering the ciphertext with the same
        settings must recover the plaintext. encipher(encipher(msg)) == msg."""
        machine1 = build_machine(
            rotor_models=(r1, r2, r3),
            reflector_model=ref,
            ring_settings=(rs1, rs2, rs3),
            positions=(p1, p2, p3),
        )
        machine2 = build_machine(
            rotor_models=(r1, r2, r3),
            reflector_model=ref,
            ring_settings=(rs1, rs2, rs3),
            positions=(p1, p2, p3),
        )
        ciphertext = machine1.encipher(message)
        plaintext = machine2.decipher(ciphertext)
        assert plaintext == message, (
            f"Reciprocal failed for rotors=({r1},{r2},{r3}) ref={ref} "
            f"rings=({rs1},{rs2},{rs3}) pos=({p1},{p2},{p3}): "
            f"message={message!r} -> cipher={ciphertext!r} -> plain={plaintext!r}"
        )

    @given(
        r1=rotor_model, r2=rotor_model, r3=rotor_model,
        ref=reflector_model,
        p1=uppercase_letter, p2=uppercase_letter, p3=uppercase_letter,
        letter=uppercase_letter,
    )
    @settings(max_examples=500, deadline=None)
    def test_letter_never_encrypts_to_itself(
        self, r1: str, r2: str, r3: str, ref: str,
        p1: str, p2: str, p3: str,
        letter: str,
    ) -> None:
        """An Enigma machine never encrypts a letter to itself.
        
        This is a historically important property and a fundamental weakness
        that was exploited by codebreakers. If this fails, the implementation is wrong.
        """
        machine = build_machine(
            rotor_models=(r1, r2, r3),
            reflector_model=ref,
            positions=(p1, p2, p3),
        )
        result = machine.encipher(letter)
        assert result != letter, (
            f"Letter {letter} encrypted to itself with rotors=({r1},{r2},{r3}) "
            f"ref={ref} pos=({p1},{p2},{p3})"
        )

    @given(
        r1=rotor_model, r2=rotor_model, r3=rotor_model,
        ref=reflector_model,
        p1=uppercase_letter, p2=uppercase_letter, p3=uppercase_letter,
    )
    @settings(max_examples=200, deadline=None)
    def test_encipher_single_letter_is_permutation(
        self, r1: str, r2: str, r3: str, ref: str,
        p1: str, p2: str, p3: str,
    ) -> None:
        """Enciphering all 26 letters (each independently, resetting between)
        should produce 26 distinct outputs — the encryption is a permutation."""
        outputs = []
        for letter in ALPHABET:
            machine = build_machine(
                rotor_models=(r1, r2, r3),
                reflector_model=ref,
                positions=(p1, p2, p3),
            )
            outputs.append(machine.encipher(letter))
        assert len(set(outputs)) == 26, (
            f"Encryption is not a permutation for rotors=({r1},{r2},{r3}) "
            f"ref={ref} pos=({p1},{p2},{p3}): {outputs}"
        )

    @given(
        r1=rotor_model, r2=rotor_model, r3=rotor_model,
        ref=reflector_model,
        p1=uppercase_letter, p2=uppercase_letter, p3=uppercase_letter,
        message=mixed_message,
    )
    @settings(max_examples=300, deadline=None, suppress_health_check=[HealthCheck.too_slow])
    def test_encipher_handles_mixed_input(
        self, r1: str, r2: str, r3: str, ref: str,
        p1: str, p2: str, p3: str,
        message: str,
    ) -> None:
        """Enciphering messages with numbers, spaces, and special chars must not crash,
        and the output must contain only uppercase letters."""
        machine = build_machine(
            rotor_models=(r1, r2, r3),
            reflector_model=ref,
            positions=(p1, p2, p3),
        )
        result = machine.encipher(message)
        for char in result:
            assert char in ALPHABET, f"Output contains invalid character: {char!r}"

    @given(
        r1=rotor_model, r2=rotor_model, r3=rotor_model,
        ref=reflector_model,
        rs1=uppercase_letter, rs2=uppercase_letter, rs3=uppercase_letter,
        p1=uppercase_letter, p2=uppercase_letter, p3=uppercase_letter,
        message=mixed_message,
    )
    @settings(max_examples=300, deadline=None, suppress_health_check=[HealthCheck.too_slow])
    def test_reciprocal_with_mixed_input(
        self, r1: str, r2: str, r3: str, ref: str,
        rs1: str, rs2: str, rs3: str,
        p1: str, p2: str, p3: str,
        message: str,
    ) -> None:
        """Reciprocal property must hold even for messages with junk characters.
        The normalized plaintext should be recovered."""
        machine1 = build_machine(
            rotor_models=(r1, r2, r3),
            reflector_model=ref,
            ring_settings=(rs1, rs2, rs3),
            positions=(p1, p2, p3),
        )
        # Normalize the message the same way the machine does internally
        normalized = message.upper().replace(" ", "")
        normalized = "".join(c for c in normalized if c in ALPHABET)
        assume(len(normalized) > 0)  # Skip empty-after-normalization

        ciphertext = machine1.encipher(message)

        machine2 = build_machine(
            rotor_models=(r1, r2, r3),
            reflector_model=ref,
            ring_settings=(rs1, rs2, rs3),
            positions=(p1, p2, p3),
        )
        plaintext = machine2.decipher(ciphertext)
        assert plaintext == normalized, (
            f"Reciprocal with mixed input failed: "
            f"normalized={normalized!r} -> cipher={ciphertext!r} -> plain={plaintext!r}"
        )

    @given(
        r1=rotor_model, r2=rotor_model, r3=rotor_model,
        ref=reflector_model,
        p1=uppercase_letter, p2=uppercase_letter, p3=uppercase_letter,
    )
    @settings(max_examples=100, deadline=None)
    def test_reset_restores_machine_state(
        self, r1: str, r2: str, r3: str, ref: str,
        p1: str, p2: str, p3: str,
    ) -> None:
        """After enciphering and resetting, enciphering the same message must
        produce the same output."""
        machine = build_machine(
            rotor_models=(r1, r2, r3),
            reflector_model=ref,
            positions=(p1, p2, p3),
        )
        msg = "THEQUICKBROWNFOXJUMPSOVERTHELAZYDOG"
        result1 = machine.encipher(msg)
        machine.reset()
        result2 = machine.encipher(msg)
        assert result1 == result2, (
            f"Reset did not restore state: {result1!r} != {result2!r}"
        )

    def test_encipher_empty_string(self) -> None:
        """Enciphering an empty string should produce an empty string."""
        machine = build_machine()
        assert machine.encipher("") == ""

    def test_encipher_only_special_chars(self) -> None:
        """Enciphering a string with no alpha chars should produce an empty string."""
        machine = build_machine()
        assert machine.encipher("123 !@#$%^&*()") == ""


# ============================================================
# Edge case / bug-hunting tests
# ============================================================


class TestEdgeCases:
    """Targeted tests for suspected edge cases and potential bugs."""

    def test_next_letter_noop_upper(self) -> None:
        """machine._next_letter has a `letter.upper()` that doesn't assign the result.
        Verify that lowercase input would produce wrong results."""
        # _next_letter is a static method
        # With uppercase input, it works fine:
        assert EnigmaMachine._next_letter("A") == "B"
        assert EnigmaMachine._next_letter("Z") == "A"
        assert EnigmaMachine._next_letter("M") == "N"

        # With lowercase input, .upper() normalizes it correctly
        assert EnigmaMachine._next_letter("z") == "A"
        assert EnigmaMachine._next_letter("a") == "B"
        assert EnigmaMachine._next_letter("m") == "N"

    def test_normalize_message_removes_all_occurrences_of_invalid_char(self) -> None:
        """_normalize_message uses str.replace() inside a loop, which removes ALL
        occurrences at once. Verify it handles repeated invalid characters."""
        machine = build_machine()
        # Message with repeated digits interspersed with letters
        result = machine._normalize_message("A1B1C1D")
        assert result == "ABCD"

    def test_normalize_message_unicode(self) -> None:
        """Test that unicode characters are properly stripped."""
        machine = build_machine()
        result = machine._normalize_message("HELLO\u00e9WORLD")  # e-acute
        assert result == "HELLOWORLD"

    @given(
        r1=rotor_model, r2=rotor_model, r3=rotor_model,
        ref=reflector_model,
    )
    @settings(max_examples=50, deadline=None)
    def test_long_message_reciprocal(
        self, r1: str, r2: str, r3: str, ref: str,
    ) -> None:
        """Test reciprocal property with a message long enough to trigger
        all rotor stepping including double-stepping (needs 26*26 = 676+ chars)."""
        # Build a message that exercises many rotor positions
        message = "A" * 700

        machine1 = build_machine(rotor_models=(r1, r2, r3), reflector_model=ref)
        machine2 = build_machine(rotor_models=(r1, r2, r3), reflector_model=ref)

        ciphertext = machine1.encipher(message)
        plaintext = machine2.decipher(ciphertext)
        assert plaintext == message

    @given(
        r1=rotor_model, r2=rotor_model, r3=rotor_model,
        ref=reflector_model,
        rs1=uppercase_letter, rs2=uppercase_letter, rs3=uppercase_letter,
        p1=uppercase_letter, p2=uppercase_letter, p3=uppercase_letter,
    )
    @settings(max_examples=100, deadline=None, suppress_health_check=[HealthCheck.too_slow])
    def test_reciprocal_with_plugboard(
        self, r1: str, r2: str, r3: str, ref: str,
        rs1: str, rs2: str, rs3: str,
        p1: str, p2: str, p3: str,
    ) -> None:
        """Test that reciprocal property holds with plugboard connections."""
        pairs = [("A", "B"), ("C", "D"), ("E", "F"), ("G", "H"), ("I", "J")]

        machine1 = build_machine(
            rotor_models=(r1, r2, r3),
            reflector_model=ref,
            ring_settings=(rs1, rs2, rs3),
            positions=(p1, p2, p3),
            plugboard_pairs=pairs,
        )
        machine2 = build_machine(
            rotor_models=(r1, r2, r3),
            reflector_model=ref,
            ring_settings=(rs1, rs2, rs3),
            positions=(p1, p2, p3),
            plugboard_pairs=pairs,
        )

        message = "THEQUICKBROWNFOXJUMPSOVERTHELAZYDOG"
        ciphertext = machine1.encipher(message)
        plaintext = machine2.decipher(ciphertext)
        assert plaintext == message

    def test_machine_without_plugboard_crashes(self) -> None:
        """Calling encipher without setting a plugboard should raise AttributeError."""
        machine = EnigmaMachine()
        machine.set_rotors([Rotor.get_rotor_I(), Rotor.get_rotor_II(), Rotor.get_rotor_III()])
        machine.set_reflector(Reflector.get_reflector_B())
        # No plugboard set
        with pytest.raises(AttributeError):
            machine.encipher("HELLO")

    def test_machine_without_rotors_crashes(self) -> None:
        """Calling encipher without setting rotors should raise AttributeError."""
        machine = EnigmaMachine()
        machine.set_reflector(Reflector.get_reflector_B())
        machine.set_plugboard(Plugboard())
        with pytest.raises(AttributeError):
            machine.encipher("HELLO")

    def test_machine_without_reflector_crashes(self) -> None:
        """Calling encipher without setting a reflector should raise AttributeError."""
        machine = EnigmaMachine()
        machine.set_rotors([Rotor.get_rotor_I(), Rotor.get_rotor_II(), Rotor.get_rotor_III()])
        machine.set_plugboard(Plugboard())
        with pytest.raises(AttributeError):
            machine.encipher("HELLO")

    def test_reflector_reflect_with_lowercase_crashes(self) -> None:
        """Passing lowercase to reflect() should raise KeyError (no input validation)."""
        reflector = Reflector.get_reflector_B()
        with pytest.raises(KeyError):
            reflector.reflect("a")

    def test_rotor_pass_forward_with_lowercase_crashes(self) -> None:
        """Passing lowercase to pass_forward() should raise an error (no input validation)."""
        rotor = Rotor.get_rotor_I()
        # This will raise ValueError because 'a' is not in ALPHABET
        with pytest.raises((KeyError, ValueError)):
            rotor.pass_forward("a")

    def test_plugboard_translate_lowercase_passthrough(self) -> None:
        """Plugboard.translate() with lowercase returns it unchanged (no validation).
        This is inconsistent — add_connection rejects lowercase but translate doesn't."""
        pb = Plugboard()
        pb.add_connection("A", "B")
        # Lowercase 'a' is NOT swapped to 'b' because the connection is stored as uppercase
        assert pb.translate("a") == "a"
