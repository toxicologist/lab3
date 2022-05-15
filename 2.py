from lab_utils import *

na = nom_ar

# exp da bateria
mvc_bat = uarray(
    [
        0,
        205,
        411,
        607,
        754,
        828,
        910,
        993,
        1037,
        870,
        1263,
        1358,
        1406,
        1436,
        1467,
        1487,
        1497,
        1498,
    ],
    1,
)
mvi_bat = uarray(
    [
        138.8,
        120.6,
        102.4,
        85.1,
        72.1,
        65.7,
        56.5,
        51.1,
        47.3,
        62,
        27.3,
        19.1,
        14.8,
        12.2,
        9.4,
        7.8,
        6.8,
        6.7,
    ],
    0.1,
)

ma_i = mvi_bat / 4.7  # mA
rc = mvc_bat / ma_i  # ohm
a_i = ma_i * 1e-3
pc = rc * (a_i ** 2)
ponto_troca = list(nom_ar(mvc_bat)).index(
    870
)  # ponto onde ocorre a troca dos potenciometros

pc_100 = pc[:ponto_troca]
rc_100 = rc[:ponto_troca]
pc_1k = pc[ponto_troca:]
rc_1k = rc[ponto_troca:]

x1, y1 = na(rc_100), na(pc_100)
x2, y2 = na(rc_1k), na(pc_1k)

mvc_ordenado = np.array(
    [
        0,
        205,
        411,
        607,
        754,
        828,
        
        870,
        1263,
        1358,
        1406,
        1436,
        1467,
        1487,
        1497,
        1498,
    ]
)
mvi_ordenado = np.array(
    [
        138.8,
        120.6,
        102.4,
        85.1,
        72.1,
        65.7,
        62,
        27.3,
        19.1,
        14.8,
        12.2,
        9.4,
        7.8,
        6.8,
        6.7,
    ]
)
a_i = (mvi_ordenado / 4.7) * 1e-3
curva_x = mvc_ordenado / (a_i * 1e3)
curva_y = curva_x * (a_i ** 2)

if 1:
    plt.plot(x1, y1)
    plt.plot(x2, y2, color='green')
    plt.plot(curva_x, curva_y, color='red', ls=':')

    plt.scatter(list(x1)+list(x2), list(y1)+list(y2), c='black', label='Valores Discretos')
    plt.ylabel("Pc (W)")
    plt.xlabel("Rc (Ohm)")
    plt.title("Gráfico de Rc x Pc")
    plt.show()

ri = uf(55, 6)

# gráfico de n x (rc/ri)
rc = (mvc_ordenado*1e-3) / a_i  # ohm
pc = rc * (a_i ** 2)

pc = nom_ar(pc)
rc = nom_ar(rc)
pi = ri.n * (( (mvi_ordenado * 1e-3 )/4.7)**2)
n = pc / (pc + pi)
plt.plot(rc/ri.n, n)
plt.scatter(rc/ri.n, n, color='black', label='Valores Reais')
plt.xlabel("Rc/Ri")
plt.ylabel("Eficiência")
plt.title("Gráfico da Eficiência x Rc/Ri")
plt.show()

ptmax = max(pi + pc)

plt.plot(rc/ri.n, pi/ptmax, color='blue', label='Pi/Ptmax')
plt.plot(rc/ri.n, pc/ptmax, color='red', label='Pc/Ptmax')
plt.plot(rc/ri.n, np.absolute((pi/ptmax) + (pc/ptmax)), color='green', label='|(Pi/Ptmax) + (Pc/Ptmax)|')
plt.xlabel("Rc/Ri")
plt.ylabel("Potência (W)")
plt.title("Gráfico das três curvas de potência")
plt.legend(loc='best')
plt.show()

print(gerar_tabela_latex(mvc_bat, mvi_bat, usar_i=False))