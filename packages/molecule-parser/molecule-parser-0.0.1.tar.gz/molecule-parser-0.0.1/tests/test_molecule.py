"""A test class that can be used to test a Molecule object."""

import unittest
from ChemicalFormulaParser.atom import Atom
from ChemicalFormulaParser.molecule import Molecule

class MoleculeTestCase(unittest.TestCase):
    """Tests for 'molecule.py'."""
    
    def setUp(self) -> None:
        """Build a Molecule object. E.g. 3(H20)."""
        self.molecule = Molecule(3, [Atom('H', 2), Atom('O')])

    def test_get_atoms(self) -> None:
        """Test if getAtoms() works."""
        self.assertEqual(self.molecule.getAtomsAsDict(), {'H': 6, 'O': 3})

    def test_add_atom(self) -> None:
        """Test if addAtom() works."""
        self.molecule.addAtom(Atom('C'))
        self.assertEqual(self.molecule.getAtomsAsDict(), {'H': 6, 'O': 3, 'C': 3})