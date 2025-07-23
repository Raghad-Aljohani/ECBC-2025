# ECBC-2025: Mapping the Virginia Company Records (1607–1623)

This project is a part of the **Data+ Summer Research Program** at Duke University. It involves building a structured data pipeline and interactive map to analyze place references across the *Virginia Company Records (VCR)* using OCR, Named Entity Recognition (NER), geocoding, and Shiny. 


***Contributors: Raghd Aljohani, Yewon Chang, Anya Deng, Isabella Xu***


## Project Overview

We explore how early colonial documents referenced space by:
- Extracting geographic place names from VCR texts
- Applying Named Entity Recognition to identify GPE (Geopolitical Entities) and LOC (Locations)
- Geocoding these places using the ArcGIS API
- Visualizing the results via a **Shiny** app and **static maps**

Here is the Shiny app website for the VCR locations extracted **only** with NER: 
https://isabella-dataplus.shinyapps.io/dataPlusv2/


## Repository Structure

```text
ECBC-2025/
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
├── shiny_app/                 # R files for visualization and app
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

- Python (NER): 
    - HuggingFace Transformers (```BART```)
    - Custom entity extraction and label scoring
- R (Geocoding + Mapping):
    - ```tidygeocoder, leaflet, ggplot2, dplyr```
    - Shiny app deployment via ```shinyapps.io```
- OCR / JSON cleanup
    - Manually reviewed and corrected OCR outputs from VCR


## Shiny Apps

**Live Map**: (input website)

Features: 
- Interactive map of place references
- Filters by year, entity type (GPE / LOC)
- Integrated geocoordinates from ArcGIS API


## Historical Timeline


| VCR Section | Assigned Year | Justification                                                                            |
| ----------- | ------------- | ---------------------------------------------------------------------------------------- |
| Section 1   | 1606          | Royal Charter granted to Virginia Company; foundation of planning begins                 |
| Section 2   | 1607          | Jamestown founded                                                                        |
| Section 3   | 1610          | De La Warr reoccupation                                                                  |
| Section 4   | 1614          | Pocahontas–Rolfe marriage                                                                |
| Section 5   | 1617          | Tobacco boom begins                                                                      |
| Section 6   | 1622          | Powhatan Uprising                                                                        |
| Section 7   | 1623          | Aftermath documentation                                                                  |
| Section 8   | 1622          | Legal disputes following 1622 uprising (e.g., Wye case; disrupted transport to Virginia) |
| Section 9   | 1622          | Trade and military expeditions post-uprising; Hamor & Smith commissions                  |
| Section 10  | 1623–1624     | Final legal defense of the Company before dissolution                                    |





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

To launch the interactive map locally:

```
shiny::runApp("shiny_app/final_app.R")
```

Once running, the map will open in your browser with an animated timeline of entity mentions by year (1607–1623). 


---

### If you read it this far, thank you so much! 

<p align="center">
  <img src="assets/cute_cat.jpg" alt="Cat" width="400"/>
</p>




