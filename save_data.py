# -*- coding: UTF-8 -*-
import json, codecs
import pickle
from pprint import pprint

with open('outfiles/playgrounds.json') as data_file:    
    data = json.loads(data_file.read().decode("utf-8-sig"))

#Zeigt kurz die Keys in der json an
"""
for r in data:
    print r

Das sind die Felder:
features --> Listet alles auf
fieldAliases
fields --> alle Felder
displayFieldName
spatialReference
geometryType
"""
"""
for element in data["features"]:
    print  element["attributes"]
"""
#Aufbau eines gesamten Feldes
"""
Resultat ist der Spieplatzname des Spielplatzes an Index[99]
data["features"][99]["attributes"]["Spielplatzname"]

Das heisst, dass die Spielplaetze über den Index von features aufgerufen werden.
"""

#Liste der Key von jedem Spielplatz, einfach zur uebersicht
output_file = codecs.open("outfiles/keys.txt", "w")

for element in data["features"][0]["attributes"]:
    pickle.dump(element, output_file) 
   
output_file.close()

"""""""""
Unsere ausgewaehlten Felder sind:
Spielplatzname, Stadtteil, Stadtbezirk, Stadtviertel, Typ, Basketballkoerbe, Fussballtore, Skaterelemente, Tischtennisplatten,Torwand, Bemerkung
"""""""""

#Anzahl Spielplaetze
courts = len(data["features"])
i = 0

#Listen zum Speichern der Eintraege
spielplatzname = []
stadtteil = []
stadtbezirk = []

while i < courts:
     spielplatzname.append(data["features"][i]["attributes"]["Spielplatzname"])
     
     i = i+1


bla = codecs.open("outfiles/bla.txt", "w",encoding="utf-8")
for item in spielplatzname:
  bla.write("%s\n" % item)

bla.close()

