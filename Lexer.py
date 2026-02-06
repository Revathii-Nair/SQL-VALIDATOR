from Token import *
import re


class Lexer:
    KEYWORDS_REGEX = re.compile(r"\b(SELECT|FROM|WHERE|INSERT|INTO|VALUES|UPDATE|SET|DELETE|DROP|TABLE|CREATE|PRIMARY|KEY|FOREIGN|AS|IN|LIKE|RENAME|MERGE)\b", re.IGNORECASE)
    IDENTIFIER_REGEX = re.compile(r"[a-zA-Z_][a-zA-Z0-9_]*")
    OPERATORS_REGEX = re.compile(r"(=|<|>|<=|>=|!=)")
    SYMBOLS_REGEX = re.compile(r"[(),;]")
    WILDCARD_REGEX = re.compile(r"\*")
    VALUE_REGEX = re.compile(r"'[^']*'|\d+(\.\d+)?")

    def split_tokens(self, text):
        parts, i, multi_ops = [], 0, {"<=", ">=", "!="}
        while i < len(text):
            if i+1 < len(text) and text[i:i+2] in multi_ops:
                parts.append(text[i:i+2]); i += 2; 
                continue
            if text[i] in "=<>!(),;*":
                parts.append(text[i]); i += 1; 
                continue
            buf = ""
            while i < len(text) and text[i] not in "=<>!(),;*":
                buf += text[i]; i += 1
            if buf: parts.append(buf)
        return parts


    def tokenize(self, sql_text):
        tokens = []
        line = 1
        words = sql_text.replace(";", " ;").split()

        
    
        for i, word in enumerate(words, start=1):
            subwords = self.split_tokens(word)
            for sub in subwords:
                if self.KEYWORDS_REGEX.fullmatch(sub):
                    tokens.append(Token("KEYWORD", sub.upper(), line, i))
                elif self.OPERATORS_REGEX.fullmatch(sub):
                    tokens.append(Token("OPERATOR", sub, line, i))
                elif self.SYMBOLS_REGEX.fullmatch(sub):
                    tokens.append(Token("SYMBOL", sub, line, i))
                elif self.WILDCARD_REGEX.fullmatch(sub):
                    tokens.append(Token("WILDCARD", sub, line, i))
                elif self.VALUE_REGEX.fullmatch(sub):
                    tokens.append(Token("VALUE", sub, line, i))
                elif self.IDENTIFIER_REGEX.fullmatch(sub):
                    tokens.append(Token("IDENTIFIER", sub, line, i))

            

        tokens.append(Token("EOF", None, line, len(words) + 1))
        return tokens

   
if __name__ == "__main__":
    sql="SELECT user FROM table_name WHERE id=5;"
    lexer = Lexer()
    for token in lexer.tokenize(sql):
        print(token)


