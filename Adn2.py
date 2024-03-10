import pandas as pd
import streamlit as st
import altair as alt
from PIL import Image
from reportlab.pdfgen import canvas 
from io import BytesIO 


# Función para contar nuclepipótidos
def DNA_nucleotide_count(seq):
    return dict(A=seq.count('A'), T=seq.count('T'), G=seq.count('G'), C=seq.count('C'))

# Función para imprimir el diccionario
def print_dictionary(X):
    st.subheader('1. Print dictionary')
    st.write(X)
    archivo_csv = pd.DataFrame.from_dict(X,orient="index").reset_index().rename(columns={"index":"nucleotide",0:"count"})
    st.download_button("Descargar archivo csv",archivo_csv.to_csv(index=False).encode("utf-8"),file_name="Nucleotidos.csv",key="Descargar diccionario")

# Función para imprimir texto
def print_text(X):
    st.subheader('2. Print text')
    pdf_buffer = BytesIO()
    pdf = canvas.Canvas(pdf_buffer)
    pdf.drawString(100,750,"Cantidad de nucleotidos")
    posicion_ejey = 730
    for nucleotide, count in X.items():
        pdf.drawString(100,posicion_ejey,f"Se han encontrado {count} {nucleotide} nucleotidos")
        posicion_ejey -= 20
    pdf.save()
    st.download_button("Descargar pdf",pdf_buffer.getvalue(),file_name="Nucleotidos.pdf",key="Text download")
#        st.write(f'There are {count} {nucleotide} nucleotides')

# Función para mostrar DataFrame
def show_dataframe(X):
    st.subheader('3. Display DataFrame')
    df = pd.DataFrame.from_dict(X, orient='index').reset_index().rename(columns={'index': 'nucleotide', 0: 'count'})
    st.write(df)

# Función para mostrar gráfico de barras
def show_bar_chart(X):
    st.subheader('4. Grafico de Barras')
    bar_width = st.slider("Ancho de barras",min_value=1, max_value = 100,value=30)
    bar_color = st.color_picker("color de las barras",value="#cccccc")#aqui las c van con mayusculas?
    background_color = st.color_picker("Color de fonde del grafico",value="#FFFFFF")
    sort_bars = st.checkbox("Ordenar barras",value=False)
    df = pd.DataFrame.from_dict(X, orient='index').reset_index().rename(columns={'index': 'nucleotide', 0: 'count'})
    #Ordenando barras de menor a mayor
    if sort_bars:
        df=df.sort_values(by="count",ascending=False)

    chart = alt.Chart(df).mark_bar(color=bar_color).encode(
        x=alt.X('nucleotide',sort=None),
        y='count',
        tooltip=['nucleotide', 'count']
    ).properties(
        width=bar_width,  # controls width of bar.
        title='Nucleotide Count Bar Chart'
    )
    text = chart.mark_text(
        align="center",
        baseline="bottom",
        dx=0,
        dy=5
    ).encode(
        text="count:Q"
    )
    chart = (chart + text).properties(
        title = "Grafico cantidad de nucleotidos",
        width = 600,
        height = 400
    ).configure_axis(
        labelFontSize = 15,
        titleFontSize = 20
    )
    chart = chart.configure_view(
        fill = background_color
    )
    chart_html = chart.to_html()
    st.altair_chart(chart)
    st.download_button("Descargar grafico de barras",chart_html,file_name="GraficoBarras.html",key="chart download")

# Función para validar la secuencia de ADN
def is_valid_dna_sequence(sequence):
    valid_characters = set('ATGC')
    return all(char.upper() in valid_characters for char in sequence)

# Configuración de la página
image = Image.open('ADN.jpeg')
st.image(image, use_column_width=True)
st.markdown(" Nucleotidos**")

# Entrada de secuencia
st.header("Ingresar CADENA DE ADN")
sequence_inputs= "DNA Query 1\nAAGAACTTATCCTATCAGGACGGAAGGTCCTGTGCTCGGG\nATCTTCCAGACGTCGCGACTCTAAATTGCCCCCTCTGAGGTCAAGGAACACAAGATGGTTTTGGAAATGC\nTGAACCCGATACATTATAACATC"
sequences = st.text_area("Sequence input", sequence_inputs, height=250).splitlines()
validar_secuencias = [seq for seq in sequences if is_valid_dna_sequence(seq)]
if validar_secuencias:
    st.success("Secuencias validads correctamente")
    st.header("Histograma de longitudes")
    length_sequence = [len(seq) for seq in validar_secuencias]
    histograma_chart = alt.Chart(pd.DataFrame({"Length":length_sequence})).mark_bar().encode(
        alt.X("Length:Q",bin=alt.Bin(maxbins=30),title="Longitud"),
        alt.Y("count():O",title="Frecuencia"),
        tooltip=["Length:Q","count()"]
    ).properties(
        width=600,
        height=400,
        title="Histograma de secuencias ADN"
    )
    st.altair_chart(histograma_chart)
    for index,sequence in enumerate(validar_secuencias,start=1):
        st.write(f"Secuencia {index}")
        st.write(sequence)

#sequence = ''.join(sequence)

# Validar la secuencia de ADN
if is_valid_dna_sequence(sequence):
    st.success("Valid DNA sequence!")
    # Mostrar entrada de secuencia
    st.write("***\n")
    st.header('INPUT (DNA Query)')
    st.write(sequence)

# Contar nucleótidos y mostrar resultados
    st.header('OUTPUT (DNA Nucleotide Count)')
    X = DNA_nucleotide_count(sequence)


# Función para calcular el porcentaje de cada nucleótido
    def calculate_pass(X, total_Log):
        return {nucleotide: count /total_Log * 100 for nucleotide, count in X.items()}

# Obtener la longitud total de la secuencia
    total_Log = len(sequence)

# Calcular el porcentaje de cada nucleótido
    PorcentageX = calculate_pass(X, total_Log)

# Mostrar el porcentaje de cada nucleótido
    st.subheader('5. Display Nucleotide Percentage')
    for nucleotide, percentage in PorcentageX .items():
        st.write(f'The percentage of {nucleotide} is {percentage:.2f}%')

# Mostrar gráfico de pastel
    st.subheader('6. Display Pie Chart')
    df_percentage = pd.DataFrame(list(PorcentageX.items()), columns=['nucleotide', 'percentage'])
    pie_chart = alt.Chart(df_percentage).mark_circle().encode(
        alt.X('nucleotide:N', axis=alt.Axis(title='Nucleotido')),
        alt.Y('percentage:Q', axis=alt.Axis(title='Porcentaje')),
        color='nucleotide:N',
        size='percentage:Q',
        tooltip=['nucleotide', 'percentage']
    ).properties(
        title='Nucleotide Percentage Pie Chart',
        width=500,
        height=500
    )
    st.altair_chart(pie_chart)
    
#NEW VAR
    nucleotide_more_comun=max(X,key=X.get)
    quantity_comun_nucleotide=X[nucleotide_more_comun]
    st.subheader("nucleotide_more_comun")
    st.write(f"the nucleotide more comun is {nucleotide_more_comun} with a quantity of {quantity_comun_nucleotide}")
    
# FUNCTION_REVERSE_FOR_SEQUENCE
    def reversed_DNA_function(sequence):
        return sequence[::-1]
    reverse_sequence=reversed_DNA_function(sequence)
    st.subheader("Reverse Sequence")
    st.write(f"The Nucleotide reversed is {reverse_sequence}")
    
    print_dictionary(X)
    print_text(X)
    show_dataframe(X)
    show_bar_chart(X)
else:
    st.error("se quencia invalidada'A', 'T', 'G', and 'C'.")

# ACTIVIDAD DE MOSTRAR EL NUCLEOTIDO MAS COMUN
