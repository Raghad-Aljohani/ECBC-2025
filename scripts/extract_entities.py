"""This module imports JSON files and extracts entities into a csv document."""

import json
import pandas as pd
import spacy
from pathlib import Path
from tqdm import tqdm

# Load spaCy model
nlp = spacy.load("en_core_web_sm")

# Directory containing JSON files
input_dir = Path("/Users/izzi/Desktop/Duke/Data+/Final Map")
output_file = "all_entities.csv"

# Load and process all JSON files
records = []

for json_file in tqdm(input_dir.glob("cleaned_VCRSection*.json")):
    with open(json_file, "r", encoding="utf-8") as f:
        content = json.load(f)
    
    for page, text in content.items():
        doc = nlp(text)
        for ent in doc.ents:
            if ent.label_ in {"GPE", "LOC"}:
                records.append({
                    "page": page,
                    "entity_name": ent.text,
                    "label": ent.label_,
                    "context": text[:300],  # snippet for R to detect year
                    "file": json_file.name
                })


df = pd.DataFrame(records)
df.to_csv(output_file, index=False)
print(f"Saved to {output_file}")
