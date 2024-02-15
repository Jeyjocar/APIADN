#APP para análisis de ADN
import pandas as pd
import streamlit as st
import altair as alt
from PIL import Image

# Función para contar nucleótidos
def DNA_nucleotide_count(seq):
    return dict(A=seq.count('A'), T=seq.count('T'), G=seq.count('G'), C=seq.count('C'))

# Función para imprimir el diccionario
def print_dictionary(X):
    st.subheader('1. Quantity Nuclotides')
    st.write(X)

# Función para imprimir texto
def print_text(X):
    st.subheader('2. Print text')
    for nucleotide, count in X.items():
        st.write(f'There are {count} {nucleotide} nucleotides')

# Función para mostrar DataFrame
def show_dataframe(X):
    st.subheader('3. Display DataFrame')
    df = pd.DataFrame.from_dict(X, orient='index').reset_index().rename(columns={'index': 'nucleotide', 0: 'count'})
    st.write(df)

# Función para mostrar gráfico de barras
def show_bar_chart(X):
    st.subheader('4. Grafico de Barras')
    df = pd.DataFrame.from_dict(X, orient='index').reset_index().rename(columns={'index': 'nucleotide', 0: 'count'})
    chart = alt.Chart(df).mark_bar().encode(
        x='nucleotide',
        y='count',
        tooltip=['nucleotide', 'count']
    ).properties(
        width=alt.Step(80),  # controls width of bar.
        title='Nucleotide Count Bar Chart'
    )
    st.altair_chart(chart)

# Función para validar la secuencia de ADN
def is_valid_dna_sequence(sequence):
    valid_characters = set('ATGC')
    return all(char.upper() in valid_characters for char in sequence)

# Configuración de la página
image = Image.open('ADN.jpeg')
st.image(image, use_column_width=True)
st.markdown("# Nucleotidos")

# Entrada de secuencia
st.header("Ingresar CADENA DE ADN")
sequence_input = ">DNA Query 2\AAGAACTTATCCTATCAGGACGGAAGGTCCTGTGCTCGGG\nATCTTCCAGACGTCGCGACTCTAAATTGCCCCCTCTGAGGTCAAGGAACACAAGATGGTTTTGGAAATGC\nTGAACCCGATACATTATAACATC"
sequence = st.text_area("Sequence input", sequence_input, height=250).splitlines()[1:]
sequence = ''.join(sequence)

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
    PorcentajeX = calculate_pass(X, total_Log)

    # Mostrar el porcentaje de cada nucleótido
    st.subheader('5. Display Nucleotide Percentage')
    for nucleotide, percentage in PorcentajeX .items():
        st.write(f'The percentage of {nucleotide} is {percentage:.2f}%')

    # Mostrar gráfico de pastel
    st.subheader('6. Display Pie Chart')
    df_percentage = pd.DataFrame(list(PorcentajeX.items()), columns=['nucleotide', 'percentage'])
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
    
    #Nucleótido más común
    nucleotide_more_comun=max(X,key=X.get)
    quantity_comun_nucleotide=X[nucleotide_more_comun]
    st.subheader("Nucleotido más Común")
    st.write(f"El Nucleotido más común es {nucleotide_more_comun} con una cantidad de: {quantity_comun_nucleotide} repeticiones")

    
    #Función para invertir la secuencia de ADN
    def reversed_DNA_function(sequence):
        return sequence[::-1]
    reverse_sequence=reversed_DNA_function(sequence)
    st.subheader("Secuencia de ADN invertida")
    st.write(f"The Nucleotide reversed is {reverse_sequence}")
    
    
    print_dictionary(X)
    print_text(X)
    show_dataframe(X)
    show_bar_chart(X)
else:
    st.error("Secuencia invalidada 'A', 'T', 'G', and 'C'.")
