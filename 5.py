from lab_utils import *

nomes_colunas= 'amp_r_2	amp_total_2	fase_2	freq_2	amp_circ_4	amp_r_4	fase_4	freq_4	v_exp5	i_exp5'.split()

dados = read_csv('5dados.csv', 10)
amp_r_2, amp_total_2, fase_2, freq_2, amp_circ_4, amp_r_4, fase_4, freq_4, v_exp_5, i_exp_5 = dados

rc = 47.3 * 0.22e-6
amp_r_2 *= 1e-3

if 1:
    w0_esperado = 15000
    def t(w):
        return 1/(np.sqrt(1 + (1/(w*rc))**2))

    modulo_t_real = amp_r_2/amp_total_2
    print('\n'.join([f'{i}, {k}' for i,k in enumerate(modulo_t_real)]))
    eixo_x = freq_2/w0_esperado
    plt.plot(eixo_x, modulo_t_real**2, c='b')
    plt.show()

if 0:
    
    phi_esperado = np.degrees(np.arctan(1/(rc*freq_2)))
    plt.plot(freq_2, phi_esperado)
    plt.xlabel('Frequência (Hz)')
    plt.ylabel('Fase (graus)')
    plt.xscale('log')
    plt.show()

    plt.plot(freq_2, fase_2, c='b', lw=1)
    plt.scatter(freq_2, fase_2, c='r')
    plt.xlabel('Frequência (Hz)')
    plt.ylabel('Fase (graus)')
    plt.xscale('log')
    plt.show()


if 0:


    plt.plot(freq_4, fase_4, c='b', lw=1)
    plt.scatter(freq_4, fase_4, c='r')
    plt.xlabel('Frequência (Hz)')
    plt.ylabel('Fase (graus)')
    plt.xscale('log')
    plt.show()