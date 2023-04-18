

# Lista de nombre de Tokens
import lex as lex
tokens  = (
    'RCALCULAR',
    'PARENTIZQ',
    'PARENTDER',
    'CORCHETIZQ',
    'CORCHETDER',
    'MAS',
    'MENOS',
    'POR',
    'DIVIDIDO',
    'DECIMAL',
    'ENTERO',
    'PTCOMA'
)

# Reglas de expresiones regulares para tokens simples
t_RCALCULAR  = r'Calcular'
t_PARENTIZQ    = r'\('
t_PARENTDER    = r'\)'
t_CORCHETIZQ    = r'\['
t_CORCHETDER    = r'\]'
t_MAS       = r'\+'
t_MENOS     = r'-'
t_POR       = r'\*'
t_DIVIDIDO  = r'/'
t_PTCOMA    = r';'

#Reglas de expresiòn regular con alguna accion
def t_DECIMAL(t):
    r'\d+\.\d+'
    try:
        t.value = float(t.value)
    except ValueError:
        print("Floaat value too large %d", t.value)
        t.value = 0
    return t

def t_ENTERO(t):
    r'\d+'
    try:
        t.value = int(t.value)
    except ValueError:
        print("Integer value too large %d", t.value)
        t.value = 0
    return t

# Caracteres ignorados
t_ignore = " \t"


def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")
    
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)
    
# Se construye el analizador léxico
lexer = lex.lex()


# Asociación de operadores y precedencia
precedence = (
    ('left','MAS','MENOS'),
    ('left','POR','DIVIDIDO'),
    ('right','UMENOS'),
    )

# Definición de la gramática usando la yacc.py
import yacc as yacc
def p_instrucciones_lista(t):
    '''instrucciones    : instruccion instrucciones
                        | instruccion '''

def p_instrucciones_evaluar(t):
    'instruccion : RCALCULAR CORCHETIZQ expresion CORCHETDER PTCOMA'
    print('El valor de la expresión es: ' + str(t[3]))

def p_expresion_binaria(t):
    '''expresion : expresion MAS expresion
                  | expresion MENOS expresion
                  | expresion POR expresion
                  | expresion DIVIDIDO expresion'''
    if t[2] == '+'  : t[0] = t[1] + t[3]
    elif t[2] == '-': t[0] = t[1] - t[3]
    elif t[2] == '*': t[0] = t[1] * t[3]
    elif t[2] == '/': t[0] = t[1] / t[3]

def p_expresion_unaria(t):
    'expresion : MENOS expresion %prec UMENOS'
    t[0] = -t[2]

def p_expresion_agrupacion(t):
    'expresion : PARENTIZQ expresion PARENTDER'
    t[0] = t[2]

def p_expresion_number(t):
    '''expresion    : ENTERO
                    | DECIMAL'''
    t[0] = t[1]

def p_error(t):
    print("Error sintáctico en '%s'" % t.value)

#Se construye el analizador sintactico
parser = yacc.yacc()


#Se analizan diferentes expresiones ingresadas en un archivo de texto o ingreso por consola
print("Seleccione si desea probar por consola (1),  o por archivo de entrada (2):")
opcion=input()
if opcion=="1":
    print("digite la cadena que va a probar")
    entrada="Calcular["+input()+"];"
    parser.parse(entrada)
elif opcion=="2":
    with open("ply/entrada.txt") as archivo:
        print()
        for linea in archivo:
            parser.parse(linea)
            print(linea)
else:
    print("Opcion no valida, fin del programa")
        
    