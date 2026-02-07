from Lexer import Lexer
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
        """Parse the SQL query starting from the first token."""
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

    #---------------------
    # Parser for SELECT
    #---------------------
    def parse_select(self):
        """Parse a SELECT statement."""
        # SELECT id, name FROM employees WHERE age > 30;
        select_list = []
        self.advance()

        while True:
            token = self.current_token()
            if token.type == "WILDCARD":
                select_list.append(ASTNode("WILDCARD", token.value)) 
                self.advance()
            elif token.type == "IDENTIFIER": 
                select_list.append(ASTNode("COLUMN", token.value)) 
                self.advance()
            elif token.type == "KEYWORD": 
                raise Exception(f"Syntax Error: Reserved keyword '{token.value}' cannot be used as a column name.\nAt line {token.line}, column {token.column} ")    
            else: 
                break 
            if self.current_token().type == "SYMBOL" and self.current_token().value == ",": 
                self.advance() 
                continue 
            else: 
                break

        if self.current_token().value.upper() != "FROM": 
            raise Exception(f"Syntax Error: Expected FROM..\nAt line {self.current_token().line}, column {self.current_token().column} ") 
        self.advance()

        table = self.current_token()
        #---------------------
        # nested query parsing
        #---------------------
        if table.type == "SYMBOL" and table.value == "(":
            self.advance()
            subquery = self.parse()  
            if self.current_token().value != ")":
                raise Exception(f"Syntax Error: Expected closing ) for subquery..\nAt line {self.current_token().line}, column {self.current_token().column}")
            self.advance()

            children = [ASTNode("SELECT_LIST", children=select_list),
                        ASTNode("SUBQUERY", children=[subquery])]  
        else:
            if table.type == "KEYWORD":
                raise Exception(f"Syntax Error: Reserved keyword '{table.value}' cannot be used as a table name.\nAt line {table.line}, column {table.column} ")
            if table.type != "IDENTIFIER":
                raise Exception(f"Syntax Error: Expected table name.\nAt line {table.line}, column {table.column} ")
            self.advance()

            children = [ASTNode("SELECT_LIST", children=select_list),
                        ASTNode("TABLE", table.value)]
            
        if self.current_token().type == "KEYWORD" and self.current_token().value.upper() == "WHERE":
            self.advance()
            condition = self.parse_condition()
            children.append(ASTNode("WHERE", children=[condition]))
        return ASTNode("SELECT_STMT", children=children)
    
    #---------------------    
    #Parser for Conditions
    #---------------------
    def parse_condition(self):
        """Parse the WHERE condition"""

        left = self.current_token()
        if left.type == "KEYWORD":
            raise Exception(f"Syntax Error: Reserved keyword '{left.value}' cannot be used as a column in condition.\nAt line {left.line}, column {left.column} ")
        if left.type != "IDENTIFIER":
            raise Exception(f"Syntax Error: Expected column in condition.\nAt line {left.line}, column {left.column} ")
        self.advance()

        op = self.current_token()
        if op.type is None or op.type != "OPERATOR":
            raise Exception(f"Syntax Error: Expected operator in condition.\nAt line {op.line}, column {op.column} ")
        self.advance()

        right = self.current_token()
        if right.type == "VALUE":
            self.advance()
            return ASTNode("CONDITION", children=[
                ASTNode("COLUMN", left.value),
                ASTNode("OPERATOR", op.value),
                ASTNode("VALUE", right.value)
            ])
        
        #---------------------
        # Nested subquery in condition where id=(...)
        #---------------------
        elif right.type == "SYMBOL" and right.value == "(":
            
            self.advance()
            subquery = self.parse()
            if self.current_token().value != ")":
                raise Exception(f"Syntax Error: Expected closing ) for subquery in condition.\nAt line {self.current_token().line}, column {self.current_token().column} ")
            self.advance()
            return ASTNode("CONDITION", children=[
                ASTNode("COLUMN", left.value),
                ASTNode("OPERATOR", op.value),
                ASTNode("SUBQUERY", children=[subquery])
            ])
        
        else:
            raise Exception(f"Syntax Error: Expected value or subquery in condition..\nAt line {self.current_token().line}, column {self.current_token().column} ")
    
    #---------------------
    #Parser for insert
    #---------------------
    def parse_insert(self):
        """Parse the INSERT condition"""
        #INSERT INTO users VALUES (1, 'name', 30);
        if self.current_token().value.upper() != "INSERT":
            raise Exception(f"Syntax Error: Expected INSERT.\nAt line {self.current_token().line}, column {self.current_token().column}")
        self.advance()

        if self.current_token().value.upper() != "INTO":
            raise Exception(f"Syntax Error: Expected INTO.\nAt line {self.current_token().line}, column {self.current_token().column}")
        self.advance()

        table = self.current_token()
        if table.type != "IDENTIFIER":
            raise Exception(f"Syntax Error: Expected table name..\nAt line {self.current_token().line}, column {self.current_token().column}")
        self.advance()
         
        if self.current_token().value.upper() == "VALUES":
            self.advance() 
            #For Parsing single/multiple values (a,b,c)
            if self.current_token().value != "(": 
                raise Exception(f"Syntax Error: Expected (.\nAt line {self.current_token().line}, column {self.current_token().column}") 
            self.advance() 
            values = [] 
            while True: 
                val = self.current_token() 
                if val.type != "VALUE": 
                    raise Exception(f"Syntax Error: Expected value.\nAt line {val.line}, column {val.column}") 
                values.append(ASTNode("VALUE", val.value)) 
                self.advance() 
                if self.current_token().value == ",": 
                    self.advance() 
                    continue 
                elif self.current_token().value == ")": 
                    self.advance() 
                    break 
                else: 
                    raise Exception(f"Syntax Error: Expected , or ).\nAt line {self.current_token().line}, column {self.current_token().column}") 
            return ASTNode("INSERT_STMT", children=[ ASTNode("TABLE", table.value), ASTNode("VALUES", children=values) ]) 
        else: 
            raise Exception(f"Syntax Error: Expected VALUES.\nAt line {self.current_token().line}, column {self.current_token().column}")

    #---------------------  
    #Parser for update
    #---------------------
    def parse_update(self):
        """Parse UPDATE query"""
        #UPDATE users SET age = 31 WHERE name = 'name';
        if self.current_token().value.upper()!="UPDATE":
            raise Exception(f"Syntax Error: Expected UPDATE.\nAt line {self.current_token().line}, column {self.current_token().column} ")
        self.advance()

        table = self.current_token() 
        if table.type != "IDENTIFIER": 
            raise Exception(f"Syntax Error: Expected table name.\nAt line {table.line}, column {table.column}") 
        self.advance()
         
        if self.current_token().value.upper() != "SET":
            raise Exception(f"Syntax Error: Expected SET.\nAt line {self.current_token().line}, column {self.current_token().column}")
        self.advance()

        col = self.current_token()
        if col.type != "IDENTIFIER":
            raise Exception(f"Syntax Error: Expected column name.\nAt line {col.line}, column {col.column}")
        self.advance()

        op = self.current_token()
        if op.type != "OPERATOR":
            raise Exception(f"Syntax Error: Expected operator.\nAt line {op.line}, column {op.column}")
        self.advance()

        val = self.current_token()
        if val.type == "VALUE": 
            self.advance() 
            assign_node = ASTNode("ASSIGNMENT", children=[
                 ASTNode("COLUMN", col.value), 
                 ASTNode("VALUE", val.value) ])
        #---------------------
        #nested query
        #---------------------
        elif val.type == "SYMBOL" and val.value == "(": 
            self.advance() 
            subquery = self.parse() 
            if self.current_token().value != ")":
                 raise Exception(f"Syntax Error: Expected closing ) for subquery in UPDATE.\nAt line {self.current_token().line}, column {self.current_token().column}")
            self.advance() 
            assign_node = ASTNode("ASSIGNMENT", children=[ 
                ASTNode("COLUMN", col.value), 
                ASTNode("SUBQUERY", children=[subquery]) ]) 
        else: 
            raise Exception(f"Syntax Error: Expected value or subquery in UPDATE.\nAt line {self.current_token().line}, column {self.current_token().column}")
        
        return ASTNode("UPDATE_STMT", children=[ ASTNode("TABLE", table.value), assign_node ])
    
    #---------------------
    #Parser for delete
    #---------------------
    def parse_delete(self):
        """Parse DELETE query"""
        #DELETE FROM users WHERE age > 30;
        if self.current_token().value.upper()!="DELETE":
            raise Exception(f"Syntax Error: DELETE.\nAt line {self.current_token().line}, column {self.current_token().column}")
        self.advance()

        if self.current_token().value.upper()!="FROM":
            raise Exception(f"Syntax Error: Expected FROM after DELETE.\nAt line {self.current_token().line}, column {self.current_token().column}")
        self.advance()

        table = self.current_token()
        if table.type != "IDENTIFIER": 
            raise Exception(f"Syntax Error: Expected table name.\nAt line {table.line}, column {table.column}") 
        self.advance()
        children = [ASTNode("TABLE", table.value)]

        if self.current_token().type == "SYMBOL" and self.current_token().value == ",":
            raise Exception(f"Syntax Error: Multiple tables not allowed in DELETE.\nAt line {self.current_token().line}, column {self.current_token().column}")
        
        if self.current_token().type == "KEYWORD" and self.current_token().value.upper() == "WHERE": 
            self.advance() 
            condition = self.parse_condition() 
            children.append(ASTNode("WHERE", children=[condition])) 
            
        return ASTNode("DELETE_STMT", children=children)


if __name__ == "__main__": 
        try:
            lexer = Lexer() 
            sql = "DELETE FROM users WHERE id = 5"
            tokens = lexer.tokenize(sql) 
            parser = Parser(tokens) 
            ast = parser.parse() 
            print(ast)
        except Exception as e:
            print(e)