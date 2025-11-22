print("== CALCULADORA CIENTÍFICA ==")
print("== TRABALHO DO LINDO WELLIGTON ==")

PI = 3.14

def seno(g):
    rad = g * PI / 180
    s = 0
    term = rad
    for i in range(1, 10):
        s += term
        term *= -(rad * rad) / ((2 * i) * (2 * i + 1))
    return s

def cos(g):
    rad = g * PI / 180
    c = 1
    term = 1
    for i in range(1, 10):
        term *= -(rad * rad) / ((2 * i - 1) * (2 * i))
        c += term
    return c

def tan(g):
    c = cos(g)
    if abs(c) < 1e-12:
        raise ValueError("Tangente indefinida")
    return seno(g) / c

def exp(x):
    soma = 1
    term = 1
    for i in range(1, 20):
        term *= x / i
        soma += term
    return soma

def ln(y):
    if y == 0:
        raise ValueError("ln não funciona em zero")
    x = y - 1
    for _ in range(20):
        x -= (exp(x) - y) / exp(x)
    return x

def log10(x):
    return ln(x) / 2.302585092994

def sqrt(x):
    return x ** 0.5

def conj(x):
    return x.conjugate()

def reduzir(x):
    return f"{x:.3f}".rstrip("0").rstrip(".")

def ncomplexo(s):
    s = s.strip().replace(" ", "").lower()
    if s == "":
        raise ValueError("Entrada vazia")
    s = s.replace("j", "i")
    if s == "i":
        return complex(0, 1)
    if s == "-i":
        return complex(0, -1)
    if "i" in s:
        idx = -1
        for i, ch in enumerate(s[:-1], start=0): 
            if (ch == "+" or ch == "-") and i != 0:
                idx = i
        if idx != -1:
            real_part = s[:idx]
            imag_part = s[idx:-1]  
            real_val = float(real_part) if real_part not in ("", "+", "-") else (0.0 if real_part=="" else float(real_part))
            if imag_part in ("+", "-"):
                imag_val = 1.0 if imag_part == "+" else -1.0
            else:
                imag_val = float(imag_part)
            return complex(real_val, imag_val)
        else:
            base = s[:-1]
            if base in ("", "+"):
                return complex(0, 1)
            if base == "-":
                return complex(0, -1)
            return complex(0, float(base))
    else:
        return complex(float(s), 0)

def format_complex(c):
    r = reduzir(c.real)
    i = reduzir(abs(c.imag))
    if c.imag == 0:
        return r
    if c.real == 0:
        sign = "-" if c.imag < 0 else ""
        return sign + i + "i"
    sign = " - " if c.imag < 0 else " + "
    return f"({r}{sign}{i}i)"

class Node:
    def __init__(self, tipo, valor=None, esq=None, dir=None):
        self.tipo = tipo
        self.valor = valor
        self.esq = esq
        self.dir = dir

variaveis = {}

def tokenize(expr):
    expr = expr.strip()
    tokens = []
    i = 0
    funcs = ["sen","cos","tan","ln","log10","raiz","conj"]
    while i < len(expr):
        ch = expr[i]
        if ch.isspace():
            i += 1
            continue
        if expr.startswith("**", i):
            tokens.append("**")
            i += 2
            continue
        if ch in "+-*/()":
            tokens.append(ch)
            i += 1
            continue
        matched = False
        for f in funcs:
            if expr.startswith(f, i):
                tokens.append(f)
                i += len(f)
                matched = True
                break
        if matched:
            continue
        if ch.isdigit() or ch == '.':
            num = ""
            while i < len(expr) and (expr[i].isdigit() or expr[i] == '.'):
                num += expr[i]
                i += 1
            if i < len(expr) and expr[i] == "i":
                num += "i"
                i += 1
            if i < len(expr) and expr[i] == "%":
                base = float(num.replace("i","")) / 100
                if "i" in num:
                    tokens.append(str(base) + "i")
                else:
                    tokens.append(str(base))
                i += 1
            else:
                tokens.append(num)
            continue
        if ch.isalpha():
            ident = ""
            while i < len(expr) and expr[i].isalpha():
                ident += expr[i]
                i += 1
            tokens.append(ident)
            continue
        raise ValueError(f"Caractere inválido: {ch}")
    return tokens

def nparser(expr):
    tokens = tokenize(expr)
    def nexpressao():
        node = ntermo()
        while tokens and tokens[0] in ["+","-"]:
            op = tokens.pop(0)
            direita = ntermo()
            node = Node("op", op, node, direita)
        return node
    def ntermo():
        node = npotencia()
        while tokens and tokens[0] in ["*","/"]:
            op = tokens.pop(0)
            direita = npotencia()
            node = Node("op", op, node, direita)
        return node
    def npotencia():
        node = nfator()
        if tokens and tokens[0] == "**":
            tokens.pop(0)
            node = Node("op","**",node,npotencia())
        return node
    def nfator():
        if not tokens:
            raise ValueError("Conta incompleta")
        tok = tokens.pop(0)
        if tok == "(":
            node = nexpressao()
            if not tokens or tokens.pop(0) != ")":
                raise ValueError("Parêntese não fechado")
            return node
        if tok in ["sen","cos","tan","ln","log10","raiz","conj"]:
            if not tokens or tokens.pop(0) != "(":
                raise ValueError("Falta parêntese pós função")
            inside = nexpressao()
            if not tokens or tokens.pop(0) != ")":
                raise ValueError("Parêntese não fechado pós função")
            return Node("func", tok, inside)
        if tok == "+":
            return nfator()
        if tok == "-":
            nodo = nfator()
            return Node("op","*", Node("num", complex(-1,0)), nodo)
        if tok in variaveis:
            return Node("num", variaveis[tok])
        try:
            val = ncomplexo(tok)
            return Node("num", val)
        except:
            return Node("var", tok)
    node = nexpressao()
    if tokens:
        raise ValueError("Tokens sobrando / sintaxe inválida")
    return node

def evaluate(node):
    if node.tipo == "num":
        return node.valor
    if node.tipo == "var":
        nome = node.valor
        if nome in variaveis:
            return variaveis[nome]
        entrada = input(f"Valor da variável {nome}: ")
        try:
            val = ncomplexo(entrada)
        except:
            raise ValueError("Valor de variável inválido")
        variaveis[nome] = val
        return val
    if node.tipo == "func":
        arg = evaluate(node.esq)
        funcoes = {
            "sen": lambda x: complex(seno(x.real),0),
            "cos": lambda x: complex(cos(x.real),0),
            "tan": lambda x: complex(tan(x.real),0),
            "ln": lambda x: complex(ln(x.real),0),
            "log10": lambda x: complex(log10(x.real),0),
            "raiz": lambda x: complex(sqrt(x.real),0),
            "conj": lambda x: conj(x)
        }
        if node.valor not in funcoes:
            raise ValueError("Função inexistente")
        return funcoes[node.valor](arg)
    esquerda = evaluate(node.esq)
    direita = evaluate(node.dir)
    ops = {
        "+": lambda a,b: a + b,
        "-": lambda a,b: a - b,
        "*": lambda a,b: a * b,
        "/": lambda a,b: (_ for _ in ()).throw(ZeroDivisionError()) if (b.real==0 and b.imag==0) else a / b,
        "**": lambda a,b: a ** b
    }
    if node.valor not in ops:
        raise ValueError("Operador inválido")
    try:
        return ops[node.valor](esquerda,direita)
    except ZeroDivisionError:
        raise ZeroDivisionError("Divisão por zero")

def mostrar_lisp(node):
    if node.tipo == "num":
        return format_complex(node.valor)
    if node.tipo == "var":
        return node.valor
    if node.tipo == "func":
        return f"({node.valor} {mostrar_lisp(node.esq)})"
    return f"({node.valor} {mostrar_lisp(node.esq)} {mostrar_lisp(node.dir)})"

def igual(a,b):
    va = evaluate(a)
    vb = evaluate(b)
    return format_complex(va) == format_complex(vb)

while True:
    print("""
1 - Porcentagem
2 - Expressão aritmética
3 - Verificação de igualdade
4 - Definir variável
"_" - Sair""")
    op = input("Escolha a opção: ")
    if op.lower() == "_":
        break
    match op:
        case "1":
            entrada = input("Digite o número: ")
            try:
                resultado = ncomplexo(entrada)
            except Exception:
                print("Erro: número inválido")
                continue
            p_input = input("Digite a porcentagem: ")
            try:
                p = ncomplexo(p_input)
            except:
                print("Erro: porcentagem inválida")
                continue
            try:
                res = resultado * (p / 100)
            except Exception:
                print("Erro no cálculo")
                continue
            print("Resultado:", format_complex(res))
        case "2":
            expr = input("Digite expressão: ")
            try:
                arv = nparser(expr)
                print("Árvore LISP:", mostrar_lisp(arv))
                res = evaluate(arv)
                print("Resultado:", format_complex(res))
            except ZeroDivisionError:
                print("Erro: divisão por zero")
            except Exception as e:
                print("Erro:", e)
        case "3":
            e1s = input("Expr 1: ")
            e2s = input("Expr 2: ")
            try:
                a1 = nparser(e1s)
                a2 = nparser(e2s)
                print("Árvore 1:", mostrar_lisp(a1))
                print("Árvore 2:", mostrar_lisp(a2))
                iguais = igual(a1,a2)
                print("Iguais" if iguais else "São diferentes")
            except ZeroDivisionError:
                print("Erro: divisão por zero")
            except Exception as e:
                print("Erro:", e)
        case "4":
            nome = input("Nome da variável: ").strip()

            if not nome.isalpha():
                print("Erro: Nome de variável deve ter apenas letras.")
                continue

            expr = input("Valor: ")

            try:
                arv = nparser(expr)          
                val = evaluate(arv)          
                variaveis[nome] = val        
                print(f"Variável '{nome}' foi definida como {format_complex(val)}")
            except Exception as e:
                print("Erro ao definir variável:", e)

