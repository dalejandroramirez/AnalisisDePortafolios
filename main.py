import nootbooks.portafolioOptimo  as portafolio 
import numpy as np 


if __name__=='__main__':

  Nombre_Acciones = input('Ingrese los nombres de las acciones a analizar separado por comas: ')

  r = input('Ingrese los respectivos retornos esperados separados por coma:  ')
  
  r = list(map(float, r.split(",")))
  
  Nombre_Acciones = list(map(str, Nombre_Acciones.replace("'","").split(",")))  
  
  #['CIB','AAPL','CL=F','SI=F']  ## Nombres de las acciones en yahoo finance
  
  # [0.23,0.20,0.14,0.06]  ## vector de retornos esperados

  
  portafolio1 = portafolio.MiPortafolio(Nombre_Acciones=Nombre_Acciones,R = 0.15)

  portafolio.graficarCurvaRiesgo(r = r, Nombre_Acciones=Nombre_Acciones)
  
  

  