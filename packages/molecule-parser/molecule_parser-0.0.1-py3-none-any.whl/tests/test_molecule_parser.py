"""A test class that can be used to test MoleculeParser object."""

import unittest
from ChemicalFormulaParser.molecule_parser import MoleculeParser

class MoleculeParserTestCase(unittest.TestCase):
    """Tests for 'molecule_parser.py'."""

    def setUp(self) -> None:
        """Build a MoleculeParser object."""
        self.mp = MoleculeParser()

    def test_are_brackets_ok(self) -> None:
        """Test if areBracketsOk() works."""
        self.assertEqual(self.mp.areBracketsOk('()'), True)
        self.assertEqual(self.mp.areBracketsOk("(CH3)(NH4)2ON3(CO2)"), True)
        self.assertEqual(self.mp.areBracketsOk('()('), False)
        self.assertEqual(self.mp.areBracketsOk('{}'), True)
        self.assertEqual(self.mp.areBracketsOk('}{'), False)
        self.assertEqual(self.mp.areBracketsOk('][]'), False)
        self.assertEqual(self.mp.areBracketsOk("(NH4)2HPO4("), False)
    
    def test_has_special_characters(self) -> None:
        """Test if hasSpecialCharacters() works."""
        self.assertEqual(self.mp.hasSpecialCharacters('HelloWorld!'), (True, [10]))
        self.assertEqual(self.mp.hasSpecialCharacters("\\"), (True, [0]))
        self.assertEqual(self.mp.hasSpecialCharacters('#'), (True, [0]))
        self.assertEqual(self.mp.hasSpecialCharacters("H2O'"), (True, [3]))
        self.assertEqual(self.mp.hasSpecialCharacters(' 3(H2O)'), (True, [0]))
        self.assertEqual(self.mp.hasSpecialCharacters('3(H2O) '), (True, [6]))
        self.assertEqual(self.mp.hasSpecialCharacters('3(H2O)'), (False, []))

    def test_has_empty_brackets(self) -> None:
        """Test if hasEmptyBrackets() works."""
        self.assertEqual(self.mp.hasEmptyBrackets('HelloWorld()!'), True)
        self.assertEqual(self.mp.hasEmptyBrackets('3(H2O)'), False)
        self.assertEqual(self.mp.hasEmptyBrackets("(NH4)2HPO4"), False)
        self.assertEqual(self.mp.hasEmptyBrackets("()NH4)2HPO4"), True)
        self.assertEqual(self.mp.hasEmptyBrackets("(NH4{)2HPO4"), True)
        self.assertEqual(self.mp.hasEmptyBrackets("(NH4[)2HPO4"), True)

    def test_has_letters(self) -> None:
        """Test if hasLetters() works."""
        self.assertEqual(self.mp.hasLetters("HelloWorld!"), True)
        self.assertEqual(self.mp.hasLetters("(2)"), False)
        self.assertEqual(self.mp.hasLetters("()"), False)
        self.assertEqual(self.mp.hasLetters("c"), True)
    
    def test_parse(self) -> None:
        """Test if parse() works."""
        # molecular formulas without any brackets
        formulas = {
            "C": {'C': 1},
            "HO": {'H': 1, 'O': 1},
            "H2O": {'H': 2, 'O': 1},
            "3H2O": {'H': 6, 'O': 3},
            "Fe2O3": {'Fe': 2, 'O': 3},
            "COOH": {'C': 1, 'O': 2, 'H': 1}
        }
        for formula, res in formulas.items():
            self.assertDictEqual(res, self.mp.parse(formula), "Issue with formula: {}.".format(formula))
        
        # molecular formulas with linear brackets (not nested)
        formulas = {
            "(C)": {'C': 1},
            "3(H2O)": {'H': 6, 'O': 3},
            "(H2O)3": {'H': 6, 'O': 3},
            "Al2(SO4)3": {'Al': 2, 'S': 3, 'O': 12},
            "(NH4)2SO4": {'S': 1, 'O': 4, 'N': 2, 'H': 8},
            "(NH4)2HPO4": {'H': 9, 'P': 1, 'O': 4, 'N': 2},
            "CH3(CH2)6CH3": {'C': 8, 'H': 18},
            "CH3C(O)CH2CH3": {'C': 4, 'H': 8, 'O': 1},
            "8Fe(H2O)4(OH)2": {'Fe': 8, 'H': 80, 'O': 48}
        }
        for formula, res in formulas.items():
            self.assertDictEqual(res, self.mp.parse(formula), "Issue with formula: {}.".format(formula))

        # molecular formulas with nested brackets
        formulas = {
            "[{(C)}]": {'C': 1},
            "((Fe3))": {'Fe': 3},
            "((Fe3))8": {'Fe': 24},
            "8((Fe3))": {'Fe': 24},
            "((O2)3)4": {'O': 24},
            "4((O2)3)": {'O': 24},
            "(Fe(NH4)(SO4)3){CO2}2": {'Fe': 1, 'N': 1, 'H': 4, 'S': 3, 'O': 16, 'C': 2},
            "Mg2[CH4{NNi2(Li2O4)5}14]3": {'Mg': 2, 'C': 3, 'H': 12, 'N': 42, 'Ni': 84, 'Li': 420, 'O': 840}
        }
        for formula, res in formulas.items():
            self.assertDictEqual(res, self.mp.parse(formula), "Issue with formula: {}.".format(formula))

    def test_parse_exceptions(self) -> None:
        """Test if parse() raises the correct exceptions."""
        formulas = {
            "H2O!": "Special(s) character(s) ['!'] at index(es) [3].",
            "H2O!!!": "Special(s) character(s) ['!', '!', '!'] at index(es) [3, 4, 5].",
            "": "The molecular formula is empty!",
            "111": "No letter in molecular formula!",
            "(H2O)(": "Missing brackets in molecular formula!",
            "()H2O": "Empty brackets in molecular formula!",
        }
        for formula, error_message in formulas.items():
            with self.assertRaises(Exception) as context:
                self.mp.parse(formula)
            self.assertTrue(error_message in str(context.exception), "Unexpected exception message '{}', excepted '{}'".format(str(context.exception), error_message))

if __name__ == "__main__":
    unittest.main()

