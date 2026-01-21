# src/module.py

class Module:
    """
    Represents a university module with its code, name, credits, and level.
    Stores static module info required for calculations.
    """
    
    def __init__(self, code, name):
        """
        initializes module with code and name
        also extracts credits and level from the module code
        """
        self.code = code
        self.name = name
        
        # extract credits and level directly from the module code
        self.credits = self._extract_credits(code)
        self.level = self._extract_level(code)
    
    def _extract_credits(self, code):
        """
        Extract the credit value from the module code.
        Format: UFCFHS-30-1 → 30 credits
        """
        parts = code.split('-')
        if len(parts) >= 2:
            return int(parts[1])
        return 0
    
    def _extract_level(self, code):
        """
        Extract the level from the module code.
        Format: UFCFHS-30-1 → Level 1 (last digit)
        """
        parts = code.split('-')
        if len(parts) >= 3:
            return int(parts[2])
        return 0
    
    def __str__(self):
        # formatted string used when printing module objects
        return f"{self.code}: {self.name} ({self.credits} credits, level {self.level})"
