import re 

#For the annotated page, surround the entities within the text with braces. Example: "I went to see {Anya} in {Paris}." 
#Leave the original page as is. 

def matchFinder(matchSet): 
    '''This function creates a template dictionary mapping each entity flagged by the user in the annotated text to a placeholder type.'''
    tempDict = {}
    for match in matchSet: 
        tempDict[match] = "ENT_TYPE"
    return(tempDict)

def test1(entDict, tempDict): 
    '''OPTIONAL: This function ensures that entDict and tempDict have the same keys (entities).'''
    status = False
    if sorted(entDict.keys()) == sorted(tempDict.keys()):
        status = True
    else: 
        for key in tempDict.keys():
            if key not in entDict.keys():
                print("You are missing the follow entities: ")
                print(key)
                print("Please correct")
    return status

def posDictMaker(original, patDict): 
    '''Using RegEx, this function creates a dictionary mapping each flagged entity to a list of the positions of all of its instances in the original text. 
    It accounts for and prevents the possibility of overlapping positions.'''
    occupied = set() #Create set of all "taken" positions of matches 
    posDict = {}
    sortedKeys = sorted(patDict.keys(), key=len, reverse=True) #Order entities from longest length to shortest length. 
    for label in sortedKeys: 
        pat = patDict[label]
        insts = []
        for inst in re.finditer(pat, original): 
            charRange = set(range(inst.start(), inst.end()))
            if not charRange & occupied: #If current match's position does not overlap with that of a pre-existing match
                insts.append((inst.start(), inst.end())) #Add position information to list 
                occupied.update(charRange) #Update occupied with range object describing that position  
        posDict[label] = insts #Map list of positions to label 
    return posDict

def goldStandardAndRefMaker(posDict, entDict): 
    '''This function generates a ready-to-use Gold Standard for spaCy's Scorer in the format of [(START, END, ENTITY TYPE)...], plus 
    a more detailed reference for the user to see in the format of [(ENTITY TEXT, START, END, ENTITY TYPE)...].'''
    goldStandard = []
    reference = []
    for (match, tupLst) in posDict.items(): 
        for (ent, label) in entDict.items(): 
            if match == ent: 
                for tup in tupLst: 
                    goldStandard.append((tup[0], tup[1], label))
                    reference.append((match, tup[0], tup[1], label))
    goldStandard = sorted(goldStandard, key = lambda x: x[0])
    reference = sorted(reference, key = lambda x: x[1])
    return (goldStandard, reference)

def test2(goldStandard, posDict):
    '''OPTIONAL: This function ensures that the position dictionary used for generating the Gold Standard has all instances of the entities.'''
    status = False
    target = 0 
    for lst in posDict.values(): 
        for inst in lst: 
            target += 1 
    actual = len(goldStandard)
    if target != actual: 
        if target > actual: 
            print("You are missing " + str(target-actual) + " instances.")
        if target < actual: 
            print("You have " + str(actual-target) + " instances than needed.")
    else: 
        status = True
    return status

if __name__ == "__main__":
    with open("[B] AnnotatedPage.txt", "r", encoding="utf8") as f: 
        annotated = f.read()
    with open("[B] OriginalPage.txt", "r", encoding="utf8") as f: 
        original = f.read()
    matches = re.findall(r'\{(.*?)\}', annotated) #Store all marked entities as matches
    matchSet = set(matches)
    tempDict = matchFinder(matchSet) 
    print("----------------------")
    print("EDIT THE TEMPLATE DICTIONARY:")
    print(tempDict) #For each entity, replace the corresponding placeholder "ENT_TYPE" with its appropriate entity type. See example below. 
    entDict = {'349': 'CARDINAL', 'Elizabeth Cittie': 'GPE', 'Sec': 'PERSON', '300 Acres': 'QUANTITY', 'Tennanté¢': 'PERSON', 'Clarkes': 'PERSON', 'Treasury': 'ORG', 'Courtes': 'ORG', 'MAY I7': 'DATE', '1620': 'CARDINAL', 'Porey': 'PERSON', 'Courts': 'ORG', '2': 'CARDINAL', '400 Acres': 'QUANTITY', 'George Thorpe': 'PERSON', '1200 Acres': 'QUANTITY', 'Lawes of the Company': 'LAW', 'Quarter Courte': 'ORG', '108': 'CARDINAL', 'Companies Land': 'LOC', 'Office': 'ORG', 'Tenn': 'CARDINAL', '100': 'CARDINAL', 'tenn': 'CARDINAL', 'Thier': 'PERSON', 'Tefnte': 'PERSON', 'next yeare': 'DATE', '40': 'CARDINAL', 'Courte': 'ORG', '’ Thomas Nuce': 'PERSON', 'Teniite': 'PERSON', 'Depu': 'PERSON', '20': 'CARDINAL', 'Henrico': 'GPE', 'Teiint¢': 'PERSON', 'Virginia': 'GPE', 'Companies': 'ORG', '115': 'CARDINAL', 'Colledge Land': 'LOC', 'Iames Cittsie': 'GPE', 'Nuce': 'PERSON', 'Colony': 'GPE', '10': 'CARDINAL', 'Charles CittIE': 'GPE', 'Kiquotan': 'GPE', 'Secretary': 'PERSON', '500 Acres': 'QUANTITY', 'Officers': 'PERSON', '600': 'CARDINAL', 'Company': 'ORG'}
    if "ENT_TYPE" in entDict.values(): #If template dictionary isn't complete, pause. 
        print("----------------------")
        print("Make sure to edit the template dictionary and input it in entDict.")
    else: #If template dictionary is complete, proceed. 
        patDict = {}
        for match in matchSet: #Create a dictionary mapping each entity to a RegEx pattern. 
            patDict[match] = fr'''{re.escape(match)}''' 
        posDict = posDictMaker(original, patDict) 
        goldStandard = goldStandardAndRefMaker(posDict, entDict)[0]
        reference = goldStandardAndRefMaker(posDict, entDict)[1]
        print("----------------------")
        print("SET-UP COMPLETE.")
        print("----------------------")
        print("YOUR GOLD STANDARD:")
        print(goldStandard)
        print("----------------------")
        print("YOUR REFERENCE:")
        print(reference)