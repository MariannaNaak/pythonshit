
import urllib, json, codecs
"""
Liest die JSON Datei direkt vom Server ein und speichert sie lokal in utf8

"""

url = "http://geoportal1.stadt-koeln.de/ArcGIS/rest/services/Spielangebote/MapServer/0/query?text=&geometry=&geometryType=esriGeometryPoint&inSR=&spatialRel=esriSpatialRelIntersects&relationParam=&objectIds=&where=objectid%20is%20not%20null&time=&returnCountOnly=false&returnIdsOnly=false&returnGeometry=true&maxAllowableOffset=&outSR=4326&outFields=%2A&f=json"
response = urllib.urlopen(url);
output_file = codecs.open("outfiles/playgrounds.json", "w", encoding="utf-8")

print "Daten werden heruntergeladen"

data = json.loads(response.read().decode("utf-8-sig"))
print "Daten erfolgreich heruntergeladen\n\n\n\n"

json.dump(data, output_file, indent=4, ensure_ascii=False)
print "Daten erfolgreich gespeichert"

