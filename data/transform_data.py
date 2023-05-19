import pandas as pd
import sys

if len(sys.argv) < 3:
    print("Se necesita especificar una ruta de entrada y una ruta de salida.")
    print("Uso: python3 {} path_in path_out".format(sys.argv[0]))
    exit()

path_in = sys.argv[1]
path_out = sys.argv[2]
print("Ruta de entrada:", path_in)
print("Ruta de salida:", path_out)

# Leer el archivo CSV
df = pd.read_csv(path_in)

# Convertir la columna de timestamp a formato de fecha y hora con resolución de décimas de segundo
df['timestamp'] = df['timestamp'].apply(lambda x: x*1000)
df['timestamp'] = pd.to_datetime(df['timestamp'], format='%Y%m%d%H%M%S%f')

start_time = df['timestamp'][0]
# Calcular la diferencia entre los valores
df['Time (s)'] = (df['timestamp'] - start_time).dt.total_seconds()
# Acumular los valores
# df['Time (s)'] = df['Time (s)'].cumsum()
# Convertir a formato científico
df['Time (s)'] = df['Time (s)'].apply(lambda x: "{:.10e}".format(x))

# Obtener solo las columnas de valores
columnas_valores = [col for col in df.columns if col.endswith('_V')]

# Normalizar los valores de cada sensor
for columna in columnas_valores:
    # 8400: Rango de los Emotiv Epoc+
    # df[columna] = (df[columna] - 8400) / 8400.0
    df[columna] = (df[columna] - df[columna].mean()) / df[columna].std()
    df[columna] = df[columna].apply(lambda x: "{:.10e}".format(x))

df['Sampling Rate'] = 200

df.to_csv(path_out, 
#columns=['Time (s)', 'F3_V', 'FC6_V', 'P7_V', 'T8_V', 'F7_V', 'F8_V', 'T7_V', 'P8_V', 'AF4_V', 'F4_V', 'AF3_V', 'O2_V', 'O1_V', 'FC5_V', 'Sampling Rate'], 
columns=['Time (s)', 'AF3_V', 'AF4_V', 'Sampling Rate'], 
index=False,  sep=';')
