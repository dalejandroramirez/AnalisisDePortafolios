import numpy as np
import matplotlib.pyplot as plt
import yfinance as yf
import pandas as pd
from scipy.stats import spearmanr

from scipy.optimize import minimize 

# R : Es la tasa esperada de retorno

# r : El valor esperado de retorno

# Nombre_Acciones : Son los nombres de las acciones dadas por yfinance

r = np.array([0.2,0.1,0.2,0.3])  ## vector de retornos esperados que no se como calcular
Nombre_Acciones = ['CIB','AAPL','CL=F','GC=F']

class MiPortafolio:

  def __init__(self,R,r,Nombre_Acciones):
    self.R = R
    self.retornos = r
    self.acciones = Nombre_Acciones

  def matriz_retornos(self):
    Retornos=pd.DataFrame()
    for accion_name in self.acciones:
      accion = yf.Ticker(accion_name)
      Retornos[accion_name] = accion.history(period="2y", interval="1wk")[['Close']].pct_change()[1:]
    return(Retornos)

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
    w0 = np.ones(len(self.retornos)) / len(self.retornos) # Punto inicial de la optimización

    result = minimize(self.sigma, w0, args=(Rho,), method='SLSQP', constraints=restriccion, bounds=rango)
    return(result)

  def sigmaMin(self):
    minima = self.minimizar()
    print(f'La minima varianza dado que R = {self.R} es {minima.fun}')
    return minima.fun

  def parametros(self):
    minima = self.minimizar()
    print(f'Los parametros para divercificar el portafolio es: \n {minima.x.round(4)}')
    return minima.x.round(4)
  


def graficarCurvaRiesgo(r, Nombre_Acciones):  
  # Generar un rango de valores de retorno esperado
  rango = np.linspace(0.1, 0.3, 100)


  volatilidad = [MiPortafolio(x,r,Nombre_Acciones).sigmaMin() for x in rango]
  ## Ajuste cuadratico
  coef = np.polyfit(rango, volatilidad, 2)
  p = np.poly1d(coef)
  print('Los coeficientes del polinomio ajustado son:\n ',coef) 

  
  plt.plot(volatilidad, rango,'o-',label='Datos')
  plt.plot(p(rango),rango, 'r-', label='Curva ajustada')

  plt.plot(p(rango),rango, 'r-', label='Curva ajustada')
  
  plt.xlabel('Volatilidad')
  plt.ylabel('Retorno Esperado')
  plt.title('Frontera Eficiente')
  plt.axhline(y=0.06, color='r', linestyle='-',label='CDF')
  plt.legend()
  plt.show()


if __name__=='__main':
  r = np.array([0.2,0.1,0.2,0.3])  ## vector de retornos esperados que no se como calcular (aun)
  Nombre_Acciones = ['CIB','AAPL','CL=F','GC=F']

  graficarCurvaRiesgo(r,Nombre_Acciones)

  