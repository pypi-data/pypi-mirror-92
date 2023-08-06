"""A test class that can be used to test an Atom object."""

import unittest
from ChemicalFormulaParser.atom import Atom

class AtomTestCase(unittest.TestCase):
    """Tests for 'atom.py'."""

    def setUp(self) -> None:
        """Build an Atom object."""
        self.atom = Atom('H')
    
    def test_get_symbol(self) -> None:
        """Test if getSymbol() works."""
        self.assertEqual(self.atom.getSymbol(), 'H')

    def test_get_number(self) -> None:
        """Test if getNumber() works."""
        self.assertEqual(self.atom.getNumber(), 1)