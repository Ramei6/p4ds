import geopandas as gpd
import matplotlib.pyplot as plt
import pandas as pd
from shapely.geometry import shape
import json

def parse_geometry(geom_data):
    """
    Parse geometry data that may be JSON string, dict, or NaN.

    Parameters:
    -----------
    geom_data : str, dict, or NaN
        Geometry data to parse

    Returns:
    --------
    shapely.geometry or None
    """
    if pd.isna(geom_data):
        return None
    elif isinstance(geom_data, str):
        try:
            return shape(json.loads(geom_data))
        except json.JSONDecodeError:
            return None
    elif isinstance(geom_data, dict):
        return shape(geom_data)
    else:
        return None

def spatial_join_data(data_gdf, geo_divisions_gdf):
    """
    Perform spatial join between data and geographic divisions.

    Parameters:
    -----------
    data_gdf : GeoDataFrame
        Data points/polygons to join
    geo_divisions_gdf : GeoDataFrame
        Geographic divisions

    Returns:
    --------
    GeoDataFrame
        Joined data with geographic division information
    """
    # Ensure both GeoDataFrames are in the same CRS
    if data_gdf.crs != geo_divisions_gdf.crs:
        data_gdf = data_gdf.to_crs(geo_divisions_gdf.crs)

    # Perform spatial join
    joined = gpd.sjoin(data_gdf, geo_divisions_gdf, how='inner', predicate='intersects')
    return joined

def aggregate_joined_data(joined_gdf, value_column, agg_method='sum'):
    """
    Aggregate spatially joined data by geographic division.

    Parameters:
    -----------
    joined_gdf : GeoDataFrame
        Result from spatial_join_data
    value_column : str
        Column name to aggregate
    agg_method : str, default 'sum'
        Aggregation method: 'sum', 'mean', 'count', 'max', 'min'

    Returns:
    --------
    DataFrame
        Aggregated data with geo_index
    """
    # Aggregation
    if agg_method == 'count':
        agg_data = joined_gdf.groupby(joined_gdf.index_right).size().reset_index(name=f'{value_column}_count')
        agg_data = agg_data.rename(columns={'index_right': 'geo_index'})
    else:
        agg_data = joined_gdf.groupby(joined_gdf.index_right)[value_column].agg(agg_method).reset_index()
        agg_data = agg_data.rename(columns={'index_right': 'geo_index', value_column: f'{value_column}_{agg_method}'})

    return agg_data

def merge_aggregated_data(geo_divisions_gdf, agg_data, value_column, agg_method='sum'):
    """
    Merge aggregated data back with geographic divisions.

    Parameters:
    -----------
    geo_divisions_gdf : GeoDataFrame
        Original geographic divisions
    agg_data : DataFrame
        Aggregated data from aggregate_joined_data
    value_column : str
        Original value column name
    agg_method : str
        Aggregation method used

    Returns:
    --------
    GeoDataFrame
        Geographic divisions with aggregated values
    """
    # Merge back with geographic divisions
    result = geo_divisions_gdf.reset_index().merge(agg_data, left_on='index', right_on='geo_index', how='left')

    # Fill NaN values with 0
    value_agg_col = f'{value_column}_{agg_method}' if agg_method != 'count' else f'{value_column}_count'
    result[value_agg_col] = result[value_agg_col].fillna(0)

    # Clean up
    result = result.drop(columns=['index', 'geo_index'], errors='ignore')

    return result

def aggregate_by_geographic_division(data_gdf, geo_divisions_gdf, value_column, agg_method='sum'):
    """
    Aggregate data by geographic divisions using spatial join.

    Parameters:
    -----------
    data_gdf : GeoDataFrame
        Data to aggregate (e.g., buildings, points of interest)
    geo_divisions_gdf : GeoDataFrame
        Geographic divisions (arrondissements, quartiers, IRIS)
    value_column : str
        Column name to aggregate
    agg_method : str, default 'sum'
        Aggregation method: 'sum', 'mean', 'count', 'max', 'min'

    Returns:
    --------
    GeoDataFrame
        Aggregated data with geographic divisions
    """
    # Step 1: Spatial join
    joined = spatial_join_data(data_gdf, geo_divisions_gdf)

    # Step 2: Aggregate
    agg_data = aggregate_joined_data(joined, value_column, agg_method)

    # Step 3: Merge back
    result = merge_aggregated_data(geo_divisions_gdf, agg_data, value_column, agg_method)

    return result

def calculate_density(gdf, value_column, area_crs='EPSG:2154'):
    """
    Calculate density for a GeoDataFrame with aggregated values.

    Parameters:
    -----------
    gdf : GeoDataFrame
        GeoDataFrame with aggregated values
    value_column : str
        Column containing the values to calculate density for
    area_crs : str, default 'EPSG:2154'
        CRS to use for area calculation (projected CRS for France)

    Returns:
    --------
    GeoDataFrame
        Input GeoDataFrame with added area and density columns
    """
    result = gdf.copy()

    # Ensure we're in a projected CRS for area calculation
    temp_gdf = result.copy()
    if temp_gdf.crs != area_crs:
        temp_gdf = temp_gdf.to_crs(area_crs)

    # Calculate area in km²
    result['area_km2'] = temp_gdf.geometry.area / 1_000_000

    # Calculate density
    density_col = f'{value_column}_density_km2'
    result[density_col] = result[value_column] / result['area_km2']

    # Handle infinite and NaN values
    result[density_col] = result[density_col].replace([float('inf'), -float('inf')], 0).fillna(0)

    return result

def visualize_aggregated_data(aggregated_gdf, value_column, title="Aggregated Data Map",
                            cmap='YlGnBu', save_path=None):
    """
    Create a choropleth map of aggregated data.

    Parameters:
    -----------
    aggregated_gdf : GeoDataFrame
        Aggregated data from aggregate_by_geographic_division
    value_column : str
        Column to visualize
    title : str
        Map title
    cmap : str
        Colormap name
    save_path : str, optional
        Path to save the figure

    Returns:
    --------
    matplotlib figure or folium map
    """
    try:
        import folium
        # Create Folium map for interactive visualization
        gdf_4326 = aggregated_gdf.to_crs(epsg=4326)

        # Add an index column for Folium
        gdf_4326 = gdf_4326.reset_index()
        gdf_4326['id'] = gdf_4326.index

        centre_paris = [48.8566, 2.3522]
        m = folium.Map(location=centre_paris, zoom_start=12, tiles="cartodbdarkmatter")

        folium.Choropleth(
            geo_data=gdf_4326.__geo_interface__,
            name=title,
            data=gdf_4326,
            columns=['id', value_column],
            key_on='feature.properties.id',
            fill_color=cmap,
            fill_opacity=0.7,
            line_opacity=0.2,
            legend_name=value_column,
            highlight=True,
        ).add_to(m)

        folium.GeoJson(
            gdf_4326,
            tooltip=folium.features.GeoJsonTooltip(
                fields=[col for col in gdf_4326.columns if col not in ['geometry', 'id', 'index']] [:5],  # Show first 5 relevant columns
                aliases=[col for col in gdf_4326.columns if col not in ['geometry', 'id', 'index']] [:5],
                localize=True
            )
        ).add_to(m)

        folium.LayerControl().add_to(m)

        if save_path:
            m.save(save_path)
            print(f"Interactive map saved to {save_path}")

        return m

    except ImportError:
        # Fallback to matplotlib if folium not available
        fig, ax = plt.subplots(1, 1, figsize=(12, 10))
        aggregated_gdf.plot(column=value_column, ax=ax, cmap=cmap, legend=True,
                          edgecolor='black', linewidth=0.5)
        ax.set_title(title, fontsize=16, fontweight='bold')
        ax.axis('off')

        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"Static map saved to {save_path}")

        plt.show()
        return fig

def visualiser_maillages(geo_data):
    """
    Create comparative visualization of Paris geographical layers.

    Parameters:
    -----------
    geo_data : dict
        Dictionary with GeoDataFrames from GeoDataParis.load_all()
    """
    required = ['arrondissements', 'quartiers', 'iris']
    for req in required:
        if req not in geo_data:
            raise ValueError(f"Missing '{req}' data. Use GeoDataParis.load_all() first.")

    fig, axes = plt.subplots(2, 2, figsize=(20, 16))
    axes = axes.flatten()

    arr = geo_data['arrondissements']
    qua = geo_data['quartiers']
    iris = geo_data['iris']

    # Arrondissements
    arr.plot(ax=axes[0], edgecolor='black', facecolor='lightblue', linewidth=2, alpha=0.7)
    axes[0].set_title(f'Arrondissements\n({len(arr)} units)', fontsize=16, fontweight='bold', pad=15)
    axes[0].axis('off')

    for idx, row in arr.iterrows():
        centroid = row.geometry.centroid
        num_col = next((col for col in ['c_ar', 'n_sq_ar', 'l_ar'] if col in arr.columns), None)
        if num_col:
            axes[0].text(centroid.x, centroid.y, str(row[num_col]), ha='center', va='center',
                        fontsize=10, fontweight='bold', bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.8))

    # Quartiers
    qua.plot(ax=axes[1], edgecolor='black', facecolor='lightcoral', linewidth=0.8, alpha=0.7)
    axes[1].set_title(f'Administrative Quarters\n({len(qua)} units)', fontsize=16, fontweight='bold', pad=15)
    axes[1].axis('off')

    # IRIS
    import matplotlib.cm as cm
    import numpy as np

    iris_copy = iris.copy()
    if 'depcom' in iris.columns:
        iris_copy['arrondissement'] = iris_copy['depcom'].str[-2:].astype(int)
    elif 'insee_com' in iris.columns:
        iris_copy['arrondissement'] = iris_copy['insee_com'].str[-2:].astype(int)
    else:
        iris_copy['arrondissement'] = 1

    colors = cm.tab20(np.linspace(0, 1, 20))
    iris_copy['color'] = iris_copy['arrondissement'].apply(lambda x: colors[x-1] if x <= 20 else colors[0])

    iris_copy.plot(ax=axes[2], edgecolor='black', color=iris_copy['color'], linewidth=0.4, alpha=0.6)
    axes[2].set_title(f'IRIS\n({len(iris)} units)', fontsize=16, fontweight='bold', pad=15)
    axes[2].axis('off')

    # Superposition Arrondissements + IRIS
    iris.plot(ax=axes[3], edgecolor='gray', facecolor='lightgreen', linewidth=0.3, alpha=0.5)
    arr.plot(ax=axes[3], edgecolor='red', facecolor='none', linewidth=2.5)
    axes[3].set_title('Superposition\nArrondissements (red) + IRIS', fontsize=16, fontweight='bold', pad=15)
    axes[3].axis('off')

    fig.suptitle('Paris Geographical Layers - Complete Comparison', fontsize=20, fontweight='bold', y=0.98)
    plt.tight_layout()
    plt.savefig('maillages_paris_complet.png', dpi=300, bbox_inches='tight')
    print("Visualization saved: maillages_paris_complet.png")
    plt.show()
