"""A class that can be used to represent a molecule."""

from ChemicalFormulaParser.atom import Atom

class Molecule:
    """
    A simple attempt to represent a molecule.

    Attributes
    ----------
    number : int, optional
        The number of molecules. Default is equal to 1.
    atoms : list, optional
        list of atoms that make the molecule.
    submolecules : list, optional
        list of submolecules that make the molecule.
    
    Methods
    ----------
    addAtom(atom: Atom):
        Add an Atom object to the molecule.
    addSubmolecule(submolecule: Molecule):
        Add a submolecule (of type Molecule) to the list of submolecules.
    getAtoms():
        Return the molecule atoms.
    getAtomsAsDict():
        Return a dictionary of the atoms that make the molecule.
    """

    def __init__(self, number: int = 1, atoms=None, submolecules=None) -> None:
        """
        Initialize the molecule's attributes.
        
        Parameters
        ----------
        number : int, optional
            The number of molecules. Default is equal to 1.
        atoms : list, optional
            list of atoms that make the molecule.
        submolecules : list, optional
            list of submolecules that make the molecule.
        """
        if atoms is not None:
            self.atoms = atoms
        else:
            self.atoms = []
        if submolecules is not None:
            self.submolecules = submolecules
        else:
            self.submolecules = []
        self.number = number
    
    def addAtom(self, atom: Atom) -> None:
        """
        Add an Atom object to the molecule.
        
        Parameters
        ----------
        atom : Atom
            The atom to be added to the attribute atoms
        """
        self.atoms.append(atom)
    
    def addSubmolecule(self, submolecule) -> None:
        """
        Add a submolecule (of type Molecule) to the list of submolecules.
        
        Parameters
        ----------
        submolecule : Molecule
            The submolecule to be added to the attribute submolecules
        """
        self.submolecules.append(submolecule)
    
    def getAtoms(self) -> list:
        """
        Return the molecule attribute atoms.
        """
        return self.atoms
    
    def getAtomsAsDict(self) -> dict:
        """
        Return a dictionary of the atoms that make the molecule.

        Keys : str
            the atom symbols, e.g. 'H'.
        Values : int
            the corresponding atom number, e.g. 1.
        """
        res = {}
        for atom in self.atoms:
            if atom.symbol in res:
                res[atom.symbol] += self.number * atom.number
            else:
                res[atom.symbol] = self.number * atom.number
        
        for submolecule in self.submolecules:
            for symbol, number in submolecule.getAtomsAsDict().items():
                if symbol in res:
                    res[symbol] += number * self.number
                else:
                    res[symbol] = number * self.number
        return res
