# final_app.R

# Load packages 
library(jsonlite)
library(tidyverse)
library(tidygeocoder)
library(shiny)
library(leaflet)

# Load csv file and inspect data
entities <- read_csv("all_entities.csv")
glimpse(entities)

# Assign years based on historical context and source section
entities <- entities %>%
  mutate(
    year = case_when(
      str_detect(file, "Section2") ~ 1607,   # 1607: Jamestown settlement founded
      str_detect(file, "Section3") ~ 1610,   # 1610: Reoccupation by De La Warr after Starving Time
      str_detect(file, "Section4") ~ 1614,   # 1614: Pocahontas–Rolfe marriage, peace with Powhatan
      str_detect(file, "Section5") ~ 1617,   # 1617: Tobacco boom begins; Pocahontas dies
      str_detect(file, "Section6") ~ 1622,   # 1622: Powhatan Uprising / Indian Massacre
      str_detect(file, "Section7") ~ 1623,
      TRUE ~ NA_real_
    )
  ) %>%
  filter(!is.na(year), !is.na(entity_name), entity_name != "")

# Remove redundant data and geocode entities
locations_unique <- entities %>%
  filter(!is.na(entity_name), entity_name != "") %>%
  select(entity_name) %>%
  distinct() %>%
  geocode(address = entity_name, method = "arcgis", lat = latitude, long = longitude)

# Join coordinates back to full dataset
entities_geo <- entities %>%
  left_join(locations_unique, by = "entity_name") %>%
  filter(!is.na(latitude), !is.na(longitude))

# Map using ggplot
world <- map_data("world")
entities_geo$label <- factor(entities_geo$label, levels = c("GPE", "LOC"))

ggplot() +
  geom_polygon(data = world, aes(x = long, y = lat, group = group),
               fill = "gray90", color = "gray70", size = 0.3) +
  geom_point(data = entities_geo,
             aes(x = longitude, y = latitude, color = label),
             alpha = 0.7, size = 2) +
  scale_color_manual(values = c("GPE" = "darkolivegreen3", "LOC" = "plum3")) +
  coord_fixed(1.3) +
  facet_wrap(~ year, ncol = 3) +
  theme_minimal(base_size = 13) +
  labs(
    title = "Places Mentioned in Virginia Company Records by Year (1607–1623)",
    subtitle = "Entity labels: GPE (geopolitical entity), LOC (location)",
    x = "Longitude", y = "Latitude", color = "Entity Type"
  ) +
  theme(panel.grid = element_blank())

# Map using Shiny
ui <- fluidPage(
  titlePanel("Animated Map of GPE and LOC Mentions (1607–1622)"),
  sidebarLayout(
    sidebarPanel(
      sliderInput("year", "Select Year", 
                  min = min(entities_geo$year), 
                  max = max(entities_geo$year),
                  value = min(entities_geo$year),
                  step = 1,
                  animate = animationOptions(interval = 1500, loop = TRUE))
    ),
    mainPanel(
      leafletOutput("map", height = 600)
    )
  )
)

server <- function(input, output) {
  output$map <- renderLeaflet({
    leaflet() %>%
      addTiles() %>%
      setView(lng = -75, lat = 37, zoom = 3)
  })
  
  observe({
    data_filtered <- entities_geo %>% filter(year == input$year)
    
    leafletProxy("map", data = data_filtered) %>%
      clearMarkers() %>%
      addCircleMarkers(
        lng = ~longitude,
        lat = ~latitude,
        radius = 5,
        popup = ~paste0("<b>", entity_name, "</b><br>Year: ", year),
        color = ~ifelse(label == "GPE", "lightsteelblue", "salmon"),
        fillOpacity = 0.7
      )
  })
}

shinyApp(ui, server)

# library(rsconnect)
# rsconnect::setAccountInfo(name='isabella-dataplus', 
#                           token='EBE952E0FB18A09591A913FDB89EDBA7', 
#                           secret='Nw42UNjSbLJoqR2LSmv3Y99Zd6oWlernX3MuWgLX')
# rsconnect::deployApp('/Users/izzi/Desktop/Duke/Data+/Final Map')











