class Parser:
    def __init__(self, tokens): 
        self.tokens = tokens 
        self.pos = 0

    def current_token(self): 
        return self.tokens[self.pos]
    
    def advance(self): 
        self.pos += 1

    def parse(self): 
        token = self.current_token() 
        if token.type == "KEYWORD": 
            kw = token.value.upper() 
        if kw == "SELECT": 
            return self.parse_select() 
        elif kw == "INSERT": 
            return self.parse_insert() 
        elif kw == "UPDATE": 
            return self.parse_update() 
        elif kw == "DELETE":
             return self.parse_delete() 
        raise Exception(f"Syntax Error: Unknown start of query at {token.line}:{token.column}")