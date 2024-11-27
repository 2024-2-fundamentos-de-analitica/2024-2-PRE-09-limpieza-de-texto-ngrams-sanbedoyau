'''Taller evaluable presencial'''

import pandas as pd
from string import punctuation

def load_data(input_file: str):
    '''Carga del archivo a un DataFrame (aunque en este caso es un DataSet)'''
    df = pd.read_csv(input_file)
    return df

def create_key(df: pd.DataFrame, n: int):
    '''Crea una nueva columa que contiene el key de la columna "text" en el Dataframe'''
    df = df.copy()
    df['key'] = df['text']              # Copia la columna 'text' a la columna 'key'
    df['key'] = df['key'].str.strip()   # Remueve los espacios en blanco al principio y al final de la cadena
    df['key'] = df['key'].str.lower()   # Convierte el texto a minúsculas

    df['key'] = df['key'].str.translate(# Elimina todos los signos de puntuación 
        str.maketrans('', '', f'{punctuation}') 
    )


    df['key'] = df['key'].str.replace(' ', '')  # Texto sin espacios en blanco
    df['key'] = df['key'].map(
        lambda x: [x[t : t + n - 1] for t in range(len(x))],    # Convierta el texto a una lista de n-gramas
    )
    df['key'] = df['key'].apply(lambda x: sorted(set(x)))       # Ordene la lista de n-gramas y remueve duplicados
    df['key'] = df['key'].str.join('')          # Convierta la lista de ngramas a una cadena
    return df

def generate_cleaned_column(df: pd.DataFrame):
    '''Crea la columna "cleaned" en el DataFrame'''
    df = df.copy()
    df = df.sort_values(by = ['key', 'text'], ascending = [True, True]) # Ordena el dataframe por 'key' y 'text'
    keys = df.drop_duplicates(subset = 'key', keep = 'first')           # Selecciona la primera fila de cada grupo en 'key'
    key_dict = dict(zip(keys['key'], keys['text']))     # Crea un diccionario con la raiz de las palabras y la primera ocurrencia de esta en la columna 'text'
    df['cleaned'] = df['key'].map(key_dict)       # Crea la nueva columna 'cleaned' con el diccionario
    return df

def save_data(df: pd.DataFrame, output_file: str):
    '''Guarda el DataFrame en un archivo'''
    df = df.copy()
    df = df[['cleaned']]
    df = df.rename(columns = {'cleaned': 'text'})
    df.to_csv(output_file, index = False)

#
# Orquestador
#
def main(input_file: str, output_file: str, n: int = 2):
    '''Ejecuta la limpieza de datos'''

    df = load_data(input_file)
    df = create_key(df, n)
    df = generate_cleaned_column(df)
    df.to_csv('files/output/test.csv', index = False)
    save_data(df, output_file)


if __name__ == '__main__':
    main(
        input_file='files/input/input.txt',
        output_file='files/output/output.txt',
    )
