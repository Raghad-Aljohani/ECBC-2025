# Load required packages
library(tidyverse)
library(tidygeocoder)
library(shiny)
library(leaflet)
library(maps)

# Load the CSV file
entities <- read_csv("all_entities.csv")

# Assign year based on source section (only keeping Section6 → 1622)
entities <- entities %>%
  mutate(
    year = case_when(
      str_detect(file, "Section6") ~ 1622,
      TRUE ~ NA_real_
    )
  ) %>%
  filter(!is.na(year), !is.na(entity_name), entity_name != "")

# Geocode unique locations using ArcGIS
locations_unique <- entities %>%
  select(entity_name) %>%
  distinct() %>%
  geocode(address = entity_name, method = "arcgis", lat = latitude, long = longitude)

# Join coordinates back to full dataset
entities_geo <- entities %>%
  left_join(locations_unique, by = "entity_name") %>%
  filter(!is.na(latitude), !is.na(longitude))

# Set label as a factor for color mapping
entities_geo$label <- factor(entities_geo$label, levels = c("GPE", "LOC"))

# Load world map data
world <- map_data("world")

# Plot map for 1622
ggplot() +
  geom_polygon(data = world, aes(x = long, y = lat, group = group),
               fill = "ghostwhite", color = "gray75", size = 0.3) +
  geom_point(data = entities_geo,
             aes(x = longitude, y = latitude, color = label),
             alpha = 0.7, size = 2) +
  scale_color_manual(values = c("GPE" = "darkolivegreen3", "LOC" = "plum3")) +
  theme_minimal(base_size = 13) +
  labs(
    title = "Places Mentioned in Virginia Company Records (1622)",
    subtitle = "Based on Section 6 | GPE = geopolitical entity, LOC = location",
    x = "Longitude", y = "Latitude", color = "Entity Type"
  ) +
  theme(panel.grid = element_blank())

# Save the map as high-resolution image
ggsave(
  filename = "VCR_1622_map.png",
  plot = last_plot(),  # optional, this is default
  dpi = 300,
  width = 12,
  height = 7,
  units = "in"
)


