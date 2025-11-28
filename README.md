Projeto A3 - Calculadora Científica de Números Complexos

Professor: Wellington Lacerda Silveira da Silva
Disciplina: Estrutura de Dados e Análise de Algoritmos

Integrantes do Grupo

Breno Dantas Oliveira Filho – RA: 1272417582

Ramon Queiroz G. Pinto – RA: 12724126768

Adrian Ferreira Andrade – RA: 12724133589

Calculadora Científica — A3 - 2025 

Este projeto é uma calculadora científica com suporte completo a números complexos, incluindo:

Aritmética básica

Funções trigonométricas reais e complexas

Logaritmos

Exponenciais

Raiz quadrada complexa

Potenciação complexa

Um parser próprio de expressões

Avaliação de expressões com variáveis

Tudo foi implementado manualmente, sem usar bibliotecas matemáticas prontas (math, cmath, etc), incluindo séries de Taylor, Euler, e aritmética complexa completa.

Funcionalidades Principais
Operações 

Soma +

Subtração -

Multiplicação *

Divisão /

Potência **

Raiz quadrada: raiz()

Conjugado: conj()

seno: sen()

cosseno: cos()

tangente: tan()

logaritmo: ln()

logaritmo base 10: log10()

Suporte total a números complexos

Entrada no formato: a+bi, a-bi, 3i, -7i, 5, etc

Funções trigonométricas e exponenciais funcionam para complexos

Potenciação complexa usando z^w = e^(w·ln(z))

Variáveis

O usuário pode definir variáveis (x, y, a, etc)

Podem ser usadas em qualquer expressão

Podem armazenar números ou complexos

Ficam salvas durante a execução

Sistema próprio de parsing

O programa:

Tokeniza

Constrói uma árvore sintática (AST)

Mostra a árvore no formato LISP

Avalia recursivamente

Como usar a calculadora

Ao rodar o programa, você verá o menu:

1 - Porcentagem
2 - Expressão aritmética
3 - Verificação de igualdade
4 - Definir variável
5 - Exibir valores salvos
"_" - Sair

Opção 1 – Porcentagem

Digite um número e depois uma porcentagem.

Exemplo:

número = 200
porcentagem = 10
resultado = 20


Funciona também com complexos:

número = 10+5i
porcentagem = 50
resultado = 5+2.5i

Opção 2 – Expressão aritmética

Você pode digitar qualquer expressão contendo:

Operadores
+  -  *  /  **  

Funções
sen(x)
cos(x)
tan(x)
ln(x)
log10(x)
raiz(x)
conj(x)

Complexos
3+2i
4-i
-7i

Variáveis
x
a
beta


Se você usar uma variável ainda não definida, o programa perguntará seu valor.

Exemplos válidos:
3+2i
raiz(9)
(2+3i) * conj(4-i)
a + 2*b - raiz(c)
sen(2+3i)
(3+2i)**(1-i)


Cada expressão mostra também sua árvore sintática LISP:

Árvore LISP: (+ 3i (* 2 (conj 4i)))

Opção 3 – Verificar se expressões são iguais

O programa avalia duas expressões e compara os resultados.

Exemplo:

Expr 1: 2+a
Expr 2: a+2
→ Iguais


Funciona inclusive com funções e complexos.

Opção 4 – Definir variável

Cria uma variável e atribui um valor.

Exemplo:

Nome da variável: x
Valor: 3-2i


Depois você pode usar:

sen(x)
x + raiz(9)
x**2

Opção 5 – Exibir valores salvos

Mostra todas as variáveis já definidas e seus valores formatados.

Exemplo:

x = 3 - 2i
y = 1.5
z = -4i

 Como o código funciona (visão geral)
Implementações matemáticas feitas manualmente

seno e coss → séries de Taylor

sinh e cosh → fórmulas exponenciais

tan → razão entre sin/cos

expo → série de Taylor + Euler para complexos

logn → forma polar ln(r) + iθ

raizQ → dedução algébrica da raiz quadrada complexa

arctang → aproximação por séries + ajustes de quadrante

ncomplexo → parser manual para strings complexas

Parser

Implementa:

Tokenização

Análise sintática (precedência: (), funções, **, * /, + -)

Construção da árvore Node

Avaliação recursiva

Requisitos

Apenas Python padrão.
Nenhuma biblioteca adicional é necessária.
