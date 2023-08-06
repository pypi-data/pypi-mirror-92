"""A class that can be used to represent an atom."""

class Atom:
    """
    A simple attempt to represent an atom.

    Attributes
    ----------
    number : int, optional
        The number of atoms. Default is equal to 1.
    symbol : str
        The chemical symbol of the atom.
    
    Methods
    ----------
    getSymbol():
        Return the atom symbol.
    getNumber():
        Return the atom number.
    """
    
    def __init__(self, symbol="", number: int = 1) -> None:
        """Initialize the atom's attributes."""
        self.symbol = symbol
        self.number = number
    
    def getSymbol(self) -> str:
        """Return the atom symbol."""
        return self.symbol

    def getNumber(self) -> int:
        """Return the atom number."""
        return self.number