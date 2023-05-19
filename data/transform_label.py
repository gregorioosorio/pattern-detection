import pandas as pd
import sys
from datetime import datetime

if len(sys.argv) < 4:
    print("Se necesita especificar una ruta de entrada, una ruta de salida y el timestamp de inicio en formato YYYYMMSSHHMMSSMMM..")
    print("Uso: python3 {} path_in path_out timestamp".format(sys.argv[0]))
    exit()

path_in = sys.argv[1]
path_out = sys.argv[2]
timestamp_start = sys.argv[3]
print("Ruta de entrada:", path_in)
print("Ruta de salida:", path_out)
print("timestamp_start:", timestamp_start)

# Leer el archivo CSV
df = pd.read_csv(path_in)

# Convertir la columna de timestamp a formato de fecha y hora con resolución de décimas de segundo
df['timestamp'] = df['timestamp'].apply(lambda x: x*1000)
df['timestamp'] = pd.to_datetime(df['timestamp'], format='%Y%m%d%H%M%S%f')

start_time = date = datetime.strptime(timestamp_start, '%Y%m%d%H%M%S%f')
# Calcular la diferencia entre los valores
df['Time (s)'] = (df['timestamp'] - start_time).dt.total_seconds()

with open(path_out, 'w') as file:
    file.write("corrupt, 0\nblinks\n")
    df.to_csv(file, 
    columns=['Time (s)', 'blink_type'], 
    index=False,  sep=',', header=False)
