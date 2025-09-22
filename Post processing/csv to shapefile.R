
library(sf)
library(sfheaders)
library (lubridate)

setwd(file.path('D:', 'WHCR_2025', '15_WHCR_survey'))

data1 <- read.table ("predict_whcr_2025_survey_Sept15.csv", sep = ",",header=TRUE, fill=TRUE)

names(data1)

#data2 <- read.table ("images_w_gr5_cranes_metadatasacr_detections_2025_summary.csv", sep = ",",header=TRUE, fill=TRUE)
#merge2 <- merge(data1, data2, by= "unique_image_jpg")
#write.table(merge2, "images_w_gr5_cranes_sum4.csv", sep=",", row.names=FALSE)

# crs1 = 4326 # WGS1984

crs1 = 4487 # utm 14N

#data1$image_lat <- (data1$BLLat + data1$BLLat) /2 
#data1$image_long <- (data1$BLLong + data1$BLLong) /2 

#write.table(data1, "Metadata_20250323_203200_images_x.csv", sep =",", row.names=FALSE)

View(data1)

export_spatial = "WHCR_predict_survey_2025.shp"

# Projections, crs = 4326--WGS84
#data2 <- data1[complete.cases(data1), ]

data1 <- data1[complete.cases(data1), ]

new_sf <- st_as_sf(data1, coords = c("x_annot", "y_annot"), crs= crs1)

plot(new_sf)

new_sf %>% 
  st_coordinates()

st_write(new_sf, export_spatial, driver = "ESRI Shapefile")  

## Make shapefile
# get rid of na's first
#a7 <- a1[complete.cases(a1), ]

# crs for MA, ME= UTMN19/EPSG:32618
# for mid_Atlantic = UTM18, EPSG:32619
utm_proj <- st_transform(new_sf, crs = crs1)

names(utm_proj)

utm_proj %>% 
  st_coordinates()

st_write(utm_proj, export_spatial, driver = "ESRI Shapefile")  
