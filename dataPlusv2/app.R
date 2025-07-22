#
# This is a Shiny web application. You can run the application by clicking
# the 'Run App' button above.
#
# Find out more about building applications with Shiny here:
#
#    https://shiny.posit.co/
#

# Load packages 
library(jsonlite)
library(tidyverse)
library(tidygeocoder)
library(shiny)
library(leaflet)

# Load csv file and inspect data
entities <- read_csv("dataPlusv2/all_entities.csv")

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

# Import from the downloaded list of geocoded locations 
locations_unique <- read_csv("dataPlusv2/geocoded_locations.csv")

# Join coordinates back to full dataset
entities_geo <- entities %>%
  left_join(locations_unique, by = "entity_name") %>%
  filter(!is.na(latitude), !is.na(longitude))

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
