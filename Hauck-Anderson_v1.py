import streamlit as st
import math
from scipy.stats import norm

def hauck_anderson_test(p1, n1, p2, n2, test_type, direction=None):
    d_hat = p1 - p2
    se_hat = math.sqrt(p1 * (1 - p1) / (n1 - 1) + p2 * (1 - p2) / (n2 - 1))
    cc = 1 / (2 * min(n1, n2))
    z = (d_hat + cc) / se_hat
    
    if test_type == "two-tailed":
        p_value = 2 * (1 - norm.cdf(abs(z)))
    else:
        if direction == "less_than":
            p_value = norm.cdf(z)
        else: # direction == "greater_than"
            p_value = 1 - norm.cdf(z)
    return p_value

st.title('Prueba de Hauck-Anderson con Corrección de Bonferroni')

p1 = st.number_input('Ingrese el porcentaje del primer grupo (como decimal, p.e. 0.5 para 50%):', min_value=0.0, max_value=1.0)
n1 = st.number_input('Ingrese el tamaño de la muestra del primer grupo:', min_value=1)
p2 = st.number_input('Ingrese el porcentaje del segundo grupo (como decimal, p.e. 0.5 para 50%):', min_value=0.0, max_value=1.0)
n2 = st.number_input('Ingrese el tamaño de la muestra del segundo grupo:', min_value=1)

test_type = st.selectbox("Seleccione el tipo de prueba", ["two-tailed", "one-tailed"])
direction = None
if test_type == "one-tailed":
    direction = st.selectbox("Seleccione la dirección", ["less_than", "greater_than"])

# Opción para incluir la corrección de Bonferroni
n_tests = st.number_input('Número de pruebas realizadas (para corrección de Bonferroni) -Agregue el número de puntos de la escala que compara-:', min_value=1, value=1)

if st.button('Calcular valor p'):
    p_value = hauck_anderson_test(p1, n1, p2, n2, test_type, direction)
    
    # Aplicar la corrección de Bonferroni al nivel de significancia deseado
    alpha = 0.05 / n_tests
    st.write(f"El valor p es: {p_value}")
    st.write(f"Nivel de significancia ajustado (α) con corrección de Bonferroni: {alpha}")

    if p_value < alpha:  # Comparar con el nivel de significancia ajustado
        st.write(f"La diferencia es estadísticamente significativa al nivel del {alpha*100}%.")
    else:
        st.write(f"La diferencia no es estadísticamente significativa al nivel del {alpha*100}%.")
