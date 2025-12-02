Projeto A3 — Calculadora Científica de Números Complexos

Disciplina: Estrutura de Dados e Análise de Algoritmos
Professor: Wellington Lacerda Silveira da Silva

Integrantes

Breno Dantas Oliveira Filho — RA: 1272417582

Ramon Queiroz G. Pinto — RA: 12724126768

Adrian Ferreira Andrade — RA: 12724133589

Descrição do Projeto

Esta calculadora científica foi inteiramente desenvolvida sem o uso de bibliotecas matemáticas prontas como math ou cmath.
Todas as operações são implementadas manualmente, incluindo:

Séries de Taylor

Fórmulas de Euler

Trigonometria hiperbolica

Aproximações iterativas

Aritmética completa com números complexos

Sistema de parsing com geração de árvore sintática (AST)

A calculadora é capaz de interpretar expressões matemáticas completas com números reais, complexos, funções científicas e constantes criadas pelo usuário.

Funcionalidades
Operações básicas

Soma: +

Subtração: -

Multiplicação: *

Divisão: /

Potência: **

Raiz quadrada complexa: raiz(x)

Conjugado: conj(x)

Funções científicas

Seno: sen(x)

Cosseno: cos(x)

Tangente: tan(x)

Exponencial: e^(x) (via expo())

Logaritmo natural: ln(x)

Logaritmo base 10: log10(x)

Todas as funções funcionam tanto para reais quanto complexos.

Números Complexos

Entrada aceita:

3+2i
4-i
-7i
5
0+3i


As operações implementadas manualmente incluem:

soma/subtração real e imaginária

multiplicação e divisão

potência usando:

z^w = e^(w · ln(z))


trigonometria complexa

exponenciais complexas

logs complexos via forma polar

Sistema de Constantes

O usuário pode definir constantes como:

x = 3-2i
k = 5
beta = -4i


Elas podem ser usadas em qualquer expressão:

sen(x)
x + raiz(9)
(3+2i)**(1-i)


As constantes ficam salvas até o usuário apagá-las.

Parser de Expressões

Totalmente feito do zero:

Tokenização manual

Precedência correta de operadores

Suporte a parênteses e funções

Construção da Árvore Sintática (AST)

Impressão no formato LISP, exemplo:

(+ 3 (* 2 i))


Avaliação recursiva do AST

Menu do Programa

Ao iniciar, o usuário vê:

1 - Porcentagem
2 - Expressão aritmética
3 - Verificação de igualdade
4 - Definir constante
5 - Exibir constantes salvas
6 - Deletar constantes
"_" - Sair

1 — Porcentagem

Exemplo:

número: 200
porcentagem: 10
→ 20


Funciona com complexos:

10+5i com 50% → 5+2.5i

2 — Expressão Aritmética

Aceita:

Reais

Complexos

Constantes definidas pelo usuário

Funções

Operadores

Parênteses

Exemplos válidos:

3+2i
raiz(9)
(2+3i) * conj(4-i)
a + 2*b - raiz(c)
sen(2+3i)
(3+2i)**(1-i)


Sempre mostra a árvore LISP da expressão.

3 — Verificação de igualdade

Compara o valor LISP de duas expressões:

Expr1: 2 + a
Expr2: a + 2
→Diferentes

4 — Definir constante
Nome: x
Valor: 3-2i

5 — Mostrar constantes salvas

Lista todas formatadas corretamente.

6 — Deletar constantes
Como os Cálculos São Feitos (Resumo Técnico)
Séries de Taylor

sen(x)

cos(x)

e^x

Parte do ln(x) via método de Newton

Trigonometria Complexa

Implementada pelas identidades:

sin(a+bi) = sin(a)cosh(b) + i cos(a)sinh(b)
cos(a+bi) = cos(a)cosh(b) - i sin(a)sinh(b)

Exponencial Complexa
e^(a+bi) = e^a (cos(b) + i sin(b))

Logaritmo Complexo
ln(a+bi) = ln(r) + iθ


com:

r = sqrt(a² + b²)
θ = atan2(b, a)

Raiz Quadrada Complexa

Derivada da identidade:

√(a+bi) = x + yi


onde:

x = sqrt((a + r)/2)
y = sign(b) * sqrt((r - a)/2)

arctan()

Implementado com:

série de Taylor para |x| ≤ 1

identidades de redução

ajuste de quadrantes (atan2)

Parser

análise léxica

análise sintática com precedência

árvore Node

avaliação recursiva

Requisitos

Apenas Python padrão

Nenhuma biblioteca externa necessária
