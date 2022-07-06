from lab_utils import *

w = 1817
c = 0.103e-6
r = 100.3
l = 46.2e-3

r += 15

v0 = 9.28

# experimento 2
frequencias = array([1817,1932,2039,2108,2213,2283,2316,2340,2477,2513,2677,2752,2850,3017,3530,4303,5753])
vpp_vo = array([9.3,8.96,8.43,7.95,7.27,7.01,6.98,7.01,7.69,7.88,8.68,8.92,9.15,9.40,9.70,9.84,9.89])
vpp_vr = array([2.7,3.34,4.113,4.64,5.39,5.63,5.65,5.68,4.96,4.74,3.73,3.36,2.97,2.46,1.61,1.01,0.7])
graus_medidos = array([-70,-63.6,-54.4,-45.0,-24.6,-7,2,8.1,38.1,43.1,58.2,62.5,66.5,71.3,78.0,81.9,85])

w0 = sqrt(1/(l*c))
print(w0 / (2*pi))

def i(v, f):
    w = 2*pi*f
    return v / np.sqrt((r**2) + ( (w*l) - (1/ (w*c)) )**2 )

def phi(f):
    w = 2*pi*f
    return np.degrees(np.arctan( ((w*l)/r  ) - (1 / (w*r*c)) ))

if 0:
    # grafico phi
    if 0:
        graus_esperados = phi(frequencias)
        plt.plot(frequencias, graus_esperados, color='black', label='Fase esperada (ω0=%.0fHz)' % (w0/(2*pi)))
        plt.scatter(frequencias, graus_medidos, color='red', label='Fase real (medida)')
        plt.xlabel('Frequência (Hz)')
        plt.ylabel('Fase (graus)')
        plt.legend(loc='best')
        plt.show()

    # grafico vr/v0 

    r_int = 25.5

    eixo_y_esperado = []
    eixo_y_real = []
    for x in range(len(frequencias)):
        eixo_y_real.append( vpp_vr[x] / vpp_vo[x])

    eixo_x = np.linspace(frequencias[0], frequencias[-1], 1000)
    eixo_y_esperado = r/np.sqrt(((r + r_int) **2) + ( (eixo_x*2*pi*l) - (1/(eixo_x*2*pi*c)) )**2 )

    plt.plot(eixo_x, eixo_y_esperado, color='black', ls='--', label='Transmissão esperada (resist. interna: %.1fΩ)' % (r_int))
    plt.scatter(frequencias, eixo_y_real, color='red', label='Transmissão real')

    plt.xlabel('Vr/V0')
    plt.ylabel('Frequência (Hz')
    plt.legend(loc='best')
    plt.show()

#exp 4
L = 10.4e-3

caps = array([1.015e-6, 0.68e-6, c, 50.7e-9, 21.8e-9])
freqs = array([1560, 1900, 4830, 6990, 10620])

if 1:
    eixo_x = (L * caps) ** (-0.5)
    eixo_y = freqs * 2 *pi
    grafico_mmq(eixo_x, eixo_y, '(LC)**(-0.5)', 'Frequência (Rad/s)')