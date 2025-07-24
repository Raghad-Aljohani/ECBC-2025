from pathlib import Path
import json
import re 

def sampleTest(sample, patDict):
    '''This function uses a list of sample spelling variations of a location and tests the accuracy of the location's regex 
    (i.e. its ability to match all given spelling variations to the patterns in the specified dictionary)''' 
    print("FOR SAMPLE:")
    found = []
    notFound = []
    total = len(sample)
    for var in sample: 
        matched = False
        for pattern in patDict.values(): 
            if pattern.search(var):
                print("Match found: " + var)
                found.append(var)
                matched = True
                break
        if not matched: 
            notFound.append(var)
            print("Match not found: " + var)  
    score = (len(found)/total)*100
    print("Accuracy score is " + str(score) + "%")
    if score == 1.0: 
        return ("----------------------")
    unmatched = list(set(sample)-set(found))
    return("Patterns miss out on: " + ", ".join(unmatched)+ "\n----------------------")

def matchInfo(folder, patDict): 
    '''This function loops through all .json files in a specified folder to produce a dictionary mapping a spelling variation of the location
    flagged by regex to the number of instances of that variation throughout the folder.'''
    print("FOR ALL FILES, MATCHES ARE:")
    d = {}
    for file in folder.glob("*.json"): #Grab all files in folder ending in .json
        with open(file, 'r', encoding='utf-8') as f:
            text = json.load(f) 
            for (page, data) in text.items(): 
                cleanData = ' '.join(data.split())
                for pattern in patDict.values(): 
                     matches = pattern.findall(cleanData)
                     if matches: 
                          for mat in matches: 
                               if mat not in d: 
                                    d[mat] = 0
                               d[mat] +=1
    return d 

if __name__ == "__main__": 
    tempDict = {  
     "Kecoughtan1": r"""kice?(?:a|o|co)?wt[ao]n""",
    "Kecoughtan2": r"""k(?:ey|i)ec?o(?:ugh|w)?t[ao]n""",
    "Kecoughtan3": r"""k(?:i|ec)k(?:a|e)t[ao]n""",
    "Kecoughtan4": r"""k[ie][qc]n?(?:uo|ou)u?g?h?t[ao]n"""
    }
    patDict = {name: re.compile(pat, flags=re.IGNORECASE) for name, pat in tempDict.items()}
    sample = ["Kecoughtan",
                "Kiquotan",
                "Kikatan",
                "Kiquoughtan",
                "Kiccowtan",
                "Kicecowtan",
                "Kiccowtan",
                "Kiecowtan",
                "Kicawtan",
                "Kequohtan",
                "Keqnoughton",
                "Kicowtan",
                "Kickoghtan",
                "Kicoughtan",
                "Kiceowtan",
                "Kecketan",
                "Kequoughtan",
                "Keyeotan",
                "Kiquotan",
                "Kieotan",
                "Keyeotan",
                "Kieoughtan", 
                "Anya"] 
    folder = Path("/Users/yewonchang/Desktop/ManualMap")
    print(sampleTest(sample, patDict))
    print(matchInfo(folder, patDict))
    
    
                               

