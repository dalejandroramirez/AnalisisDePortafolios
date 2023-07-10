# Analisis de portafolio

- Este repositorio esta pensado en estudiar posibles optimizaciones de portafolio.

1) Se inicio con una estimación de 4 acciones tomadas de yfinances, en las que se quiere encontrar los parametros optimos para invertir en estas acciones, dado el rendimiento esperado y minimizando la varianza del proceso.

2) Se crearon 2 nootbooks. Cargadata y analisis de portafolio. En estos se analizo la data para tratar de encontrar algun modelo bayesiano que se le ajustara, al darnos cuenta que no se pudo ajustos, se opto por usar una tecnica de minima varianza, dado un rendimiento fijo.

Los resultados del analisis se consolidaron en el archivo portafolio optimo. El cual contiene una clase, y una funcion graficadora.

* La clase **MiPortafolio** basta con ingresarle en nombre de la accion, el rendimiento esperado $R$ 
y por el momento, aunque posteriormente se modificará se debe ingresar el valor esperado de cada acción (esto se podria calcular apriori de  la lista, de retornos de cada accion, pero dado que la serie no es estacionaria, considero que esta media es poco acertada, y deseo conseguir un mejor estimador insesgado)

* la funcion **graficarCurvaRiesgo** va a graficar la curva de riego y ademas de ajustar un polinomio cuadratico. Esto con el fin de mas adelante encontrar la ecuación de la recta tangente a la curva que sea mas proxima al valor de un CDT.