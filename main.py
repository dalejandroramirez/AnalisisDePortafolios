import nootbooks.portafolioOptimo  as portafolio 
import numpy as np 


if __name__=='__main__':

  Nombre_Acciones = input('Ingrese los nombres de las acciones a analizar separado por comas')
  r = input('Ingrese los respectivos de retornos esperados separados por coma')

  r = list(map(float, r.split(",")))
  Nombre_Acciones = list(map(str, Nombre_Acciones.replace("'","").split(",")))

  # r = np.array([0.2,0.1,0.2,0.3])  ## vector de retornos esperados que no se como calcular (aun)
  # Nombre_Acciones = ['CIB','AAPL','CL=F','GC=F']

  # print(portafolio.MiPortafolio(0.2,r,Nombre_Acciones).minimizar())
  

  portafolio.graficarCurvaRiesgo(r,Nombre_Acciones)

  