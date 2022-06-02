from lab_utils import *

i_calib = uarray([0.10, 0.24, 0.35, 0.49, 0.60, 0.75, 0.85, 1, 1.10, 1.25], 0.01)
v_hall = uarray([0.18, 0.434, 0.60, 0.865, 1.05, 1.314, 1.48, 1.771, 1.930, 2.19], 0.01) - 8.5e-3
n_solenoide = 760
L_solenoide = uf(0.15, 0.01)

#grafico_mmq(nom_ar(i_calib), nom_ar(v_hall), 'Corrente (A)', 'Tensão Hall (V)')

def b_solenoide(i, n, mu0, L, R, z):
    return mu0*n*i* L/ sqrt( ((L/2)**2) + R**2)*0.5

Rzao = 70.5 * 1e-3 / 2
rzinho = 45 * 1e-3 / 2
R_medio = (Rzao - rzinho)/2 + rzinho

campo_magnetico_calib = array([b_solenoide(i.n, n_solenoide, const.mu_0, L_solenoide.n, R_medio, 0) for i in i_calib]) *1e3

a, da, b, db, dy = grafico_mmq(nom_ar(v_hall), campo_magnetico_calib, 'Tensão Hall (V)', 'Campo Magnético (mT)', show=False)
#coef_sonda = uf(a, da) *1e-3 # T/V
coef_sonda = uf(1/280, 1/10)

# dados outros experimentos
#3.1 bobina

D_bobina = 0.292
r_bobina = 0.146
vbobina = array([25, 33, 45, 61, 75, 83, 78, 65, 50, 37, 27]) * 1e-3
dbobina = np.linspace(-17.5, 17.5, len(vbobina)) *1e-2

# fio infinito
nfio = 30
ifio = 1.2

vfio = array([54.4,29.7,24.3,20.9,18.8,17.5,16.8,15.6,15.3,15,14.7,14.7]) * 1e-3
dfio = np.linspace(1.5, 18, len(vfio)) * 1e-2

campo_fio_esperado = 30 * ( 1 / (2*pi)) * const.mu_0 * ifio * (1/dfio)
campo_fio_real = vfio * coef_sonda.n

if 1:
    plt.plot(dfio, campo_fio_esperado, label='Campo Esperado')
    plt.plot(dfio, campo_fio_real, label='Campo Real')
    plt.xlabel("Distancia (m)")
    plt.ylabel("Campo (T)")
    plt.legend(loc='best')
    plt.show()


# 3.2 helmholtz
vhelm = array([35.6,46.3,55.9,61.4,63.1,63,60,52.2,41.0,31.4,24.6])
dhelm = np.linspace(-17.5, 17.5, len(vhelm))

# anti helmholtz
vantihelm = array([-13.6,-19.2,-21.9,-18.1,-6,9,24.2,32.8,32.8,27.8,22.9,17.2])
dantihelm = np.linspace(-17.5, 21, len(vantihelm))


