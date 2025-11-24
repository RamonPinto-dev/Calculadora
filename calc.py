print("== CALCULADORA CIENTÍFICA ==")
print("== TRABALHO DO LINDO WELLIGTON ==")
import math

PI = 3.14

def seno(g):
    # sin(a + bi) = sin(a)cosh(b) + i*cos(a)sinh(b)
    parte_real = math.sin(g.real) * math.cosh(g.imag)
    parte_imag = math.cos(g.real) * math.sinh(g.imag)
    return complex(parte_real, parte_imag)

def coss(g):
    # cos(a + bi) = cos(a)cosh(b) - i*sin(a)sinh(b)
    parte_real = math.cos(g.real) * math.cosh(g.imag)
    parte_imag = - math.sin(g.real) * math.sinh(g.imag)
    return complex(parte_real, parte_imag)

def tang(g):
    # tan(z) = sin(z) / cos(z)
    seno_g = seno(g)
    cos_g = coss(g)
    if cos_g.real == 0 and cos_g.imag == 0:
        raise ValueError("Tangente indefinida (divisão por 0)")
    return (seno_g/cos_g)

def expo(x):
    # Se o número for complexo:
    if isinstance(x, complex):
        # e^(a+bi) = e^a * (cos(b) + i*sin(b)), a formula de Euler
        magnitude = expo(x.real) # e^a

        parte_real = magnitude * coss(x.imag)
        parte_imag = magnitude * seno(x.imag)
        return complex(parte_real, parte_imag)
    
    # Série de Taylor para numero real:
    else:
        soma = 1
        term = 1
        for i in range(1, 20):
            term *=  x/i
            soma += term
        return soma

def logn(x):
    # Aqui é necessário usar a forma polar do número complexo, r*e^(i*theta)
    # ln(r*e^(i*theta)) = ln(r) + i*theta
    # Para achar r é só utilizar o teorema de Pitagoras, r = raiz quadrada de (a^2 + b^2)
    # Theta é arctan(b/a)

    # Quando o número for complexo:
    if isinstance(x, complex):
        # Zero:
        if x.real == 0 and x.imag == 0:
            raise ValueError("ln não funciona em zero")
    
        # r:
        magnitude = raizQ(x.real**2 + x.imag**2)

        # theta:
        theta = math.atan(x.imag/x.real)

        parte_real = logn(magnitude)
        parte_imag = theta
        return complex(parte_real, parte_imag)
    
    # Para os números reais:
    else:
        if x == 0:
            raise ValueError("ln não funciona em zero")
        y = x - 1
        for _ in range(20):
            y -= (exp(y) - x) / exp(y)
        return y

def log10(x):
    return logn(x) / logn(10)

def sqrt(x):
    return x ** 0.5

def conj(x):
    return complex(x.real, -x.imag)

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
            "sen": lambda x: seno(x),
            "cos": lambda x: coss(x),
            "tan": lambda x: tang(x),
            "logn": lambda x: logn(x),
            "log10": lambda x: log10(x),
            "raiz": lambda x: sqrt(x),
            "conj": lambda x: conj(x)
        }
        if node.valor not in funcoes:
            raise ValueError("Função inexistente")
        return funcoes[node.valor](arg)
    
    # Operadores binários:
    esquerda = evaluate(node.esq)
    direita = evaluate(node.dir)
    if node.valor == "+":
        # (a + bi) + (c + di) = (a + c) + (bi + di):
        return complex(esquerda.real + direita.real, esquerda.imag + direita.imag)
    elif node.valor == "-":
        # (a + bi) + (c + di) = (a - c) + (bi - di):
        return complex(esquerda.real - direita.real, esquerda.imag - direita.imag)
    
    elif node.valor == "*":
        # Distributiva:
        # (a + bi) * (c + di) = a(c + di) + bi(c + di) = ac + adi + bci + bdi*i = ac + adi + bci - bd =
        # ac - bd + adi + bci = (ac - bd) + (ad + bc)i
        real = esquerda.real * direita.real - esquerda.imag * direita.imag
        imag = esquerda.real * direita.imag + esquerda.imag * direita.real
        return complex(real, imag)
    
    elif node.valor == "/":
        # (a+bi)/(c+di) = (a+bi)/(c+di) * (c-di)/(c-di) = (ac - adi + bci - bdi*i)/(c^2 - cdi + cdi - d^2*i^2) =
        # (ac + bd + bci - adi)/(c^2 + d^2) =
        # [(ac + bd) + (bc - ad)i] / (c^2 + d^2) =
        # (ac + bd)/(c^2 + d^2) + (bc - ad)i/(c^2 + d^2)
        if direita.real == 0 and direita.imag == 0:
            raise ZeroDivisionError("Divisão por zero")
        denominador = direita.real**2 + direita.imag**2
        real = (esquerda.real * direita.real + esquerda.imag * direita.imag) / denominador
        imag = (esquerda.imag * direita.real - esquerda.real * direita.imag) / denominador
        return complex(real, imag)
    
    elif node.valor == "**":
        # Potência complexa. Para isto se utiliza esta formula baseada na formula de Euler: z^w = e^(w*ln(z))

        # Se a base for 0...
        if direita.real == 0 and direita.imag == 0:

            # ...e o expoente também for 0, retorna 1, por convenção.
            if esquerda.real == 0 and esquerda.imag == 0:
                return complex(1, 0)
            
            # ...e o expoente for positivo, retorna 0.
            elif direita.real > 0:
                return complex(0, 0)
            
            # ...e o expoente for 0, invalido:
            else:
                raise ValueError("Invalido (divisão por 0)")
        
        # ln(z) = ln(r) + i*theta, como já estabelecido (na função logn)
        magnitude = raizQ(direita.real**2 + direita.imag**2) 
        theta = math.arctan(esquerda.imag/esquerda.real)
    
        # w * ln(z) = (a + bi) * (ln(r) + iθ) = a*ln(r) + a*theta*i + ln(r)*b*i + b*theta*i*i =
        # a*ln(r) + a*theta*i + ln(r)*b*i - b*theta = (a*ln(r) - b*theta) + i*(a*theta + b*ln(r))
        expoente_real = esquerda.real * logn(magnitude) - esquerda.imag * theta
        expoente_imag = esquerda.real * theta + esquerda.imag * logn(magnitude)
        expoente = complex(expoente_real, expoente_imag)

        # Finalmente calcular e^(w*ln(z)):
        return expoente

    else:
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
5 - Exibir valores salvos
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
        case "5":
            if not variaveis:
                print("Nenhuma variável salva.")
            else:
                print("VARIÁVEIS SALVAS:")
                for nome, valor in variaveis.items():
                    print(f"{nome} = {format_complex(valor)}")
