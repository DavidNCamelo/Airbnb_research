''' 
Created By David Camelo on 07/02/2024
'''

import geopandas as gpd
import matplotlib.pyplot as plt
import contextily as ctx
import seaborn as sns

class comunas:
    # Inicializar la clase y asignar variables
    def __init__(self, titulo, commune_filter=None):
        self.titulo = titulo
        self.comunas_file = "Comunas y Corregimientos de Medellín.geojson"  # Documento principal, donde se extraerá la información geográfica
        self.load_comunas_data(commune_filter)

    # Convertir el GeoJSON a GeoDataFrame y cargar la información requerida
    def load_comunas_data(self, commune_filter=None):
        self.comunas_gdf = gpd.read_file(self.comunas_file, driver='GeoJSON')
        if commune_filter is not None and len(commune_filter) > 0:
            self.comunas_area_gdf = self.comunas_gdf[self.comunas_gdf['Commune_name'].isin(commune_filter)]
        else:
            self.comunas_area_gdf = self.comunas_gdf
        self.comunas_area_gdf = self.comunas_area_gdf.to_crs(epsg=4326)

    # Graficar el área y el perímetro por zona comunal
    def plot_comunas_area(self):
        fig, ax = plt.subplots(figsize=(15, 15))
        if 'Commune_name' in self.comunas_area_gdf.columns:
            colores = sns.color_palette("husl", n_colors=len(self.comunas_area_gdf['Commune_name'].unique()))
            diccionario_colores = dict(zip(self.comunas_area_gdf['Commune_name'].unique(), colores))
            self.comunas_area_gdf['color'] = self.comunas_area_gdf['Commune_name'].map(diccionario_colores)
        else:
            colores = sns.color_palette("husl", n_colors=len(self.comunas_gdf['Commune_name'].unique()))
            diccionario_colores = dict(zip(self.comunas_gdf['Commune_name'].unique(), colores))
            self.comunas_gdf['color'] = self.comunas_gdf['Commune_name'].map(diccionario_colores)
        self.comunas_area_gdf.boundary.plot(ax=ax, color='black', linewidth=1)
        self.comunas_area_gdf.plot(ax=ax, alpha=0.5, edgecolor='black', linewidth=0.5, color=self.comunas_area_gdf['color'])
        ctx.add_basemap(ax, crs=self.comunas_area_gdf.crs, source=ctx.providers.OpenStreetMap.CH)
        plt.title(self.titulo)
        plt.show()

    #Plotting the perimeter when is called as a map layer
    def commune_croquis(self, ax = None):
        if ax is None:
            fig, ax = plt.subplots(figsize=(10, 10))
        # Plot perimeter1
        self.comunas_area_gdf.boundary.plot(ax=ax, color='black', linewidth=1.5)
