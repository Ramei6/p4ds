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

def load_green_spaces():
    """
    Load and union green space areas from three different datasets.

    Returns:
    --------
    GeoDataFrame
        Union of all green space geometries
    """
    print("Loading green spaces...")

    # Dataset 1: Plan de voirie - Emprises espaces verts
    print("  Loading roadway green spaces...")
    green1_url = "https://opendata.paris.fr/api/explore/v2.1/catalog/datasets/plan-de-voirie-emprises-espaces-verts/exports/csv?lang=fr&timezone=Europe%2FBerlin&use_labels=true&delimiter=%3B"
    green1_df = pd.read_csv(green1_url, sep=";")

    green1_gdf = gpd.GeoDataFrame(
        green1_df.dropna(subset=['geo_shape']),
        geometry=green1_df['geo_shape'].dropna().apply(parse_geometry),
        crs='EPSG:4326'
    ).to_crs('EPSG:2154')
    green1_gdf = green1_gdf[green1_gdf.geometry.is_valid]
    print(f"  Loaded {len(green1_gdf)} roadway green space geometries")

    # Dataset 2: Espaces verts et assimilés
    print("  Loading green spaces and assimilated...")
    green2_url = "https://opendata.paris.fr/api/explore/v2.1/catalog/datasets/espaces_verts/exports/csv?lang=fr&timezone=Europe%2FBerlin&use_labels=true&delimiter=%3B"
    green2_df = pd.read_csv(green2_url, sep=";")

    print(f"  Dataset 2 columns: {green2_df.columns.tolist()}")
    print(f"  Dataset 2 shape: {green2_df.shape}")
    print(f"  First few rows:")
    print(green2_df.head(2))

    # Try different geometry column names (more flexible search)
    geom_col_green2 = None
    for col in green2_df.columns:
        col_clean = col.lower().replace(' ', '').replace('_', '')
        if 'geoshape' in col_clean or 'geom' in col_clean or 'geometry' in col_clean:
            geom_col_green2 = col
            break

    if geom_col_green2 is None:
        print("  ❌ CONCLUSION: This dataset contains only tabular address data, no geometry information.")
        print("  This dataset provides green space information but not spatial geometries.")
        print("  Skipping this dataset as it cannot be used for spatial exclusion.")
        green2_gdf = gpd.GeoDataFrame([], geometry=[], crs='EPSG:2154')
    else:
        print(f"  ✓ Found geometry column: {geom_col_green2}")
        green2_gdf = gpd.GeoDataFrame(
            green2_df.dropna(subset=[geom_col_green2]),
            geometry=green2_df[geom_col_green2].dropna().apply(parse_geometry),
            crs='EPSG:4326'
        ).to_crs('EPSG:2154')
        green2_gdf = green2_gdf[green2_gdf.geometry.is_valid]
        print(f"  Loaded {len(green2_gdf)} green space geometries (using column '{geom_col_green2}')")

    # Dataset 3: Ilots de fraîcheur - Espaces verts "frais"
    print("  Loading fresh air green spaces...")
    green3_url = "https://opendata.paris.fr/api/explore/v2.1/catalog/datasets/ilots-de-fraicheur-espaces-verts-frais/exports/csv?lang=fr&timezone=Europe%2FBerlin&use_labels=true&delimiter=%3B"
    green3_df = pd.read_csv(green3_url, sep=";")

    green3_gdf = gpd.GeoDataFrame(
        green3_df.dropna(subset=['geo_shape']),
        geometry=green3_df['geo_shape'].dropna().apply(parse_geometry),
        crs='EPSG:4326'
    ).to_crs('EPSG:2154')
    green3_gdf = green3_gdf[green3_gdf.geometry.is_valid]
    print(f"  Loaded {len(green3_gdf)} fresh air green space geometries")

    # Union all green space geometries
    print("  Creating union of green spaces...")

    all_green_geoms = []
    if not green1_gdf.empty:
        all_green_geoms.append(green1_gdf.unary_union)
    if not green2_gdf.empty:
        all_green_geoms.append(green2_gdf.unary_union)
    if not green3_gdf.empty:
        all_green_geoms.append(green3_gdf.unary_union)

    if all_green_geoms:
        union_geom = gpd.GeoSeries(all_green_geoms).union_all()
        all_green_spaces = gpd.GeoDataFrame(
            {'geometry': [union_geom]},
            crs='EPSG:2154'
        )
    else:
        all_green_spaces = gpd.GeoDataFrame(
            {'geometry': []},
            crs='EPSG:2154'
        )

    print(f"  Green spaces loaded: {len(all_green_spaces)} features")
    return all_green_spaces

def load_all_nonbuildable_areas():
    """
    Load and union all non-buildable areas (water bodies, railways, and green spaces).

    Returns:
    --------
    tuple
        (all_non_buildable_gdf, green_spaces_gdf)
    """
    print("Loading all non-buildable areas (water + railways + green spaces)...")

    # Load water and railways
    non_buildable_no_green = load_non_buildable_areas()

    # Load green spaces
    green_spaces = load_green_spaces()

    # Combine all non-buildable areas
    print("  Creating union of all non-buildable areas...")

    all_geoms = []
    if not non_buildable_no_green.empty:
        all_geoms.append(non_buildable_no_green.unary_union)
    if not green_spaces.empty:
        all_geoms.append(green_spaces.unary_union)

    if all_geoms:
        union_geom = gpd.GeoSeries(all_geoms).union_all()
        all_non_buildable = gpd.GeoDataFrame(
            {'geometry': [union_geom]},
            crs='EPSG:2154'
        )
    else:
        all_non_buildable = gpd.GeoDataFrame(
            {'geometry': []},
            crs='EPSG:2154'
        )

    print(f"  All non-buildable areas loaded: {len(all_non_buildable)} features")
    return all_non_buildable, green_spaces

def load_non_buildable_areas():
    """
    Load and union non-buildable areas (water bodies and railways).

    Returns:
    --------
    GeoDataFrame
        Union of all non-buildable geometries
    """
    print("Loading non-buildable areas...")

    # Load water bodies
    print("  Loading water bodies...")
    water_url = "https://opendata.paris.fr/api/explore/v2.1/catalog/datasets/plan-de-voirie-voies-deau/exports/csv?lang=fr&timezone=Europe%2FBerlin&use_labels=true&delimiter=%3B"
    water_df = pd.read_csv(water_url, sep=";")

    # Use 'geo_shape' column as identified from analysis
    geom_col_water = 'geo_shape'

    water_gdf = gpd.GeoDataFrame(
        water_df.dropna(subset=[geom_col_water]),
        geometry=water_df[geom_col_water].dropna().apply(parse_geometry),
        crs='EPSG:4326'
    ).to_crs('EPSG:2154')
    water_gdf = water_gdf[water_gdf.geometry.is_valid]
    print(f"  Loaded {len(water_gdf)} water body geometries")

    # Load railways
    print("  Loading railways...")
    rail_url = "https://opendata.paris.fr/api/explore/v2.1/catalog/datasets/plan-de-voirie-emprises-ferroviaires/exports/csv?lang=fr&timezone=Europe%2FBerlin&use_labels=true&delimiter=%3B"
    rail_df = pd.read_csv(rail_url, sep=";")

    # Use 'geo_shape' column as identified from analysis
    geom_col_rail = 'geo_shape'

    rail_gdf = gpd.GeoDataFrame(
        rail_df.dropna(subset=[geom_col_rail]),
        geometry=rail_df[geom_col_rail].dropna().apply(parse_geometry),
        crs='EPSG:4326'
    ).to_crs('EPSG:2154')
    rail_gdf = rail_gdf[rail_gdf.geometry.is_valid]
    print(f"  Loaded {len(rail_gdf)} railway geometries")

    # Union all non-buildable geometries
    print("  Creating union of non-buildable areas...")

    # Combine all geometries
    all_geoms = []
    if not water_gdf.empty:
        all_geoms.append(water_gdf.unary_union)
    if not rail_gdf.empty:
        all_geoms.append(rail_gdf.unary_union)

    if all_geoms:
        union_geom = gpd.GeoSeries(all_geoms).union_all()
        all_non_buildable = gpd.GeoDataFrame(
            {'geometry': [union_geom]},
            crs='EPSG:2154'
        )
    else:
        # Fallback if no geometries
        all_non_buildable = gpd.GeoDataFrame(
            {'geometry': []},
            crs='EPSG:2154'
        )

    print(f"  Non-buildable areas loaded: {len(all_non_buildable)} features")
    return all_non_buildable

def create_buildable_geometries(geo_divisions_gdf, non_buildable_gdf):
    """
    Create buildable area geometries by subtracting non-buildable areas.

    Parameters:
    -----------
    geo_divisions_gdf : GeoDataFrame
        Original geographic divisions
    non_buildable_gdf : GeoDataFrame
        Non-buildable areas to subtract

    Returns:
    --------
    GeoDataFrame
        Geographic divisions with buildable geometries and areas
    """
    result = geo_divisions_gdf.copy()

    # Ensure both are in the same CRS
    if result.crs != non_buildable_gdf.crs:
        result = result.to_crs(non_buildable_gdf.crs)

    # Create buildable geometries
    buildable_geoms = []
    for geom in result.geometry:
        # Subtract non-buildable areas from each geographic division
        buildable_geom = geom
        for non_buildable_geom in non_buildable_gdf.geometry:
            try:
                buildable_geom = buildable_geom.difference(non_buildable_geom)
            except:
                continue  # Skip if difference fails
        buildable_geoms.append(buildable_geom)

    result['buildable_geometry'] = buildable_geoms
    buildable_series = gpd.GeoSeries(buildable_geoms, crs=result.crs)
    result['buildable_area_m2'] = buildable_series.area

    # Calculate percentage of buildable area
    original_area = result.geometry.area
    result['buildable_percentage'] = (result['buildable_area_m2'] / original_area * 100).round(1)

    return result

def create_buildable_geodataframe(geo_divisions_gdf, non_buildable_gdf):
    """
    Create a GeoDataFrame with buildable geometries as the active geometry column.

    Parameters:
    -----------
    geo_divisions_gdf : GeoDataFrame
        Original geographic divisions
    non_buildable_gdf : GeoDataFrame
        Non-buildable areas to subtract

    Returns:
    --------
    GeoDataFrame
        Geographic divisions with buildable geometries as active geometry
    """
    # Create buildable geometries
    buildable_gdf = create_buildable_geometries(geo_divisions_gdf, non_buildable_gdf)

    # Create new GeoDataFrame with buildable geometries as active geometry
    buildable_result = buildable_gdf.set_geometry('buildable_geometry').copy()
    buildable_result.crs = geo_divisions_gdf.crs  # Ensure CRS is set

    return buildable_result

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

    # Calculate density: building area / total area
    density_col = f'{value_column}_density_km2'
    result[density_col] = result[value_column] / result['area_km2']

    # Handle infinite and NaN values
    result[density_col] = result[density_col].replace([float('inf'), -float('inf')], 0).fillna(0)

    # Also provide density in proper m²/m² units (divide by 1M to avoid millions)
    result[f'{value_column}_density_m2_m2'] = result[density_col] / 1_000_000

    return result

def calculate_corrected_density(gdf, value_column, buildable_area_column='buildable_area_m2'):
    """
    Calculate corrected density using buildable area instead of total area.

    Parameters:
    -----------
    gdf : GeoDataFrame
        GeoDataFrame with aggregated values and buildable areas
    value_column : str
        Column containing the values to calculate density for
    buildable_area_column : str
        Column containing buildable area in m²

    Returns:
    --------
    GeoDataFrame
        Input GeoDataFrame with corrected density columns
    """
    result = gdf.copy()

    # Calculate corrected density: building_volume ÷ buildable_area
    corrected_density_col = f'{value_column}_corrected_density_m2_m2'
    result[corrected_density_col] = result[value_column] / result[buildable_area_column]

    # Handle infinite and NaN values
    result[corrected_density_col] = result[corrected_density_col].replace([float('inf'), -float('inf')], 0).fillna(0)

    # Also provide density in more readable units (multiply by 1M for m²/km² equivalent)
    result[f'{value_column}_corrected_density_readable'] = result[corrected_density_col] * 1_000_000

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
