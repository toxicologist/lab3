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

# grafico: carga 1
#plt.plot(carga1_t, carga1_v)
#plt.show()

lnd = np.log(descarga_v)

a, da, b, db, dy = grafico_mmq(descarga_t, lnd, 'tempo (s)', 'Ln(V)', title=' ')
R = 47e3
alpha = uf(a, da)
c = -1/(R*alpha)


graf_x = np.linspace(descarga_t[0], descarga_t[-1], 1000)
graf_y = (np.e**(b)) * (np.e**(-graf_x/(R*c.n)))
plt.xlabel('Tempo (s)')
plt.ylabel('Voltagem (V)')
plt.plot(graf_x, graf_y, c='r', label='Equação Aproximada')
plt.scatter(descarga_t, descarga_v, c='black', label='Valores Reais')
plt.legend(loc='best')
plt.show()