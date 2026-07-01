import re
from dataclasses import dataclass
from typing import List, Optional, Dict

# ============================================
# 1. ANALISIS LEKSIKAL (Tokenizer)
# ============================================

@dataclass
class Token:
    type: str
    value: str
    line: int
    column: int

class LexicalAnalyzer:
    def __init__(self, source_code: str):
        self.source = source_code
        self.tokens = []
        self.position = 0
        self.line = 1
        self.column = 1
        
        # Definisi token patterns
        self.token_patterns = [
            ('KEYWORD', r'\b(if|else|while|for|int|float|string|bool|true|false|return)\b'),
            ('IDENTIFIER', r'[a-zA-Z_][a-zA-Z0-9_]*'),
            ('NUMBER', r'\d+'),
            ('OPERATOR', r'[+\-*/=<>!]=?'),
            ('COMPARISON', r'[<>]=?|==|!='),
            ('LPAREN', r'\('),
            ('RPAREN', r'\)'),
            ('LBRACE', r'\{'),
            ('RBRACE', r'\}'),
            ('SEMICOLON', r';'),
            ('WHITESPACE', r'\s+'),
            ('COMMENT', r'//.*'),
        ]
        
    def tokenize(self) -> List[Token]:
        while self.position < len(self.source):
            match = None
            remaining = self.source[self.position:]
            
            for token_type, pattern in self.token_patterns:
                regex = re.compile(pattern)
                match = regex.match(remaining)
                if match:
                    value = match.group(0)
                    
                    # Skip whitespace dan comment
                    if token_type not in ['WHITESPACE', 'COMMENT']:
                        token = Token(token_type, value, self.line, self.column)
                        self.tokens.append(token)
                    
                    # Update posisi
                    self.position += len(value)
                    if '\n' in value:
                        self.line += value.count('\n')
                        last_newline = value.rfind('\n')
                        self.column = len(value) - last_newline
                    else:
                        self.column += len(value)
                    break
            
            if not match:
                raise SyntaxError(f"Token tidak dikenal di baris {self.line}, kolom {self.column}")
        
        return self.tokens


# ============================================
# 2. ANALISIS SINTAKSIS (Parser & AST)
# ============================================

@dataclass
class ASTNode:
    pass

@dataclass
class IfNode(ASTNode):
    condition: ASTNode
    then_body: List[ASTNode]
    else_body: Optional[List[ASTNode]]

@dataclass
class BinaryOpNode(ASTNode):
    left: ASTNode
    operator: str
    right: ASTNode

@dataclass
class AssignNode(ASTNode):
    identifier: str
    value: ASTNode

@dataclass
class IdentifierNode(ASTNode):
    name: str

@dataclass
class NumberNode(ASTNode):
    value: int

class Parser:
    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.position = 0
        self.current_token = tokens[0] if tokens else None
    
    def advance(self):
        self.position += 1
        if self.position < len(self.tokens):
            self.current_token = self.tokens[self.position]
        else:
            self.current_token = None
    
    def expect(self, token_type: str, value: Optional[str] = None):
        if not self.current_token:
            raise SyntaxError("Unexpected end of input")
        if self.current_token.type != token_type:
            raise SyntaxError(f"Expected {token_type}, got {self.current_token.type}")
        if value and self.current_token.value != value:
            raise SyntaxError(f"Expected '{value}', got '{self.current_token.value}'")
        token = self.current_token
        self.advance()
        return token
    
    def parse(self) -> List[ASTNode]:
        statements = []
        while self.current_token:
            if self.current_token.value == 'if':
                statements.append(self.parse_if())
            else:
                statements.append(self.parse_assignment())
        return statements
    
    def parse_if(self) -> IfNode:
        self.expect('KEYWORD', 'if')
        self.expect('LPAREN')
        condition = self.parse_expression()
        self.expect('RPAREN')
        then_body = self.parse_block()
        
        else_body = None
        if self.current_token and self.current_token.value == 'else':
            self.expect('KEYWORD', 'else')
            else_body = self.parse_block()
        
        return IfNode(condition, then_body, else_body)
    
    def parse_block(self) -> List[ASTNode]:
        self.expect('LBRACE')
        statements = []
        while self.current_token and self.current_token.type != 'RBRACE':
            if self.current_token.value == 'if':
                statements.append(self.parse_if())
            else:
                statements.append(self.parse_assignment())
        self.expect('RBRACE')
        return statements
    
    def parse_assignment(self) -> AssignNode:
        identifier = self.expect('IDENTIFIER').value
        self.expect('OPERATOR', '=')
        value = self.parse_expression()
        self.expect('SEMICOLON')
        return AssignNode(identifier, value)
    
    def parse_expression(self) -> ASTNode:
        left = self.parse_term()
        
        while self.current_token and self.current_token.type == 'COMPARISON':
            operator = self.current_token.value
            self.advance()
            right = self.parse_term()
            left = BinaryOpNode(left, operator, right)
        
        return left
    
    def parse_term(self) -> ASTNode:
        if self.current_token.type == 'NUMBER':
            value = int(self.current_token.value)
            self.advance()
            return NumberNode(value)
        elif self.current_token.type == 'IDENTIFIER':
            name = self.current_token.value
            self.advance()
            return IdentifierNode(name)
        else:
            raise SyntaxError(f"Unexpected token: {self.current_token}")


# ============================================
# 3. ANALISIS SEMANTIK (Validasi)
# ============================================

class SemanticAnalyzer:
    def __init__(self):
        self.symbol_table = {}
        self.errors = []
    
    def analyze(self, ast: List[ASTNode]) -> bool:
        for node in ast:
            self.visit(node)
        return len(self.errors) == 0
    
    def visit(self, node: ASTNode):
        if isinstance(node, IfNode):
            self.visit_if(node)
        elif isinstance(node, AssignNode):
            self.visit_assign(node)
        elif isinstance(node, BinaryOpNode):
            self.visit_binary(node)
        elif isinstance(node, IdentifierNode):
            self.visit_identifier(node)
        elif isinstance(node, NumberNode):
            pass  # Number selalu valid
    
    def visit_if(self, node: IfNode):
        # Validasi condition
        self.visit(node.condition)
        # Validasi then body
        for stmt in node.then_body:
            self.visit(stmt)
        # Validasi else body
        if node.else_body:
            for stmt in node.else_body:
                self.visit(stmt)
    
    def visit_assign(self, node: AssignNode):
        # Cek apakah variabel sudah dideklarasikan
        if node.identifier not in self.symbol_table:
            self.symbol_table[node.identifier] = 'int'  # Auto-declare dengan tipe int
            print(f"  [Semantic] Mendeklarasikan variabel: {node.identifier}")
        
        # Validasi nilai yang diassign
        self.visit(node.value)
    
    def visit_binary(self, node: BinaryOpNode):
        self.visit(node.left)
        self.visit(node.right)
    
    def visit_identifier(self, node: IdentifierNode):
        if node.name not in self.symbol_table:
            self.errors.append(f"Variabel '{node.name}' belum dideklarasikan")
            print(f"  [Error] Variabel '{node.name}' belum dideklarasikan!")


# ============================================
# 4. GENERASI THREE-ADDRESS CODE (TAC)
# ============================================

class TACGenerator:
    def __init__(self):
        self.temp_counter = 0
        self.label_counter = 0
        self.tac_code = []
        self.symbol_table = {}
    
    def new_temp(self) -> str:
        self.temp_counter += 1
        return f"t{self.temp_counter}"
    
    def new_label(self) -> str:
        self.label_counter += 1
        return f"L{self.label_counter}"
    
    def generate(self, ast: List[ASTNode]) -> List[str]:
        for node in ast:
            self.visit(node)
        return self.tac_code
    
    def visit(self, node: ASTNode):
        if isinstance(node, IfNode):
            self.visit_if(node)
        elif isinstance(node, AssignNode):
            self.visit_assign(node)
        elif isinstance(node, BinaryOpNode):
            return self.visit_binary(node)
        elif isinstance(node, IdentifierNode):
            return node.name
        elif isinstance(node, NumberNode):
            return str(node.value)
    
    def visit_if(self, node: IfNode):
        # Evaluasi kondisi
        cond_left = self.visit(node.condition.left)
        cond_op = node.condition.operator
        cond_right = self.visit(node.condition.right)
        
        # Labels
        else_label = self.new_label()
        end_label = self.new_label()
        
        # Generate condition check
        self.tac_code.append(f"if {cond_left} {cond_op} {cond_right} goto {else_label}")
        
        # Then body
        self.tac_code.append(f"# THEN BLOCK:")
        for stmt in node.then_body:
            self.visit(stmt)
        self.tac_code.append(f"goto {end_label}")
        
        # Else body
        self.tac_code.append(f"{else_label}:")
        self.tac_code.append(f"# ELSE BLOCK:")
        if node.else_body:
            for stmt in node.else_body:
                self.visit(stmt)
        
        # End label
        self.tac_code.append(f"{end_label}:")
    
    def visit_assign(self, node: AssignNode):
        result = self.visit(node.value)
        self.tac_code.append(f"{node.identifier} = {result}")
    
    def visit_binary(self, node: BinaryOpNode):
        left = self.visit(node.left)
        right = self.visit(node.right)
        temp = self.new_temp()
        self.tac_code.append(f"{temp} = {left} {node.operator} {right}")
        return temp


# ============================================
# 5. MAIN COMPILER
# ============================================

class Compiler:
    def __init__(self, source_code: str):
        self.source = source_code
        self.tokens = []
        self.ast = []
        self.tac = []
        self.semantic_errors = []
    
    def compile(self):
        print("=" * 60)
        print("PROSES KOMPILASI")
        print("=" * 60)
        
        # STEP 1: Lexical Analysis
        print("\n[1] ANALISIS LEKSIKAL")
        print("-" * 40)
        lexer = LexicalAnalyzer(self.source)
        self.tokens = lexer.tokenize()
        print(f"Total token: {len(self.tokens)}")
        for token in self.tokens[:15]:  # Tampilkan 15 token pertama
            print(f"  {token.type:12} | '{token.value}'")
        
        # STEP 2: Syntax Analysis
        print("\n[2] ANALISIS SINTAKSIS")
        print("-" * 40)
        parser = Parser(self.tokens)
        self.ast = parser.parse()
        print(f"AST berhasil dibuat")
        self.print_ast(self.ast, 0)
        
        # STEP 3: Semantic Analysis
        print("\n[3] ANALISIS SEMANTIK")
        print("-" * 40)
        semantic = SemanticAnalyzer()
        is_valid = semantic.analyze(self.ast)
        print(f"Validasi semantik: {'✅ BERHASIL' if is_valid else '❌ GAGAL'}")
        if semantic.errors:
            for err in semantic.errors:
                print(f"  Error: {err}")
        self.semantic_errors = semantic.errors
        
        # STEP 4: TAC Generation
        print("\n[4] GENERASI THREE-ADDRESS CODE")
        print("-" * 40)
        tac_gen = TACGenerator()
        self.tac = tac_gen.generate(self.ast)
        print("Three-Address Code:")
        for i, code in enumerate(self.tac, 1):
            print(f"  {i:3}. {code}")
        
        print("\n" + "=" * 60)
        return self.tac
    
    def print_ast(self, nodes: List[ASTNode], indent: int):
        for node in nodes:
            if isinstance(node, IfNode):
                print(f"{'  ' * indent}└── If Statement")
                print(f"{'  ' * (indent+1)}└── Condition:")
                self.print_ast([node.condition], indent+2)
                print(f"{'  ' * (indent+1)}└── Then Body:")
                self.print_ast(node.then_body, indent+2)
                if node.else_body:
                    print(f"{'  ' * (indent+1)}└── Else Body:")
                    self.print_ast(node.else_body, indent+2)
            elif isinstance(node, AssignNode):
                print(f"{'  ' * indent}└── {node.identifier} = ", end="")
                self.print_ast([node.value], indent)
            elif isinstance(node, BinaryOpNode):
                print(f"{'  ' * indent}└── {node.left} {node.operator} {node.right}")
            elif isinstance(node, IdentifierNode):
                print(f"{node.name}")
            elif isinstance(node, NumberNode):
                print(f"{node.value}")


# ============================================
# 6. MAIN PROGRAM
# ============================================

if __name__ == "__main__":
    # Contoh source code dengan berbagai konstruksi
    source_code = """
    if ( x > 10 ) {
        y = 5;
        z = y + 3;
    } else {
        y = 0;
        z = 1;
    }
    """
    
    # Buat compiler
    compiler = Compiler(source_code)
    
    # Jalankan kompilasi
    tac_result = compiler.compile()
    
    # Tampilkan hasil akhir
    print("\n📋 HASIL AKHIR TAC:")
    print("-" * 40)
    for code in tac_result:
        print(f"  {code}")
