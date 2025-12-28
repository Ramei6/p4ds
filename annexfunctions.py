import pandas as pd
import json


# ArRPostalRegion (arrets.csv)
path = /home/kril/


# return the transport station in Paris (df pandas) according to Idf mobilité
def ArretInParis():
    df_arrets = pd.read_csv(path +"arrets.csv",sep= ';', usecols=['ArRName', 'ArRType','ArRTown', 'ArRPostalRegion','ArRAccessibility','ArRFareZone', 'ArRGeopoint'])
    df_arrets_Paris = df_arrets[df_arrets['ArRPostalRegion'].astype(str).str.match(r"^75")]
    return df_arrets_Paris






# return the arrondissemnt of the transport station in Paris (df pandas) according to Idf mobilité
def InArrondissement(nb_arrondissement):
    df_arrets = pd.read_csv(path +"arrets.csv",sep= ';', usecols=['ArRName', 'ArRType','ArRTown', 'ArRPostalRegion','ArRAccessibility','ArRFareZone', 'ArRGeopoint'])
    df_arrets_Paris = df_arrets[df_arrets['ArRPostalRegion'].astype(str).str.match(r"^")]
    return df_arrets_Paris