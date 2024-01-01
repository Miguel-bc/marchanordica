import pandas as pd
import gpxpy

from geopy.distance import geodesic

class dfgpx:
    
    def __init__(self, gpxfile):
        
        with open(gpxfile, "r") as gpx_file:
            gpx = gpxpy.parse(gpx_file)
        
        # Definir columnas del dataframe
        
        latitudes = []
        longitudes = []
        altitudes = []
        tiempo = []
        
        
        #Acceder a puntos de ruta (waypoints), rutas (tracks), pistas (routes), etc.

        for track in gpx.tracks:
            for segment in track.segments:
                    for point in segment.points:
                        latitudes.append(point.latitude)
                        longitudes.append(point.longitude)
                        altitudes.append(point.elevation)
                        tiempo.append(point.time.replace(tzinfo=None))
                        
        # Crear un DataFrame de pandas con los datos

        data = {
                'Latitud': latitudes, 
                'Longitud': longitudes, 
                'Altitud': altitudes, 
                'Tiempo': tiempo,            
                }
       
       
        df = pd.DataFrame(data)
        
        # Agregar a cada fila del dataframe los datos inmediatamente anteriores
      
        Latitud_Anterior = df['Latitud'].shift()
        Longitud_Anterior = df['Longitud'].shift()
        Altitud_Anterior = df['Altitud'].shift()
        Tiempo_Anterior = df['Tiempo'].shift()


        df['LatitudAnterior'] = Latitud_Anterior
        df['LongitudAnterior'] = Longitud_Anterior
        df['AltitudAnterior'] = Altitud_Anterior
        df['TiempoAnterior'] = Tiempo_Anterior
        
        # Agregar nuevas columnas con los calculos deseados
        
        df['DesnivelSuperado'] = df['Altitud'] - df['AltitudAnterior']
        
        df['Hora'] = df['Tiempo'].dt.strftime('%H:%M:%S')
        df['HoraAnterior'] = df['TiempoAnterior'].dt.strftime('%H:%M:%S')
        
        # Convertir las columnas 'Hora' y 'HoraAnterior' a objetos datetime
        
        df['Hora'] = pd.to_datetime(df['Hora'], format='%H:%M:%S')
        df['HoraAnterior'] = pd.to_datetime(df['HoraAnterior'], format='%H:%M:%S')
        
       
        df['TiempoTranscurrido'] = (df['Hora'] - df['HoraAnterior']).dt.total_seconds()
        
        self.df = df
        
    def calculate_distance(lat1,lon1,lat2,lon2):
    
        try:
            
            # Obtener las coordenadas de los puntos
            coords_anterior = (lat1, lon1)
            coords_actual = (lat2, lon2)

            # Calcular la distancia entre los dos puntos
            distancia = geodesic(coords_anterior, coords_actual).meters
            
            return distancia
        
        except ValueError as e:
            
            return 0
        
    def desnivel_acumulado(self, unit):
        
        # Sumar los valores de 'columna' que cumplen con la condición
        
        condicion = self.df['DesnivelSuperado'] > 0
        altura_acumulada = self.df.loc[condicion, 'DesnivelSuperado'].sum()
        
        return altura_acumulada
            
   
    

   
        
        
