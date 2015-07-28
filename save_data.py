# -*- coding: UTF-8 -*-
import json, codecs
import pickle
from pprint import pprint
import sqlite3
from itertools import izip

conn = sqlite3.connect('spielplaetze.db')
c = conn.cursor()
jsonfile = codecs.open("outfiles/playgrounds.json", "r", "utf-8")
data = json.loads(jsonfile.read())
jsonfile.close()

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
    encoded_element = element.encode("utf-8")
    pickle.dump(encoded_element, output_file) 
   
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
stadtviertel = []
typ = []
basketballkoerbe = []
fussballtore = []
skaterelemente = []
tischtennisplatten = []
torwand = []
bemerkung = []

while i < courts:
     sn = (data["features"][i]["attributes"]["Spielplatzname"])
     spielplatzname.append(sn)
     
     st = (data["features"][i]["attributes"]["Stadtteil"])
     stadtteil.append(st)
     
     sb = (data["features"][i]["attributes"]["Stadtbezirk"])
     stadtbezirk.append(sb)
     
     sv = (data["features"][i]["attributes"]["Stadtviertel"])
     stadtviertel.append(sv)
     
     t = (data["features"][i]["attributes"]["Typ"])
     typ.append(t)
     
     bk = (data["features"][i]["attributes"]["Basketballkoerbe"])
     basketballkoerbe.append(bk)
     
     ft = (data["features"][i]["attributes"]["Fussballtore"])
     fussballtore.append(ft)
     
     sk = (data["features"][i]["attributes"]["Skaterelemente"])
     skaterelemente.append(sk)
     
     tp = (data["features"][i]["attributes"]["Tischtennisplatten"])
     tischtennisplatten.append(tp)
     
     tw = (data["features"][i]["attributes"]["Torwand"])
     torwand.append(tw)
     
     b = (data["features"][i]["attributes"]["Bemerkung"])
     bemerkung.append(b)
          
     i = i+1
for x in stadtviertel:
    print x


"""    
for item in spielplatzname:
  c.execute('insert into daten(Spielplatzname) values (:item)', {'item':item})
db.commit()
"""
