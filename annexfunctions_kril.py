import pandas as pd

# path of the file
path = "/home/kril/Data/"


##### return stations in Paris ####
def InParis():
    df_arrets = pd.read_csv(
        path + "arrets.csv",
        sep=';',
        usecols=[
            'ArRName', 'ArRType', 'ArRTown',
            'ArRPostalRegion', 'ArRGeopoint'
        ]
    )

    mask = (
        (df_arrets["ArRPostalRegion"] >= 75000) &
        (df_arrets["ArRPostalRegion"] < 76000)
    )
    return df_arrets.loc[mask]


# return the arrondissemnt of the transport station in Paris (df pandas) according to Idf mobilité
def InArrondissement(nb_arrondissement):
    df_arrets = pd.read_csv(
        path + "arrets.csv",
        sep=';',
        usecols=[
            'ArRName', 'ArRType', 
            'ArRPostalRegion'
        ]
    )

    mask = (
        (df_arrets["ArRPostalRegion"] >= 75000) &
        (df_arrets["ArRPostalRegion"] < 76000) &
        (df_arrets["ArRPostalRegion"] % 100 == nb_arrondissement)
    )

    return df_arrets.loc[mask]




############# functions that return the number of transport stations in each arrondissement of Paris ################

def BusInArrondissement(nb_arrondissement):
    df_arrets = pd.read_csv(
        path + "arrets.csv",
        sep=';',
        usecols=[
            'ArRName', 'ArRType', 
            'ArRPostalRegion'
        ]
    )

    mask = (
        (df_arrets["ArRPostalRegion"] >= 75000) &
        (df_arrets["ArRPostalRegion"] < 76000) &
        (df_arrets["ArRPostalRegion"] % 100 == nb_arrondissement) &
        (df_arrets["ArRPostalRegion"].st.strip() == "bus")
    )
    df_arret_arrondissement = df_arrets.loc[mask]
    nb_station = df_arret_arrondissement.shape[0]

    return nb_station

def MetroInArrondissement(nb_arrondissement):
    df_arrets = pd.read_csv(
        path + "arrets.csv",
        sep=';',
        usecols=[
            'ArRName', 'ArRType', 
            'ArRPostalRegion'
        ]
    )

    mask = (
        (df_arrets["ArRPostalRegion"] >= 75000) &
        (df_arrets["ArRPostalRegion"] < 76000) &
        (df_arrets["ArRPostalRegion"] % 100 == nb_arrondissement) &
        (df_arrets["ArRPostalRegion"].st.strip() == "metro")
    )
    df_arret_arrondissement = df_arrets.loc[mask]
    nb_station = df_arret_arrondissement.shape[0]

    return nb_station

def TramInArrondissement(nb_arrondissement):
    df_arrets = pd.read_csv(
        path + "arrets.csv",
        sep=';',
        usecols=[
            'ArRName', 'ArRType', 
            'ArRPostalRegion'
        ]
    )

    mask = (
        (df_arrets["ArRPostalRegion"] >= 75000) &
        (df_arrets["ArRPostalRegion"] < 76000) &
        (df_arrets["ArRPostalRegion"] % 100 == nb_arrondissement) &
        (df_arrets["ArRPostalRegion"].st.strip() == "tram")
    )
    df_arret_arrondissement = df_arrets.loc[mask]
    nb_station = df_arret_arrondissement.shape[0]

    return nb_station

def TrainInArrondissement(nb_arrondissement):
    df_arrets = pd.read_csv(
        path + "arrets.csv",
        sep=';',
        usecols=[
            'ArRName', 'ArRType', 
            'ArRPostalRegion'
        ]
    )

    mask = (
        (df_arrets["ArRPostalRegion"] >= 75000) &
        (df_arrets["ArRPostalRegion"] < 76000) &
        (df_arrets["ArRPostalRegion"] % 100 == nb_arrondissement) &
        (df_arrets["ArRPostalRegion"].st.strip() == "rail")
    )
    df_arret_arrondissement = df_arrets.loc[mask]
    nb_station = df_arret_arrondissement.shape[0]

    return nb_station



def TaxiInArrondissement(nb_arrondissement):
    df_taxi = pd.read_csv(
        path +"bornes-dappel-taxi.csv",
        sep=';',
        usecols=[
            'nom', 'insee', 'emplacements'
        ]
    )

    # Sécurisation + extraction de l’arrondissement
    mask = (
        (df_taxi["insee"] >= 75000) &
        (df_taxi["insee"] < 76000) &
        (df_taxi["insee"] % 100 == nb_arrondissement)
    )

    df_taxi_arrondissement = df_taxi.loc[mask]
    return df_taxi_arrondissement["emplacements"].sum()
##########################################################################