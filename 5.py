from lab_utils import *

nomes_colunas= 'amp_r_2	amp_total_2	fase_2	freq_2	amp_circ_4	amp_r_4	fase_4	freq_4	v_exp5	i_exp5'.split()

dados = read_csv('5dados.csv', 10)
amp_r_2, amp_total_2, fase_2, freq_2, amp_circ_4, amp_r_4, fase_4, freq_4, v_exp_5, i_exp_5 = dados

rc = 47.3 * 0.214e-6
amp_r_2 *= 1e-3
R = 47.3
if 1:
    w0_esperado = (1/(rc * 2 * pi))
    def t(w):
        return 1/(np.sqrt(1 + (1/(w*rc))**2))
    modulo_t_esperado = t(freq_2*2*pi)
    modulo_t_real = amp_r_2/amp_total_2
    eixo_x = freq_2/w0_esperado
    plt.plot(eixo_x, modulo_t_esperado**2, c='r', label='Função esperada (ω0 = %.0f Hz)' % (w0_esperado/(2*pi)))
    plt.plot(eixo_x, modulo_t_real**2, c='b', label='Função real (Vr/V0)')
    plt.xlabel('ω/ω0')
    plt.ylabel('(Vr/V0)²')
    plt.legend(loc='best')
    plt.show()

if 0:
    phi_esperado = np.degrees(np.arctan(1/(rc*freq_2*2*pi)))
    #plt.plot(freq_2, phi_esperado)
    #plt.xlabel('Frequência (Hz)')
    #plt.ylabel('Fase (graus)')
    #plt.xscale('log')
    #plt.show()

    plt.plot(freq_2, phi_esperado, c='black', ls='--', label='Fase esperada')
    plt.scatter(freq_2, fase_2, c='r', label='Fase real')
    plt.xlabel('Frequência (Hz)')
    plt.ylabel('Fase (graus)')
    plt.xscale('log')
    plt.legend(loc='best')
    plt.show()


if 0:
    R #+= 12
    L = 44e-3
    w0_esperado = R/L
    freq_4 *= 2*pi
    def t(w):
        return 1/np.sqrt(1 + ((w*L)/R)**2)
    modulo_t_esperado = t(freq_4)
    modulo_t_real = amp_r_4 / amp_circ_4
    
    eixo_x = freq_4/w0_esperado
    #eixo_x = freq_4
    if 1:
        plt.plot(eixo_x, modulo_t_esperado**2, c='r', label='Função esperada (ω0 = %.0f Hz)' % (w0_esperado/(2*pi)))
        plt.plot(eixo_x, modulo_t_real**2, c='b', label='Função real (Vr/V0)')
        plt.xlabel('ω/ω0')
        #plt.xlabel('ω')
        plt.ylabel('(Vr/V0)²')
        plt.legend(loc='best')
        plt.show()

    R += 15
    phi_esperado = np.degrees(np.arctan(freq_4 * L/ R))
    plt.plot(freq_4, phi_esperado, c='black', ls='--', label='Fase esperada')
    plt.scatter(freq_4, fase_4, c='r', label='Fase real')
    #plt.plot(freq_4, fase_4, c='b', lw=1)
    plt.scatter(freq_4, fase_4, c='r')
    plt.xlabel('Frequência (Hz)')
    plt.ylabel('Fase (graus)')
    plt.xscale('log')
    plt.legend(loc='best')
    plt.show()

if 1:
    grafico_mmq(i_exp_5, v_exp_5, 'Corrente (I)', 'Tensão (V)')