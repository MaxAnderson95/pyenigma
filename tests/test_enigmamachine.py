from pyenigma import EnigmaMachine, Rotor, Reflector, Plugboard


def test_enigma_machine_no_plugboard_default_settings_same_letter():
    rotorI = Rotor.get_rotor_I("A", "A")
    rotorII = Rotor.get_rotor_II("A", "A")
    rotorIII = Rotor.get_rotor_III("A", "A")
    reflectorB = Reflector.get_reflector_B()
    plugboard = Plugboard()

    enigma = EnigmaMachine()
    enigma.set_rotors([rotorI, rotorII, rotorIII])
    enigma.set_reflector(reflectorB)
    enigma.set_plugboard(plugboard)

    encrypted = enigma.encipher("AAAAA")
    assert encrypted == "BDZGO"


def test_enigma_machine_no_plugboard_default_settings_same_letter_decipher():
    rotorI = Rotor.get_rotor_I("A", "A")
    rotorII = Rotor.get_rotor_II("A", "A")
    rotorIII = Rotor.get_rotor_III("A", "A")
    reflectorB = Reflector.get_reflector_B()
    plugboard = Plugboard()

    enigma = EnigmaMachine()
    enigma.set_rotors([rotorI, rotorII, rotorIII])
    enigma.set_reflector(reflectorB)
    enigma.set_plugboard(plugboard)

    encrypted = enigma.decipher("BDZGO")
    assert encrypted == "AAAAA"


def test_enigma_machine_all_settings_configured():
    rotorIII = Rotor.get_rotor_III("L", "F")
    rotorIV = Rotor.get_rotor_IV("E", "R")
    rotorI = Rotor.get_rotor_I("T", "H")
    reflectorB = Reflector.get_reflector_B()
    plugboard = Plugboard()
    plugboard.add_connection("E", "M")
    plugboard.add_connection("U", "G")
    plugboard.add_connection("H", "T")
    plugboard.add_connection("Y", "I")
    plugboard.add_connection("R", "F")
    plugboard.add_connection("A", "J")

    enigma = EnigmaMachine()
    enigma.set_rotors([rotorIII, rotorIV, rotorI])
    enigma.set_reflector(reflectorB)
    enigma.set_plugboard(plugboard)

    encrypted = enigma.encipher("HELLOWORLD")
    assert encrypted == "ZZASKXUKIH"


def test_enigma_machine_middle_rotor_step():
    rotorI = Rotor.get_rotor_I("A", "A")
    rotorII = Rotor.get_rotor_II("A", "A")
    rotorIII = Rotor.get_rotor_III("A", "U")
    reflectorB = Reflector.get_reflector_B()
    plugboard = Plugboard()

    enigma = EnigmaMachine()
    enigma.set_rotors([rotorI, rotorII, rotorIII])
    enigma.set_reflector(reflectorB)
    enigma.set_plugboard(plugboard)

    encrypted = enigma.encipher("AAA")
    assert encrypted == "MUQ"


def test_enigma_machine_double_rotor_step():
    rotorI = Rotor.get_rotor_I("A", "B")
    rotorII = Rotor.get_rotor_II("A", "D")
    rotorIII = Rotor.get_rotor_III("A", "U")
    reflectorB = Reflector.get_reflector_B()
    plugboard = Plugboard()

    enigma = EnigmaMachine()
    enigma.set_rotors([rotorI, rotorII, rotorIII])
    enigma.set_reflector(reflectorB)
    enigma.set_plugboard(plugboard)

    encrypted = enigma.encipher("AAA")
    assert encrypted == "WRL"


def test_enigma_machine_long_string():
    rotorI = Rotor.get_rotor_I("A", "A")
    rotorII = Rotor.get_rotor_II("A", "A")
    rotorIII = Rotor.get_rotor_III("A", "A")
    reflectorB = Reflector.get_reflector_B()
    plugboard = Plugboard()

    enigma = EnigmaMachine()
    enigma.set_rotors([rotorI, rotorII, rotorIII])
    enigma.set_reflector(reflectorB)
    enigma.set_plugboard(plugboard)

    encrypted = enigma.encipher(
        "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
    )
    assert encrypted == "BDZGOWCXLTKSBTMCDLPBMUQOFXYHCXTGYJFLINHNXSHIUNTHEORXPQPKOVHCBUBTZSZSOOSTGOTFSODBBZZLXLCYZXIFGWFDZEEQIBMGFJBWZFCKPFMGBXQCIVIBBRNCOCJUVYDKMVJPFMDRMTGLWFOZLXGJEYYQPVPBWNCKVKLZTCBDLDCTSNRCOOVPTGBVBBISGJSOYHDENCTNUUKCUGHREVWBDJCTQ"


def test_enigma_machine_even_longer_string():
    rotorI = Rotor.get_rotor_I("A", "A")
    rotorII = Rotor.get_rotor_II("A", "A")
    rotorIII = Rotor.get_rotor_III("A", "A")
    reflectorB = Reflector.get_reflector_B()
    plugboard = Plugboard()

    enigma = EnigmaMachine()
    enigma.set_rotors([rotorI, rotorII, rotorIII])
    enigma.set_reflector(reflectorB)
    enigma.set_plugboard(plugboard)

    encrypted = enigma.encipher(
        "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
    )
    assert encrypted == "BDZGOWCXLTKSBTMCDLPBMUQOFXYHCXTGYJFLINHNXSHIUNTHEORXPQPKOVHCBUBTZSZSOOSTGOTFSODBBZZLXLCYZXIFGWFDZEEQIBMGFJBWZFCKPFMGBXQCIVIBBRNCOCJUVYDKMVJPFMDRMTGLWFOZLXGJEYYQPVPBWNCKVKLZTCBDLDCTSNRCOOVPTGBVBBISGJSOYHDENCTNUUKCUGHREVWBDJCTQXXOGLEBZMDBRZOSXDTZSZBGDCFPRBZYQGSNCCHGYEWOHVJBYZGKDGYNNEUJIWCTYCYTUUMBOYVUNNQUKKSOBSCORSUOSCNVROQLHEUDSUKYMIGIBSXPIHNTUVGGHIFQTGZXLGYQCNVNSRCLVPYOSVRBKCEXRNLGDYWEBFXIVKKTUGKPVMZOTUOGMHHZDREKJHLEFKKPOXLWBWVBYUKDTQUHDQTREVRQJMQWNDOVWLJHCCXCFXRPPXMSJEZCJUFTBRZZMCSSNJNYLCGLOYCITVYQXPDIYFGEFYVXSXHKEGXKMMDSWBCYRKIZOCGMFDDTMWZTLSSFLJMOOLUUQJMIJSCIQVRUISTLTGNCLGKIKTZHRXENRXJHYZTLXICWWMYWXDYIBLERBFLWJQYWONGIQQCUUQTPPHBIEHTUVGCEGPEYMWICGKWJCUFKLUIDMJDIVPJDMPGQPWITKGVIBOOMTNDUHQPHGSQRJRNOOVPWMDNXLLVFIIMKIEYIZMQUWYDPOULTUWBUKVMMWRLQLQSQPEUGJRCXZWPFYIYYBWLOEWROUVKPOZTCEUWTFJZQWPBQLDTTSRMDFLGXBXZRYQKDGJRZEZMKHJNQYPDJWCJFJLFNTRSNCNLGSSG"


def test_enigma_machine_all_settings_configured_reciprocal():
    rotorIII = Rotor.get_rotor_III("L", "F")
    rotorIV = Rotor.get_rotor_IV("E", "R")
    rotorI = Rotor.get_rotor_I("T", "H")
    reflectorB = Reflector.get_reflector_B()
    plugboard = Plugboard()
    plugboard.add_connection("E", "M")
    plugboard.add_connection("U", "G")
    plugboard.add_connection("H", "T")
    plugboard.add_connection("Y", "I")
    plugboard.add_connection("R", "F")
    plugboard.add_connection("A", "J")

    enigma = EnigmaMachine()
    enigma.set_rotors([rotorIII, rotorIV, rotorI])
    enigma.set_reflector(reflectorB)
    enigma.set_plugboard(plugboard)

    encrypted = enigma.encipher("HELLOWORLD")
    assert encrypted == "ZZASKXUKIH"

    # Reset the machine
    rotorIII = Rotor.get_rotor_III("L", "F")
    rotorIV = Rotor.get_rotor_IV("E", "R")
    rotorI = Rotor.get_rotor_I("T", "H")
    reflectorB = Reflector.get_reflector_B()
    plugboard = Plugboard()
    plugboard.add_connection("E", "M")
    plugboard.add_connection("U", "G")
    plugboard.add_connection("H", "T")
    plugboard.add_connection("Y", "I")
    plugboard.add_connection("R", "F")
    plugboard.add_connection("A", "J")

    enigma = EnigmaMachine()
    enigma.set_rotors([rotorIII, rotorIV, rotorI])
    enigma.set_reflector(reflectorB)
    enigma.set_plugboard(plugboard)
    decrypted = enigma.encipher(encrypted)
    assert decrypted == "HELLOWORLD"


def test_enigma_machine_handles_lower_case_message():
    rotorI = Rotor.get_rotor_I("A", "A")
    rotorII = Rotor.get_rotor_II("A", "A")
    rotorIII = Rotor.get_rotor_III("A", "A")
    reflectorB = Reflector.get_reflector_B()
    plugboard = Plugboard()

    enigma = EnigmaMachine()
    enigma.set_rotors([rotorI, rotorII, rotorIII])
    enigma.set_reflector(reflectorB)
    enigma.set_plugboard(plugboard)

    encrypted = enigma.encipher("aaaaa")
    assert encrypted == "BDZGO"


def test_enigma_machine_handles_spaces():
    rotorI = Rotor.get_rotor_I("A", "A")
    rotorII = Rotor.get_rotor_II("A", "A")
    rotorIII = Rotor.get_rotor_III("A", "A")
    reflectorB = Reflector.get_reflector_B()
    plugboard = Plugboard()

    enigma = EnigmaMachine()
    enigma.set_rotors([rotorI, rotorII, rotorIII])
    enigma.set_reflector(reflectorB)
    enigma.set_plugboard(plugboard)

    encrypted = enigma.encipher("A A A A A")
    assert encrypted == "BDZGO"


def test_enigma_machine_handles_invalid_characters():
    rotorI = Rotor.get_rotor_I("A", "A")
    rotorII = Rotor.get_rotor_II("A", "A")
    rotorIII = Rotor.get_rotor_III("A", "A")
    reflectorB = Reflector.get_reflector_B()
    plugboard = Plugboard()

    enigma = EnigmaMachine()
    enigma.set_rotors([rotorI, rotorII, rotorIII])
    enigma.set_reflector(reflectorB)
    enigma.set_plugboard(plugboard)

    encrypted = enigma.encipher("AAAAA1")
    assert encrypted == "BDZGO"


def test_enigma_machine_reset():
    rotorI = Rotor.get_rotor_I("A", "A")
    rotorII = Rotor.get_rotor_II("A", "A")
    rotorIII = Rotor.get_rotor_III("A", "A")
    reflectorB = Reflector.get_reflector_B()
    plugboard = Plugboard()

    enigma = EnigmaMachine()
    enigma.set_rotors([rotorI, rotorII, rotorIII])
    enigma.set_reflector(reflectorB)
    enigma.set_plugboard(plugboard)

    encrypted = enigma.encipher("AAAAA")
    assert encrypted == "BDZGO"

    enigma.reset()

    encrypted = enigma.encipher("AAAAA")
    assert encrypted == "BDZGO"
