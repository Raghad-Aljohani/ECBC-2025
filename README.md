# ECBC 2025: Mapping the Records of the Virginia Company of London (1606–1626)

This project is a part of the **Data+ Program** at Duke University. It involves building a structured data pipeline and interactive map to analyze place references across *The Records of the Virginia Company of London* (VCR) using OCR, Named Entity Recognition (NER), regex, geocoding, and Shiny. 


***Contributors: Raghd Aljohani, Yewon Chang, Anya Deng, Isabella Xu***


## Project Overview

We explore how early colonial documents referenced space by:
- Fine-tuning BART and GPT-4o on OCR'd pages of the VCR
- Correcting OCR errors across the VCR pages with GPT-4o
- Applying Named Entity Recognition (NER) to VCR texts to identify potential GPE (geopolitical entities) and LOC (location) entities
- Manually validating and adding relevant (Virginian and other English colonial) entities to our NER output
- Using regex to track the mention frequency of said place names throughout the text, accounting for historical spelling variations
- Visualizing the results via a **Shiny** app and **static maps**

Here is the Shiny app website for the VCR locations extracted **only** with NER (the "dirty" map): 
https://isabella-dataplus.shinyapps.io/dataPlusv2/

Here is the Shiny app website for the VCR locations extracted with **both** NER and regex (the "clean" map): 
https://yewonchang.shinyapps.io/manualmap/ 


## Repository Structure

```text
ECBC-2025/
│
├── automatedscorerpipeline/        # Python code for computing NER model evaluation scores
│   ├── AnnotatedPage.txt
│   ├── GoldStandardGenerator.py
│   ├── OriginalPage.txt
│   ├── ScorerPipeline.py
│
├── cleanmap/        # Python code for preparing location mention density data for map; R files for "clean map" app
│   ├── CombineCSVs.py
│   ├── Combined.csv
│   ├── Coordinates.csv
│   ├── MakeMapCsv.py
│   ├── MakeRegexCSVs.py
|   ├── Map.csv
|   ├── TestRegex.py
│
├── data/                      # Cleaned and preprocessed data
│   ├── all_entities.csv
│   ├── cleaned_VCRSection2.json
│   ├── ...
│   └── cleaned_VCRSection7.json
│
├── scripts/                   # Python code for NER and text processing
│   ├── extract_entities.py
│   ├── bart_fine_tuning.py
│   ├── pretrained_bart.py
│   ├── ner&scorer.py
│   └── ner_and_labels_frequencies.py
│
├── shiny_app/                 # R files for "dirty map" app
│   ├── final_app.R
│   ├── final_map.Rmd
│   └── VCR_1622_map.png
│   └── 1622 map.R             # Standalone script for 1622 map plot
│
├── rsconnect/                 # Deployment configs for shinyapps.io
│
├── .gitignore
└── README.md
```

## Key Technologies

- Python (Data cleaning + analysis): 
    - HuggingFace Transformers (```BART```)
    - Custom entity extraction via spaCy's NER model
    - Computation of NER model's accuracy via spaCy's Scorer
    - Refining NER output via regex 
- R (Geocoding + Mapping):
    - ```tidygeocoder, leaflet, ggplot2, dplyr```
    - Shiny app deployment via ```shinyapps.io```
- OCR / JSON cleanup
    - Manually reviewed and corrected OCR outputs from VCR

## Shiny Apps

"Dirty" Map Features: 
- Interactive map of place references
- Filters by year, entity type (GPE / LOC)
- Integrated geocoordinates from ArcGIS API

"Clean" Map Features:
- Interactive map of key place references and their mention density per year
- Filters by year

## Historical Timeline

| VCR Section | "Dirty Map" Assigned Year     | Justification                                                                            |
| ----------- | ----------------------------- | ---------------------------------------------------------------------------------------- |
| Section 1   | 1606                          | Royal Charter granted to Virginia Company; foundation of planning begins                 |
| Section 2   | 1607                          | Jamestown founded                                                                        |
| Section 3   | 1610                          | De La Warr reoccupation                                                                  |
| Section 4   | 1614                          | Pocahontas–Rolfe marriage                                                                |
| Section 5   | 1617                          | Tobacco boom begins                                                                      |
| Section 6   | 1622                          | Powhatan Uprising                                                                        |
| Section 7   | 1623                          | Aftermath documentation                                                                  |
| Section 8   | 1622                          | Legal disputes following 1622 uprising (e.g., Wye case; disrupted transport to Virginia) |
| Section 9   | 1622                          | Trade and military expeditions post-uprising; Hamor & Smith commissions                  |
| Section 10  | 1623–1624                     | Final legal defense of the Company before dissolution                                    |



## Setup Instructions

### 1. Clone the Repository

First, clone this GitHub repository to your local machine:

```bash
git clone https://github.com/Raghad-Aljohani/ECBC-2025.git
cd ECBC-2025
```

### 2. Install Required R Packages

Open R or RStudio and install the necessary packages by running:

```
install.packages(c(
  "tidyverse", 
  "tidygeocoder", 
  "shiny", 
  "leaflet", 
  "maps",
  "jsonlite"
))
```  

If using ```renv```, you can restore the project-specific environment with: 
```
renv::restore()
```

### 3. Run the Shiny App

To launch the interactive map locally (ex. for the "dirty map"):

```
shiny::runApp("shiny_app/final_app.R")
```

Once running, the map will open in your browser with an animated timeline of entity mentions by year.


