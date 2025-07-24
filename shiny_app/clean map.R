library(shiny)
library(leaflet)
library(tidyverse)
library(scales) 

df <- read_csv("/Users/yewonchang/cleanmap/Map.csv") %>%
  rename(
    LAT = DLATITUDE,
    LON = DLONGITUDE
  ) %>%
  filter(
    !is.na(YEAR), !is.na(MENTIONS), !is.na(LAT), !is.na(LON)
  )

ui <- fluidPage(
  titlePanel("Locations Mentioned in the Records of the Virginia Company of London (1606-1626)"),
  
  sidebarLayout(
    sidebarPanel(
      sliderInput("year", "Select Year:",
                  min = min(df$YEAR),
                  max = max(df$YEAR),
                  value = min(df$YEAR),
                  step = 1,
                  animate = animationOptions(interval = 1500, loop = TRUE))
    ),
    
    mainPanel(
      leafletOutput("map", height = 650)
    )
  )
)

server <- function(input, output, session) {
  
  output$map <- renderLeaflet({
    leaflet() %>%
      addProviderTiles("CartoDB.Positron") %>%
      setView(lng = mean(df$LON), lat = mean(df$LAT), zoom = 5)
  })
  
  observe({
    df_year <- df %>% filter(YEAR == input$year)
    
    leafletProxy("map", data = df_year) %>%
      clearMarkers() %>%
      addCircleMarkers(
        lng = ~LON,
        lat = ~LAT,
        radius = ~case_when( 
  MENTIONS > 0 & MENTIONS <= 5   ~ 4,
  MENTIONS > 5 & MENTIONS <= 10  ~ 8,
  MENTIONS > 10 & MENTIONS <= 20 ~ 12,
  MENTIONS > 20 & MENTIONS <= 50 ~ 16,
  MENTIONS > 50 & MENTIONS <= 100 ~ 20,
  MENTIONS > 100                 ~ 24,
  TRUE                          ~ 0  
),
        fillColor = "royalblue",
        color = "ghostwhite",
        weight = 1,
        fillOpacity = 0.75,
        popup = ~paste0("<b>", PLACE, "</b><br>Mentions: ", MENTIONS, 
                        "<br>Year: ", sprintf("%d", YEAR))
      )
  })
}

shinyApp(ui = ui, server = server)
