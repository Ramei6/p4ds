import geopandas as gpd
import requests
from io import BytesIO
from zipfile import ZipFile
import py7zr
import os

class GeoDataParis:
    """Manages loading and caching of Paris geographical data layers."""

    def __init__(self):
        self.data = {}

    def load_arrondissements(self):
        """Load Paris arrondissements."""
        if 'arrondissements' not in self.data:
            url = "https://opendata.paris.fr/api/explore/v2.1/catalog/datasets/arrondissements/exports/geojson"
            self.data['arrondissements'] = gpd.read_file(url)
        return self.data['arrondissements']

    def load_quartiers(self):
        """Load Paris administrative quarters."""
        if 'quartiers' not in self.data:
            url = "https://opendata.paris.fr/api/explore/v2.1/catalog/datasets/quartier_paris/exports/geojson"
            self.data['quartiers'] = gpd.read_file(url)
        return self.data['quartiers']

    def load_iris(self):
        """Load Paris IRIS with fallback methods."""
        if 'iris' not in self.data:
            try:
                url = "https://data.iledefrance.fr/api/explore/v2.1/catalog/datasets/iris/exports/geojson"
                gdf = gpd.read_file(url)
                self.data['iris'] = gdf[gdf['depcom'].str.startswith('751')].copy()
            except Exception:
                try:
                    url = "https://public.opendatasoft.com/api/explore/v2.1/catalog/datasets/georef-france-iris/exports/geojson?where=dep_code='75'&lang=fr&timezone=Europe%2FParis"
                    self.data['iris'] = gpd.read_file(url)
                except Exception:
                    url = "https://data.geopf.fr/telechargement/download/IRIS-GE/IRIS-GE_3-0__SHP_LAMB93_D075_2024-01-01/IRIS-GE_3-0__SHP_LAMB93_D075_2024-01-01.7z"
                    response = requests.get(url)
                    with py7zr.SevenZipFile(BytesIO(response.content), mode='r') as z:
                        z.extractall(path='temp_iris_ign')
                    shp_files = [f for f in os.listdir('temp_iris_ign/IRIS-GE_3-0__SHP_LAMB93_D075_2024-01-01') if f.endswith('.shp')]
                    if shp_files:
                        self.data['iris'] = gpd.read_file(f'temp_iris_ign/IRIS-GE_3-0__SHP_LAMB93_D075_2024-01-01/{shp_files[0]}')
                    else:
                        raise ValueError("Shapefile not found")
        return self.data['iris']

    def load_all(self):
        """Load all available geographical layers."""
        self.load_arrondissements()
        self.load_quartiers()
        self.load_iris()
        return self.data

    def get_data(self, key):
        """Get specific dataframe by key."""
        return self.data.get(key)

    def list_available_data(self):
        """List loaded data keys."""
        return list(self.data.keys())
