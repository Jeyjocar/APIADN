import streamlit as st
import pandas as pd
import altair as alt
from PIL import Image


st.set_page_config(layout='wide', page_title="ADN", page_icon=":dna:")
imagen = Image.open("ADN.gif")
st.image(imagen, width=200, caption="ADN")
st.header("Aplicación WEB de Nucleótidos")
st.subheader("Secuencia ingresada")
inputSecuencia= "DNA Query 2\nGAACACGTGGAGGCAAACAGGAAGGTGAAGAAGAACTTATCCTATCAGGACGGAAGGTCCTGTGCTCGGG\nATCTTCCAGACGTCGCGACTCTAAATTGCCCCCTCTGAGGTCAAGGAACACAAGATGGTTTTGGAAATGC\nTGAACCCGATACATTATAACATCACCAGCATCGTGCCTGAAGCCATGCCTGCTGCCACCATGCCAGTCCT"

secuenciaAdn = st.text_area("Secuencia", inputSecuencia, height=250)
secuenciaAdn = secuenciaAdn.splitlines()
secuenciaAdn = secuenciaAdn[1:]
secuenciaAdn = ''.join(secuenciaAdn)
st.write("Continuando...")
st.header("Nueva entrada")
secuenciaAdn
st.header("Resultado:")
st.subheader("Nucleótidos encontrados")

def contadorAdn(secuencia):
    d = dict([("A",secuencia.count("A")),
              ("G",secuencia.count("G")),
              ("C",secuencia.count("C")),
              ("T",secuencia.count("T"))
            ])
    return d

contadorX = contadorAdn(secuenciaAdn)
contadorX 
st.subheader("Datos")
st.write("Se encontraron: " + str(contadorX ["A"])+" Adenina")
st.write("Se encontraron: " + str(contadorX ["G"])+" Guanina")
st.write("Se encontraron: " + str(contadorX ["C"])+" Citosina")
st.write("Se encontraron: " + str(contadorX ["T"])+" Timina")
    
# creamos dataframe 

st.subheader('Tabla de Datos')
tabla = pd.DataFrame.from_dict(contadorX, orient='index')
tabla = tabla.rename({0 : 'Cantidad'}, axis='columns')
tabla.reset_index(inplace=True)
tabla = tabla.rename(columns={'index' : 'Nucleótidos'})
st.write(tabla)

st.subheader('Gráfico de Barras')
propiedad = alt.Chart(tabla).mark_bar().encode(x='Nucleótidos',y='Cantidad')
propiedad = propiedad.properties(width=alt.Step(80))
st.write(propiedad)




