import geopandas as gpd
import matplotlib.pyplot as plt

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
