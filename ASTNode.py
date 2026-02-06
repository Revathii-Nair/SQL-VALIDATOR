class ASTNode:
    def __init__(self, type_, value=None, children=None): 
        self.type = type_
        self.value = value
        self.children = children if children else [] 
        
    def __repr__(self): 
        return f"ASTNode({self.type}, {self.value}, children={self.children})"



