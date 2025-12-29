"""
Paris Building Density Data Visualization
Creates comprehensive statistical visualizations and analysis from extracted dataframes
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

# Set style for all plots
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")
plt.rcParams['figure.dpi'] = 100
plt.rcParams['savefig.dpi'] = 300

def load_dataframes():
    """
    Load the three main dataframes created by extract_density_dataframes.py
    """
    print("Loading dataframes...")

    arr_df = pd.read_csv('data/paris_arrondissements_complete.csv')
    quartiers_df = pd.read_csv('data/paris_quartiers_complete.csv')
    iris_df = pd.read_csv('data/paris_iris_complete.csv')

    print(f"Loaded: Arrondissements ({arr_df.shape[0]} zones), Quartiers ({quartiers_df.shape[0]} zones), IRIS ({iris_df.shape[0]} zones)")
    return arr_df, quartiers_df, iris_df

def create_density_distributions(df, level_name, save_dir="plots"):
    """
    Create density distribution plots for a geographic level
    """
    Path(save_dir).mkdir(exist_ok=True)

    print(f"Creating density distributions for {level_name}...")

    # Prepare data for plotting
    density_cols = [col for col in df.columns if 'density_m2_m2_' in col and 'ultra' in col]
    if not density_cols:
        density_cols = [col for col in df.columns if 'density_m2_m2_' in col]

    if not density_cols:
        print(f"No density columns found for {level_name}")
        return

    density_col = density_cols[0]  # Use ultra-corrected density

    # 1. Overall histogram with KDE
    fig, ax = plt.subplots(1, 1, figsize=(12, 8))
    sns.histplot(data=df, x=density_col, bins=30, kde=True, ax=ax, alpha=0.7)
    ax.set_title(f'Building Density Distribution - {level_name.title()}\n(n={len(df)} zones)', fontsize=16, fontweight='bold')
    ax.set_xlabel('Ultra-Corrected Density (m²/m²)', fontsize=12)
    ax.set_ylabel('Frequency', fontsize=12)
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(f"{save_dir}/density_histogram_{level_name}.png", dpi=300, bbox_inches='tight')
    plt.close()

    # 2. Box plot
    fig, ax = plt.subplots(1, 1, figsize=(10, 6))
    sns.boxplot(data=df, y=density_col, ax=ax, color='skyblue', width=0.4)
    ax.set_title(f'Building Density Box Plot - {level_name.title()}', fontsize=14, fontweight='bold')
    ax.set_ylabel('Ultra-Corrected Density (m²/m²)', fontsize=12)
    ax.grid(True, alpha=0.3, axis='y')
    plt.tight_layout()
    plt.savefig(f"{save_dir}/density_boxplot_{level_name}.png", dpi=300, bbox_inches='tight')
    plt.close()

    # 3. Violin plot
    fig, ax = plt.subplots(1, 1, figsize=(10, 6))
    sns.violinplot(data=df, y=density_col, ax=ax, color='lightgreen', inner='quartile')
    ax.set_title(f'Building Density Violin Plot - {level_name.title()}', fontsize=14, fontweight='bold')
    ax.set_ylabel('Ultra-Corrected Density (m²/m²)', fontsize=12)
    ax.grid(True, alpha=0.3, axis='y')
    plt.tight_layout()
    plt.savefig(f"{save_dir}/density_violin_{level_name}.png", dpi=300, bbox_inches='tight')
    plt.close()

def create_area_composition_charts(df, level_name, save_dir="plots"):
    """
    Create area composition charts (buildable vs excluded areas)
    """
    Path(save_dir).mkdir(exist_ok=True)

    print(f"Creating area composition charts for {level_name}...")

    # Check if we have the required columns
    if 'buildable_percentage_ultra' not in df.columns or 'excluded_percentage_ultra' not in df.columns:
        print(f"Missing area composition columns for {level_name}")
        return

    # Calculate averages for the level
    avg_buildable = df['buildable_percentage_ultra'].mean()
    avg_excluded = df['excluded_percentage_ultra'].mean()

    # 1. Overall pie chart for the level
    fig, ax = plt.subplots(1, 1, figsize=(10, 8))
    wedges, texts, autotexts = ax.pie([avg_buildable, avg_excluded],
                                    labels=['Buildable Areas', 'Excluded Areas\n(Water + Rail + Green)'],
                                    autopct='%1.1f%%', startangle=90,
                                    colors=['#4CAF50', '#FF5722'], explode=[0, 0.1])

    # Style the text
    for text in texts:
        text.set_fontsize(12)
        text.set_fontweight('bold')
    for autotext in autotexts:
        autotext.set_fontsize(11)
        autotext.set_color('white')
        autotext.set_fontweight('bold')

    ax.set_title(f'Area Composition - {level_name.title()}\nAverage Across All Zones (n={len(df)})',
                fontsize=16, fontweight='bold', pad=20)
    plt.tight_layout()
    plt.savefig(f"{save_dir}/area_composition_pie_{level_name}.png", dpi=300, bbox_inches='tight')
    plt.close()

    # 2. Buildable percentage distribution
    fig, ax = plt.subplots(1, 1, figsize=(12, 8))
    sns.histplot(data=df, x='buildable_percentage_ultra', bins=20, kde=True, ax=ax, color='skyblue')
    ax.set_title(f'Buildable Area Percentage Distribution - {level_name.title()}', fontsize=16, fontweight='bold')
    ax.set_xlabel('Buildable Area Percentage (%)', fontsize=12)
    ax.set_ylabel('Frequency', fontsize=12)
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(f"{save_dir}/buildable_percentage_dist_{level_name}.png", dpi=300, bbox_inches='tight')
    plt.close()

def create_comparative_analysis(arr_df, quartiers_df, iris_df, save_dir="plots"):
    """
    Create comparative analysis plots between geographic levels
    """
    Path(save_dir).mkdir(exist_ok=True)

    print("Creating comparative analysis plots...")

    # Prepare comparison data
    comparison_data = []

    # Get density column
    density_col = 'density_m2_m2_ultra_corrected'

    for level_name, df in [('arrondissements', arr_df), ('quartiers', quartiers_df), ('iris', iris_df)]:
        if density_col in df.columns:
            temp_df = df[[density_col]].copy()
            temp_df['level'] = level_name
            temp_df = temp_df.rename(columns={density_col: 'density'})
            comparison_data.append(temp_df)

    if comparison_data:
        combined_df = pd.concat(comparison_data, ignore_index=True)

        # 1. Box plot comparison
        fig, ax = plt.subplots(1, 1, figsize=(12, 8))
        sns.boxplot(data=combined_df, x='level', y='density', ax=ax,
                   palette=['#FF6B6B', '#4ECDC4', '#45B7D1'])
        ax.set_title('Building Density Comparison by Geographic Level', fontsize=16, fontweight='bold')
        ax.set_xlabel('Geographic Level', fontsize=12)
        ax.set_ylabel('Ultra-Corrected Density (m²/m²)', fontsize=12)
        ax.grid(True, alpha=0.3, axis='y')

        # Add sample size labels
        for i, level in enumerate(['arrondissements', 'quartiers', 'iris']):
            count = len([df for name, df in [('arrondissements', arr_df), ('quartiers', quartiers_df), ('iris', iris_df)] if name == level][0])
            ax.text(i, ax.get_ylim()[0] - (ax.get_ylim()[1] - ax.get_ylim()[0]) * 0.05,
                   f'n={count}', ha='center', va='top', fontsize=10, fontweight='bold')

        plt.tight_layout()
        plt.savefig(f"{save_dir}/density_comparison_levels.png", dpi=300, bbox_inches='tight')
        plt.close()

        # 2. Violin plot comparison
        fig, ax = plt.subplots(1, 1, figsize=(12, 8))
        sns.violinplot(data=combined_df, x='level', y='density', ax=ax,
                      palette=['#FF6B6B', '#4ECDC4', '#45B7D1'], inner='quartile')
        ax.set_title('Building Density Distribution Comparison by Geographic Level', fontsize=16, fontweight='bold')
        ax.set_xlabel('Geographic Level', fontsize=12)
        ax.set_ylabel('Ultra-Corrected Density (m²/m²)', fontsize=12)
        ax.grid(True, alpha=0.3, axis='y')
        plt.tight_layout()
        plt.savefig(f"{save_dir}/density_violin_comparison.png", dpi=300, bbox_inches='tight')
        plt.close()

def create_correlation_analysis(df, level_name, save_dir="plots"):
    """
    Create correlation analysis plots for a geographic level
    """
    Path(save_dir).mkdir(exist_ok=True)

    print(f"Creating correlation analysis for {level_name}...")

    # Select numeric columns for correlation
    numeric_cols = df.select_dtypes(include=[np.number]).columns

    # Focus on key metrics
    key_cols = []
    for col in numeric_cols:
        if any(keyword in col.lower() for keyword in ['density', 'percentage', 'area', 'volume']):
            key_cols.append(col)

    if len(key_cols) < 2:
        print(f"Not enough numeric columns for correlation analysis in {level_name}")
        return

    # Create correlation matrix
    corr_matrix = df[key_cols].corr()

    # 1. Correlation heatmap
    fig, ax = plt.subplots(1, 1, figsize=(12, 10))
    mask = np.triu(np.ones_like(corr_matrix, dtype=bool))
    sns.heatmap(corr_matrix, mask=mask, annot=True, cmap='coolwarm', center=0,
                square=True, linewidths=0.5, ax=ax, fmt='.2f', cbar_kws={'shrink': 0.8})
    ax.set_title(f'Correlation Matrix - {level_name.title()}', fontsize=16, fontweight='bold')
    plt.tight_layout()
    plt.savefig(f"{save_dir}/correlation_heatmap_{level_name}.png", dpi=300, bbox_inches='tight')
    plt.close()

    # 2. Key scatter plots
    density_col = [col for col in key_cols if 'ultra_corrected' in col and 'density' in col]
    if density_col:
        density_col = density_col[0]

        # Density vs Buildable Percentage
        buildable_col = [col for col in key_cols if 'buildable_percentage_ultra' in col]
        if buildable_col:
            fig, ax = plt.subplots(1, 1, figsize=(10, 8))
            sns.scatterplot(data=df, x=buildable_col[0], y=density_col, ax=ax, s=100, alpha=0.7)
            ax.set_title(f'Density vs Buildable Area - {level_name.title()}', fontsize=14, fontweight='bold')
            ax.set_xlabel('Buildable Area Percentage (%)', fontsize=12)
            ax.set_ylabel('Ultra-Corrected Density (m²/m²)', fontsize=12)
            ax.grid(True, alpha=0.3)

            # Add correlation coefficient
            corr = df[buildable_col[0]].corr(df[density_col])
            ax.text(0.05, 0.95, f'Correlation: {corr:.3f}',
                   transform=ax.transAxes, fontsize=12, verticalalignment='top',
                   bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))

            plt.tight_layout()
            plt.savefig(f"{save_dir}/density_vs_buildable_{level_name}.png", dpi=300, bbox_inches='tight')
            plt.close()

def generate_summary_statistics(arr_df, quartiers_df, iris_df, save_dir="plots"):
    """
    Generate comprehensive summary statistics
    """
    Path(save_dir).mkdir(exist_ok=True)

    print("Generating summary statistics...")

    # Create summary for all levels
    summary_data = []

    for level_name, df in [('Arrondissements', arr_df), ('Quartiers', quartiers_df), ('IRIS', iris_df)]:
        density_col = [col for col in df.columns if 'ultra_corrected' in col and 'density' in col]
        if density_col:
            density_col = density_col[0]
            stats = {
                'Level': level_name,
                'Zones': len(df),
                'Mean_Density': df[density_col].mean(),
                'Median_Density': df[density_col].median(),
                'Std_Density': df[density_col].std(),
                'Min_Density': df[density_col].min(),
                'Max_Density': df[density_col].max(),
                'Q25_Density': df[density_col].quantile(0.25),
                'Q75_Density': df[density_col].quantile(0.75)
            }

            # Add buildable percentage if available
            buildable_col = [col for col in df.columns if 'buildable_percentage_ultra' in col]
            if buildable_col:
                stats['Mean_Buildable_Pct'] = df[buildable_col[0]].mean()

            summary_data.append(stats)

    summary_df = pd.DataFrame(summary_data)

    # Save summary
    summary_df.to_csv(f"{save_dir}/summary_statistics.csv", index=False)

    # Print summary
    print("\n" + "="*80)
    print("BUILDING DENSITY ANALYSIS SUMMARY")
    print("="*80)

    for _, row in summary_df.iterrows():
        print(f"\n{row['Level'].upper()}:")
        print(f"  Zones: {int(row['Zones'])}")
        print(f"  Mean Density: {row['Mean_Density']:.3f} m²/m²")
        print(f"  Median Density: {row['Median_Density']:.3f} m²/m²")
        print(f"  Density Range: {row['Min_Density']:.3f} - {row['Max_Density']:.3f} m²/m²")
        if 'Mean_Buildable_Pct' in row:
            print(f"  Mean Buildable Area: {row['Mean_Buildable_Pct']:.1f}%")

    print("\n" + "="*80)

    # Create summary visualization
    fig, axes = plt.subplots(1, 3, figsize=(18, 6))

    # Density comparison
    levels = summary_df['Level']
    means = summary_df['Mean_Density']
    stds = summary_df['Std_Density']

    axes[0].bar(levels, means, yerr=stds, capsize=5, color=['#FF6B6B', '#4ECDC4', '#45B7D1'], alpha=0.7)
    axes[0].set_title('Mean Density by Geographic Level', fontsize=14, fontweight='bold')
    axes[0].set_ylabel('Ultra-Corrected Density (m²/m²)', fontsize=12)
    axes[0].grid(True, alpha=0.3, axis='y')

    # Zone count comparison
    zones = summary_df['Zones']
    axes[1].bar(levels, zones, color=['#FF6B6B', '#4ECDC4', '#45B7D1'], alpha=0.7)
    axes[1].set_title('Number of Zones by Geographic Level', fontsize=14, fontweight='bold')
    axes[1].set_ylabel('Number of Zones', fontsize=12)
    axes[1].grid(True, alpha=0.3, axis='y')

    # Density variability
    cv = stds / means * 100  # Coefficient of variation
    axes[2].bar(levels, cv, color=['#FF6B6B', '#4ECDC4', '#45B7D1'], alpha=0.7)
    axes[2].set_title('Density Variability by Geographic Level', fontsize=14, fontweight='bold')
    axes[2].set_ylabel('Coefficient of Variation (%)', fontsize=12)
    axes[2].grid(True, alpha=0.3, axis='y')

    plt.suptitle('Building Density Analysis Summary', fontsize=16, fontweight='bold', y=1.02)
    plt.tight_layout()
    plt.savefig(f"{save_dir}/analysis_summary.png", dpi=300, bbox_inches='tight')
    plt.close()

def create_top_zones_analysis(arr_df, quartiers_df, iris_df, save_dir="plots"):
    """
    Analyze and visualize top density zones
    """
    Path(save_dir).mkdir(exist_ok=True)

    print("Creating top zones analysis...")

    # Get density column
    density_col = 'density_m2_m2_ultra_corrected'

    # Find top 5 zones from each level
    top_zones = []

    for level_name, df, id_col, name_col in [
        ('Arrondissements', arr_df, 'arr_id', 'arr_name'),
        ('Quartiers', quartiers_df, 'quartier_id', 'quartier_name'),
        ('IRIS', iris_df, 'iris_code', 'iris_name')
    ]:
        if density_col in df.columns:
            top_5 = df.nlargest(5, density_col)[[id_col, name_col, density_col, 'buildable_percentage_ultra']].copy()
            top_5['level'] = level_name
            top_5 = top_5.rename(columns={
                id_col: 'zone_id',
                name_col: 'zone_name',
                density_col: 'density',
                'buildable_percentage_ultra': 'buildable_pct'
            })
            top_zones.append(top_5)

    if top_zones:
        combined_top = pd.concat(top_zones, ignore_index=True)

        # Create visualization
        fig, ax = plt.subplots(1, 1, figsize=(14, 8))

        # Create color mapping
        colors = {'Arrondissements': '#FF6B6B', 'Quartiers': '#4ECDC4', 'IRIS': '#45B7D1'}

        for level in ['Arrondissements', 'Quartiers', 'IRIS']:
            level_data = combined_top[combined_top['level'] == level]
            ax.scatter(level_data['buildable_pct'], level_data['density'],
                      s=150, alpha=0.8, color=colors[level], label=level, edgecolors='black', linewidth=0.5)

            # Add zone labels
            for _, row in level_data.iterrows():
                ax.annotate(f"{row['zone_name']}", (row['buildable_pct'], row['density']),
                           xytext=(5, 5), textcoords='offset points', fontsize=8, alpha=0.8)

        ax.set_title('Top 5 Highest Density Zones by Geographic Level', fontsize=16, fontweight='bold')
        ax.set_xlabel('Buildable Area Percentage (%)', fontsize=12)
        ax.set_ylabel('Ultra-Corrected Density (m²/m²)', fontsize=12)
        ax.legend(title='Geographic Level')
        ax.grid(True, alpha=0.3)

        plt.tight_layout()
        plt.savefig(f"{save_dir}/top_density_zones.png", dpi=300, bbox_inches='tight')
        plt.close()

        # Print top zones
        print("\nTOP 5 DENSITY ZONES BY LEVEL:")
        for level in ['Arrondissements', 'Quartiers', 'IRIS']:
            level_data = combined_top[combined_top['level'] == level]
            print(f"\n{level.upper()}:")
            for _, row in level_data.iterrows():
                print(".3f")

def main():
    """
    Main function to create all data visualizations
    """
    print("="*80)
    print("PARIS BUILDING DENSITY DATA VISUALIZATION")
    print("="*80)

    # Load dataframes
    arr_df, quartiers_df, iris_df = load_dataframes()

    print("\n" + "="*60)
    print("CREATING VISUALIZATIONS")
    print("="*60)

    # Create visualizations for each level
    for level_name, df in [('arrondissements', arr_df), ('quartiers', quartiers_df), ('iris', iris_df)]:
        print(f"\nProcessing {level_name}...")
        create_density_distributions(df, level_name)
        create_area_composition_charts(df, level_name)
        create_correlation_analysis(df, level_name)

    # Create comparative analysis
    print("\nProcessing comparative analysis...")
    create_comparative_analysis(arr_df, quartiers_df, iris_df)

    # Generate summary statistics
    print("\nGenerating summary statistics...")
    generate_summary_statistics(arr_df, quartiers_df, iris_df)

    # Create top zones analysis
    print("\nCreating top zones analysis...")
    create_top_zones_analysis(arr_df, quartiers_df, iris_df)

    print("\n" + "="*80)
    print("VISUALIZATION COMPLETE!")
    print("="*80)
    print("Generated files in 'plots/' directory:")
    print("- Density distribution plots (histograms, box plots, violin plots)")
    print("- Area composition charts (pie charts, distributions)")
    print("- Correlation analysis (heatmaps, scatter plots)")
    print("- Comparative analysis (level comparisons)")
    print("- Summary statistics and top zones analysis")
    print("- analysis_summary.png (overview dashboard)")
    print("\n" + "="*80)

if __name__ == "__main__":
    main()
