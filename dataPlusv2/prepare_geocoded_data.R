# prepare_geocoded_data.R

# Load required libraries
library(tidyverse)
library(tidygeocoder)

# Load your original entity data
entities <- read_csv("dataPlusv2/all_entities.csv")

# Filter unique non-empty entity names
locations_unique <- entities %>%
  filter(!is.na(entity_name), entity_name != "") %>%
  distinct(entity_name)

# Geocode using ArcGIS (may take a few minutes depending on number of entities)
locations_geocoded <- locations_unique %>%
  geocode(address = entity_name, method = "arcgis", lat = latitude, long = longitude)

# Save to CSV
write_csv(locations_geocoded, "geocoded_locations.csv")
