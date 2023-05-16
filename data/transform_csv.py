import pandas as pd

# Leer el archivo CSV
df = pd.read_csv('EEG-IO/S00_data.csv')

# Calcular la diferencia entre los valores
df['diff'] = df['timestamp'].diff()
# Evitar NaN
df['diff'] = df['diff'].fillna(0)
# Acumular los valores
df['diff'] = df['diff'].cumsum()
# Transform millisencons to seconds
df['diff'] = df['diff'] / 1000
# Convertir a formato científico
df['diff'] = df['diff'].apply(lambda x: "{:.10e}".format(x))



# Guardar los resultados en un nuevo archivo CSV
df.to_csv('EEG-IO/S00_data_t.csv', index=False)
