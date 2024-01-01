import gpxpy
import pandas as pd
from gpxfunctions import calculate_distance

archivo = input("Nombre de Archivo para geestionar:")
ruta= archivo + ".gpx"

latitudes = []
longitudes = []
altitudes = []
tiempo = []

path = "rutas_gpx\\" + ruta

# Leer un archivo GPX
with open(path, "r") as gpx_file:
    gpx = gpxpy.parse(gpx_file)

#Acceder a puntos de ruta (waypoints), rutas (tracks), pistas (routes), etc.

for track in gpx.tracks:
   for segment in track.segments:
        for point in segment.points:
            latitudes.append(point.latitude)
            longitudes.append(point.longitude)
            altitudes.append(point.elevation)
            tiempo.append(point.time.replace(tzinfo=None))

# Crear un DataFrame de pandas con los datos

data = {'Latitud': latitudes, 'Longitud': longitudes, 'Altitud': altitudes}
df = pd.DataFrame(data)

# Añadir columna desnivel acumulado

desnivel = []

Altitud_Anterior = df['Altitud'].shift()
Latitud_Anterior = df['Latitud'].shift()
Longitud_Anterior = df['Longitud'].shift()


df['LatitudAnterior'] = Latitud_Anterior
df['LongitudAnterior'] = Longitud_Anterior
df['AltitudAnterior'] = Altitud_Anterior
df['Tiempo'] = tiempo
df['Hora'] = df['Tiempo'].dt.strftime('%H:%M:%S')
df['DesnivelSuperado'] = df['Altitud'] - df['AltitudAnterior']

Distancias = []

for x in range(0,len(df)):
    distancia = calculate_distance(df['LatitudAnterior'][x],df['LongitudAnterior'][x],df['Latitud'][x],df['Longitud'][x])
    print(distancia)
    Distancias.append(distancia)
    
    

   
df['DistanciaRecorrida'] = Distancias 

print(df['DistanciaRecorrida'])


nombre = "rutas_xlsx\\" + archivo + ".xlsx"


# Guardar el dataframe en un archivo de Excel
df.to_excel(nombre, index=False) 

# Sumar los valores de 'columna' que cumplen con la condición
condicion = df['DesnivelSuperado'] > 0
altura_acumulada = df.loc[condicion, 'DesnivelSuperado'].sum()

distancia_recorrida = df['DistanciaRecorrida'].sum()

print(altura_acumulada)
print(distancia_recorrida)

           


