# Tugas UAS Teknik Kompilasi - Implementasi Compiler Sederhana

## 📌 Deskripsi
Proyek ini mengimplementasikan compiler sederhana untuk konstruksi **If-Else** yang melalui 4 tahapan utama kompilasi:
1. Analisis Leksikal
2. Analisis Sintaksis
3. Analisis Semantik
4. Generasi Three-Address Code (TAC)

## 🔧 Konstruksi yang Dipilih
**Percabangan/Kondisi (If-Then-Else)**

## 📐 Grammar / BNF
```bnf
<program> ::= <statement>*
<statement> ::= <if_statement> | <assignment>
<if_statement> ::= "if" "(" <condition> ")" <block> "else" <block>
<block> ::= "{" <statement>* "}"
<condition> ::= <identifier> <operator> <value>
<operator> ::= ">" | "<" | "==" | "!=" | ">=" | "<="
<value> ::= <number> | <identifier>
<assignment> ::= <identifier> "=" <value> ";"
<identifier> ::= <letter> (<letter> | <digit>)*
<number> ::= <digit>+

## 🚀 Cara Menjalankan

### Prerequisites
- Python 3.6 atau lebih tinggi

### Menjalankan Program
```bash
python compiler.py
Contoh Input
python
if ( x > 10 ) {
    y = 5;
    z = y + 3;
} else {
    y = 0;
    z = 1;
}
📊 Output Program
1. Analisis Leksikal
Menghasilkan token-token dari source code:

text
TOKEN        | VALUE
KEYWORD      | if
LPAREN       | (
IDENTIFIER   | x
OPERATOR     | >
NUMBER       | 10
RPAREN       | )
LBRACE       | {
IDENTIFIER   | y
OPERATOR     | =
NUMBER       | 5
SEMICOLON    | ;
...
2. Analisis Sintaksis
Membentuk Abstract Syntax Tree (AST):

text
└── If Statement
    └── Condition:
        └── x > 10
    └── Then Body:
        └── y = 5
        └── z = y + 3
    └── Else Body:
        └── y = 0
        └── z = 1
3. Analisis Semantik
Validasi tipe data dan deklarasi variabel:

text
[Semantic] Mendeklarasikan variabel: x
[Semantic] Mendeklarasikan variabel: y
[Semantic] Mendeklarasikan variabel: z
Validasi semantik: ✅ BERHASIL
4. Three-Address Code (TAC)
text
1. if x > 10 goto L1
2. # THEN BLOCK:
3. y = 5
4. t1 = y + 3
5. z = t1
6. goto L2
7. L1:
8. # ELSE BLOCK:
9. y = 0
10. z = 1
11. L2:
🏗️ Struktur Program
text
compiler.py
├── LexicalAnalyzer    # Scanner / Tokenizer
│   └── tokenize()
├── Parser            # Syntax Analyzer
│   └── parse()
├── SemanticAnalyzer  # Semantic Analyzer
│   └── analyze()
├── TACGenerator     # Code Generator
│   └── generate()
└── Compiler         # Main Compiler Class
    └── compile()
💡 Penjelasan Tahapan
1. Analisis Leksikal
Memecah source code menjadi token-token

Menggunakan Regular Expression untuk mengenali pola

Token types: KEYWORD, IDENTIFIER, NUMBER, OPERATOR, LPAREN, RPAREN, etc.

2. Analisis Sintaksis
Memeriksa struktur grammar berdasarkan BNF

Membentuk Abstract Syntax Tree (AST)

Menggunakan metode recursive descent parsing

3. Analisis Semantik
Validasi deklarasi variabel

Pengecekan tipe data (auto-declare dengan tipe int)

Menyimpan informasi dalam symbol table

4. Generasi Three-Address Code
Mengubah AST menjadi kode antara

Menggunakan temporary variables (t1, t2, ...)

Menggunakan labels untuk control flow

📝 Catatan
Program menggunakan pendekatan sederhana untuk memudahkan pemahaman

Implementasi dapat dikembangkan untuk mendukung konstruksi bahasa lainnya
