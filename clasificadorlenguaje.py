from dataframegen import ngramas
from dataframegen import eliminasimbolos
import math
import pandas as pd

"""	ngramas(num, documento)
	Argumentos:
	num - tamaño de los n gramas en los que se dividirá el texto.
	documento - buffer del documento a separar.
	Devuelve una lista de ngramas pertenecientes al documento de entrada."""
"""def ngramas(num, documento):
	salida, texto = [], ''
	for linea in documento.readlines():
		texto += linea
	texto = texto.replace('\n', ' ')
	texto = eliminasimbolos(texto)
	texto = texto.lower()
	for i in range(0,len(texto)-num):
			salida.append(texto[i:i+num])
	return salida"""

"""	eliminasimbolos(texto)
	Argumentos:
	texto - texto a limpiar.
	Elimina caracteres inútiles del texto de entrada."""
"""def eliminasimbolos(texto):
	for c in texto:
		if ord(c) in range(34,39) or ord(c) in range(40,63) or ord(c) in range(64,65) or ord(c) in range(91,97) or ord(c) in range(123,161) or ord(c) in range(162,191):
			texto = texto.replace(c, '')
	return texto"""

"""	calculaprob(ngramas, df, sumas, x, k)
	Argumentos:
	ngramas - Lista de ngramas del documento a analizar.
	df - Dataframe obtenido del archivo .csv, contiene los counts de los idiomas.
	sumas - Lista que contiene el total de las columnas, es decir, la magnitud de ngramas por cada idioma.
	x - Número de clases (en este caso 3)
	k - Constante para el "aplanamiento" de Laplace.
	Calcula la probabilidad de que el documento de entrada sea de cualquiera de los tres idiomas, utiliza un "aplanado"
	de Laplace para evitar que haya indeterminaciones en los logaritmos. Importante mencionar que se usan logaritmos para 
	evitar perdidas de datos por exactitud, ya que las probabilidades son muy pequeñas.
	Se determina el idioma del documento a partir de la probabilidad máxima."""
def calculaprob(ngramas, df, sumas, x, k):
	probing = math.log(df['count(ingles)'].gt(0).sum()+k)-math.log(len(list(df.index))+k*x)
	probesp = math.log(df['count(espanol)'].gt(0).sum()+k)-math.log(len(list(df.index))+k*x)
	probport = math.log(df['count(portugues)'].gt(0).sum()+k)-math.log(len(list(df.index))+k*x)
	for n in ngramas:
		if n in list(df.index):
			probing += math.log(list(df.loc[n])[0]+k)-math.log(sumas[0]+k*len(list(df.index)))
			probesp += math.log(list(df.loc[n])[1]+k)-math.log(sumas[1]+k*len(list(df.index)))
			probport += math.log(list(df.loc[n])[2]+k)-math.log(sumas[2]+k*len(list(df.index)))
	res = max([probing, probesp, probport])
	if res == probing:
		return 'El idioma de tu documento es ingles'
	elif res == probesp:
		return 'El idioma de tu documentos es espanol'
	else:
		return 'El idioma de tu documento es portugues'

"""Procesamiento de datos
	El usuario da el nombre del archivo .csv que contiene los counts de los idiomas y del archivo a analizar."""
def main():
	df = pd.read_csv(input('Archivo .csv: '), index_col = 0)
	archivo = open(input('Archivo a analizar: '))
	print(calculaprob(ngramas(len(list(df.index)[0]), archivo), df, list(df.sum()), 3, int(input('Dame la k: '))))

main()