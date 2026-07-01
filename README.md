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
