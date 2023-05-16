import pandas as pd
import matplotlib.pyplot as plt

# Leer el archivo CSV
df = pd.read_csv('EEG-IO/S00_data.csv')

print(df.dtypes)

# Convertir la columna de timestamp a formato de fecha y hora con resolución de décimas de segundo
df['timestamp'] = df['timestamp'].apply(lambda x: x*1000)
df['timestamp'] = pd.to_datetime(df['timestamp'], format='%Y%m%d%H%M%S%f')

# Obtener solo las columnas de valores (_V)
columnas_valores = [col for col in df.columns if col.endswith('_Q')]

# Normalizar los valores de cada sensor
for columna in columnas_valores:
    min_valor = df[columna].min()
    max_valor = df[columna].max()
    #df[columna] = (df[columna] - min_valor) / (max_valor - min_valor)
    df[columna] = (df[columna] - 8400) / 8400

# Graficar la información de cada sensor en gráficas separadas
colores = ['blue', 'orange', 'green', 'red', 'purple', 'brown', 'pink', 'gray', 'olive', 'cyan']
plt.figure(figsize=(12, 6))
num_subplots = len(columnas_valores)
for i, columna in enumerate(columnas_valores):
    plt.subplot(num_subplots, 1, i + 1)
    plt.plot(df['timestamp'], df[columna], color=colores[i % len(colores)])
    plt.xlabel('Tiempo')
    plt.ylabel('Valor')
    plt.title(columna)

plt.tight_layout()
plt.show()
