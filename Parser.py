from Lexer import *
from ASTNode import *

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


    # Parser for SELECT
    def parse_select(self):
        select_list = []
        if self.current_token().value.upper() != "SELECT": 
            raise Exception("Syntax Error: Expected SELECT.\nAt line {token.line}, column {token.column} ") 
        self.advance()

        while True:
            token = self.current_token()

            if token.type == "WILDCARD":
                select_list.append(ASTNode("WILDCARD", token.value)) 
                self.advance()
            elif token.type == "IDENTIFIER": 
                select_list.append(ASTNode("COLUMN", token.value)) 
                self.advance()
            elif token.type == "KEYWORD": # Explicitly catch reserved keyword misuse 
                raise Exception(f"Syntax Error: Reserved keyword '{token.value}' cannot be used as a column name.\nAt line {token.line}, column {token.column} ")    
            else: 
                break 
            if self.current_token().type == "SYMBOL" and self.current_token().value == ",": 
                self.advance() 
                continue 
            else: 
                break

        if self.current_token().value.upper() != "FROM": 
            raise Exception(f"Syntax Error: Expected FROM.\nAt line {token.line}, column {token.column} ") 
        self.advance()

        table = self.current_token()
        # nested query parsing
        if table.type == "SYMBOL" and table.value == "(":
            self.advance()
            subquery = self.parse()  
            if self.current_token().value != ")":
                raise Exception(f"Syntax Error: Expected closing ) for subquery.\nAt line {token.line}, column {token.column} ")
            self.advance()

            children = [ASTNode("SELECT_LIST", children=select_list),
                        ASTNode("SUBQUERY", children=[subquery])]
            
        else:
            if table.type == "KEYWORD":
                raise Exception(f"Syntax Error: Reserved keyword '{table.value}' cannot be used as a table name.\nAt line {token.line}, column {token.column} ")
            if table.type != "IDENTIFIER":
                raise Exception(f"Syntax Error: Expected table name.\nAt line {token.line}, column {token.column} ")
            self.advance()

            children = [ASTNode("SELECT_LIST", children=select_list),
                        ASTNode("TABLE", table.value)]
            
        if self.current_token().type == "KEYWORD" and self.current_token().value.upper() == "WHERE":
            self.advance()
            condition = self.parse_condition()
            children.append(ASTNode("WHERE", children=[condition]))
        return ASTNode("SELECT_STMT", children=children)
    

    #Parser for Conditions
    def parse_condition(self):
        left = self.current_token()
        if left.type == "KEYWORD":
            raise Exception(f"Syntax Error: Reserved keyword '{left.value}' cannot be used as a column in condition.\nAt line {token.line}, column {token.column} ")
        if left.type != "IDENTIFIER":
            raise Exception(f"Syntax Error: Expected column in condition.\nAt line {token.line}, column {token.column} ")
        self.advance()

        op = self.current_token()
        if op.type != "OPERATOR":
            raise Exception(f"Syntax Error: Expected operator in condition.\nAt line {token.line}, column {token.column} ")
        self.advance()

        right = self.current_token()
        if right.type == "VALUE":
            self.advance()
            return ASTNode("CONDITION", children=[
                ASTNode("COLUMN", left.value),
                ASTNode("OPERATOR", op.value),
                ASTNode("VALUE", right.value)
            ])
        
        elif right.type == "SYMBOL" and right.value == "(":
            # Nested subquery in condition
            self.advance()
            subquery = self.parse()
            if self.current_token().value != ")":
                raise Exception(f"Syntax Error: Expected closing ) for subquery in condition.\nAt line {token.line}, column {token.column} ")
            self.advance()
            return ASTNode("CONDITION", children=[
                ASTNode("COLUMN", left.value),
                ASTNode("OPERATOR", op.value),
                ASTNode("SUBQUERY", children=[subquery])
            ])
        
        else:
            raise Exception(f"Syntax Error: Expected value or subquery in condition.\nAt line {token.line}, column {token.column} ")
    
    #Parser for insert
    def parse_insert(self):
        pass

    #Parser for update
    def parse_update():
        pass
    
    #Parser for delete
    def parse_delete():
        pass

    


if __name__ == "__main__": 
    try:
        lexer = Lexer() 
        sql = "SELECT  name, age FROM users WHERE age=(select user from table1);" 
        tokens = lexer.tokenize(sql) 
        parser = Parser(tokens) 
        ast = parser.parse() 
        print(ast)
    except Exception as e:
        print(e)