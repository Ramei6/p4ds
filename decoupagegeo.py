from geoclass import GeoDataParis
from annexfunctions import visualiser_maillages

# Usage example
if __name__ == "__main__":
    geo = GeoDataParis()
    data = geo.load_all()
    visualiser_maillages(data)
