from geoclass import GeoDataParis
from annexfunctions import (visualiser_maillages, aggregate_by_geographic_division,
                           calculate_density, calculate_corrected_density, visualize_aggregated_data,
                           load_non_buildable_areas, load_all_nonbuildable_areas, create_buildable_geometries,
                           create_buildable_geodataframe, parse_geometry)
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

    # Parse geometry from 'geom' column (GeoJSON polygons) - as identified from analysis
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

    # Create visualization - use proper m²/m² units instead of millions
    density_col = 'M2_PL_TOT_sum_density_m2_m2'
    avg_density = aggregated_with_density[density_col].mean()
    print(f"Average density: {avg_density:.2f} m²/m²")

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

def create_corrected_building_density_map(buildings, geo_divisions, non_buildable_gdf, geo_level='arrondissements'):
    """
    Create corrected building density map excluding water and railways.
    Uses original geographic boundaries for building aggregation but buildable area for density calculation.

    Parameters:
    -----------
    buildings : GeoDataFrame
        Pre-loaded building data
    geo_divisions : GeoDataFrame
        Geographic divisions (arrondissements, quartiers, or iris)
    non_buildable_gdf : GeoDataFrame
        Non-buildable areas (water + railways)
    geo_level : str
        'arrondissements', 'quartiers', or 'iris'
    """
    print(f"Processing corrected {geo_level}...")

    print("Step 1: Calculating buildable areas...")
    # Calculate buildable areas for each geographic division
    buildable_areas = create_buildable_geometries(geo_divisions, non_buildable_gdf)
    print(f"  Average buildable percentage: {buildable_areas['buildable_percentage'].mean():.1f}%")

    print("Step 2: Aggregating building surface by geographic divisions...")
    # Aggregate buildings using original geographic boundaries (simpler approach)
    aggregated = aggregate_by_geographic_division(
        buildings,
        geo_divisions,  # Use original boundaries for spatial join
        value_column='M2_PL_TOT',
        agg_method='sum'
    )

    # Merge with buildable area information
    aggregated_with_areas = aggregated.merge(
        buildable_areas[['buildable_area_m2', 'buildable_percentage']],
        left_index=True,
        right_index=True,
        how='left'
    )

    print("Step 3: Calculating corrected density...")
    # Calculate corrected density using buildable area (not total area)
    aggregated_with_corrected_density = calculate_corrected_density(
        aggregated_with_areas,
        'M2_PL_TOT_sum',
        'buildable_area_m2'
    )

    # Create visualization using original geometries (simpler for web display)
    print("Step 4: Creating corrected density visualization...")

    # Use original geometries for display, but show corrected density values
    final_data = geo_divisions.merge(
        aggregated_with_corrected_density[['M2_PL_TOT_sum_corrected_density_m2_m2', 'buildable_percentage']],
        left_index=True,
        right_index=True,
        how='left'
    )

    # Create visualization
    density_col = 'M2_PL_TOT_sum_corrected_density_m2_m2'
    avg_density = final_data[density_col].mean()
    print(f"Average corrected density: {avg_density:.4f} m²/m²")

    title = f'Densité du bâti corrigée - {geo_level.title()}'
    print("Step 5: Creating interactive map...")

    map_obj = visualize_corrected_building_density(
        final_data,
        density_col,
        geo_level,
        non_buildable_gdf=non_buildable_gdf,  # Pass non-buildable areas for overlay
        title=title,
        save_path=f'building_density_corrected_{geo_level}.html'
    )

    return final_data, map_obj

def create_ultra_corrected_building_density_map(buildings, geo_divisions, geo_level='arrondissements'):
    """
    Create ultra-corrected building density map excluding water, railways, and green spaces.
    Uses original geographic boundaries for building aggregation but ultra-buildable area for density calculation.

    Parameters:
    -----------
    buildings : GeoDataFrame
        Pre-loaded building data
    geo_divisions : GeoDataFrame
        Geographic divisions (arrondissements, quartiers, or iris)
    geo_level : str
        'arrondissements', 'quartiers', or 'iris'
    """
    print(f"Processing ultra-corrected {geo_level}...")

    print("Step 1: Loading all non-buildable areas (water + railways + green spaces)...")
    # Load all non-buildable areas (water, railways, green spaces)
    all_non_buildable, green_spaces = load_all_nonbuildable_areas()

    print("Step 2: Calculating ultra-buildable areas...")
    # Calculate ultra-buildable areas for each geographic division (excluding water + railways + green)
    ultra_buildable_areas = create_buildable_geometries(geo_divisions, all_non_buildable)
    print(f"  Average ultra-buildable percentage: {ultra_buildable_areas['buildable_percentage'].mean():.1f}%")

    print("Step 3: Aggregating building surface by geographic divisions...")
    # Aggregate buildings using original geographic boundaries (simpler approach)
    aggregated = aggregate_by_geographic_division(
        buildings,
        geo_divisions,  # Use original boundaries for spatial join
        value_column='M2_PL_TOT',
        agg_method='sum'
    )

    # Merge with ultra-buildable area information
    aggregated_with_areas = aggregated.merge(
        ultra_buildable_areas[['buildable_area_m2', 'buildable_percentage']],
        left_index=True,
        right_index=True,
        how='left'
    )

    print("Step 4: Calculating ultra-corrected density...")
    # Calculate ultra-corrected density using ultra-buildable area (not total area)
    aggregated_with_ultra_corrected_density = calculate_corrected_density(
        aggregated_with_areas,
        'M2_PL_TOT_sum',
        'buildable_area_m2'
    )

    # Create visualization using original geometries (simpler for web display)
    print("Step 5: Creating ultra-corrected density visualization...")

    # Use original geometries for display, but show ultra-corrected density values
    final_data = geo_divisions.merge(
        aggregated_with_ultra_corrected_density[['M2_PL_TOT_sum_corrected_density_m2_m2', 'buildable_percentage']],
        left_index=True,
        right_index=True,
        how='left'
    )

    # Create visualization
    density_col = 'M2_PL_TOT_sum_corrected_density_m2_m2'
    avg_density = final_data[density_col].mean()
    print(f"Average ultra-corrected density: {avg_density:.4f} m²/m²")

    title = f'Densité du bâti ultra-corrigée - {geo_level.title()}'
    print("Step 6: Creating interactive map with all non-buildable overlays...")

    map_obj = visualize_ultra_corrected_building_density(
        final_data,
        density_col,
        geo_level,
        all_non_buildable_gdf=all_non_buildable,  # Pass all non-buildable areas for overlay
        green_spaces_gdf=green_spaces,  # Pass green spaces for separate overlay
        title=title,
        save_path=f'building_density_ultra_corrected_{geo_level}.html'
    )

    return final_data, map_obj

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
            fill_color='YlOrRd',  # Yellow-orange-red color scheme
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

def visualize_corrected_building_density(aggregated_gdf, density_column, geo_level, non_buildable_gdf=None,
                                       title="Corrected Building Density Map", save_path=None):
    """
    Create a specialized corrected building density choropleth map with enhanced tooltips
    and visual representation of non-buildable areas.

    Parameters:
    -----------
    aggregated_gdf : GeoDataFrame
        Data with corrected density calculations
    density_column : str
        Column containing corrected density values
    geo_level : str
        Geographic level ('arrondissements', 'quartiers', or 'iris')
    non_buildable_gdf : GeoDataFrame, optional
        Non-buildable areas to overlay on the map
    title : str
        Map title
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

        # Use consistent YlOrRd color scheme for all levels
        density_values = gdf_4326[density_column].dropna()
        if len(density_values) > 0:
            bins = list(density_values.quantile([0, 0.2, 0.4, 0.6, 0.8, 1.0]))
            if len(set(bins)) < 3:
                bins = None
        else:
            bins = None

        fill_color = 'YlOrRd'  # Yellow-orange-red color scheme for all maps
        legend_name = 'Densité corrigée (m²/m²)'

        choropleth = folium.Choropleth(
            geo_data=gdf_4326.__geo_interface__,
            name='Densité corrigée',
            data=gdf_4326,
            columns=['id', density_column],
            key_on='feature.properties.id',
            fill_color=fill_color,
            fill_opacity=0.8,
            line_opacity=0.3,
            legend_name=legend_name,
            highlight=True,
            bins=bins,
        ).add_to(m)

        # Add non-buildable areas as dark overlay if provided
        if non_buildable_gdf is not None:
            try:
                non_buildable_4326 = non_buildable_gdf.to_crs(epsg=4326)
                folium.GeoJson(
                    non_buildable_4326.__geo_interface__,
                    name='Zones non-bâtissables (eau + rails)',
                    style_function=lambda x: {
                        'fillColor': '#2F2F2F',  # Dark gray
                        'color': '#1F1F1F',      # Darker border
                        'weight': 1,
                        'fillOpacity': 0.7
                    },
                    tooltip='Zone non-bâtissable (exclue du calcul de densité)'
                ).add_to(m)
            except Exception as e:
                print(f"Warning: Could not add non-buildable areas overlay: {e}")

        # Enhanced tooltips showing corrected info
        folium.GeoJson(
            gdf_4326,
            tooltip=folium.features.GeoJsonTooltip(
                fields=[ref_col, density_column, 'buildable_percentage'],
                aliases=[ref_label, 'Densité corrigée (m²/m²)', 'Surface bâtissable (%)'],
                labels=True,
                style="font-size: 12px; font-weight: bold;",
                localize=True
            ),
            style_function=lambda x: {'fillOpacity': 0, 'color': 'transparent'}
        ).add_to(m)

        folium.LayerControl(collapsed=False).add_to(m)

        if save_path:
            m.save(save_path)
            print(f"Interactive map saved to {save_path}")

        return m

    except ImportError:
        # Fallback to matplotlib
        fig, ax = plt.subplots(1, 1, figsize=(12, 10))

        # Use robust color scaling for outliers
        import matplotlib.colors as mcolors
        density_values = aggregated_gdf[density_column].dropna()
        if len(density_values) > 0:
            # Use percentiles for color scaling
            vmin = density_values.quantile(0.05)  # 5th percentile
            vmax = density_values.quantile(0.95)  # 95th percentile
            norm = mcolors.Normalize(vmin=vmin, vmax=vmax)
        else:
            norm = None

        aggregated_gdf.plot(column=density_column, ax=ax, cmap='RdYlBu_r',
                          legend=True, edgecolor='black', linewidth=0.5, norm=norm)
        ax.set_title(title, fontsize=16, fontweight='bold')
        ax.axis('off')

        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"Static map saved to {save_path}")

        plt.show()
        return fig

def visualize_ultra_corrected_building_density(aggregated_gdf, density_column, geo_level,
                                             all_non_buildable_gdf=None, green_spaces_gdf=None,
                                             title="Ultra-Corrected Building Density Map", save_path=None):
    """
    Create a specialized ultra-corrected building density choropleth map with enhanced tooltips
    and visual representation of all non-buildable areas (water, railways, green spaces).

    Parameters:
    -----------
    aggregated_gdf : GeoDataFrame
        Data with ultra-corrected density calculations
    density_column : str
        Column containing ultra-corrected density values
    geo_level : str
        Geographic level ('arrondissements', 'quartiers', or 'iris')
    all_non_buildable_gdf : GeoDataFrame, optional
        All non-buildable areas (water + railways + green spaces)
    green_spaces_gdf : GeoDataFrame, optional
        Green spaces for separate overlay
    title : str
        Map title
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

        # Use consistent YlOrRd color scheme for all levels
        density_values = gdf_4326[density_column].dropna()
        if len(density_values) > 0:
            bins = list(density_values.quantile([0, 0.2, 0.4, 0.6, 0.8, 1.0]))
            if len(set(bins)) < 3:
                bins = None
        else:
            bins = None

        fill_color = 'YlOrRd'  # Yellow-orange-red color scheme for all maps
        legend_name = 'Densité ultra-corrigée (m²/m²)'

        choropleth = folium.Choropleth(
            geo_data=gdf_4326.__geo_interface__,
            name='Densité ultra-corrigée',
            data=gdf_4326,
            columns=['id', density_column],
            key_on='feature.properties.id',
            fill_color=fill_color,
            fill_opacity=0.8,
            line_opacity=0.3,
            legend_name=legend_name,
            highlight=True,
            bins=bins,
        ).add_to(m)

        # Add green spaces as green overlay if provided
        if green_spaces_gdf is not None:
            try:
                green_spaces_4326 = green_spaces_gdf.to_crs(epsg=4326)
                folium.GeoJson(
                    green_spaces_4326.__geo_interface__,
                    name='Espaces verts',
                    style_function=lambda x: {
                        'fillColor': '#228B22',  # Forest green
                        'color': '#006400',      # Dark green border
                        'weight': 1,
                        'fillOpacity': 0.6       # Semi-transparent
                    },
                    tooltip='Espace vert (exclu du calcul de densité)'
                ).add_to(m)
            except Exception as e:
                print(f"Warning: Could not add green spaces overlay: {e}")

        # Add other non-buildable areas (water + railways) as dark overlay
        if all_non_buildable_gdf is not None:
            try:
                non_green_4326 = all_non_buildable_gdf.to_crs(epsg=4326)
                folium.GeoJson(
                    non_green_4326.__geo_interface__,
                    name='Eau + Voies ferrées',
                    style_function=lambda x: {
                        'fillColor': '#2F2F2F',  # Dark gray
                        'color': '#1F1F1F',      # Darker border
                        'weight': 1,
                        'fillOpacity': 0.7
                    },
                    tooltip='Eau/Voies ferrées (exclus du calcul de densité)'
                ).add_to(m)
            except Exception as e:
                print(f"Warning: Could not add non-buildable areas overlay: {e}")

        # Enhanced tooltips showing ultra-corrected info
        folium.GeoJson(
            gdf_4326,
            tooltip=folium.features.GeoJsonTooltip(
                fields=[ref_col, density_column, 'buildable_percentage'],
                aliases=[ref_label, 'Densité ultra-corrigée (m²/m²)', 'Surface ultra-bâtissable (%)'],
                labels=True,
                style="font-size: 12px; font-weight: bold;",
                localize=True
            ),
            style_function=lambda x: {'fillOpacity': 0, 'color': 'transparent'}
        ).add_to(m)

        folium.LayerControl(collapsed=False).add_to(m)

        if save_path:
            m.save(save_path)
            print(f"Interactive map saved to {save_path}")

        return m

    except ImportError:
        # Fallback to matplotlib
        fig, ax = plt.subplots(1, 1, figsize=(12, 10))

        # Use robust color scaling for outliers
        import matplotlib.colors as mcolors
        density_values = aggregated_gdf[density_column].dropna()
        if len(density_values) > 0:
            # Use percentiles for color scaling
            vmin = density_values.quantile(0.05)  # 5th percentile
            vmax = density_values.quantile(0.95)  # 95th percentile
            norm = mcolors.Normalize(vmin=vmin, vmax=vmax)
        else:
            norm = None

        aggregated_gdf.plot(column=density_column, ax=ax, cmap='RdYlBu_r',
                          legend=True, edgecolor='black', linewidth=0.5, norm=norm)
        ax.set_title(title, fontsize=16, fontweight='bold')
        ax.axis('off')

        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"Static map saved to {save_path}")

        plt.show()
        return fig

def main():
    """
    Main function to generate all Paris building density maps and return processed data.

    Returns:
    --------
    dict
        Dictionary containing all processed DataFrames organized by geographic level
    """
    print("=" * 60)
    print("PARIS BUILDING DENSITY ANALYSIS")
    print("=" * 60)

    # Initialize results dictionary
    results = {
        'arrondissements': {},
        'quartiers': {},
        'iris': {}
    }

    # Load geographic layers
    print("\n1. Loading geographic layers...")
    geo = GeoDataParis()
    geo_data = geo.load_all()
    visualiser_maillages(geo_data)

    # Load building data
    print("\n2. Loading building data...")
    buildings = load_building_data()

    # Load non-buildable areas
    print("\n3. Loading non-buildable areas...")
    non_buildable = load_non_buildable_areas()

    # Generate all density maps
    print("\n4. Generating building density maps...")

    for geo_level in ['arrondissements', 'quartiers', 'iris']:
        print(f"\n--- {geo_level.title()} ---")

        # Get appropriate geographic divisions
        geo_divisions = geo_data[geo_level]

        # Create raw density map
        print("Creating raw density map...")
        raw_data, _ = create_building_density_map(buildings, geo_divisions, geo_level)
        results[geo_level]['raw'] = raw_data

        # Create corrected density map (excluding water + railways)
        print("Creating corrected density map...")
        corrected_data, _ = create_corrected_building_density_map(buildings, geo_divisions, non_buildable, geo_level)
        results[geo_level]['corrected'] = corrected_data

        # Create ultra-corrected density map (excluding water + railways + green spaces)
        print("Creating ultra-corrected density map...")
        ultra_corrected_data, _ = create_ultra_corrected_building_density_map(buildings, geo_divisions, geo_level)
        results[geo_level]['ultra_corrected'] = ultra_corrected_data

    print("\n" + "=" * 60)
    print("COMPLETED: All building density maps created")
    print("Raw density maps:")
    print("- building_density_arrondissements.html")
    print("- building_density_quartiers.html")
    print("- building_density_iris.html")
    print("\nCorrected density maps (excluding water & railways):")
    print("- building_density_corrected_arrondissements.html")
    print("- building_density_corrected_quartiers.html")
    print("- building_density_corrected_iris.html")
    print("\nUltra-corrected density maps (excluding water + railways + green spaces):")
    print("- building_density_ultra_corrected_arrondissements.html")
    print("- building_density_ultra_corrected_quartiers.html")
    print("- building_density_ultra_corrected_iris.html")
    print("=" * 60)

    return results


if __name__ == "__main__":
    # Run the main analysis
    results = main()

    # Import and run data analysis if available
    try:
        from data_analysis import create_data_analysis
        print("\n5. Creating data analysis and visualizations...")
        create_data_analysis(results)
    except ImportError:
        print("\nNote: data_analysis.py not found - run create_data_analysis.py to generate plots and export data")
