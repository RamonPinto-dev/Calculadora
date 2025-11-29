print("== CALCULADORA CIENTÍFICA COMPLEXA ==")

PI = 3.141592653589793

def seno(g):
    # Números complexos:
    if isinstance(g, complex):
        # sin(a + bi) = sin(a)cosh(b) + i*cos(a)sinh(b)
        parte_real = seno(g.real) * cossh(g.imag)
        parte_imag = coss(g.real) * senoh(g.imag)
        return complex(parte_real, parte_imag)
    # Números reais (Série de Taylor):
    else:
        soma = 0
        termo = g
        for n in range(1, 15):
            soma += termo
            termo *= -g*g / ((2*n) * (2*n+1))
        return soma

def coss(g):
    # Números complexos:
    if isinstance(g, complex):
        # cos(a + bi) = cos(a)cosh(b) - i*sin(a)sinh(b)
        parte_real = coss(g.real) * cossh(g.imag)
        parte_imag = - seno(g.real) * senoh(g.imag)
        return complex(parte_real, parte_imag)
    # Números reais (Série de Taylor):
    else:
        soma = 1
        termo = 1
        for n in range(1, 15):
            termo *= -g*g / ((2*n-1) * (2*n))
            soma += termo
        return soma

def tang(g):
    # tan(z) = sin(z) / cos(z)
    seno_g = seno(g)
    cos_g = coss(g)
    if cos_g.real == 0 and cos_g.imag == 0:
        raise ValueError("Tangente indefinida (divisão por 0)")
    return (seno_g/cos_g)

def senoh(g):
    # sinh(x) = (e^x - e^(-x)) / 2
    return (expo(g) - expo(-g)) / 2

def cossh(g):
    # cosh(x) = (e^x + e^(-x)) / 2
    return (expo(g) + expo(-g)) / 2

def arctang_taylor(g):
    if abs(g) > 1:
        return (PI/2) - arctang_taylor(1/g)
    soma = 0
    termo = g
    for n in range(0, 20):
        soma += termo / (2*n + 1)
        termo *= -g*g
    return soma

def arctang(b, a):
    if a > 0:
        return arctang_taylor(b/a)
    elif a < 0:
        if b >= 0:
            return arctang_taylor(b/a) + PI
        else:
            return arctang_taylor(b/a) - PI
    else:
        if b > 0:
            return PI/2
        elif b < 0:
            return -PI/2
        else:
            raise ValueError("Invalido (divisão por 0)")
            


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
        magnitude = raizQ(x.real*x.real + x.imag*x.imag)

        # theta:
        theta = arctang(x.imag, x.real)

        parte_real = logn(magnitude)
        parte_imag = theta
        return complex(parte_real, parte_imag)
    
    # Para os números reais:
    else:
        if x == 0:
            raise ValueError("ln não funciona em zero")
        y = x - 1
        for _ in range(20):
            y -= (expo(y) - x) / expo(y)
        return y

def log10(x):
    return logn(x) / logn(10)

def raizQ(x):
    # Extraindo a raiz de a + ib...
    # v(a + bi) = x + yi.
    # [v(a + bi)]^2 = (x + yi)^2 -> a + bi = x^2 + 2xyi + (yi)^2 = x^2 + 2xyi - y^2.
    # Se a + bi = x^2 + 2xyi - y^2, então a = (x^2 - y^2) e bi = 2xyi.

    # Se (x + iy)^2 é igual a (a + bi), como estabelecido no segundo comentário da função, concluimos que a magnitude de ambos é a mesma, r.
    # r = raiz quadrada de (a^2 + b^2) = raiz quadrada de (x^2 + y^2)^2. v(a^2 + b^2) = (x^2 + y^2).

    # a + r = (x^2 - y^2) + (x^2 + y^2) = x^2 + x^2 = 2x^2 ->
    # (a + r)/2 = x^2 -> x = mais ou menos v[(a + r)/2]
    # r - a = (x^2 + y^2) - (x^2 - y^2) = 2y^2 ->
    # (r - a)/2 = y^2 -> y = mais ou menos v[(r - a)/2]

    # √(a + bi) = x + yi = {mais ou menos v[(a + r)/2]} + {mais ou menos v[(r - a)/2]}*i
    # bi = 2xyi, portanto b = 2xy. Para determinar os sinais das raizes podemos usar b.
    # Se b for negativo, então x e y devem ter sinais opostos, se b for positivo os sinais devem ser iguais. Se b for 0 o número é real, claramente.
    # Faremos com que x sempre seja positivo, o sinal de b determinará o sinal de y.
    
    a, b = x.real, x.imag
    
    # Se x for complexo:
    if isinstance(x, complex):
        magnitude = raizQ(a*a + b*b)
        
        parte_real = raizQ((a + magnitude) / 2)
        parte_imag = (1 if b >= 0 else -1) * raizQ((magnitude - a) / 2)

        return complex(parte_real, parte_imag)
    
    # Se x for real:
    else:
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

constantes = {}

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
        if ch == "^":
            tokens.append("**")
            i += 1
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
        
        try:
            val = ncomplexo(tok)
            return Node("num", val)
        except:
            return Node("var", tok)
    node = nexpressao()
    if tokens:
        raise ValueError("Tokens sobrando / sintaxe inválida")
    return node

def evaluate(node, valores_substituidos=None):
    if valores_substituidos is None:
        valores_substituidos = {}

    if node.tipo == "num":
        return node.valor, valores_substituidos
    
    # Variáveis:
    if node.tipo == "var":
        nome = node.valor

        # Checar se o valor da variável já não foi registrada pelo usuário (para evitar que o programa interprete os 2 x em "x + x" como variáveis diferentes, por exemplo)
        if nome in valores_substituidos:
            return valores_substituidos[nome], valores_substituidos

        # Pede entrada de valor da variável:
        entrada = input(f"Valor da variável {nome}: ")

        try:
            val = ncomplexo(entrada)
        except:
            raise ValueError(f"Valor inválido para variável '{nome}'")
        valores_substituidos[nome] = val
        return val, valores_substituidos
    
    if node.tipo == "func":
        arg, valores_substituidos = evaluate(node.esq, valores_substituidos)
        funcoes = {
            "sen": lambda x: seno(x),
            "cos": lambda x: coss(x),
            "tan": lambda x: tang(x),
            "ln": lambda x: logn(x),
            "log10": lambda x: log10(x),
            "raiz": lambda x: raizQ(x),
            "conj": lambda x: conj(x)
        }
        if node.valor not in funcoes:
            raise ValueError("Função inexistente")
        return funcoes[node.valor](arg), valores_substituidos
    
    # Operadores binários:
    esquerda, valores_substituidos = evaluate(node.esq, valores_substituidos)
    direita, valores_substituidos = evaluate(node.dir, valores_substituidos)

    if node.valor == "+":
        # (a + bi) + (c + di) = (a + c) + (bi + di):
        resultado = complex(esquerda.real + direita.real, esquerda.imag + direita.imag)
    elif node.valor == "-":
        # (a + bi) + (c + di) = (a - c) + (bi - di):
        resultado = complex(esquerda.real - direita.real, esquerda.imag - direita.imag)
    
    elif node.valor == "*":
        # Distributiva:
        # (a + bi) * (c + di) = a(c + di) + bi(c + di) = ac + adi + bci + bdi*i = ac + adi + bci - bd =
        # ac - bd + adi + bci = (ac - bd) + (ad + bc)i
        real = esquerda.real * direita.real - esquerda.imag * direita.imag
        imag = esquerda.real * direita.imag + esquerda.imag * direita.real
        resultado = complex(real, imag)
    
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
        resultado = complex(real, imag)
    
    elif node.valor == "**":
        # Potência complexa. Para isto se utiliza esta formula baseada na formula de Euler: z^w = e^(w*ln(z))
        base = esquerda
        expoente = direita

        # Se a base for 0...
        if base.real == 0 and base.imag == 0:

            # ...e o expoente também for 0, retorna 1, por convenção.
            if expoente.real == 0 and expoente.imag == 0:
                resultado = complex(1, 0)
            
            # ...e o expoente for positivo, retorna 0.
            elif expoente.real > 0:
                resultado = complex(0, 0)
            
            # ...e o expoente for 0, invalido:
            else:
                raise ValueError("Invalido (divisão por 0)")
        
        # ln(z) = ln(r) + i*theta, como já estabelecido (na função logn)
        magnitude = raizQ(base.real*base.real + base.imag*base.imag) 
        theta = arctang(base.imag, base.real)
    
        # w * ln(z) = (a + bi) * (ln(r) + iθ) = a*ln(r) + a*theta*i + ln(r)*b*i + b*theta*i*i =
        # a*ln(r) + a*theta*i + ln(r)*b*i - b*theta = (a*ln(r) - b*theta) + i*(a*theta + b*ln(r))
        expoente_real = expoente.real * logn(magnitude) - expoente.imag * theta
        expoente_imag = expoente.real * theta + expoente.imag * logn(magnitude)
        expoente = complex(expoente_real, expoente_imag)

        # Finalmente calcular e^(w*ln(z)):
        resultado = expo(expoente)

    else:
        raise ValueError("Operador inválido")
    
    return resultado, valores_substituidos

    try:
        return ops[node.valor](esquerda,direita)
    except ZeroDivisionError:
        raise ZeroDivisionError("Divisão por zero")

# Função que monta a notação LISP:
def mostrar_lisp(node):
    if node.tipo == "num":
        return format_complex(node.valor)
    
    if node.tipo == "var":
        return node.valor
    
    if node.tipo == "func":
        return f"({node.valor} {mostrar_lisp(node.esq)})"
    
    return f"({node.valor} {mostrar_lisp(node.esq)} {mostrar_lisp(node.dir)})"

# Na função acima, a notação LISP montada utiliza os nomes das variaveis e constants (ex: (+ x y)), aqui faz outra notação onde seus valores são mostrados para o usuário:
def mostrar_lisp_substituido(node, valores_substituidos=None):
    if valores_substituidos is None:
        valores_substituidos = {}
    
    if node.tipo == "num":
        return format_complex(node.valor)
    
    # Variaveis e constants substituidos pelo seus valores:
    if node.tipo == "var":
        if node.valor in valores_substituidos:
            return format_complex(valores_substituidos[node.valor])
        return node.valor
    
    if node.tipo == "func":
        return f"({node.valor} {mostrar_lisp_substituido(node.esq, valores_substituidos)})"
    
    return f"({node.valor} {mostrar_lisp_substituido(node.esq, valores_substituidos)} {mostrar_lisp_substituido(node.dir, valores_substituidos)})"

def igual(a,b):
    va, _ = evaluate(a)
    vb, _ = evaluate(b)
    return format_complex(va) == format_complex(vb)

while True:
    print("""
1 - Porcentagem
2 - Expressão aritmética
3 - Verificação de igualdade
4 - Definir constante
5 - Exibir constantes salvas
6 - Deletar constants
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
                res, valores_substituidos = evaluate(arv)

                if valores_substituidos:
                    print("Árvore LISP:", mostrar_lisp_substituido(arv, valores_substituidos))
                
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
                # Basicamente inutinizavel agora/ Seria bom mudar esse case para Nome da Cosntante
        case "4":
            nome = input("Nome da constante: ").strip()

            if not nome.isalpha():
                print("Erro: Nome de constante deve ter apenas letras.")
                continue

            expr = input("Valor: ")

            try:
                arv = nparser(expr)          
                val, _ = evaluate(arv)          
                constantes[nome] = val        
                print(f"Constante '{nome}' foi definida como {format_complex(val)}")
            except Exception as e:
                print("Erro ao definir constante: ", e)
        case "5":
            if not constantes:
                print("Nenhuma constante salva.")
            else:
                print("CONSTANTES SALVAS:")
                for nome, valor in constantes.items():
                    print(f"{nome} = {format_complex(valor)}")
        
        case "6":
            if not constantes:
                print("Nenhuma constante salva para deletar.")
                continue
                
            print("Constantes disponíveis:")
            for nome in constantes.keys():
                print(f"- {nome}")
                
            nome = input("Nome da constante a deletar: ").strip()
            if nome in constantes:
                del constantes[nome]
                print(f"Constante '{nome}' deletada.")
            else:
                print(f"Constante '{nome}' não encontrada.")
