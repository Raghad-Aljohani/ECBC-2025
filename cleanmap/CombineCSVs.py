from pathlib import Path
import csv 

def combineCSV(host): 
    '''This function loops over all CSV files in a specified folder and combines and condenses the data stored in them into 
    one dictionary. The resulting dictionary maps (Year, Location Name) to the location's number of mentions in that year.'''
    folder = Path(host)
    combinedDict = {} #Dictionary mapping (Year, Location Name) to number of mentions in that year.  
    for file in folder.glob("*.csv"): #Grab all files in folder ending in .csv (created using MakeRegexCSVs.py)
        with file.open(newline='', encoding='utf-8') as f:
            reader = csv.reader(f) 
            next(reader)
            for row in reader: 
                (year, place, mentions) = row 
                year = int(year) 
                place = place.strip()
                if place[-1].isdigit(): #If location has multiple patterns (ex. Kecoughtan1), remove the pattern number (ex. 1)
                    place = place[:-1]
                mentions = int(mentions)
                key = (year, place)
                if key not in combinedDict: #Ensure the (Year, Location Name) is unique (ex. (1619, Kecoughtan) is tracked only once)
                    combinedDict[key] = 0 
                combinedDict[key] += mentions
    return combinedDict

if __name__ == "__main__": 
    hostFolder = Path("/Users/yewonchang/Desktop/RegexOutputs")
    combinedDict = combineCSV(hostFolder)
    sortedData = sorted(combinedDict.items(), key=lambda x:(x[0][0], x[0][1])) #Sort location years in ascending order, then locations in alphabetical
    targetFolder = Path("/Users/yewonchang/Desktop/ManualMap")
    csv_path = targetFolder / f"Combined.csv"
    with csv_path.open('w', newline='', encoding='utf-8') as csvfile: #Make a new CSV file to store this condensed data 
        writer = csv.writer(csvfile)
        writer.writerow(['YEAR', 'PLACE', 'NUMBER OF MENTIONS'])
        for ((year, place), mentions) in sortedData: 
            writer.writerow([year, place, mentions])