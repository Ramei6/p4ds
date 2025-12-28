#!/usr/bin/env python3
"""
Testing script for GeoDataParis class.
Focus on testing carroyage functionality and overall data loading.
"""

import sys
import traceback
from geoclass import GeoDataParis

def test_individual_loads():
    """Test loading each geographical layer individually."""
    print("=" * 60)
    print("TESTING INDIVIDUAL DATA LOADING")
    print("=" * 60)

    geo = GeoDataParis()

    # Test methods and expected keys
    test_methods = [
        ('load_arrondissements', 'arrondissements'),
        ('load_quartiers', 'quartiers'),
        ('load_iris', 'iris')
    ]

    for method_name, expected_key in test_methods:
        print(f"\nTesting {method_name}()...")
        try:
            method = getattr(geo, method_name)
            result = method()

            if result is not None:
                print(f"  ✓ Success: {expected_key}")
                print(f"    Shape: {result.shape}")
                print(f"    Columns: {list(result.columns)}")
                print(f"    CRS: {result.crs}")

                # Check if data is actually loaded
                if expected_key in geo.data:
                    print(f"    Cached: {len(geo.data)} datasets loaded")
                else:
                    print("    ⚠️ Warning: Not cached properly")
            else:
                print(f"  ❌ Failed: {method_name} returned None")

        except Exception as e:
            print(f"  ❌ Error in {method_name}: {str(e)}")
            print(f"    Full traceback: {traceback.format_exc()}")

def test_load_all():
    """Test load_all method."""
    print("\n" + "=" * 60)
    print("TESTING LOAD_ALL METHOD")
    print("=" * 60)

    print("\nTesting load_all()...")
    try:
        geo = GeoDataParis()
        data = geo.load_all()
        print(f"  ✓ Success: {len(data)} datasets loaded")
        for key, gdf in data.items():
            print(f"    {key}: {gdf.shape}")
    except Exception as e:
        print(f"  ❌ Error: {str(e)}")
        print(f"    Full traceback: {traceback.format_exc()}")

def test_caching():
    """Test that caching works properly."""
    print("\n" + "=" * 60)
    print("TESTING CACHING BEHAVIOR")
    print("=" * 60)

    geo = GeoDataParis()

    print("\nTesting caching with multiple calls...")
    try:
        # First call
        arr1 = geo.load_arrondissements()
        print(f"First call - Shape: {arr1.shape}")

        # Second call (should use cache)
        arr2 = geo.load_arrondissements()
        print(f"Second call - Shape: {arr2.shape}")

        # Check if same object
        if arr1 is arr2:
            print("  ✓ Caching works: Same object returned")
        else:
            print("  ⚠️ Warning: Different objects returned (no caching)")

        print(f"Total cached datasets: {len(geo.data)}")

    except Exception as e:
        print(f"  ❌ Error in caching test: {str(e)}")



def test_visualization():
    """Test that visualization works with loaded data."""
    print("\n" + "=" * 60)
    print("TESTING VISUALIZATION")
    print("=" * 60)

    try:
        from annexfunctions import visualiser_maillages

        geo = GeoDataParis()
        data = geo.load_all()

        print(f"Loaded {len(data)} datasets for visualization")
        print("Attempting visualization (this may take a moment)...")

        # This would normally show a plot, but in testing we'll just check it doesn't crash
        visualiser_maillages(data)
        print("  ✓ Visualization completed successfully")

    except ImportError:
        print("  ⚠️ annexfunctions not available for testing")
    except Exception as e:
        print(f"  ❌ Visualization error: {str(e)}")
        print(f"    Full traceback: {traceback.format_exc()}")

def main():
    """Run all tests."""
    print("GeoDataParis Testing Script")
    print("===========================")
    print(f"Python version: {sys.version}")
    print(f"Working directory: {sys.path[0]}")

    try:
        test_individual_loads()
        test_load_all()
        test_caching()
        test_visualization()

        print("\n" + "=" * 60)
        print("TESTING COMPLETE")
        print("=" * 60)

    except KeyboardInterrupt:
        print("\nTesting interrupted by user")
    except Exception as e:
        print(f"\nUnexpected error during testing: {str(e)}")
        traceback.print_exc()

if __name__ == "__main__":
    main()
