import pandas as pd
from shapely.geometry import Point, Polygon
import json
import geopandas as gpd


# Cargar datos desde el archivo CSV
df_csv = pd.read_csv('Data_Medellin.csv')

# Convertir las columnas de coordenadas en geometrías
geometry_csv = [Point(xy) for xy in zip(df_csv['long'], df_csv['latitude'])]

# Cargar datos desde el archivo GeoJSON
with open('Comunas y Corregimientos de Medellín.geojson', encoding='utf-8') as f:
    geojson_data = json.load(f)

# Filtrar los polígonos válidos
valid_polygons = [feature['geometry']['coordinates'][0] for feature in geojson_data['features'] if len(feature['geometry']['coordinates'][0]) >= 3]

# Crear objetos Polygon solo para polígonos válidos
polygons = [Polygon(coords) for coords in valid_polygons]

# Función para encontrar la comuna correspondiente
def find_commune(point):
    for i, polygon in enumerate(polygons):
        if polygon.contains(point):
            properties = geojson_data['features'][i]['properties']
            commune_name = properties.get('Commune_name')
            commune_number = properties.get('Commune_number')
            return commune_name, commune_number
    return None, None  # Devolver None si no se encuentra ninguna comuna

# Aplicar la función para encontrar la comuna a cada punto
df_csv['Commune_info'] = df_csv.apply(lambda row: find_commune(Point(row['long'], row['latitude'])), axis=1)

# Dividir la información de la comuna en columnas separadas
df_csv[['Commune_name', 'Commune_number']] = pd.DataFrame(df_csv['Commune_info'].tolist(), index=df_csv.index)

#Se generó una comuna con puntos erroneamente clasificados, por tanto se modifica antes de la siguiente iteración
df_csv.loc[df_csv['Commune_name'] == 'San Javier', ['Commune_name']] = 'Villa Hermosa'
print(df_csv['Commune_name'].unique())

#Esta comuna tiene una conformación compleja, lo cual se implementa una nueva versión a través de límites
#Puntos San Javier
min_lon = -75.6324264433567
max_lon = -75.6000000
min_lat = 6.24056591548945
max_lat = 6.27000000
# Filtra los puntos que pertenecen a la comuna 'San Javier' y no tienen comuna asignada
geomap1 = df_csv[(df_csv['long'] < 0) & (df_csv['Commune_name'].isnull())]
geomap1 = geomap1[(geomap1['long'] >= min_lon) & (geomap1['long'] <= max_lon) &
             (geomap1['latitude'] >= min_lat) & (geomap1['latitude'] <= max_lat)]

#Clasificar puntos de comuna excluida con lo limites anteriores
geomap1['Commune_name'] = 'San Javier'
geomap1['Commune_number'] = 'Comuna 13'
#Elimina columnas innecesarias para fases futuras
geomap1 = geomap1.drop(columns=['Commune_info'])
df_csv = df_csv.drop(columns=['Commune_info'])
#Actualizar información de columnas
update_column = ['Commune_name', 'Commune_number']
df_csv = df_csv.merge(geomap1[['id'] + update_column], on = 'id', how = 'left', suffixes=('_original', '_nuevo'))
# Actualiza los valores en las columnas específicas en df1 con los valores de df2
for column in update_column:
    df_csv[column] = df_csv[f'{column}_nuevo'].fillna(df_csv[f'{column}_original'])

# Elimina las columnas auxiliares creadas durante la fusión
df_csv.drop([f'{column}_original' for column in update_column] + [f'{column}_nuevo' for column in update_column], axis=1, inplace=True)
df_csv = df_csv.rename(columns= {'Commune_name_original': 'Commune_name',
                                 'Commmune_number_original': 'Commune_number'})


#Aun así hay puntos mal clasificados en la iteración anterior
# Reemplazar los valores en la columna 'Commune_name' según la especificación dada
df_csv['Commune_name'].replace({'El Poblado': 'Guayabal',
                                 'Guayabal': 'La América',
                                 'La América': 'La Candelaria',
                                 'La Candelaria': 'Laureles Estadio',
                                 'Laureles Estadio': 'Popular',
                                 'Popular': 'Robledo',
                                 '12 de Octubre': 'El Poblado',
                                 'Manrique': 'Popular'}, inplace=True)

#Revisar listado de comunas
print(df_csv['Commune_name'].unique())

#Obervar la información del nuevo dataframe
print(df_csv.info())

#Guardar el dataframe
df_csv.to_csv('Data_Medellin.csv', index= False)