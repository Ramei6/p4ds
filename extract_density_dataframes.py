"""
Extract Building Density DataFrames
Creates tidy dataframes for arrondissements, quartiers, and iris with surface areas and density metrics
"""

import pandas as pd
from pathlib import Path
from decoupagegeo import GeoDataParis, load_building_data, load_non_buildable_areas, load_all_nonbuildable_areas
from annexfunctions import aggregate_by_geographic_division, calculate_density, calculate_corrected_density, create_buildable_geometries

def create_arrondissements_dataframe():
    """
    Create comprehensive dataframe for Paris arrondissements with all density metrics.
    """
    print("Creating Arrondissements DataFrame...")

    # Load geographic data
    geo = GeoDataParis()
    geo_data = geo.load_all()
    buildings = load_building_data()

    # Load non-buildable areas
    non_buildable = load_non_buildable_areas()
    all_non_buildable, green_spaces = load_all_nonbuildable_areas()

    arrondissements = geo_data['arrondissements']

    # Calculate areas for original arrondissements
    arrondissements_with_areas = arrondissements.copy()
    arrondissements_with_areas['total_area_m2'] = arrondissements.geometry.area
    arrondissements_with_areas['total_area_km2'] = arrondissements_with_areas['total_area_m2'] / 1_000_000

    # Calculate buildable areas (excluding water + railways)
    buildable_areas_corrected = create_buildable_geometries(arrondissements, non_buildable)

    # Calculate ultra-buildable areas (excluding water + railways + green spaces)
    buildable_areas_ultra = create_buildable_geometries(arrondissements, all_non_buildable)

    # Merge area information
    arrondissements_complete = arrondissements_with_areas.merge(
        buildable_areas_corrected[['buildable_area_m2', 'buildable_percentage']],
        left_index=True, right_index=True, how='left', suffixes=('', '_corrected')
    ).merge(
        buildable_areas_ultra[['buildable_area_m2', 'buildable_percentage']],
        left_index=True, right_index=True, how='left', suffixes=('', '_ultra')
    )

    # Rename columns for clarity
    arrondissements_complete = arrondissements_complete.rename(columns={
        'buildable_area_m2': 'buildable_area_m2_corrected',
        'buildable_percentage': 'buildable_percentage_corrected',
        'buildable_area_m2_ultra': 'buildable_area_m2_ultra',
        'buildable_percentage_ultra': 'buildable_percentage_ultra'
    })

    # Calculate excluded areas
    arrondissements_complete['excluded_area_m2_corrected'] = (
        arrondissements_complete['total_area_m2'] - arrondissements_complete['buildable_area_m2_corrected']
    )
    arrondissements_complete['excluded_percentage_corrected'] = (
        100 - arrondissements_complete['buildable_percentage_corrected']
    )

    arrondissements_complete['excluded_area_m2_ultra'] = (
        arrondissements_complete['total_area_m2'] - arrondissements_complete['buildable_area_m2_ultra']
    )
    arrondissements_complete['excluded_percentage_ultra'] = (
        100 - arrondissements_complete['buildable_percentage_ultra']
    )

    # Convert areas to km²
    arrondissements_complete['buildable_area_km2_corrected'] = arrondissements_complete['buildable_area_m2_corrected'] / 1_000_000
    arrondissements_complete['excluded_area_km2_corrected'] = arrondissements_complete['excluded_area_m2_corrected'] / 1_000_000
    arrondissements_complete['buildable_area_km2_ultra'] = arrondissements_complete['buildable_area_m2_ultra'] / 1_000_000
    arrondissements_complete['excluded_area_km2_ultra'] = arrondissements_complete['excluded_area_m2_ultra'] / 1_000_000

    # Process density calculations for each type
    for density_type in ['raw', 'corrected', 'ultra_corrected']:
        print(f"  Processing {density_type} density calculations...")

        if density_type == 'raw':
            # Raw density: building area / total area
            aggregated = aggregate_by_geographic_division(
                buildings, arrondissements, value_column='M2_PL_TOT', agg_method='sum'
            )
            density_data = calculate_density(aggregated, 'M2_PL_TOT_sum')
            density_col = 'M2_PL_TOT_sum_density_m2_m2'

        elif density_type == 'corrected':
            # Corrected density: building area / buildable area (excluding water + railways)
            aggregated = aggregate_by_geographic_division(
                buildings, arrondissements, value_column='M2_PL_TOT', agg_method='sum'
            )
            # Merge with buildable areas
            aggregated_with_areas = aggregated.merge(
                buildable_areas_corrected[['buildable_area_m2']],
                left_index=True, right_index=True, how='left'
            )
            density_data = calculate_corrected_density(
                aggregated_with_areas, 'M2_PL_TOT_sum', 'buildable_area_m2'
            )
            density_col = 'M2_PL_TOT_sum_corrected_density_m2_m2'

        elif density_type == 'ultra_corrected':
            # Ultra-corrected density: building area / ultra-buildable area (excluding water + railways + green)
            aggregated = aggregate_by_geographic_division(
                buildings, arrondissements, value_column='M2_PL_TOT', agg_method='sum'
            )
            # Merge with ultra-buildable areas
            aggregated_with_areas = aggregated.merge(
                buildable_areas_ultra[['buildable_area_m2']],
                left_index=True, right_index=True, how='left'
            )
            density_data = calculate_corrected_density(
                aggregated_with_areas, 'M2_PL_TOT_sum', 'buildable_area_m2'
            )
            density_col = 'M2_PL_TOT_sum_corrected_density_m2_m2'

        # Extract relevant columns and merge
        # Note: calculate_density doesn't return area_km2, only the density column
        density_cols_to_keep = [density_col, 'M2_PL_TOT_sum']
        density_extract = density_data[density_cols_to_keep].copy()

        # Rename columns to include density type
        rename_dict = {}
        for col in density_extract.columns:
            if col == 'M2_PL_TOT_sum':
                rename_dict[col] = f'building_volume_m2_{density_type}'
            elif col == 'area_km2':
                rename_dict[col] = f'area_km2_{density_type}'
            elif density_col in col:
                rename_dict[col] = f'density_m2_m2_{density_type}'

        density_extract = density_extract.rename(columns=rename_dict)

        # Merge with main dataframe
        arrondissements_complete = arrondissements_complete.merge(
            density_extract, left_index=True, right_index=True, how='left'
        )

    # Add arrondissement identifiers
    arrondissements_complete['arr_id'] = arrondissements_complete.get('c_ar', arrondissements_complete.index)
    arrondissements_complete['arr_name'] = arrondissements_complete.get('l_ar', 'Unknown')

    # Reorder columns for clarity
    priority_cols = [
        'arr_id', 'arr_name', 'total_area_km2',
        'buildable_percentage_corrected', 'excluded_percentage_corrected',
        'buildable_area_km2_corrected', 'excluded_area_km2_corrected',
        'buildable_percentage_ultra', 'excluded_percentage_ultra',
        'buildable_area_km2_ultra', 'excluded_area_km2_ultra',
        'density_m2_m2_raw', 'density_m2_m2_corrected', 'density_m2_m2_ultra_corrected',
        'building_volume_m2_raw', 'building_volume_m2_corrected', 'building_volume_m2_ultra_corrected'
    ]

    # Keep only existing columns
    final_cols = [col for col in priority_cols if col in arrondissements_complete.columns]
    other_cols = [col for col in arrondissements_complete.columns if col not in final_cols]
    arrondissements_complete = arrondissements_complete[final_cols + other_cols]

    print(f"Created arrondissements dataframe: {arrondissements_complete.shape[0]} rows × {arrondissements_complete.shape[1]} columns")
    return arrondissements_complete

def create_quartiers_dataframe():
    """
    Create comprehensive dataframe for Paris quartiers with all density metrics.
    """
    print("Creating Quartiers DataFrame...")

    # Load geographic data
    geo = GeoDataParis()
    geo_data = geo.load_all()
    buildings = load_building_data()

    # Load non-buildable areas
    non_buildable = load_non_buildable_areas()
    all_non_buildable, green_spaces = load_all_nonbuildable_areas()

    quartiers = geo_data['quartiers']

    # Calculate areas for original quartiers
    quartiers_with_areas = quartiers.copy()
    quartiers_with_areas['total_area_m2'] = quartiers.geometry.area
    quartiers_with_areas['total_area_km2'] = quartiers_with_areas['total_area_m2'] / 1_000_000

    # Calculate buildable areas
    buildable_areas_corrected = create_buildable_geometries(quartiers, non_buildable)
    buildable_areas_ultra = create_buildable_geometries(quartiers, all_non_buildable)

    # Merge area information
    quartiers_complete = quartiers_with_areas.merge(
        buildable_areas_corrected[['buildable_area_m2', 'buildable_percentage']],
        left_index=True, right_index=True, how='left', suffixes=('', '_corrected')
    ).merge(
        buildable_areas_ultra[['buildable_area_m2', 'buildable_percentage']],
        left_index=True, right_index=True, how='left', suffixes=('', '_ultra')
    )

    # Rename columns for clarity
    quartiers_complete = quartiers_complete.rename(columns={
        'buildable_area_m2': 'buildable_area_m2_corrected',
        'buildable_percentage': 'buildable_percentage_corrected',
        'buildable_area_m2_ultra': 'buildable_area_m2_ultra',
        'buildable_percentage_ultra': 'buildable_percentage_ultra'
    })

    # Calculate excluded areas
    quartiers_complete['excluded_area_m2_corrected'] = (
        quartiers_complete['total_area_m2'] - quartiers_complete['buildable_area_m2_corrected']
    )
    quartiers_complete['excluded_percentage_corrected'] = (
        100 - quartiers_complete['buildable_percentage_corrected']
    )

    quartiers_complete['excluded_area_m2_ultra'] = (
        quartiers_complete['total_area_m2'] - quartiers_complete['buildable_area_m2_ultra']
    )
    quartiers_complete['excluded_percentage_ultra'] = (
        100 - quartiers_complete['buildable_percentage_ultra']
    )

    # Convert areas to km²
    quartiers_complete['buildable_area_km2_corrected'] = quartiers_complete['buildable_area_m2_corrected'] / 1_000_000
    quartiers_complete['excluded_area_km2_corrected'] = quartiers_complete['excluded_area_m2_corrected'] / 1_000_000
    quartiers_complete['buildable_area_km2_ultra'] = quartiers_complete['buildable_area_m2_ultra'] / 1_000_000
    quartiers_complete['excluded_area_km2_ultra'] = quartiers_complete['excluded_area_m2_ultra'] / 1_000_000

    # Process density calculations for each type
    for density_type in ['raw', 'corrected', 'ultra_corrected']:
        print(f"  Processing {density_type} density calculations...")

        if density_type == 'raw':
            aggregated = aggregate_by_geographic_division(
                buildings, quartiers, value_column='M2_PL_TOT', agg_method='sum'
            )
            density_data = calculate_density(aggregated, 'M2_PL_TOT_sum')
            density_col = 'M2_PL_TOT_sum_density_m2_m2'

        elif density_type == 'corrected':
            aggregated = aggregate_by_geographic_division(
                buildings, quartiers, value_column='M2_PL_TOT', agg_method='sum'
            )
            aggregated_with_areas = aggregated.merge(
                buildable_areas_corrected[['buildable_area_m2']],
                left_index=True, right_index=True, how='left'
            )
            density_data = calculate_corrected_density(
                aggregated_with_areas, 'M2_PL_TOT_sum', 'buildable_area_m2'
            )
            density_col = 'M2_PL_TOT_sum_corrected_density_m2_m2'

        elif density_type == 'ultra_corrected':
            aggregated = aggregate_by_geographic_division(
                buildings, quartiers, value_column='M2_PL_TOT', agg_method='sum'
            )
            aggregated_with_areas = aggregated.merge(
                buildable_areas_ultra[['buildable_area_m2']],
                left_index=True, right_index=True, how='left'
            )
            density_data = calculate_corrected_density(
                aggregated_with_areas, 'M2_PL_TOT_sum', 'buildable_area_m2'
            )
            density_col = 'M2_PL_TOT_sum_corrected_density_m2_m2'

        # Extract relevant columns and merge
        density_cols_to_keep = [density_col, 'M2_PL_TOT_sum']
        density_extract = density_data[density_cols_to_keep].copy()

        # Rename columns to include density type
        rename_dict = {}
        for col in density_extract.columns:
            if col == 'M2_PL_TOT_sum':
                rename_dict[col] = f'building_volume_m2_{density_type}'
            elif col == 'area_km2':
                rename_dict[col] = f'area_km2_{density_type}'
            elif density_col in col:
                rename_dict[col] = f'density_m2_m2_{density_type}'

        density_extract = density_extract.rename(columns=rename_dict)

        # Merge with main dataframe
        quartiers_complete = quartiers_complete.merge(
            density_extract, left_index=True, right_index=True, how='left'
        )

    # Add quartier identifiers
    quartiers_complete['quartier_id'] = quartiers_complete.get('c_qu', quartiers_complete.get('c_qa', quartiers_complete.index))
    quartiers_complete['quartier_name'] = quartiers_complete.get('l_qu', quartiers_complete.get('l_qa', 'Unknown'))

    # Reorder columns for clarity
    priority_cols = [
        'quartier_id', 'quartier_name', 'total_area_km2',
        'buildable_percentage_corrected', 'excluded_percentage_corrected',
        'buildable_area_km2_corrected', 'excluded_area_km2_corrected',
        'buildable_percentage_ultra', 'excluded_percentage_ultra',
        'buildable_area_km2_ultra', 'excluded_area_km2_ultra',
        'density_m2_m2_raw', 'density_m2_m2_corrected', 'density_m2_m2_ultra_corrected',
        'building_volume_m2_raw', 'building_volume_m2_corrected', 'building_volume_m2_ultra_corrected'
    ]

    # Keep only existing columns
    final_cols = [col for col in priority_cols if col in quartiers_complete.columns]
    other_cols = [col for col in quartiers_complete.columns if col not in final_cols]
    quartiers_complete = quartiers_complete[final_cols + other_cols]

    print(f"Created quartiers dataframe: {quartiers_complete.shape[0]} rows × {quartiers_complete.shape[1]} columns")
    return quartiers_complete

def create_iris_dataframe():
    """
    Create comprehensive dataframe for Paris IRIS with all density metrics.
    """
    print("Creating IRIS DataFrame...")

    # Load geographic data
    geo = GeoDataParis()
    geo_data = geo.load_all()
    buildings = load_building_data()

    # Load non-buildable areas
    non_buildable = load_non_buildable_areas()
    all_non_buildable, green_spaces = load_all_nonbuildable_areas()

    iris = geo_data['iris']

    # Calculate areas for original iris
    iris_with_areas = iris.copy()
    iris_with_areas['total_area_m2'] = iris.geometry.area
    iris_with_areas['total_area_km2'] = iris_with_areas['total_area_m2'] / 1_000_000

    # Calculate buildable areas
    buildable_areas_corrected = create_buildable_geometries(iris, non_buildable)
    buildable_areas_ultra = create_buildable_geometries(iris, all_non_buildable)

    # Merge area information
    iris_complete = iris_with_areas.merge(
        buildable_areas_corrected[['buildable_area_m2', 'buildable_percentage']],
        left_index=True, right_index=True, how='left', suffixes=('', '_corrected')
    ).merge(
        buildable_areas_ultra[['buildable_area_m2', 'buildable_percentage']],
        left_index=True, right_index=True, how='left', suffixes=('', '_ultra')
    )

    # Rename columns for clarity
    iris_complete = iris_complete.rename(columns={
        'buildable_area_m2': 'buildable_area_m2_corrected',
        'buildable_percentage': 'buildable_percentage_corrected',
        'buildable_area_m2_ultra': 'buildable_area_m2_ultra',
        'buildable_percentage_ultra': 'buildable_percentage_ultra'
    })

    # Calculate excluded areas
    iris_complete['excluded_area_m2_corrected'] = (
        iris_complete['total_area_m2'] - iris_complete['buildable_area_m2_corrected']
    )
    iris_complete['excluded_percentage_corrected'] = (
        100 - iris_complete['buildable_percentage_corrected']
    )

    iris_complete['excluded_area_m2_ultra'] = (
        iris_complete['total_area_m2'] - iris_complete['buildable_area_m2_ultra']
    )
    iris_complete['excluded_percentage_ultra'] = (
        100 - iris_complete['buildable_percentage_ultra']
    )

    # Convert areas to km²
    iris_complete['buildable_area_km2_corrected'] = iris_complete['buildable_area_m2_corrected'] / 1_000_000
    iris_complete['excluded_area_km2_corrected'] = iris_complete['excluded_area_m2_corrected'] / 1_000_000
    iris_complete['buildable_area_km2_ultra'] = iris_complete['buildable_area_m2_ultra'] / 1_000_000
    iris_complete['excluded_area_km2_ultra'] = iris_complete['excluded_area_m2_ultra'] / 1_000_000

    # Process density calculations for each type
    for density_type in ['raw', 'corrected', 'ultra_corrected']:
        print(f"  Processing {density_type} density calculations...")

        if density_type == 'raw':
            aggregated = aggregate_by_geographic_division(
                buildings, iris, value_column='M2_PL_TOT', agg_method='sum'
            )
            density_data = calculate_density(aggregated, 'M2_PL_TOT_sum')
            density_col = 'M2_PL_TOT_sum_density_m2_m2'

        elif density_type == 'corrected':
            aggregated = aggregate_by_geographic_division(
                buildings, iris, value_column='M2_PL_TOT', agg_method='sum'
            )
            aggregated_with_areas = aggregated.merge(
                buildable_areas_corrected[['buildable_area_m2']],
                left_index=True, right_index=True, how='left'
            )
            density_data = calculate_corrected_density(
                aggregated_with_areas, 'M2_PL_TOT_sum', 'buildable_area_m2'
            )
            density_col = 'M2_PL_TOT_sum_corrected_density_m2_m2'

        elif density_type == 'ultra_corrected':
            aggregated = aggregate_by_geographic_division(
                buildings, iris, value_column='M2_PL_TOT', agg_method='sum'
            )
            aggregated_with_areas = aggregated.merge(
                buildable_areas_ultra[['buildable_area_m2']],
                left_index=True, right_index=True, how='left'
            )
            density_data = calculate_corrected_density(
                aggregated_with_areas, 'M2_PL_TOT_sum', 'buildable_area_m2'
            )
            density_col = 'M2_PL_TOT_sum_corrected_density_m2_m2'

        # Extract relevant columns and merge
        density_cols_to_keep = [density_col, 'M2_PL_TOT_sum']
        density_extract = density_data[density_cols_to_keep].copy()

        # Rename columns to include density type
        rename_dict = {}
        for col in density_extract.columns:
            if col == 'M2_PL_TOT_sum':
                rename_dict[col] = f'building_volume_m2_{density_type}'
            elif col == 'area_km2':
                rename_dict[col] = f'area_km2_{density_type}'
            elif density_col in col:
                rename_dict[col] = f'density_m2_m2_{density_type}'

        density_extract = density_extract.rename(columns=rename_dict)

        # Merge with main dataframe
        iris_complete = iris_complete.merge(
            density_extract, left_index=True, right_index=True, how='left'
        )

    # Add IRIS identifiers
    iris_complete['iris_code'] = iris_complete.get('CODE_IRIS', iris_complete.get('iris_code', iris_complete.index))
    iris_complete['iris_name'] = iris_complete.get('LIB_IRIS', 'Unknown')

    # Reorder columns for clarity
    priority_cols = [
        'iris_code', 'iris_name', 'total_area_km2',
        'buildable_percentage_corrected', 'excluded_percentage_corrected',
        'buildable_area_km2_corrected', 'excluded_area_km2_corrected',
        'buildable_percentage_ultra', 'excluded_percentage_ultra',
        'buildable_area_km2_ultra', 'excluded_area_km2_ultra',
        'density_m2_m2_raw', 'density_m2_m2_corrected', 'density_m2_m2_ultra_corrected',
        'building_volume_m2_raw', 'building_volume_m2_corrected', 'building_volume_m2_ultra_corrected'
    ]

    # Keep only existing columns
    final_cols = [col for col in priority_cols if col in iris_complete.columns]
    other_cols = [col for col in iris_complete.columns if col not in final_cols]
    iris_complete = iris_complete[final_cols + other_cols]

    print(f"Created IRIS dataframe: {iris_complete.shape[0]} rows × {iris_complete.shape[1]} columns")
    return iris_complete

def save_dataframes(arr_df, quartiers_df, iris_df, output_dir="data"):
    """
    Save all three dataframes to CSV format (Parquet requires pyarrow).
    """
    Path(output_dir).mkdir(exist_ok=True)

    print("Saving dataframes to CSV...")

    # Save arrondissements
    arr_df.to_csv(f"{output_dir}/paris_arrondissements_complete.csv", index=False)
    print(f"Saved arrondissements: {arr_df.shape[0]} rows × {arr_df.shape[1]} columns")

    # Save quartiers
    quartiers_df.to_csv(f"{output_dir}/paris_quartiers_complete.csv", index=False)
    print(f"Saved quartiers: {quartiers_df.shape[0]} rows × {quartiers_df.shape[1]} columns")

    # Save IRIS
    iris_df.to_csv(f"{output_dir}/paris_iris_complete.csv", index=False)
    print(f"Saved IRIS: {iris_df.shape[0]} rows × {iris_df.shape[1]} columns")

def main():
    """
    Main function to extract comprehensive building density dataframes.
    """
    print("="*80)
    print("PARIS BUILDING DENSITY DATA EXTRACTION")
    print("="*80)

    # Create all three dataframes
    arr_df = create_arrondissements_dataframe()
    print()
    quartiers_df = create_quartiers_dataframe()
    print()
    iris_df = create_iris_dataframe()

    print("\n" + "="*80)
    print("DATA EXTRACTION COMPLETE")
    print("="*80)

    # Display summary
    print("Summary:")
    print(f"  Arrondissements: {arr_df.shape[0]} zones × {arr_df.shape[1]} features")
    print(f"  Quartiers: {quartiers_df.shape[0]} zones × {quartiers_df.shape[1]} features")
    print(f"  IRIS: {iris_df.shape[0]} zones × {iris_df.shape[1]} features")

    # Save dataframes
    save_dataframes(arr_df, quartiers_df, iris_df)

    print("\nFiles saved to 'data/' directory:")
    print("- paris_arrondissements_complete.csv/.parquet")
    print("- paris_quartiers_complete.csv/.parquet")
    print("- paris_iris_complete.csv/.parquet")

    print("\n" + "="*80)

    return arr_df, quartiers_df, iris_df

if __name__ == "__main__":
    # Run the data extraction
    arr_df, quartiers_df, iris_df = main()

    # Optional: Display first few rows of each dataframe
    print("\nArrondissements preview:")
    print(arr_df[['arr_id', 'arr_name', 'total_area_km2', 'buildable_percentage_ultra', 'density_m2_m2_ultra_corrected']].head())

    print("\nQuartiers preview:")
    print(quartiers_df[['quartier_id', 'quartier_name', 'total_area_km2', 'buildable_percentage_ultra', 'density_m2_m2_ultra_corrected']].head())

    print("\nIRIS preview:")
    print(iris_df[['iris_code', 'iris_name', 'total_area_km2', 'buildable_percentage_ultra', 'density_m2_m2_ultra_corrected']].head())
