from pathlib import Path
import json
import csv 
import re 

#Dictionary mapping a key location to its corresponding regex (and thus accounts for its historical spelling variations). 
#Locations extracted using a combination of NER and manual cleaning; regex generated manually. 
tempDict = {
    "Martin's Hundred": r"""mart[iy]n(?:'s|s)?(?:-|\s+)hundred""",
    "Smith's Hundred":  r"""sm[yi]?the?(?:'s|s)?(?:-|\s+)hundred""",
    "Berkeley's Hundred":   r"""berke?le?y(?:'s|s)?(?:-|\s+)hundred""",
    "Bermuda Hundred":   r"""bermuda(?:'s|s)?(?:-|\s+)hundred""",
    "Southampton Hundred":  r"""so?uthampto?n(?:-|\s+)hundred""",
    "Elizabeth City": r"""eli[zs]abeth?(?:-|\s)+citt?(?:y|ie)""",
    "Jamestown": r"""[ji]ames?(?:\s+|-)?towne?""",
    "James City": r"""[ji]ames?(?:\s+|-)citt?(?:y|ie)""",
    "Charles City": r"""ch?arle?s(?:\s+|-)+citt?(?:y|ie)""",
    "Chesapeake Bay": r"""ches[aei]p[ie]?[ae]?c?ke?""",
    "Henrico City": r"""hene?ric(?:o|us)""",
    "James River": r"""[ji]ames?(?:\s+|-)+ri[uv]?er""",
    "Point Comfort": r"""pointe?(?:-|\s+)?comforte?""",
    "Cape Comfort": r"""cape?(?:-|\s+)comforte?""",
    "Cape Henry": r"""cape?\s+henry?""",
    "Chickahominy River": r"""chick[ao]hom[ai]n[iy](?:-|\s+)ri[uv]?er""",
    "Potomac River": r"""p[ao]t[oa](?:wa)?m[ae]ck(?:-|\s+)ri[uv]?er""",
    "Plymouth": r"""pl[yi]mm?ou?th""",
    "Cape Cod": r"""cape(?:-|\s+)codd?""",
    "Newfoundland": r"""new\s+?fo[uw]ndland""",
    "West Indies": r"""west(?:-|\s+)ind[iy]es""",
    "Somers Isles": r"""s[uo]mm?ers?(?:-|\s+)islands?""",
    "Newport News": r"""n(?:ew|u)porte?s?(?:-|\s+)+newe?s""",
    "Roanoke": r"""roanoc?ke?""",
    "Blunt's Point": r"""blunt(?:'s|s)?(?:-|\s+)?po[iy]nt""",
    "Warrascoyack1": r"""warr?[oi]s[cq](?:o|ua|a)yac?ke?""", #Requires multiple patterns to capture all variations. 
    "Warrascoyack2": r"""warr?is[ec]o?yac?ke?""",
    "Mattaponi River": r"""mat?t[ea]p[ao]n[iy]""",
    "Pamunkey River": r"""pa(?:co)?m(?:o|a)?unke?y(?:\s+|-)ri[uv]e?r""",
    "Choapooks Creek": r"""ch[oi]a?pp?oo?ke?s(?:\s+|-)creek""",
    "Ritanoe": r"""R[ie]tt?anoe?w?""",
    "Moyompo": r"""Moyompo?s?""",
    "Monahigon": r"""Mon[ae]h?i[gc][oa]?[nm]""",
    "Bowiers Bay": r"""b[ou]w?(?:ie|y)rs?""",
    "Queen's Creek": r"""quee?ne?(?:'s|s)?(?:\s|-)cree?k""",
    "Appomattox": r"""ap[oa]matt?[uo]cke?""",
    "Tappahanna": r"""tapp?ahann?a""",
    "Rappahannock River": r"""rapp?ahan?noc?k?e?""",
    "Smith's Island": r"""smith(?:'s|s)\s+island""",
    "Kecoughtan1": r"""kice?(?:a|o|co)?wt[ao]n""", #Requires multiple patterns to capture all variations. 
    "Kecoughtan2": r"""k(?:ey|i)ec?o(?:ugh|w)?t[ao]n""",
    "Kecoughtan3": r"""k(?:i|ec)k(?:a|e)t[ao]n""",
    "Kecoughtan4": r"""k[ie][qc]n?(?:uo|ou)u?g?h?t[ao]n"""
}

patDict= {}
for (name, pat) in tempDict.items(): 
    patDict[name] = re.compile(pat, flags=re.IGNORECASE) #Compiles regex pattern into regex object; makes regex case-insensitive 

def parseYear(file):
   '''This function produces a dictionary that matches a page in the VCR .json file to its estimated date of authorship.'''
   year = 0 #To intialize, but note that if year = 0, the page is likely an INTRODUCTION page (and thus not a record) 
   yearDict = {}
   items = list(file.items())
   for i in range(len(items)):
       (page, data) = (items[i][0], items[i][1]) #page number (key), text (value)
       text = data.split()
       if len(text) > 3: #To account for blank/short pages 
           for string in text: 
                if string.isdigit(): #Capture first numerical string, as it is likely to be a year 
                    try: 
                        if 1626 >= int(string) >= 1606: #Must fall within range of VCR (1606-1626)
                            year = int(string)
                            break
                    except ValueError: #If it's a numerical subscript or superscript 
                        continue
           else: 
               if i > 0: #Other than the first page 
                   year = yearDict[str(int(page)-1)] #If no year is found, use the year of the previous page 
       yearDict[page] = year #Assign the year
   return yearDict

def patMatchDict(file): 
    '''This function produces a dictionary that maps a page in the VCR to a list of dictionaries in the format of 
    {Location Name: Number of Times Found In Page, ...}.'''
    matchDict = {}
    for (page, data) in file.items(): 
        cleanData = ' '.join(data.split())
        for (name, pattern) in patDict.items(): 
            matches = pattern.findall(cleanData) #For each location, finds all strings matching regex pattern (thus accounting for spelling variations) 
            if len(matches) > 0: #If matches found 
                if page not in matchDict:
                    matchDict[page] = {} 
                matchDict[page][name] = len(matches) 
    return matchDict

def joinDict(yearDict, matchDict):
    '''This function produces a dictionary that maps a VCR page's estimated year of authorship to a list of dictionaries 
    in the format of {Location Name: Number of Times Found In Page, ...}.'''
    joinDict = {}
    for (page, info) in matchDict.items():
        year = yearDict[page]
        if year not in joinDict:
            joinDict[year] = []
        joinDict[year] += [info]
    return joinDict 

def finalDict(data): 
    '''This function produces a dictionary that maps a VCR page's estimated year of authorship to a list of dictionaries in the format of
    {Location Name: Number of Times Found In Page, ...}.'''
    d = {}
    for (year, dictLst) in data.items(): 
        if year > 0: #Removes all pages assigned year 0 (with the assumption that they are INTRODUCTION sections)
            if year not in d: 
                d[year] = {}
            for dict in dictLst: 
                for (place, mentions) in dict.items(): 
                    if place not in d[year]:
                        d[year][place] = 0 
                    d[year][place] += mentions
    return d

if __name__ == "__main__": 
    hostFolder = Path("/Users/yewonchang/Desktop/ManualMap") #The folder that the VCR .json files are in
    targetFolder = Path("/Users/yewonchang/Desktop/RegexOutputs") #The folder you'd like to place your CSV files in 
    for file in hostFolder.glob("*.json"): #For each file in folder ending in .json (i.e. each VCR file)
        with open(file, 'r', encoding='utf-8') as f:
            text = json.load(f) 
            yearDict = parseYear(text)
            matchDict = patMatchDict(text)
            penultDict = joinDict(yearDict, matchDict)
            fullDict = finalDict(penultDict)
        csv_path = targetFolder / f"{file.stem}.csv"
        with csv_path.open('w', newline='', encoding='utf-8') as csvfile: #Create a corresponding CSV file to store data 
            writer = csv.writer(csvfile)
            writer.writerow(['YEAR', 'PLACE', 'NUMBER OF MENTIONS']) 
            for (year, dict) in fullDict.items():
                for (place, count) in dict.items(): 
                    writer.writerow([year, place, count])
                    