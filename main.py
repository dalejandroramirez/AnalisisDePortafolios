import nootbooks.portafolioOptimo  as portafolio 
import numpy as np 


if __name__=='__main__':

  # Nombre_Acciones = input('Ingrese los nombres de las acciones a analizar separado por comas: ')

  # r = input('Ingrese los respectivos de retornos esperados separados por coma:  ')

  # r = list(map(float, r.split(",")))
  # Nombre_Acciones = list(map(str, Nombre_Acciones.replace("'","").split(",")))

  # r = np.array([0.2,0.1,0.2])   # vector de retornos esperados 
  # Nombre_Acciones = ['CIB','^DJI','LCID']
  
  
  r = np.array([0.2,0.1,0.2,0.3])  ## vector de retornos

  Nombre_Acciones = ['CIB','AAPL','^TNX','^RUT']
  
  portafolio1 = portafolio.MiPortafolio(Nombre_Acciones=Nombre_Acciones,R = 0.04)

  print(portafolio1.retornoMedio())
  portafolio1.swapRetornoEsperado(portafolio1.retornoMedio())
  

  #portafolio.graficarCurvaRiesgo(r = portafolio1.retornoMedio() , Nombre_Acciones=Nombre_Acciones)
  portafolio.graficarCurvaRiesgo(r = r , Nombre_Acciones=Nombre_Acciones)

  