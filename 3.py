from lab_utils import *
import csv

# importando dados do csv

dados = {}

for i in range(10):
    dados[i] = []

with open('3dados.csv', newline='') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        for i in range(10):
            if row[i] != '':
                dados[i].append(float(row[i]))

#from pprint import pprint
#pprint(dados)

# criando arrays dos dados
carga1_v, carga1_t, descarga_v, descarga_t, carga2_v, carga2_t, carga3_v, carga3_t, carga4_v, carga4_t = [np.array(x) for x in dados.values()]



# grafico: descarga
if 0:
    print(gerar_tabela_latex(descarga_t, descarga_v, usar_i=False, max_precision=2))

    lnd = np.log(descarga_v)

    a, da, b, db, dy = grafico_mmq(descarga_t, lnd, 'tempo (s)', 'Ln(V)', title=' ')
    R = 47e3
    alpha = uf(a, da)
    c = -1/(R*alpha)
    print("C obtido:", c)


    graf_x = np.linspace(descarga_t[0], descarga_t[-1], 1000)
    graf_y = (np.e**(b)) * (np.e**(-graf_x/(R*c.n)))
    plt.xlabel('Tempo (s)')
    plt.ylabel('Voltagem (V)')
    plt.plot(graf_x, graf_y, c='r', label='Equação Aproximada')
    plt.scatter(descarga_t, descarga_v, c='black', label='Valores Reais')
    plt.legend(loc='best')
    plt.show()

# grafico: carga 1
carga1_t -= 6.8
carga2_t -= 1.4
carga3_t -= 1.7
carga4_t -= 3.4

# Calculando valor dos capacitores

if 0:
    i = 0
    for tempo, voltagem in zip([carga1_t, carga2_t, carga3_t, carga4_t], [carga1_v, carga2_v, carga3_v, carga4_v]):
        i += 1

        print(i, ':')
        print(gerar_tabela_latex(tempo, voltagem, usar_i=False, max_precision=2))
        print('\n\n')

        carga_t = uarray(tempo, 0.1)
        carga_v = uarray(voltagem, 0.03)
        v0 = uf(10, 0.2)
        r = uf(47e3, (47e3) * 0.05) if i != 4 else uf(10e3, (10e3) * 0.05)
        lny = un.log((v0 - carga_v) / v0)
        lista_cs = (-carga_t/r) * (1/lny)
        c = uf_media_lista(lista_cs)
        print(f'\n-------\n{i}:\n{c}')

        continue
        # graficando a curva de carga
        eixo_x = np.linspace(tempo[0], tempo[-1], 1000)
        eixo_y = v0.n * (1 - np.e**(-eixo_x/(r.n*c.n))) if i != 3 else 3.56 * (1 - np.e**(-eixo_x/(r.n*(1/6)*c.n)))
        plt.plot(tempo, voltagem, label='Valores Medidos')
        plt.scatter(tempo, voltagem, c='black', label='Valores Discretos')
        plt.plot(eixo_x, eixo_y, label='Aproximação Numérica', ls="--", lw=2)
        plt.legend(loc='best')
        plt.xlabel('Tempo (s)')
        plt.ylabel('Voltagem (V)')
        plt.savefig(fname=f'cap_{i}_com_aprox')
        plt.show()

        plt.plot(tempo, voltagem, label='Valores Medidos')
        plt.scatter(tempo, voltagem, c='black', label='Valores Discretos')
        plt.legend(loc='best')
        plt.xlabel('Tempo (s)')
        plt.ylabel('Voltagem (V)')
        plt.savefig(fname=f'cap_{i}_valores')
        plt.show()


# experimentos 4 e 5
vi = uf(10.25, 0.3)
c1 = uf(192.7, 10) * 1e-6
c2 = uarray([192.7, 101.4, 9.97, 3.26, 1.01], 10) * 1e-6
vf = uarray([4.44, 6.80, 9.86, 10.11, 10.18], 0.2)

energia_inicial = 0.5*c1*(vi**2)
carga_inicial = c1*vi
energias_finais = []
cargas_finais = []

for i in range(len(c2)):
    energia_final = 0.5*(vf[i]**2)*(c2[i] + c1)
    carga_final = vf[i] * (c1 + c2[i])
    energias_finais.append(energia_final)
    cargas_finais.append(carga_final)

energias_finais = array(energias_finais)
cargas_finais = array(cargas_finais)

print(gerar_tabela_latex(
    [192.7] * 5,
    [192.7, 101.4, 9.97, 3.26, 1.01],
    [vi.n] * 5,
    [4.44, 6.80, 9.86, 10.11, 10.18],
    [energia_inicial * 1e3] * 5,
    energias_finais * 1e3,
    [carga_inicial *1e3] * 5,
    cargas_finais * 1e3,
    notacao_cientifica = True,
    usar_i = False,
    max_precision=2
))

eixo_x = nom_ar(c2) / c1.n
eixo_y = [x.n / energia_inicial.n for x in energias_finais]
grafico_mmq(eixo_x, eixo_y, 'Razão entre C2 e C1', 'Razão entre energias', title=' ')
plt.show()