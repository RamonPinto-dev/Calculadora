print("== CALCULADORA CIENTÍFICA COMPLEXA ==")

# Constante para pi:
PI = 3.141592653589793
# Constantes que auxiliam na Série de Taylor:
LIMITE_TAYLOR = 100  # O máximo número pelo qual se vai fazer a Série de Taylor (para ter cuidado com o overflow)
TERMOS_TAYLOR = 1000   # Quantidade de termos utilizados na série
TOLERANCIA_TAYLOR = 1e-10  # Como os termos da Série de Taylor vão ficando cada vez menores, tinha uma hora que ele atrapalhava a redudância (ex 511.999 em vez de 512), daí esta "tolerância" para parar a série quando um termo for menor que ela se fez necessário

def seno(g):
    # Números complexos:
    if isinstance(g, complex):
        # sin(a + bi) = sin(a)cosh(b) + i*cos(a)sinh(b)
        parte_real = seno(g.real) * cossh(g.imag)
        parte_imag = coss(g.real) * senoh(g.imag)
        return complex(parte_real, parte_imag)
    
    # Números reais (Série de Taylor):
    else:
        g = g % (2*PI)
        soma = 0
        termo = g
        for n in range(1, TERMOS_TAYLOR):
            soma += termo
            termo *= -g*g / ((2*n) * (2*n+1))

            if abs(termo) < TOLERANCIA_TAYLOR:
                break
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
        g = g % (2*PI)
        soma = 1
        termo = 1
        for n in range(1, TERMOS_TAYLOR):
            termo *= -g*g / ((2*n-1) * (2*n))
            soma += termo
            if abs(termo) < TOLERANCIA_TAYLOR:
                break

        return soma

def tang(g):
    # tan(z) = sin(z) / cos(z)
    seno_g = seno(g)
    cos_g = coss(g)

    if not isinstance(g, complex):
        g = g % (2*PI)

    if abs(cos_g.real) < TOLERANCIA_TAYLOR and abs(cos_g.imag) < TOLERANCIA_TAYLOR:
        raise ValueError("Tangente indefinida para este número")
    
    return (seno_g/cos_g)

def senoh(g):
    # sinh(x) = (e^x - e^(-x)) / 2
    return (expo(g) - expo(-g)) / 2

def cossh(g):
    # cosh(x) = (e^x + e^(-x)) / 2
    return (expo(g) + expo(-g)) / 2

def arctang_taylor(g): #calcula arctan(g) usando a série de Taylor válida para |x| ≤ 1.
    #arctan(x) = x - x³/3 + x⁵/5 - x⁷/7 +..  se |g| > 1, usa a identidade: arctan(g) = π/2 - arctan(1/g)
    #parâmetros globais usados:
    #TERMOS_TAYLOR: número máximo de termos da expansão
    #TOLERANCIA_TAYLOR: limite mínimo para interromper a série cedo
    
    # se o valor estiver fora do intervalo de convergência da série,
    # usa a identidade para reduzir para uma região de cálculo melhor.
    if abs(g) > 1:
        return (PI/2) - arctang_taylor(1/g)
    
    soma = 0 #acumula a soma da série
    termo = g #primeiro termo da série é x¹
    
    for n in range(0, TERMOS_TAYLOR):
    #soma o termo atual dividido pelo denominador adequado (1, 3, 5...
        soma += termo / (2*n + 1)
        #calcula o próximo termo multiplicando por -x²
        #isso gera automaticamente x³, x⁵, x⁷, alternando sinais.
        termo *= -g*g
        #se o termo ficou muito pequeno, para para evitar cálculos desnecessários
        if abs(termo) < TOLERANCIA_TAYLOR:
            break
    return soma

def arctang(b, a):
    #implementa atan2(b, a):
    #b é o eixo Y   O objetivo é retornar o ângulo correto no plano,considerando o quadrante do ponto (a, b).
    #a é o eixo X
    #o objetivo é retornar o ângulo correto no plano,considerando o quadrante do ponto (a, b).
    #regras:
    # 1)se a > 0:
    #atan2(b, a) = arctan(b/a)
    # 2)se a < 0:
    #se b ≥ 0 → arctan(b/a) + π
    #se b <  0 → arctan(b/a) - π
    #3)se a == 0:
    #se b >  0 → π/2
    #se b <  0 → -π/2
    #se b == 0 → indefinido (0,0 não define ângulo)
    
    #quadrante à direita
    if a > 0:
        return arctang_taylor(b/a)
    #quadrante a esquerda
    elif a < 0:
        if b >= 0:
            return arctang_taylor(b/a) + PI
        else:
            return arctang_taylor(b/a) - PI
    #eixo vertical (a == 0)
    else:
        if b > 0:
            return PI/2
        elif b < 0:
            return -PI/2
        else:
            #ponto (0,0) não possui ângulo definido
            raise ValueError("Invalido (divisão por 0)")

def expo(x):
    # Se o número for complexo:
    if isinstance(x, complex):
        # e^(a+bi) = e^a * (cos(b) + i*sin(b)), a formula de Euler
        magnitude = expo(x.real) # e^a

        parte_real = magnitude * coss(x.imag)
        parte_imag = magnitude * seno(x.imag)
        return complex(parte_real, parte_imag)
    
    # Se o número for real:
    else:
        # Casos de e^0 (1), e^1 (e) e e^-1 (1/e):
        if x == 0: 
            return 1
        if x == 1: 
            return 2.718281828459045
        if x == -1: 
            return 0.36787944117144233
        
        # Quando x for muito grande, se utiliza uma propridade da exponenciação para "partir" o número entre duas séries...
        # e^(a + b) = e^a * e^b -> e^(a) = e^(b + (a - b)) = e^(b) * e^(a - b)
        if x > LIMITE_TAYLOR:
            # e^x = e^LIMITE_TAYLOR * e^(x - LIMITE_TAYLOR)
            return expo(LIMITE_TAYLOR) * expo(x - LIMITE_TAYLOR)
        elif x < -LIMITE_TAYLOR:
            # e^x = e^(-LIMITE_TAYLOR) * e^(x + LIMITE_TAYLOR)  
            return expo(-LIMITE_TAYLOR) * expo(x + LIMITE_TAYLOR)
        # A "partição" acima faz com que, em vez de se computar e^1000 diretamente e dar um número errado, se compute e^100 * e^900 (e e^900 como e^100 * e^800 e por aí vai)
        
        soma = 1
        termo = 1

        for i in range(1, TERMOS_TAYLOR):
            termo *=  x/i
            soma += termo

            # Rompe o loop se o termo ficar muito pequeno:
            if abs(termo) < TOLERANCIA_TAYLOR:
                break

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
        if x == 1:
            return 0
        if abs(x - 2.718281828459045) < TOLERANCIA_TAYLOR:  # Ou seja, se x = e
            return 1
        
        # Reduzindo o argumento para ter melhor precisão, usando a propriedade de que log(x) = -log(1/x). Neste caso, para quando 1/x > 0.5
        if x > 2:
            return -logn(1/x)
        
        y = x - 1
        for _ in range(TERMOS_TAYLOR):
            y -= (expo(y) - x) / expo(y)
            if abs(y) < TOLERANCIA_TAYLOR:
                break
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
# Retorna conjugado de um número complexo.
    # se x = a + bi → retorna a - bi
    
def reduzir(x):
    if abs(x) < 0.001 and x != 0:
        return f"{x:.6f}".rstrip("0").rstrip(".")
    elif abs(x) < 1:
        return f"{x:.6f}".rstrip("0").rstrip(".")
    else:
        return f"{x:.6f}".rstrip("0").rstrip(".")
 #  Formata números deixando até 6 casas decimais
    # removendo zeros desnecessários.

def ncomplexo(s):
    # Converte uma string em número complexo manualmente,
    # sem usar bibliotecas de fora, aceita formas ex. 5,-3,2.5,4i,-i,3+4i etc.
    # Lida com: sinais positivos e negativos,números com parte real, imaginária ou ambas
    # formato “i” ao invés de “j”
    
        # limpeza básica da string
    s = s.strip().replace(" ", "").lower()
    if s == "":
        raise ValueError("Entrada vazia")
    s = s.replace("j", "i")
     # valores simples
    if s == "i":
        return complex(0, 1)
    if s == "-i":
        return complex(0, -1)
    # valores com parte imagi
    if "i" in s:
         # procura o último + ou - que separa real e imagi
        idx = -1
        for i, ch in enumerate(s[:-1], start=0): 
            if (ch == "+" or ch == "-") and i != 0:
                idx = i
        # caso tenha parte real + imaginária
        if idx != -1:
            real_part = s[:idx]
            imag_part = s[idx:-1]  
            real_val = float(real_part) if real_part not in ("", "+", "-") else (0.0 if real_part=="" else float(real_part))
             # lida com casos como "2+i" e "2-i"
            if imag_part in ("+", "-"):
                imag_val = 1.0 if imag_part == "+" else -1.0
            else:
                imag_val = float(imag_part)
            return complex(real_val, imag_val)
         # formato apenas imagi
        else:
            base = s[:-1]
            if base in ("", "+"):
                return complex(0, 1)
            if base == "-":
                return complex(0, -1)
            return complex(0, float(base))
    # caso seja apenas real
    else:
        return complex(float(s), 0)
#  formata um número complexo em uma string legível
def format_complex(c):
    # função reduz dígitos que n precisam e trata casos especiais
    # como parte real ou imaginária zero
    r = reduzir(c.real) #formata real
    i = reduzir(abs(c.imag)) #formata imagi magnetitude
    # real
    if c.imag == 0:
        return r
    # imagi
    if c.real == 0:
        sign = "-" if c.imag < 0 else ""
        return sign + i + "i"
    # real+imagi
    sign = " - " if c.imag < 0 else " + "
    return f"({r}{sign}{i}i)"

class Node:
    # nó usada na arvore, Cada nó representa: um tipo (ex: 'NUM', 'OP', 'VAR')
    # um valor (ex: número, operador, nome da variável)
    #filhos esquerdo e direito (para operações binárias)   tipo num("NUM", valor=5) Node("OP",valor="+",esq=n1, dir=n2)
    #isso permite ao interpretador percorrer a expressão e avaliá-la.

    def __init__(self, tipo, valor=None, esq=None, dir=None):
        self.tipo = tipo # ex: 'NUM', 'OP', 'VAR'
        self.valor = valor  # conteúdo do nó
        self.esq = esq  #filho esquerdo
        self.dir = dir #filho direito

constantes = {}
# pi e e adicionados como constante para a facilidade do usuário:
constantes["pi"] = PI
constantes["e"] = expo(1)

def tokenize(expr):
    # converte uma expressão matemática (string) em uma lista de tokens.
    #  exemplo "3+5"  ["3", "+", "5"],
    # essa função é usada pelo parser para montar a árvore  
    # regras importantes:
    # ignora espaços
    # converte ^ para ** (potência)
    # reconhece operadores: +, -, *, /, (, )
    # reconhece funções como sen, cos, tan, ln, log10, raiz, conj
    expr = expr.strip() # remove espaços do início e fim
    tokens = [] # lista de tokens que será retornada
    i = 0  # indice atual na string 
     # lista das funções reconhecidas pelo parser
    funcs = ["sen","cos","tan","ln","log10","raiz","conj"]
    while i < len(expr):
        ch = expr[i]
        # ignora espaços dentro da expressão
        if ch.isspace():
            i += 1
            continue
        # detecta operador de potência "**" diretamente na string
        if expr.startswith("**", i):
            tokens.append("**")
            i += 2
            continue
         # permite "^" como potencia, convertendo para "**"
        if ch == "^":
            tokens.append("**")
            i += 1
            continue
         # operadores simples e parênteses
        if ch in "+-*/()":
            tokens.append(ch)
            i += 1
            continue
         # lista de possíveis nomes que representam a operação de raiz.
         # # se qualquer um deles aparecer no início da expressão, será convertido para o token padrão "raiz".
        variantes_raiz = ["sqrt", "raizq", "raizQ", "v"]
        matched_raiz = False
        #verifica se alguma variante de "raiz" aparece na posição atual `i'
        for variante in variantes_raiz:
            if expr.startswith(variante, i):
                tokens.append("raiz")  # <- normalizer para "raiz" normaliza qualquer variante encontrada para o token "raiz"
                i += len(variante)  #avança o índice pelo tamanho da palavra
                matched_raiz = True
                break
        #se encontrou uma variante de raiz, volta para o loop principal
        if matched_raiz:
            continue
        # reconhecer funções matemáticas listadas em funcs (ex: sin, cos, log)
        matched = False
        for f in funcs:
            if expr.startswith(f, i):
                tokens.append(f) # adiciona a função como token
                i += len(f) # avança o índice pelo tamanho da função
                matched = True
                break
        #se encontrou uma função, volta para o loop principal
        if matched:
            continue
        #trata números (inclui decimais, números com 'i' e porcentagens)
        if ch.isdigit() or ch == '.':
            num = ""
            #constrói o número enquanto houver dígitos ou ponto
            while i < len(expr) and (expr[i].isdigit() or expr[i] == '.'):
                num += expr[i]
                i += 1
            #verifica se o número termina com 'i' (número imaginário
            if i < len(expr) and expr[i] == "i":
                num += "i"
                i += 1
            #verifica se o número possui '%' logo depois (porcentagem)
            if i < len(expr) and expr[i] == "%":
                base = float(num.replace("i","")) / 100 #converte para porcentagem
                if "i" in num:
                    tokens.append(str(base) + "i") #caso seja número imaginário percentual
                else:
                    tokens.append(str(base)) #real percentual
                i += 1
            else:
                tokens.append(num) #numero comum
            continue
        # Identificadores formados apenas por letras (ex: x, var, abc)
        if ch.isalpha():
            ident = ""
            # Constrói o identificador enquanto houver letras contínuas
            while i < len(expr) and expr[i].isalpha():
                ident += expr[i]
                i += 1
            tokens.append(ident)
            continue
        #qualquer outro caractere é inválido
        raise ValueError(f"Caractere inválido: {ch}")
    #retorna a lista de tokens gerados
    return tokens

def nparser(expr):
    tokens = tokenize(expr)
    #soma e subtração
    def nexpressao():
        node = ntermo()
        while tokens and tokens[0] in ["+","-"]:
            op = tokens.pop(0)
            direita = ntermo()
            node = Node("op", op, node, direita)
        return node
    # multiplicação e divisão termo
    def ntermo():
        node = npotencia()
        while tokens and tokens[0] in ["*","/"]:
            op = tokens.pop(0)
            direita = npotencia()
            node = Node("op", op, node, direita)
        return node
    # potencia operador **
    def npotencia():
        node = nfator()
        if tokens and tokens[0] == "**":
            tokens.pop(0)
            node = Node("op","**",node,npotencia())
        return node
    #números, variáveis, constantes, funções e parênteses
    def nfator():
        if not tokens:
            raise ValueError("Conta incompleta")
        tok = tokens.pop(0)
        #parênteses
        if tok == "(":
            node = nexpressao()
            if not tokens or tokens.pop(0) != ")":
                raise ValueError("Parêntese não fechado")
            return node
        #constantes salvas (pi, e, ou definidas pelo usuário)
        if tok in constantes:
            return Node("num", constantes[tok])
        #funções reconhecidas
        if tok in ["sen","cos","tan","ln","log10","raiz","conj"]:
            if not tokens or tokens.pop(0) != "(":
                raise ValueError("Falta parêntese pós função")
            inside = nexpressao()
            # unario positivo
            if not tokens or tokens.pop(0) != ")":
                raise ValueError("Parêntese não fechado pós função")
            return Node("func", tok, inside)
        #unario positivo
        if tok == "+":
            return nfator()
        #unario negativo transforma em (-1)*expr
        if tok == "-":
            nodo = nfator()
            return Node("op","*", Node("num", complex(-1,0)), nodo)
        #interpreta como número complexo
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
            val = ncomplexo(entrada)  #converte string em número complexo
        except:
            raise ValueError(f"Valor inválido para variável '{nome}'")
        valores_substituidos[nome] = val
        return val, valores_substituidos
    
    if node.tipo == "func":
        # avalia o argumento da função (ex: em sen(x), avalia 'x')
        arg, valores_substituidos = evaluate(node.esq, valores_substituidos)
        #tabela de funções reconhecidas
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
        # aplica função correspondente
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
                resultado = 1
            
            # ...e o expoente for positivo, retorna 0.
            elif expoente.real > 0:
                resultado = 0
            
            # ...e o expoente for negativo, invalido:
            else:
                raise ValueError("Invalido (divisão por 0)")
        
        else:
            # E expoente for inteiro...
            if (expoente.imag == 0 and expoente.real != 0 and abs(expoente.real - round(expoente.real)) < TOLERANCIA_TAYLOR):
                # Faz a multiplicação:
                n = int(round(expoente.real))
                if n == 0:
                    resultado = 1
                elif n == 1:
                    resultado = base

                elif n > 0:
                    resultado = complex(1, 0)  # Começa com 1...
                    
                    # Repetir n vezes:
                    for _ in range(n):
                        # Multiplica resultado * base; a*c - b*d, a*d + b*c
                        resultado = complex(resultado.real*base.real - resultado.imag*base.imag, resultado.real*base.imag + resultado.imag*base.real)
                
                else: # n < 0
                    resultado = complex(1, 0)  # Começa com 1...
                    
                    # Repetir n vezes:
                    for _ in range(abs(n)):
                        # Multiplica resultado * base; a*c - b*d, a*d + b*c
                        resultado = complex(resultado.real*base.real - resultado.imag*base.imag, resultado.real*base.imag + resultado.imag*base.real)
                        
                    # Fazer o reciproco (1/resultado):
                    denom = resultado.real*resultado.real + resultado.imag*resultado.imag
                    resultado = complex(resultado.real/denom, -resultado.imag/denom)
            
            # Se o expoente for real ou complexo:
            else:
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

# Função de igualdade, compara os nós de forma recursiva:
def igual(a,b):

    # Se os dois nós forem None, são iguais:
    if a is None and b is None:
        return True
    
    # Se um nó for None e outro não, são diferentes:
    if a is None or b is None:
        return False
    
    # Se os tipos de nó são diferente, são diferente:
    if a.tipo != b.tipo:
        return False
    
    # Se os valores forem diferentes, são difernetes:
    if a.valor != b.valor:
        return False
    
    # Para o números, se compara o valor complexo de ambos diretamente:
    if a.tipo == "num":
        return a.valor == b.valor
    
    # Para variáveis, se compara o nome:
    if a.tipo == "var":
        return a.valor == b.valor
    
    # Para operações unárias, se compara as próprias operações e os seus argumentos:
    if a.tipo == "func":
        return a.valor == b.valor and igual(a.esq, b.esq)
    
    # Para operações binárias, mesma coisa mas com ambos argumentos:
    if a.tipo == "op":
        return igual(a.esq, b.esq) and igual(a.dir, b.dir)
    
    return False

while True:
#opções no terminal
    print(""" 
1 - Porcentagem
2 - Expressão aritmética
3 - Verificação de igualdade
4 - Definir constante
5 - Exibir constantes salvas
6 - Deletar constantes
"_" - Sair""")
    op = input("Escolha a opção: ")
    if op.lower() == "_":   # atalho para sair da calculadora
        break
    match op:
        case "1":
            entrada = input("Digite o número: ")
            try:
                resultado = ncomplexo(entrada)   # converte entrada para número complexo
            except Exception:
                print("Erro: número inválido")
                continue
            p_input = input("Digite a porcentagem: ")
            try:
                p = ncomplexo(p_input)           # porcentagem também aceita números complexos
            except:
                print("Erro: porcentagem inválida")
                continue

            try:
                res = resultado * (p / 100)      # cálculo da porcentagem
            except Exception:
                print("Erro no cálculo")
                continue

            print("Resultado:", format_complex(res))

        case "2":
            expr = input("Digite expressão: ")
            try:
                arv = nparser(expr)              # monta a árvore sintática da expressão
                print("Árvore LISP:", mostrar_lisp(arv))

                # evaluate retorna o valor e um dicionário contendo variáveis substituídas
                res, valores_substituidos = evaluate(arv)

                if valores_substituidos:
                    # Mostra a árvore com substituições aplicadas (se houver)
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

                # compara se as árvores são estruturalmente iguais
                print("Árvore 1:", mostrar_lisp(a1))
                print("Árvore 2:", mostrar_lisp(a2))

                iguais = igual(a1, a2)
                print("Iguais" if iguais else "São diferentes")

            except ZeroDivisionError:
                print("Erro: divisão por zero")
            except Exception as e:
                print("Erro:", e)
                # OBS: futuramente esse case pode virar um "comparar constantes"

        case "4":
            nome = input("Nome da constante: ").strip()

            if not nome.isalpha():
                print("Erro: Nome de constante deve ter apenas letras.")
                continue

            expr = input("Valor: ")

            try:
                arv = nparser(expr)
                val, _ = evaluate(arv)   # calcula valor final da constante
                constantes[nome] = val   # salva no dicionário permanente
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
                del constantes[nome]        # remove do armazenamento
                print(f"Constante '{nome}' deletada.")
            else:
                print(f"Constante '{nome}' não encontrada.")
