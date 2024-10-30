rm(list=ls())
##Para copiar directamente datos como dataframe
install.packages("datapasta")

##Activamos las librerias
library(datapasta)
library(ggplot2)
library(readxl)
#library(lubridate)
library(leaflet)
#library(leaflet.extras) 
#library(rworldxtra)
library(tidyverse)
library(sf)

##Para ubicar el directorio con los datos
setwd("E:/MARY/DOCENCIA UMSA/DOCENCIA 2024/ESTADISTICA/DPA2 - 2024/TEMA 2/Ejemplo Mapas/MAPAS-POBREZA")

##Una forma de recuperar los datos
##Se recupera los datos de la tabla excell del INE con datapasta

pobrefin <- data.frame(
  stringsAsFactors = FALSE,
       check.names = FALSE,
            COD_DEP = c(1, 2, 3, 4, 5, 6, 7, 8, 9),
                         depto = c("Chuquisaca","La Paz","Cochabamba","Oruro",
                                   "Potosí","Tarija","Santa Cruz","Beni","Pando"),
                      NP_NBS = c(21.94,
                                   26.5,25.86,25.47,17.08,27.92,28.13,
                                   16.04,14.44),
                      NP_Umb = c(23.53,
                                   27.2,28.69,27.55,23.17,37.49,36.4,27.54,
                                   26.71),
                      Pob_Mod = c(38.2,
                                   35.3,35.17,34.42,40.87,31.34,31.68,45.93,
                                   47.03),
                      Pob_Ind = c(15.64,
                                   10.63,9.74,12.05,17.81,3.2,3.71,9.49,
                                   11.23),
                     Pob_Marg = c(0.69,
                                   0.36,0.55,0.5,1.06,0.06,0.09,1,0.58)
            )

pobrefin
summary(pobrefin)

#Para ver el tipo de dato del campo que se unira despues
class(pobrefin$COD_DEP)

#Para recuperar el shape de los departamentos
shapefin <- st_read("datosfin/Departamentos_Bolivia.shp")

class(shapefin$COD_DEP)
##Podemos ver el mapa
shapefin

##Se puede trabajar como una grafica normal
plot(st_geometry(shapefin))

##Si le colocamos algunas caracteristicas adicionales
ggplot() + 
  geom_sf(data = shapefin)

##Se pueden modificar colores
ggplot(data = shapefin) +
  geom_sf(fill = "greenyellow", color = "black")


#Para convertir como caracter al campo COD_DEP de la base pobrefin
pobrefin$COD_DEP <- as.character(pobrefin$COD_DEP)

##Adicionamos los datos del mapa con datos de pobreza al shape
final <- left_join(x=shapefin,y=pobrefin,by="COD_DEP")
final

##Utilizamos los datos ya unidos y creamos un mapa temàtico con la variable 
#Pobreza Marginal 
ggplot(data = final) +
  geom_sf(aes(fill = Pob_Marg))

##Para colocar otros detalles como ejes y titulos y subtitulos
ggplot(data = final) +
  geom_sf(aes(fill=Pob_Marg)) +
  xlab("Longitud") + ylab("Latitud") +
  ggtitle("Mapa de los departamentos de Bolivia",
          subtitle = "Realizado por: Marisol Paredes")

##Se puede realizar un mapa por departamento con alguno de los indicadores
##de pobreza con PLOT
final %>% 
  dplyr::select(Pob_Marg) %>% plot()

##Otra forma de realizarlo, seleccionamos variable
final %>% 
  select(NP_Umb, geometry) %>% 
  plot(lwd=0.06)

##Creamos un mapa tematico con GGPLOT con las variables de Pobreza

ggplot(data = final, aes(fill = NP_NBS)) +
  geom_sf(color=NA) +
  theme_void()

##Colocando algunos detalles mas
ggplot(data = final, aes(fill = NP_NBS)) + 
  geom_sf(color = NA) +
  scale_fill_viridis_c() +
  labs(title = "Bolivia: Necesidades basicas satisfechas por departamentos",
       subtitle = "Mapa tematico",
       fill = "No pobres") +
  theme_void()

##Adicionalmente colocando otra capa de nombres de los departamentos
ggplot(data = final, aes(fill = NP_NBS)) +
  geom_sf(color = NA) +
  geom_sf_text(data = final, 
               aes(label = NOM_DEP), size=3)+
  theme(legend.position = 'top')+
  scale_fill_viridis_c(option = 'C') +
  labs(title = "Bolivia: Necesidades basicas satisfechas por departamentos",
       subtitle = "Mapa tematico",
       fill = "No pobres") +
  theme_void()

###############################################################################
#Para recuperar el shape de los municipios
shapemun <- st_read("datosmun/municipal.shp")
##Podemos ver el mapa
shapemun

##Se puede trabajar como una grafica normal
plot(st_geometry(shapemun))

##Si le colocamos algunas caracteristicas adicionales
ggplot() + 
  geom_sf(data = shapemun)

##Se pueden modificar colores
ggplot(data = shapemun) +
  geom_sf(fill = "greenyellow", color = "black")

#Recuperamos los datos de la tabla excel por municipio
datos <- read_excel("data/datos_mun.xlsx")
#Verificamos el tipo de dato de la clave que los va a enlazar al shape
class(shapemun$c_ut)
class(datos$c_ut)

#Convertimos a caracter uno de ellos
datos$c_ut <- as.character(datos$c_ut)

##Adicionamos los datos del mapa con datos de la tabla excel al shape
datosmun <- left_join(x=shapemun,y=datos,by="c_ut")
class(datos$ids)
datosmun
##Utilizamos los datos ya unidos y creamos un mapa temàtico con las variables

ggplot(data = datosmun) +
  geom_sf(aes(fill = Mort_inf))

ggplot(data = datosmun) +
  geom_sf(aes(fill = ids))

ggplot(data = datosmun) +
  geom_sf(aes(fill = Tasa_urb))

##########################################################
##GRAFICANDO CON GGPLOT2
###########################################################
#Eliminado los datos faltantes
final1 <- na.omit(final)
#Creando las primreas graficas
ggplot(final1,aes(x = depto, y = Pob_Mod)) +
  geom_bar(stat = "identity") +
coord_flip() 

##Siguiendo a diegokoz
#Para no considera los valores faltantes
datosmun1 <- na.omit(datosmun)
#Para el histograma, solo con cuantitativas
class(datosmun1$Tasa_urb)
#Elegimos la variable tasa de urbanizacion
hist(datosmun1$Tasa_urb, col = "lightsalmon1", main = "Tasa de urbanizacion por municipio")

#Realizamos un diagrama de dispersion con dos variables
plot(datosmun1$Tasa_urb, datosmun1$ids)

#Otro tipo de grafico con ggplot, de densidades
ggplot(datosmun1, aes(x = Tasa_urb, y = DEPARTAMEN, fill=DEPARTAMEN)) + 
  geom_density_ridges()
#Diagramas de caja por departamento, para el Indice de Desarrollo Sostenible (ids)
ggplot(datosmun1, aes(x = DEPARTAMEN, y = ids)) +
  geom_boxplot()+
  scale_y_continuous(limits = c(0, 100))

#Diagramas de caja por departamento, para la Tasa de Urbanización (Tasa_urb)
ggplot(datosmun1, aes(x = DEPARTAMEN, y = Tasa_urb)) +
  geom_boxplot()+
  scale_y_continuous(limits = c(0, 100))


###Para los bordes blancos
ggplot(datosmun) +
  geom_sf(color = "white", aes(fill = Mort_inf)) +
  theme(legend.position = "none")

##Para colocar etiquetas de municipios
ggplot(datosmun) +
  geom_sf(color = "white", aes(fill = Mort_inf)) +
  geom_sf_text(aes(label = MUNICIPIO), size = 2) +
  theme(legend.position = "none")

##Para hacerlo interactivo
install.packages("plotly")
library(plotly)
p <- ggplot(datosmun) +
  geom_sf(color = "black", aes(fill = Mort_inf)) +
  theme(legend.position = "rigth")
ggplotly(p)

##Otra funcion para graficos
plot(datosmun[, "Mort_inf"],
     breaks = "jenks",
     nbreaks = 10,
     pal = hcl.colors(10),
     main = "Tasa de Mortalidad infantil") 


  
