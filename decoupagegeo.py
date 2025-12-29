from geoclass import GeoDataParis
from annexfunctions import (visualiser_maillages, aggregate_by_geographic_division,
                           calculate_density, visualize_aggregated_data, parse_geometry)
import pandas as pd
import geopandas as gpd
import requests
from io import BytesIO

# Constants
CRS_PARIS = 'EPSG:2154'  # Lambert 93
CRS_FOLIUM = 4326  # WGS84

def load_building_data():
    """
    Load building data from OpenData Paris.

    Returns:
    --------
    GeoDataFrame
        Buildings with geometry and surface area
    """
    print("Loading building data...")
    url = "https://opendata.paris.fr/api/explore/v2.1/catalog/datasets/volumesbatisparis/exports/csv?lang=fr&timezone=Europe%2FBerlin&use_labels=true&delimiter=%3B"

    df_bati = pd.read_csv(url, sep=";")
    print(f"Loaded {len(df_bati)} building records")

    # Parse geometry from 'geom' column (GeoJSON polygons)
    df_bati['geometry'] = df_bati['geom'].apply(parse_geometry)

    # Create GeoDataFrame
    gdf_bati = gpd.GeoDataFrame(
        df_bati.dropna(subset=['geometry']),
        geometry='geometry',
        crs=CRS_FOLIUM
    ).to_crs(CRS_PARIS)

    # Keep only valid geometries
    gdf_bati = gdf_bati[gdf_bati.geometry.is_valid].copy()

    print(f"Converted to {len(gdf_bati)} valid building polygons")
    return gdf_bati

def create_building_density_map(buildings, geo_divisions, geo_level='arrondissements'):
    """
    Create building density map for specified geographic level using pre-loaded data.

    Parameters:
    -----------
    buildings : GeoDataFrame
        Pre-loaded building data
    geo_divisions : GeoDataFrame
        Geographic divisions (arrondissements, quartiers, or iris)
    geo_level : str
        'arrondissements', 'quartiers', or 'iris'
    """
    print(f"Processing {geo_level}...")

    print("Step 1: Aggregating building surface...")
    # Aggregate building surface by geographic division
    aggregated = aggregate_by_geographic_division(
        buildings,
        geo_divisions,
        value_column='M2_PL_TOT',
        agg_method='sum'
    )

    print("Step 2: Calculating density...")
    # Calculate density separately
    aggregated_with_density = calculate_density(aggregated, 'M2_PL_TOT_sum')

    # Create visualization
    density_col = 'M2_PL_TOT_sum_density_km2'
    avg_density = aggregated_with_density[density_col].mean()
    print(f"Average density: {avg_density:.1f} m²/m²")

    title = f'Densité du bâti - {geo_level.title()}'
    print("Step 3: Creating interactive map...")

    map_obj = visualize_building_density(
        aggregated_with_density,
        density_col,
        geo_level,
        title=title,
        save_path=f'building_density_{geo_level}.html'
    )

    return aggregated_with_density, map_obj

def visualize_building_density(aggregated_gdf, density_column, geo_level, title="Building Density Map",
                              cmap='RdYlBu_r', save_path=None):
    """
    Create a specialized building density choropleth map with custom tooltips.

    Parameters:
    -----------
    aggregated_gdf : GeoDataFrame
        Data with density calculations
    density_column : str
        Column containing density values
    geo_level : str
        Geographic level ('arrondissements', 'quartiers', or 'iris')
    title : str
        Map title
    cmap : str
        Colormap (RdYlBu_r emphasizes high values with red)
    save_path : str, optional
        Path to save the HTML file

    Returns:
    --------
    folium.Map object
    """
    try:
        import folium
        # Create Folium map
        gdf_4326 = aggregated_gdf.to_crs(epsg=4326)

        # Add an index column for Folium
        gdf_4326 = gdf_4326.reset_index()
        gdf_4326['id'] = gdf_4326.index

        centre_paris = [48.8566, 2.3522]
        m = folium.Map(location=centre_paris, zoom_start=12, tiles="cartodbdarkmatter")

        # Determine the reference column based on geo_level
        if geo_level == 'arrondissements':
            ref_col = 'c_ar'
            ref_label = 'Arrondissement'
        elif geo_level == 'quartiers':
            # Try different possible column names for quartiers
            if 'c_qu' in gdf_4326.columns:
                ref_col = 'c_qu'
            elif 'c_qa' in gdf_4326.columns:
                ref_col = 'c_qa'
            elif 'n_sq_qu' in gdf_4326.columns:
                ref_col = 'n_sq_qu'
            else:
                ref_col = list(gdf_4326.columns)[0]  # fallback to first column
            ref_label = 'Quartier'
        elif geo_level == 'iris':
            # Try different possible column names for IRIS
            if 'CODE_IRIS' in gdf_4326.columns:
                ref_col = 'CODE_IRIS'
            elif 'iris_code' in gdf_4326.columns:
                ref_col = 'iris_code'
            elif 'depcom' in gdf_4326.columns:
                ref_col = 'depcom'
            else:
                ref_col = list(gdf_4326.columns)[0]  # fallback to first column
            ref_label = 'IRIS'
        else:
            ref_col = 'id'
            ref_label = 'Zone'

        folium.Choropleth(
            geo_data=gdf_4326.__geo_interface__,
            name=title,
            data=gdf_4326,
            columns=['id', density_column],
            key_on='feature.properties.id',
            fill_color=cmap,  # RdYlBu_r: red for high density, blue for low
            fill_opacity=0.8,
            line_opacity=0.3,
            legend_name='Densité (m² bâti / m² surface)',
            highlight=True,
        ).add_to(m)

        # Add tooltips to the choropleth layer
        folium.GeoJson(
            gdf_4326,
            tooltip=folium.features.GeoJsonTooltip(
                fields=[ref_col, density_column],
                aliases=[ref_label, 'Densité (m²/m²)'],
                labels=True,
                style="font-size: 12px; font-weight: bold;",
                localize=True
            ),
            style_function=lambda x: {'fillOpacity': 0, 'color': 'transparent'}
        ).add_to(m)

        folium.LayerControl().add_to(m)

        if save_path:
            m.save(save_path)
            print(f"Interactive map saved to {save_path}")

        return m

    except ImportError:
        # Fallback to matplotlib
        fig, ax = plt.subplots(1, 1, figsize=(12, 10))
        aggregated_gdf.plot(column=density_column, ax=ax, cmap=cmap, legend=True,
                          edgecolor='black', linewidth=0.5)
        ax.set_title(title, fontsize=16, fontweight='bold')
        ax.axis('off')

        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"Static map saved to {save_path}")

        plt.show()
        return fig

# Usage example
if __name__ == "__main__":
    print("=" * 60)
    print("PARIS BUILDING DENSITY ANALYSIS")
    print("=" * 60)

    # Option 1: Visualize geographic layers
    print("\n1. Visualizing geographic layers...")
    geo = GeoDataParis()
    data = geo.load_all()
    visualiser_maillages(data)

    # Option 2: Create building density maps for all three geographic levels
    print("\n2. Creating building density maps...")

    # Load building data once
    print("\nLoading building data (once for all maps)...")
    buildings = load_building_data()

    # Load geographic data
    print("Loading geographic divisions...")
    geo_data = data  # Already loaded above

    # Create maps for all three levels
    maps_data = {}

    for geo_level in ['arrondissements', 'quartiers', 'iris']:
        print(f"\n--- {geo_level.title()} ---")

        # Select appropriate geographic divisions
        if geo_level == 'arrondissements':
            geo_divisions = geo_data['arrondissements']
        elif geo_level == 'quartiers':
            geo_divisions = geo_data['quartiers']
        elif geo_level == 'iris':
            geo_divisions = geo_data['iris']

        # Create density map
        agg_data, map_obj = create_building_density_map(buildings, geo_divisions, geo_level)
        maps_data[geo_level] = {'data': agg_data, 'map': map_obj}

    print("\n" + "=" * 60)
    print("COMPLETED: All building density maps created")
    print("- building_density_arrondissements.html")
    print("- building_density_quartiers.html")
    print("- building_density_iris.html")
    print("=" * 60)

    # Display maps in Jupyter-like environment
    try:
        from IPython.display import display
        for geo_level, map_info in maps_data.items():
            print(f"\nDisplaying {geo_level} map:")
            display(map_info['map'])
    except ImportError:
        print("\nMaps saved as HTML files. Open in browser to view.")
