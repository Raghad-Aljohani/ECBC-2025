import spacy 
import json 
from spacy.training import Example 
from spacy.scorer import Scorer

nlp = spacy.load("en_core_web_sm") #Load pipeline 

with open("/Users/yewonchang/Desktop/ManualMap/cleaned_VCRSection3.json", "r", encoding="utf-8") as f: #Use pre-existing VCR .json file 
    placeholder = json.load(f)

with open("OriginalPage.txt", "r", encoding="utf-8") as f: #Use text file of VCR page created by user 
    original = f.read() 

chunk = nlp(original)

def ent_info_extract(text): 
    '''This function returns a list of tuples in the format [(START, END, ENTITY TYPE)...].'''
    return [(ent.start_char, ent.end_char, ent.label_) for ent in text.ents]

def ent_info_to_edit(text): 
    '''This function returns a list of tuples in the format [(ENTITY TEXT, START, END, ENTITY TYPE)...]. 
    This is a more readable/editable list than that returned by ent_info_extract.'''
    return [(ent.text, ent.start_char, ent.end_char, ent.label_) for ent in text.ents]

def scorer(data):
    '''This function computes evaluation scores (precision, recall, F1) for spaCy's NER model when run on an input page by comparing 
    the model's predictions and the user's manually created gold standard.'''
    examples = []
    for (page, annotations) in data: 
        doc = nlp.make_doc(page) 
        example = Example.from_dict(doc, annotations)
        examples.append(example) #Create Example objects from gold standard. 
    predictedExamples = []
    for example in examples: #Run NER model on input text
        predDoc = nlp(example.text) #Store model's output (predictions)
        predictedExample = Example(predDoc, example.reference)
        predictedExamples.append(predictedExample) #Create Example objects comparing model prediction to gold standard
    scorer = Scorer()
    scores = scorer.score(predictedExamples) #Run Scorer on the comparison Example objects
    return scores 

def overlapInfo(goldStandard, modelPredict, dirtyModelPredict): 
    '''This function generates information about the specific entities shared by the NER model predictions and gold standard.'''
    overlapCt = 0 #1: Number of entity instances that overlap between model predictions and gold standard
    overlapLst = [] 
    for item in goldStandard: 
        if item in modelPredict: 
            overlapCt +=1 
            overlapLst.append(item)
    overlapLabels = [tup[2] for tup in overlapLst] 
    overlapDict = {}
    for label in overlapLabels: 
        if label not in overlapDict: 
            overlapDict[label] = 0 
        overlapDict[label] += 1 
    overlapItems = sorted(overlapDict.items(), key=lambda x: x[1], reverse=True) #2: Overlapping entity labels mapped to number of such overlaps 
    overlapEnts = set() #3: Texts of the entities that overlap
    for tup in reference: 
        if tup in dirtyModelPredict: 
            overlapEnts.add(tup[0])
    return (overlapCt, overlapItems, overlapEnts)

if __name__ == "__main__":
    #Copy and paste the Gold Standard from GoldStandardGenerator.py
    goldStandard = [(0, 12, 'DATE'), (13, 16, 'CARDINAL'), (67, 73, 'ORG'), (108, 114, 'ORG'), (119, 128, 'ORG'), (175, 176, 'CARDINAL'), (181, 189, 'PERSON'), (205, 206, 'CARDINAL'), (207, 211, 'PERSON'), (249, 250, 'CARDINAL'), (279, 287, 'GPE'), (298, 301, 'CARDINAL'), (303, 316, 'PERSON'), (336, 343, 'ORG'), (419, 432, 'LOC'), (450, 459, 'QUANTITY'), (503, 505, 'CARDINAL'), (506, 513, 'PERSON'), (588, 599, 'PERSON'), (641, 645, 'PERSON'), (682, 696, 'LOC'), (697, 703, 'PERSON'), (708, 716, 'GPE'), (827, 837, 'QUANTITY'), (880, 886, 'ORG'), (888, 891, 'CARDINAL'), (896, 904, 'GPE'), (918, 934, 'GPE'), (935, 944, 'QUANTITY'), (949, 963, 'GPE'), (965, 968, 'CARDINAL'), (974, 981, 'GPE'), (997, 1000, 'CARDINAL'), (1006, 1019, 'GPE'), (1074, 1076, 'CARDINAL'), (1078, 1085, 'PERSON'), (1133, 1135, 'CARDINAL'), (1171, 1173, 'CARDINAL'), (1264, 1278, 'ORG'), (1381, 1387, 'ORG'), (1396, 1401, 'PERSON'), (1406, 1409, 'PERSON'), (1479, 1488, 'QUANTITY'), (1524, 1530, 'ORG'), (1537, 1539, 'CARDINAL'), (1540, 1549, 'PERSON'), (1593, 1597, 'CARDINAL'), (1623, 1627, 'CARDINAL'), (1632, 1642, 'DATE'), (1644, 1653, 'PERSON'), (1752, 1759, 'PERSON'), (1814, 1821, 'ORG'), (1824, 1827, 'CARDINAL'), (1880, 1884, 'PERSON'), (2167, 2172, 'PERSON'), (2260, 2280, 'LAW'), (2360, 2367, 'ORG'), (2385, 2391, 'GPE'), (2477, 2485, 'ORG')]
    data = [(original, {"entities": goldStandard})]
    #Copy and paste the Reference from GoldStandardGenerator.py
    reference = [('MAY I7, 1620', 0, 12, 'DATE'), ('349', 13, 16, 'CARDINAL'), ('Courts', 67, 73, 'ORG'), ('Courte', 108, 114, 'ORG'), ('Companies', 119, 128, 'ORG'), ('2', 175, 176, 'CARDINAL'), ('Officers', 181, 189, 'PERSON'), ('2', 205, 206, 'CARDINAL'), ('Depu', 207, 211, 'PERSON'), ('2', 249, 250, 'CARDINAL'), ('Virginia', 279, 287, 'GPE'), ('115', 298, 301, 'CARDINAL'), ('George Thorpe', 303, 316, 'PERSON'), ('Company', 336, 343, 'ORG'), ('Colledge Land', 419, 432, 'LOC'), ('300 Acres', 450, 459, 'QUANTITY'), ('10', 503, 505, 'CARDINAL'), ('Teniite', 506, 513, 'PERSON'), ('Thomas Nuce', 588, 599, 'PERSON'), ('Nuce', 641, 645, 'PERSON'), ('Companies Land', 682, 696, 'LOC'), ('Tefnte', 697, 703, 'PERSON'), ('Virginia', 708, 716, 'GPE'), ('1200 Acres', 827, 837, 'QUANTITY'), ('Office', 880, 886, 'ORG'), ('600', 888, 891, 'CARDINAL'), ('Kiquotan', 896, 904, 'GPE'), ('Elizabeth Cittie', 918, 934, 'GPE'), ('400 Acres', 935, 944, 'QUANTITY'), ('Charles CittIE', 949, 963, 'GPE'), ('100', 965, 968, 'CARDINAL'), ('Henrico', 974, 981, 'GPE'), ('100', 997, 1000, 'CARDINAL'), ('Iames Cittsie', 1006, 1019, 'GPE'), ('40', 1074, 1076, 'CARDINAL'), ('Teiint¢', 1078, 1085, 'PERSON'), ('20', 1133, 1135, 'CARDINAL'), ('20', 1171, 1173, 'CARDINAL'), ('Quarter Courte', 1264, 1278, 'ORG'), ('Courte', 1381, 1387, 'ORG'), ('Porey', 1396, 1401, 'PERSON'), ('Sec', 1406, 1409, 'PERSON'), ('500 Acres', 1479, 1488, 'QUANTITY'), ('Office', 1524, 1530, 'ORG'), ('20', 1537, 1539, 'CARDINAL'), ('Tennanté¢', 1540, 1549, 'PERSON'), ('Tenn', 1593, 1597, 'CARDINAL'), ('tenn', 1623, 1627, 'CARDINAL'), ('next yeare', 1632, 1642, 'DATE'), ('Secretary', 1644, 1653, 'PERSON'), ('Clarkes', 1752, 1759, 'PERSON'), ('Courtes', 1814, 1821, 'ORG'), ('108', 1824, 1827, 'CARDINAL'), ('Nuce', 1880, 1884, 'PERSON'), ('Thier', 2167, 2172, 'PERSON'), ('Lawes of the Company', 2260, 2280, 'LAW'), ('Courtes', 2360, 2367, 'ORG'), ('Colony', 2385, 2391, 'GPE'), ('Treasury', 2477, 2485, 'ORG')]
    modelPredict = ent_info_extract(chunk)
    dirtyModelPredict = ent_info_to_edit(chunk)
    print("-----------------------------")
    print("EVALUATION SCORES:")
    print(scorer(data))
    print("-----------------------------")
    print("Gold standard has: " + str(len(goldStandard)) + " entities")
    print("Model predicts: " + str(len(modelPredict)) + " entities")
    overlapMetrics = overlapInfo(goldStandard, modelPredict, dirtyModelPredict)
    print("Number of overlapping entities: " + str(overlapMetrics[0]))
    print("Labels of entities that overlap and number of overlapping instances:")
    print(overlapMetrics[1])
    print("Text of entities that overlap:")
    print(overlapMetrics[2])
