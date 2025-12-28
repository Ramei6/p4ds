import pandas as pd
import json


# ArRPostalRegion (arrets.csv)
path = "/home/kril/"


# return the transport station in Paris (df pandas) according to Idf mobilité
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
            'ArRName', 'ArRType', 'ArRTown',
            'ArRPostalRegion', 'ArRGeopoint'
        ]
    )

    mask = (
        (df_arrets["ArRPostalRegion"] >= 75000) &
        (df_arrets["ArRPostalRegion"] < 76000) &
        (df_arrets["ArRPostalRegion"] % 100 == nb_arrondissement)
    )

    return df_arrets.loc[mask]



###################### Number of station per Arrondissement ###################
def nb_bus_station(nb_arrondissement):
    df = InArrondissement(nb_arrondissement)
    nb_station = df[df["ArRType"].str.strip()== 'bus']["ArRName"].count()
    return nb_station



def nb_metro_station(nb_arrondissement):
    df = InArrondissement(nb_arrondissement)
    nb_station = df[df["ArRType"].str.strip()== 'metro']["ArRName"].count()
    return nb_station



def nb_tram_station(nb_arrondissement):
    df = InArrondissement(nb_arrondissement)
    nb_station = df[df["ArRType"].str.strip()== 'tram']["ArRName"].count()
    return nb_station

def nb_train_station(nb_arrondissement):
    df = InArrondissement(nb_arrondissement)
    nb_station = df[df["ArRType"].str.strip()== 'rail']["ArRName"].count()
    return nb_station
##########################################################################