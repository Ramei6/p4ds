# Spatial Aggregation Methodology with GeoDataParis

## Core Methodology: Spatial Aggregation

The process involves **spatial joins** followed by **group-by aggregations**, where geographical divisions act as the "grouping categories" instead of traditional categorical columns.

### Step 1: Load Your Data Layers
```python
from decoupagegeo import GeoDataParis
geo = GeoDataParis()
divisions = geo.load_all()  # Your "group by" categories
```

### Step 2: Prepare Your Data to Aggregate
Assume you have a GeoDataFrame with point/polygon data and attributes to aggregate:
```python
# Example: buildings with surface area, population data with counts, etc.
buildings_gdf = gpd.read_file('your_buildings.shp')
population_gdf = gpd.read_file('your_population.shp')
```

### Step 3: Spatial Join - Assign Data to Divisions
Use geopandas `sjoin` to spatially match your data to divisions:

**For Point-in-Polygon (most common):**
```python
# Assign buildings to arrondissements
buildings_with_arr = gpd.sjoin(
    buildings_gdf,
    divisions['arrondissements'],
    how='left',  # Keep all buildings, add arrondissement info
    predicate='within'  # Point within polygon
)
```

**For Polygon Intersections:**
```python
# If your data are polygons (e.g., building footprints)
buildings_with_arr = gpd.sjoin(
    buildings_gdf,
    divisions['arrondissements'],
    how='left',
    predicate='intersects'  # Any intersection
)
```

### Step 4: Aggregate by Division
```python
# Group by arrondissement and sum surface areas
arr_summary = buildings_with_arr.groupby('c_ar').agg({
    'surface_bati': 'sum',  # Total building surface per arrondissement
    'nbr_etages': 'mean',   # Average floors per arrondissement
}).reset_index()
```

### Step 5: Join Back to Geography for Mapping
```python
# Merge aggregated data back to arrondissements for choropleth maps
arrondissements_with_data = divisions['arrondissements'].merge(
    arr_summary,
    on='c_ar',  # Join key
    how='left'
)
```

## Advanced Patterns

### Multi-Level Aggregation
```python
# Same data, different granularities
arr_agg = aggregate_by_division(buildings_gdf, divisions['arrondissements'])
iris_agg = aggregate_by_division(buildings_gdf, divisions['iris'])
quart_agg = aggregate_by_division(buildings_gdf, divisions['quartiers'])
```

### Spatial Overlay for Complex Cases
When you need proportional allocation (e.g., a building spans multiple IRIS):
```python
# Use overlay for area-weighted allocation
overlay_result = gpd.overlay(
    buildings_gdf,
    divisions['iris'],
    how='intersection'
)
overlay_result['area_fraction'] = overlay_result.geometry.area / overlay_result['original_area']
overlay_result['weighted_value'] = overlay_result['building_value'] * overlay_result['area_fraction']
```

## Tool Enhancement Ideas

You could extend GeoDataParis with aggregation methods:
```python
class GeoDataParis:
    # ... existing methods ...

    def aggregate_data(self, data_gdf, division_key, agg_dict, predicate='within'):
        """Aggregate geographical data by a division layer."""
        division_gdf = self.get_data(division_key)
        joined = gpd.sjoin(data_gdf, division_gdf, how='left', predicate=predicate)
        return joined.groupby(f'{division_key}_id').agg(agg_dict).reset_index()
```

## Best Practices

1. **Choose Appropriate Predicate:**
   - `within`: For points in polygons
   - `intersects`: For any overlap
   - `contains`: When division contains the data

2. **Handle Edge Cases:**
   - Data outside all divisions (null values)
   - Multiple assignments (choose how='left' vs 'inner')
   - Coordinate system consistency (ensure same CRS)

3. **Performance:**
   - Use spatial indices (automatic in geopandas)
   - Filter data geographically before joining
   - Consider grid-based divisions for very large datasets

4. **Validation:**
   - Check for data loss (total sums before/after)
   - Visualize joins to verify correctness

This gives you flexible spatial aggregation where geographical divisions become reusable "group by" categories for any future dataset with spatial components.
