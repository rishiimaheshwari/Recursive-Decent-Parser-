import tkinter as tk
from tkinter import messagebox

INTEGER = 'INTEGER'
PLUS = 'PLUS'
MINUS = 'MINUS'
MULTIPLY = 'MULTIPLY'
DIVIDE = 'DIVIDE'
LPAREN = 'LPAREN'
RPAREN = 'RPAREN'
EOF = 'EOF'

class Token:
    def __init__(self, type1, value1):
        self.type1 = type1
        self.value1 = value1

class Lexer:
    def __init__(self, t):
        self.text = t
        self.pos = 0
        self.current_char = self.text[self.pos]

    def error(self):
        raise Exception('Invalid character')

    def advance(self):
        self.pos += 1
        if self.pos >= len(self.text):
            self.current_char = None
        else:
            self.current_char = self.text[self.pos]

    def integer(self):
        result = ''
        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char
            self.advance()
        return int(result)

    def get_next_token(self):
        while self.current_char is not None:
            if self.current_char.isspace():
                self.advance()
                continue
            elif self.current_char.isdigit():
                return Token(INTEGER, self.integer())
            elif self.current_char == '+':
                self.advance()
                return Token(PLUS, '+')
            elif self.current_char == '-':
                self.advance()
                return Token(MINUS, '-')
            elif self.current_char == '*':
                self.advance()
                return Token(MULTIPLY, '*')
            elif self.current_char == '/':
                self.advance()
                return Token(DIVIDE, '/')
            elif self.current_char == '(':
                self.advance()
                return Token(LPAREN, '(')
            elif self.current_char == ')':
                self.advance()
                return Token(RPAREN, ')')
            else:
                self.error()
        return Token(EOF, None)

class Parser:
    def __init__(self, lexer, grammar=None):
        self.lexer = lexer
        self.current_token = self.lexer.get_next_token()
        self.grammar = grammar

    def error(self):
        raise Exception('Invalid syntax')

    def eat(self, token_type):
        if self.current_token.type1 == token_type:
            self.current_token = self.lexer.get_next_token()
        else:
            self.error()

    def factor(self):
        token = self.current_token
        if token.type1 == INTEGER:
            self.eat(INTEGER)
            return token.value1
        elif token.type1 == LPAREN:
            self.eat(LPAREN)
            result = self.expr()
            self.eat(RPAREN)
            return result
        else:
            self.error()

    def term(self):
        result = self.factor()
        while self.current_token.type1 in (MULTIPLY, DIVIDE):
            token = self.current_token
            if token.type1 == MULTIPLY:
                self.eat(MULTIPLY)
                result *= self.factor()
            elif token.type1 == DIVIDE:
                self.eat(DIVIDE)
                result /= self.factor()
        return result

    def expr(self):
        result = self.term()
        while self.current_token.type1 in (PLUS, MINUS):
            token = self.current_token
            if token.type1 == PLUS:
                self.eat(PLUS)
                result += self.term()
            elif token.type1 == MINUS:
                self.eat(MINUS)
                result -= self.term()
        return result

    def parse(self):
        if self.grammar:
            # Apply grammar rules if provided
            # Implement your grammar validation logic here
            pass
        else:
            return self.expr()

def validate_input(grammar_text, string_text):
    try:
        lexer = Lexer(string_text)
        if grammar_text:
            # If grammar is provided, pass it to the parser
            parser = Parser(lexer, grammar_text)
        else:
            parser = Parser(lexer)
        result = parser.parse()
        messagebox.showinfo("Result", f"The result of evaluating the expression is: {result}")
    except Exception as e:
        messagebox.showerror("Error", str(e))

def main():
    root = tk.Tk()
    root.title("Arithmetic Expression Evaluator")

    grammar_label = tk.Label(root, text="Enter grammar (Optional):")
    grammar_label.pack()

    grammar_entry = tk.Entry(root, width=50)
    grammar_entry.pack()

    string_label = tk.Label(root, text="Enter arithmetic expression:")
    string_label.pack()

    string_entry = tk.Entry(root, width=50)
    string_entry.pack()

    validate_button = tk.Button(root, text="Validate", command=lambda: validate_input(grammar_entry.get(), string_entry.get()))
    validate_button.pack()

    root.mainloop()

if __name__ == "__main__":
    main()
#5 * 4,  (3 + 2) * 4   (20),   15 / 3  ,