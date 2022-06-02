from uncertainties import ufloat as uf
from uncertainties.umath import *
from uncertainties import unumpy as un
from uncertainties.unumpy import uarray
from numpy import array
from math import pi, sqrt
from scipy import constants as const
import matplotlib.pyplot as plt
import uncertainties
import numpy as np
import math
from uncertainties import umath

def e_c(m, v):
    # energia cinética (1/2 m v**2)
    
    return (m/2)*(v**2)

def equivalentes(x, d_x, y=0, d_y=0):
    """Verifica se dois valores com incerteza são equivalentes. 
        x e d_x podem ser ou valores normais, ou ufloats (floats com incerteza), para facilitar a vida.
    """
    if type(x) == un and type(d_x) == un:
        y, d_y = d_x.n, d_x.s
        x, d_x = x.n, x.s
    
    if abs(x - y) < 2*(d_x + d_y):
        return True
    elif abs(x - y) > 3*(d_x + d_y):
        return False
    else:
        print("Inconclusive!!!")
        return None

def split_uf(n: uf):
    to_format = n.__str__()

    return to_format.split('+/-')

def lista_das_diferencas(lista):
    m = media_aritmetica(lista)
    return [l - m for l in lista]

def delta_lista(lista):
    m = media_aritmetica(lista)
    modulos = [abs(l - m) for l in lista]

    return media_aritmetica(modulos)

def media_aritmetica(lista):
    return sum(lista) / len(lista)

def coef_angular(x, y):
    ca = []
    for i in range(len(x)):
        if i > 0:
            ca.append((y[i]-y[i-1])/(x[i]-x[i-1]))

    return sum(ca)/len(ca)

def minimo_quadrado(x: np.array, y: np.array):
    # Calcula o coef. angular, coef.linear, e delta_y utilizando o metodo dos minimos quadrados.
    # x e y sao a lista de todos os dados.
    # Retorna alpha, beta, delta_y.

    xm = sum(x)/len(x)
    ym = sum(y)/len(y)

    N = len(x)

    numerador = sum([(x[i] - xm) * y[i] for i in range(N)])
    denominador = sum([(x[i] - xm)**2 for i in range(N)])

    alpha = numerador/denominador
    beta = ym - alpha*xm
    
    numerador_deltay = sum([((alpha * x[i]) + beta - y[i])**2 for i in range(N)])

    delta_y = sqrt(numerador_deltay / (N-2))
    
    delta_a = delta_y / sqrt(denominador)
    
    delta_b = sqrt(sum(x[i]**2 for i in range(N)) / (N * denominador))

    return alpha, delta_a, beta, delta_b, delta_y

def gerar_tabela_latex(*args, usar_i=True, usar_virgulas=True, notacao_cientifica=False, max_precision=None, template_string=None, ):
    """
    Generates a latex table based on the '{}' (.format) template and the other list arguments.
    If a list has uf's it is automatically unpacked into '({}+/-{})' (i.e. uncertainty,)
    
    max_precision = significant digits for floats. doesnt affect uncertainties ints
    usar_virgulas: if true, will replace '.' with ',' (for Brazilian number formatting.)
    notacao_cientifica: if true, will use scientific notation
    """

    to_print = []

    # check if the length of all arguments is the same
    lengths = {str(a): len(a) for a in args}
    for l in lengths:
        if lengths[l] != lengths[str(args[0])]:
            raise IndexError(f'The following list does not have the same length as the other lists: \n{l}')

    l = lengths[l] # set default length if the above check succeeds

    # create template string

    template_length = len(args) + (1 if usar_i else 0)

    if not template_string:
        template_string = ' & '.join(['{}' for i in range(template_length)]) + ' \\\\'

    for i in range(l):
        to_format = [i+1, ] if usar_i else []
        #to_format = [i, ] if usar_i else []
        for arg in args:
            x = arg[i]

            if type(x) in [uncertainties.core.Variable, uncertainties.core.AffineScalarFunc]:
                s = split_uf(x)
                to_append = f'${s[0]}\\pm{s[1]}$'

            elif type(x) == int:
                to_append = float(x)

            elif type(x) in (float, np.float16, np.float32, np.float64) and max_precision is not None:
                to_append = ('{:.%df}' % max_precision).format(x)

            else:
                to_append = x

            if notacao_cientifica and type(to_append) in [int, float]:
                sig, exp = ('{:.2e}'.format(to_append)).split('e')
                exp = int(exp)

                #if exp != 0:
                to_append = f'${sig} \\cdot 10^{exp}$'

                #else:
                #    to_append = f'${sig}$'


            to_format.append(to_append)

        to_print.append(template_string.format(*to_format))
        #print(to_print)
    
    if usar_virgulas:
        to_print = [s.replace('.', ',') for s in to_print]

    return '\n'.join(to_print)

def nom_ar(a):
    # nominal values for the array
    return un.nominal_values(a)

def uncert_ar(a):
    return un.std_devs(a)

def clean_nom(a):
    # clean nominal values
    return [split_uf(x)[0] for x in a]

def clean_array(a):
    # clean array
    return [x.__str__() for x in a]

def grafico_mmq(x_val, y_val, x_label, y_label, annotate=None,save=False, filename=None, return_values=False, show_margem=True, show=True, title:str=None, pulo=(0, 0.2)):
    """
    Cria um gráfico de reta linearizada utilizando o método do MMQ.

    x_val: Lista de valores no eixo x
    y_val: Lista de valores no eixo y
    x_label: Subtítulo para o eixo x
    y_label: Subtítulo para o eixo y

    annotate: Lista / array de valores que serão "anotados" ao longo de cada ponto no scatter. Seu length deve ser igual ao x_val, y_val.
    save: Salvar ou não o gráfico.
    filename: Caso for salvar o gráfico, o nome do arquivo para ser utilizado.
    show_margem: Fazer linhas com a margem de erro.
    show: Mostrar (ou não) o gráfico.
    title: O título do gráfico. Se for vazio, utiliza o título default.
    pulo: Tupla (x,y) representando o pulo do texto anotado em relação aos pontos no gráfico
    """
    alpha, delta_a, beta, delta_b, delta_y = minimo_quadrado(x_val, y_val)

    if not show:
        return alpha, delta_a, beta, delta_b, delta_y
    
    x = np.linspace(x_val[0], x_val[-1], 10)

    reta = alpha*x + beta
    reta_max = (alpha+delta_a)*x + beta + delta_y
    reta_min = (alpha-delta_a)*x + beta - delta_y

    plt.plot(x, reta, c='r', lw='1', label='Linearização (a=%.2f, b=%.2f)' % (alpha, beta))

    if show_margem:
        plt.plot(x, reta_max, c='b', ls=':', lw='1', label='Margem de erro (Δy)')
        plt.plot(x, reta_min, c='b', ls=':', lw=1)

    plt.scatter(x_val, y_val, c='black', label='Valores Discretos')
    if annotate:
        for i in range(len(x_val)):
            plt.annotate(annotate[i], (x_val[i] + pulo[0], y_val[i] + pulo[1]))

    plt.xlabel(x_label)
    plt.ylabel(y_label)

    if not title:
        pass
        #plt.title(f'Gráfico de {x_label} x {y_label}')
    else:
        plt.title(title)

    plt.legend(loc='best')
    
    if save:
        plt.savefig(fname=filename)
        
    if show:
        plt.show()


    return alpha, delta_a, beta, delta_b, delta_y

def uf_media_lista(lista) -> uf:
    """Retorna um uf, com valor nominal da média aritmética da lista, e valor de incerteza, a variação interna da lista."""
    return uf(media_aritmetica(lista).n, delta_lista(lista).n)

def open_print(title=''):
    print('\n--------------\n' + title)

def close_print():
    print('--------------\n')

g = 9.81
avo = 6.0221415000000003e+023
atm = 101325
