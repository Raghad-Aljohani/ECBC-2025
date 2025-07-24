import csv 

def coordCSVToDict(file): 
    '''This function converts a CSV file in the format of LOCATION, DLATITUDE, DLONGITUDE to a dictionary that maps each location
    to its longitude and latitude.'''
    with open(file, 'r', encoding='utf-8') as f: 
        tempDict = {}
        reader = csv.reader(f) 
        next(reader) 
        for row in reader: 
            (place, dlon, dlat) = row
            place = place.strip()
            dlon = float(dlon)
            dlat = float(dlat)
            tempDict[place] = (dlon, dlat)
    return tempDict

def mapDict(file, d): 
    '''Referencing the dictionary created by coordCSVToDict, this function converts a CSV file in the format of 
    YEAR, LOCATION, MENTIONS to a dictionary that maps (Year, Location) to [Number of Mentions, Location's Coordinates].'''
    with open(file, 'r', encoding='utf-8') as f:
        coordDict = {} 
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            (year, place, mentions) = row 
            year = int(year) 
            place = place.strip() 
            mentions = int(mentions)
            key = (year, place)
            if key not in coordDict: 
                loc = key[1] 
                val = d[loc]
                coordDict[key] = [0, val]
            coordDict[key][0] += mentions
    return coordDict

if __name__ == "__main__": 
    tempDict = coordCSVToDict('Coordinates.csv')
    coordDict = mapDict('Combined.csv', tempDict)
    sortedData = sorted(coordDict.items(), key=lambda x:(x[0][0], x[0][1])) #Sort location years in ascending order, then location names in alphabetical order
    with open('Map.csv', 'w', newline='', encoding='utf-8') as csvfile: #Store combined and condensed data into CSV file
        writer = csv.writer(csvfile)
        writer.writerow(['YEAR', 'PLACE', 'MENTIONS', 'DLATITUDE', 'DLONGITUDE'])
        for ((year, place), [mentions, (dlat, dlon)]) in sortedData: 
            writer.writerow([year, place, mentions, dlat, dlon])
