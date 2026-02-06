import Token
import re


class Lexer:
    KEYWORDS_REGEX = re.compile(r"\b(SELECT|FROM|WHERE|INSERT|INTO|VALUES|UPDATE|SET|DELETE|DROP|TABLE|CREATE|PRIMARY|KEY|FOREIGN|AS|IN|LIKE|RENAME|MERGE)\b", re.IGNORECASE)
    IDENTIFIER_REGEX = re.compile(r"[a-zA-Z_][a-zA-Z0-9_]*")
    OPERATORS_REGEX = re.compile(r"(=|<|>|<=|>=|!=)")
    SYMBOLS_REGEX = re.compile(r"[(),;]")
    WILDCARD_REGEX = re.compile(r"\*")
    VALUE_REGEX = re.compile(r"'[^']*'|\d+(\.\d+)?")

    def tokenize(self, sql_text):
        tokens = []
        line = 1
        words = sql_text.replace(";", " ;").split()

        for i, word in enumerate(words, start=1):
            if self.KEYWORDS_REGEX.fullmatch(word):
                tokens.append(Token.Token("KEYWORD", word.upper(), line, i))
            elif self.OPERATORS_REGEX.fullmatch(word):
                tokens.append(Token.Token("OPERATOR", word, line, i))
            elif self.SYMBOLS_REGEX.fullmatch(word):
                tokens.append(Token.Token("SYMBOL", word, line, i))
            elif self.WILDCARD_REGEX.fullmatch(word):
                tokens.append(Token.Token("WILDCARD", word, line, i))
            elif self.VALUE_REGEX.fullmatch(word):
                tokens.append(Token.Token("VALUE", word, line, i))
            elif self.IDENTIFIER_REGEX.fullmatch(word):
                tokens.append(Token.Token("IDENTIFIER", word, line, i))
            

        tokens.append(Token.Token("EOF", None, line, len(words) + 1))
        return tokens

   
# if __name__ == "__main__":
#     sql="SELECT user FROM table_name WHERE id=5;"
#     lexer = Lexer()
#     for token in lexer.tokenize(sql):
#         print(token)


