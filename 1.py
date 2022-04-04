from lab_utils import *

incerteza_ma = 0.1
incerteza_volts = 0.01

resist = {
    # Resistores. 1a coluna = resistencia. 2a coluna = mA, 3a = V (volts)
    '1k': 
    [
        1000,
        [2.3, 3.4, 4.9, 6.1, 7.2, 8.1, 8.9, 10.2, 11.6, 12.5],
        [2.3, 3.36, 4.86, 6.08, 7.06, 7.95, 8.76, 10.02, 11.35, 12.28]
    ],
    '820':
    [
        820,
        [1.5, 2.3, 3.3, 4.2, 5.5, 6.5, 7.2, 8.3, 9.1, 10.4],
        [1.25, 1.93, 2.77, 3.49, 4.56, 5.40, 5.98, 6.88, 7.99, 8.52]
    ],

    '1.5k':
    [
        1500,
        [1, 2.2, 3.3, 4.2, 5.2, 6.6, 7.5, 8.3, 9.7, 10.6],
        [1.54, 3.42, 5.15, 6.58, 7.96, 10.11, 11.28, 12.81, 14.80, 16.05]
    ]   
}


led_ma = array([0, 0, 0, 0.01, 0.28, 1.14, 2.28, 3.10, 3.80, 4.50, 5.54, 6.5, 11.5])
led_v = array([1.31, 1.4, 1.52, 1.6, 1.7, 1.86, 1.88, 1.90, 1.92, 1.94, 1.96, 1.98, 2.08])

incandescente_ma = array([
    8.8, 16.5, 17.6, 22.1, 23.5, 25.0, 27.2, 30.6, 35.2, 43.7, 51.7, 59.0, 72.5, 76.4, 82.8])
incandescente_v = array([
    0.1, 0.34, 0.50, 0.78, 0.90, 1.18, 1.42, 1.71, 2.19, 3.19, 4.28, 5.41, 7.77, 8.53, 9.81])

#print(gerar_tabela_latex(incandescente_ma, incandescente_v, usar_i=False))

for r in resist:
    resistencia, ma, v = resist[r]
    ma = 1e-3 * array(ma)
    #grafico_mmq(ma, v, 'Corrente (A)', 'Volts (V)', title='Gráfico da resistência %s ohms' % resistencia)

# teste lampada incandescente
if 0:
    incandescente_ma = 1e-3 * incandescente_ma
    alpha, delta_a, beta, delta_b, delta_y = minimo_quadrado(incandescente_ma[:5], incandescente_v[:5])
    mmq2 = minimo_quadrado(incandescente_ma[1:8], incandescente_v[1:8])
    x = np.linspace(incandescente_ma[0], incandescente_ma[-1], 10)
    a2, b2 = mmq2[0], mmq2[2]
    reta = alpha*x + beta
    reta2 = a2*x + b2


    plt.plot(x, reta, c='r', lw='1', label='Linearização para v<1(a=%.2f, b=%.2f)' % (alpha, beta))
    plt.plot(x, reta2, c='g', lw='1', label='Linearização para 0.1<v<2.20(a=%.2f, b=%.2f)' % (a2, b2))

    plt.plot(incandescente_ma, incandescente_v, ls=':')
    plt.scatter(incandescente_ma, incandescente_v, c='black', label='Valores reais')
    plt.xlabel('corrente (A)')
    plt.ylabel('voltagem (V)')
    plt.legend(loc='best')
    plt.title("Gráfico de I x V para a lâmpada incandescente.")
    plt.show()

    resistencias = incandescente_v / incandescente_ma
    grafico_mmq(incandescente_ma, resistencias, 'corrente (A)', 'resistência (V/I) [Ω]', annotate=['%sV' % v for v in incandescente_v],
    pulo=(0,5))
    grafico_mmq(incandescente_ma[5:], resistencias[5:], 'corrente (A)', 'resistência (V/I) [Ω]', annotate=['%sV' % v for v in incandescente_v[5:]],
    title='Gráfico de I x V/I a partir de V>1.20', pulo=(0,2))

# led
if 0:
    led_ma *= 1e-3
    plt.plot(led_ma, led_v, ls=':')
    plt.scatter(led_ma, led_v, c='black', label='Valores Reais')
    plt.xlabel('corrente (A)')
    plt.ylabel('voltagem (V)')
    plt.legend(loc='best')
    #plt.xscale('log')
    plt.title("Gráfico de IxV para lâmpada LED (diodo).")
    plt.show()


# aluminio

incert_x = 1
incert_mv_al = 0.1
x_aluminio = array([4, 8, 12, 16, 20, 24, 28, 32, 36, 41, 44, 48, 52, 56, 60])
mV_aluminio = array([0.1, 0.4, 0.7, 1, 1.3, 1.6, 2.1, 2.4, 2.9, 3.3, 4.1, 4.9, 5.8, 6.7, 7.6])
espessura_aluminio = 0.09

x_al = nom_ar(x_aluminio)
mv_al = nom_ar(mV_aluminio)

plt.plot(x_al, mv_al, ls=':')
plt.scatter(x_al, mv_al, c='black', label='Valores Discretos')
plt.xlabel('posição (x, cm)')
plt.ylabel('tensão (mV)')
plt.axvline(20, color='k', linestyle='--')
plt.axvline(40, color='k', linestyle='--')
plt.axvline(0, color='k', linestyle='--')
plt.text(0, 2, 'início (L=3cm)', ha='center', va='center',rotation='vertical', backgroundcolor='white')
plt.text(20, 4, '20cm (L=2cm)', ha='center', va='center',rotation='vertical', backgroundcolor='white')
plt.text(40, 6, '40cm (L=1cm)', ha='center', va='center',rotation='vertical', backgroundcolor='white')

locs = {3: 20, 2: 41, 1: 60}
colors = {3: 'r', 2:'g', 1: 'pink'}
loc_prev = 0
for i in range(0): # vai de 3 -> 2 -> 1
    until = x_aluminio.tolist().index(locs[i])
    alpha, delta_a, beta, delta_b, delta_y = minimo_quadrado(x_aluminio[loc_prev:until+1], mV_aluminio[loc_prev:until+1])
    x = np.linspace(x_aluminio[loc_prev], x_aluminio[until], 10)
    reta = alpha*x + beta
    reta_max = (alpha+delta_a)*x + beta + delta_y
    reta_min = (alpha-delta_a)*x + beta - delta_y

    plt.plot(x, reta, c=colors[i], lw='1', label='Linearização para %scm (a=%.2f, b=%.2f)' % (i, alpha, beta))
    plt.plot(x, reta_max, c='b', ls=':', lw='1')
    plt.plot(x, reta_min, c='b', ls=':', lw=1)
    loc_prev = until
    

plt.title("Gráfico de posição x tensão")


plt.legend(loc='best')


plt.show()