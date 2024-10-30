#######################################
# DISEÑO, PROCESAMIENTO Y ANALISIS ESTADÍSTICO I #
# MARISOL PAREDES        #
# MAYO 2024 #
#######################################
#Para borrar todos los objetos previos
rm(list=ls())
#Se instalan las librerias necesarias
#install.packages("visdat")
#library(visdat)
##Se activan las librerias
library(ggridges)
library(ggplot2)
library(GGally)
library(tidyverse)
library(plotly)
library(visdat)
#Recupera base de datos Iris implementada en R
iris

#Para ver las primeras 10 filas de los datos
iris[1:10,]
#Algunas graficas con los datos
plot(iris)

plot(iris$Sepal.Length,type = "p")
plot(iris$Sepal.Length,type = "l")
plot(iris$Sepal.Length,type = "h")

#Histograma de frecuencias con una de las variables
?hist
hist(iris$Sepal.Width)
hist(iris$Sepal.Length, col = "blue", main = "Histograma")

#Graficas más sofisticadas con ggplot
?ggplot

ggplot(data = iris, aes(x = Petal.Length, Petal.Width, color = Species))+
  geom_point(alpha=0.75)+
  labs(title = "Medidas de los pétalos por especie")+
  theme(legend.position = 'none')+
  facet_wrap(~Species)

ggplot(iris, aes(x = Sepal.Length, y = Species, fill=Species)) + 
  geom_density_ridges()

#Estadisticos descriptivos de los datos
summary(iris)

#Grafica para ver datos faltantes
?vis_dat
vis_dat(iris)

#Grafica de cajas de los datos
boxplot(iris$Petal.Width)

#Graficas interactivas con plotly de R
fig <- plot_ly(data = iris, x = ~Sepal.Length, y = ~Petal.Length)
fig

fig1 <- plot_ly(data = iris, x = ~Sepal.Length, y = ~Petal.Length, color = ~Species)
fig1

#LIMPIEZA DE DATOS
#DATOS FALTANTES
#A los datos de Iris asignamos de forma aleatoria datos faltantes, que en R 
#son denotados como NA
summary(iris)

for(j in 1:7){
  inst.aleat <- sample(1:nrow(iris), 1, replace=F)
  iris[inst.aleat, "Petal.Length"] <- NA
}

#Estadisticas de iris
summary(iris)
#Para visualizar datos faltantes
vis_dat(iris)

# Si deseamos ver las filas con los datos faltantes
iris[is.na(iris$Sepal.Length),]

#Analisis de datos faltantes
#Podemos contar la cantidad de faltantes para una variable
sum(is.na(iris$Sepal.Length))

#Tambien podemos analizar la proporcion de faltantes sobre el total de datos
round(sum(is.na(iris$Sepal.Length))/nrow(iris)*100,2)

#VALORES FALTANTES:REGISTROS COMPLETOS
#Si quisieramos trabajar unicamente con aquellos registros con datos completos
#eliminamos los NA
iris.reg_completos <- na.omit(iris)
#Podemos ver las filas que quedaron
nrow(iris.reg_completos)
#Tambien se puede calcular la media aritmetica omitiendo los valores faltantes
print(mean(iris$Petal.Length, na.rm=TRUE))

#IMPUTACION POR LA MEDIA
#Reemplazamos los valores faltantes con el promedio
iris.imp <- iris
iris.imp$media <- iris$Sepal.Length
iris.imp$media[is.na(iris.imp$media)] <- mean(iris.imp$media, na.rm=TRUE)
#Verificamos que no quedan faltantes
sum(is.na(iris.imp$media))
summary(iris.imp$Sepal.Length)
summary(iris.imp$media)

#Graficas para los valores faltantes
install.packages("visdat")
library(visdat)
vis_dat(iris)
#VALORES FALTANTES: IMPUTACION POR HOT DECK
#instalamos la libreria que hace imputacion Hot Deck
install.packages("VIM")
library(VIM)
#La grafica muestra donde se ubican los valores faltantes con rojo
aggr(iris,prop=F, border=NA,numbers=T,axes=T,combined=T)

#Definimos un dataframe auxiliar para no perder la variable original
df_aux <- hotdeck(iris, variable="Sepal.Length")
#Se realiza la asignacon a los faltantes por Hotdeck
iris.imp$hotdeck <- df_aux$Sepal.Length
iris.imp$hotdeckbool <- df_aux$Sepal.Length_imp
#Ahora verificamos que no existen faltantes
sum(is.na(iris.imp$hotdeck))

#ANALISIS GRAFICO DE AMBOS METODOS DE IMPUTACION
iris.imp <- iris.imp[,-c(2:5)]    
iris.imp
names(iris.imp)[1] <- "original"

#sE REALIZA GRAFICOS PARA COMPARAR DATOS ORIGINALES Y LA
#IMPUTACION POR LA MEDIA Y LA IMPUTACION HOTDECK
plot(density(iris.imp$original,na.rm=TRUE), type="l",
     col="red", ylab="Original", ylim=c(0,0.5))
lines(density(iris.imp$media,na.rm=TRUE), type="l",
      col="blue")
lines(density(iris.imp$hotdeck,na.rm=TRUE), type="l",
      col="green")
legend(7,0.5,legend=c("Original", "Media","Hotdeck"),
       col=c("red","blue","green"),lty=1, cex=0.8)

#LIMPIEZA DE DATOS: DETECCION DE OUTLIERS O DATOS ATIPICOS
#Para esto utilizamos una nueva base de datos llamada airquality
airquality
#Para ver caracteristicas de la base de datos de R
?airquality

#Algunas estadisticas y graficos de los datos
hist(airquality$Ozone)
summary(airquality)

#Grafica para ver los datos faltantes
vis_dat(airquality)

#Algunas operaciones para los faltantes, omitiendolos
plot(sort(airquality$Solar.R,decreasin=FALSE))
print(mean(airquality$Ozone, na.rm=TRUE))
print(min(airquality$Ozone, na.rm=TRUE))
print(max(airquality$Ozone, na.rm=TRUE))

#Una grafica de caja para analizar si las variables tienen outliers
boxplot(airquality,na.rm=TRUE)