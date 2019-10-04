import pandas as pd

"""	ngramas(num, documento)
	Argumentos:
	num - tamaño de los n gramas en los que se dividirá el texto.
	documento - buffer del documento a separar.
	Devuelve una lista de ngramas pertenecientes al documento de entrada."""
def ngramas(num, documento):
	salida, texto = [], ''
	for linea in documento.readlines():
		texto += linea
	texto = texto.replace('\n', ' ')
	texto = eliminasimbolos(texto)
	texto = texto.lower()
	for i in range(0,len(texto)-num):
			salida.append(texto[i:i+num])
	return salida

"""	eliminasimbolos(texto)
	Argumentos:
	texto - texto a limpiar.
	Elimina caracteres inútiles del texto de entrada."""
def eliminasimbolos(texto):
	for c in texto:
		if ord(c) in range(34,39) or ord(c) in range(40,63) or ord(c) in range(64,65) or ord(c) in range(91,97) or ord(c) in range(123,161) or ord(c) in range(162,191):
			texto = texto.replace(c, '')
	return texto

"""	crearbanco(n)
	Argumentos:
	n - lista de n-gramas
	Crea un diccionario que contiene los n-gramas del idioma correspondiente y los counts."""
def crearbanco(n):
	banco = {}
	for grama in n:
		if grama not in banco.keys():
			banco[grama] = 1
		else: 
			banco[grama] += 1
	return banco 

""" creartabla(ing, esp, port)
	Argumentos:
	ing - banco de inglés
	esp - banco de español
	port - banco de portugués
	Crea el dataframe de pandas a partir de los bancos de ngramas, los indices sestám conformados por los datagramas,
	mientras que las columnas corresponden al count de inglés, español y portugués respectivamente.""" 
def creartabla(ing, esp, port):
	llaves = list(ing.keys()) + list(esp.keys()) + list(port.keys())
	llaves = list(set(llaves))
	llaves.sort()
	counti, counte, countp = [], [], []
	for k in llaves:
		if k in ing.keys():
			counti.append(ing[k])
		else:
			counti.append(0)
		if k in esp.keys():
			counte.append(esp[k])
		else:
			counte.append(0)
		if k in port.keys():
			countp.append(port[k])
		else:
			countp.append(0)
	dic = {'count(ingles)':counti, 'count(espanol)':counte, 'count(portugues)':countp}
	tabla = pd.DataFrame(dic)
	tabla.index = llaves
	return tabla

""" Procesamiento de datos y creación del archivo .csv final
	El usurio da todos los datos requeridos para exportar el archivo .csv que contiene los counts de los 
	lenguajes."""
def main():
	ingles = open(input('Archivo de ingles: '), encoding = "utf8")
	espanol = open(input('Archivo de espanol: '), encoding = "utf8")
	portugues = open(input('Archivo de portugues: '), encoding = "utf8")
	tam = int(input('Tamano de n-grama: '))
	bancoing = crearbanco(ngramas(tam, ingles))
	bancoesp = crearbanco(ngramas(tam, espanol))
	bancoport = crearbanco(ngramas(tam, portugues))
	df = creartabla(bancoing, bancoesp, bancoport)
	export_csv = df.to_csv(input('Archivo de salida .csv: '), index = True, header = True)

if __name__ == '__main__': 
	main()