''' 
Created By David Camelo on 01/02/2024
'''

import geopandas as gpd
import matplotlib.pyplot as plt
import contextily as ctx
import seaborn as sns

class Municipios:
    #Iinitialize de class and asign the required variables
    def __init__(self, ciudades, departamento, titulo):
        self.ciudades = ciudades
        self.departamento = departamento
        self.titulo = titulo
        self.municipios_file = "MGN_MPIO_POLITICO - copia.geojson" #Main document, where will be extracted
                                                                #the geographical information
        self.load_municipios_data()

    #Convert the GeoJson to GeoDataframe and load the required informacion by item (city and dapartamento or state)
    def load_municipios_data(self):
        self.municipios_gdf = gpd.read_file(self.municipios_file, driver='GeoJSON')
        self.municipio_area_gdf = self.municipios_gdf[
            self.municipios_gdf['MPIO_CNMBR'].isin(self.ciudades) & (self.municipios_gdf['DPTO_CNMBR'] == self.departamento)
        ] #Search for the choosed cities and respective department
        self.municipio_area_gdf = self.municipio_area_gdf.to_crs(epsg=4326)

    #Plot the perimeter and colored area in each chosen city
    def plot_municipio_area(self):
        fig, ax = plt.subplots(figsize=(15, 15))
        colores = sns.color_palette("husl", n_colors=len(self.ciudades))
        diccionario_colores = dict(zip(self.ciudades, colores))
        self.municipio_area_gdf['color'] = self.municipio_area_gdf['MPIO_CNMBR'].map(diccionario_colores)
        self.municipio_area_gdf.boundary.plot(ax=ax, color='black', linewidth=1)
        self.municipio_area_gdf.plot(ax=ax, alpha=0.5, edgecolor='black', linewidth=0.5, color=self.municipio_area_gdf['color'])
        ctx.add_basemap(ax, crs=self.municipio_area_gdf.crs, source=ctx.providers.OpenStreetMap.CH)
        plt.title(self.titulo)
        plt.show()

    #Plot just the perimeter of the chosen cities
    def plot_municipio_croquis(self, ax = None):
        if ax is None:
            fig, ax = plt.subplots(figsize=(15, 15))
        #Perimeters
        self.municipio_area_gdf.boundary.plot(ax=ax, color='black', linewidth=1.5)
        ctx.add_basemap(ax, crs=self.municipio_area_gdf.crs, source=ctx.providers.OpenStreetMap.CH)
        plt.title(f'Croquis de {self.titulo}')
        plt.show()

    def filter_croquis(self, ax = None):
        if ax is None:
            fig, ax = plt.subplots(figsize=(10, 10))
        # Plot perimeter1
        self.municipio_area_gdf.boundary.plot(ax=ax, color='black', linewidth=1.5)
        #plt.show()
        
    
'''# Uso de la clase
ciudades = ['MEDELLÍN', 'BELLO', 'ITAGÜÍ', 'ENVIGADO', 'COPACABANA', 'LA ESTRELLA', 'SABANETA', 'BARBOSA', 'CALDAS', 'GIRARDOTA']
departamento = 'ANTIOQUIA'
titulo = 'Municipios Área Metropolitana'
area_metropolitana = Municipios(ciudades, departamento, titulo)
area_metropolitana.plot_municipio_area()
area_metropolitana.plot_municipio_croquis()
area_metropolitana.filter_croquis()'''
