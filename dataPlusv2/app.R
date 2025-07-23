# Load packages 
library(jsonlite)
library(tidyverse)
library(tidygeocoder)
library(shiny)
library(leaflet)

# Load csv file and inspect data
entities <- read_csv("all_entities.csv")

# Assign years based on historical context and source section
entities <- entities %>%
  mutate(
    year = case_when(
      str_detect(file, "Section2") ~ 1607,
      str_detect(file, "Section3") ~ 1610,
      str_detect(file, "Section4") ~ 1614,
      str_detect(file, "Section5") ~ 1617,
      str_detect(file, "Section6") ~ 1622,
      str_detect(file, "Section7") ~ 1623,
      TRUE ~ NA_real_
    )
  ) %>%
  filter(!is.na(year), !is.na(entity_name), entity_name != "")

# Import geocoded locations
locations_unique <- read_csv("geocoded_locations.csv")

# Join coordinates back to full dataset
entities_geo <- entities %>%
  left_join(locations_unique, by = "entity_name") %>%
  filter(!is.na(latitude), !is.na(longitude))

# Unique year list for dropdown
year_choices <- sort(unique(entities_geo$year))

# Shiny UI
ui <- fluidPage(
  titlePanel("Animated Map of GPE and LOC Mentions (1607–1622)"),
  sidebarLayout(
    sidebarPanel(
      selectInput("year", "Select Year",
                  choices = year_choices,
                  selected = min(year_choices))
    ),
    mainPanel(
      leafletOutput("map", height = 600)
    )
  )
)

# Shiny Server
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
        popup = ~paste0("<b>", entity_name, " (", label, ")</b><br>Year: ", year),
        color = ~ifelse(label == "GPE", "lightsteelblue", "salmon"),
        fillOpacity = 0.7
      )
  })
}

# Launch App
shinyApp(ui, server)

