import numpy as np
import matplotlib.pyplot as plt
import yfinance as yf
import pandas as pd
from scipy.stats import spearmanr

from scipy.optimize import minimize 

# R : Es la tasa esperada de retorno

# r : El valor esperado de retorno

# Nombre_Acciones : Son los nombres de las acciones dadas por yfinance

# r = np.array([0.2,0.1,0.2,0.3])  ## vector de retornos esperados

# Nombre_Acciones = ['CIB','AAPL','CL=F','GC=F','EURUSD=X']

class MiPortafolio:

  def __init__(self,R,Nombre_Acciones, r = np.array([0.2,0.1,0.2,0.3]) ):
    self.R = R
    self.retornos = r
    self.acciones = Nombre_Acciones

  def matriz_retornos(self):
    Retornos=pd.DataFrame()
    for accion_name in self.acciones:
      accion = yf.Ticker(accion_name)
      Retornos[accion_name] = accion.history(period="1mo", interval="1d")[['Close']].pct_change()[1:]
    return(Retornos)

  def retornoMedio(self):
    retornosMatriz = self.matriz_retornos()
    return(np.array(retornosMatriz.mean()).round(3))

  def swapRetornoEsperado(self, nuevoRetorno):
    self.r = nuevoRetorno

  def matriz_covarianza(self):
    Rho, _ = spearmanr(self.matriz_retornos(), axis=0)
    return(Rho)

  def valor_retorno_deseado(self):
    print(self.R)

  ## Funcion a optimizar
  def sigma(self, w, cov):
    return np.dot(w.T, np.dot(cov, w))

  ## E(r * w) = R
  def retorno(self, w):
    return np.dot(w.T, self.retornos) - self.R

  def minimizar(self):

    Rho = self.matriz_covarianza()

    # Restricciones de ponderación
    restriccion = ({'type': 'eq', 'fun': self.retorno},
               {'type': 'eq', 'fun': lambda w: np.sum(w) - 1})


    # Rango de ponderación de los activos (el valor de cada 0<w_i<1)
    rango = tuple((0, 1) for i in range(len(self.retornos)))

    # Solución de la optimización
    
    w0 = np.ones(len(self.retornos)) / len(self.retornos) ## Punto inicial de la optimización
    

    result = minimize(self.sigma, w0, args=(Rho,), method='SLSQP', constraints=restriccion, bounds=rango)
    return(result)

  def sigmaMin(self):
    minima = self.minimizar()
    if minima.success:
      print(f'La minima varianza dado que R = {self.R} es {minima.fun}')
      return minima.fun
    else:
      print(f'El algoritmo con R={self.R} no converge')

  def parametros(self):
    minima = self.minimizar()
    print(f'Los parametros para divercificar el portafolio es: \n {minima.x.round(4)}')
    return minima.x.round(4)

  def export_csv(self):
    rango = np.linspace(0.01, 0.3, 100)
    volatilidad = [self.sigmaMin(x,r,Nombre_Acciones) for x in rango]
    df = pd.DataFrame(volatilidad,rango)
    df.to_csv('data/portafolio2',index=False)


def graficarCurvaRiesgo(r, Nombre_Acciones):  
  
  def rectaTan(x,xo,a,b,cdt):
    return (2*a*xo+b)*x + cdt

  # Generar un rango de valores de retorno esperado
  minimo = np.min(r)
  maximo = np.max(r)
  rango = np.linspace(minimo, maximo, 20)

  volatilidad = [MiPortafolio(R=x,r = r,Nombre_Acciones=Nombre_Acciones).sigmaMin() for x in rango]


  ## Ajuste cuadratico
  coef = np.polyfit(rango, volatilidad, 2)
  p = np.poly1d(coef)
  print('Los coeficientes del polinomio ajustado son:\n ',coef) 
  
  a = coef[0]
  b = coef[1]
  c = coef[2]
  cdt = 0.06
  xo= np.sqrt((c-cdt)/a)
  yo= p(xo)

  ## Parametros del punto critico
  pts = MiPortafolio(R=xo,r = r,Nombre_Acciones=Nombre_Acciones).parametros()


  fig ,ax = plt.subplots(figsize=(8,10))

  ## Grafica de datos

  ax.plot(volatilidad, rango,'o-',label='Datos')
  ax.plot(p(rango),rango, 'r-', label='Curva ajustada')

  ## Grafica de la recta tangente
  ax.scatter(yo,xo)  
  ax.plot(rectaTan(rango,xo,a,b,cdt),rango, 'g-', label=f'Recta Tangente en: {xo.round(3),yo.round(3) }')

  plt.xlabel('Volatilidad')
  plt.ylabel('Retorno Esperado')
  plt.title('Frontera Eficientes')

  # Eje del cdt
  plt.axhline(y=0.06, color='r', linestyle='--',label='CDT')
  
  plt.subplots_adjust(bottom=0.4)
  
  legenda = r'Porcentaje para cada accion:' + f'\n \n({[(pts[x], Nombre_Acciones[x]) for x in range(len(Nombre_Acciones))]}) \n'
  ax.legend(bbox_to_anchor=(0.5, -0.7),loc='lower center',fontsize='medium', title=legenda )

  plt.show()


if __name__=='__main__':
  
  r = np.array([0.2,0.1,0.2,0.3])  ## vector de retornos

  Nombre_Acciones = ['CIB','AAPL','CL=F','GC=F']

  graficarCurvaRiesgo(r = r, Nombre_Acciones=Nombre_Acciones)

  