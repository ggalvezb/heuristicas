#Ubicación C:\Users\Gonzalo\Google Drive\Respaldo\TESIS\Heuristica para Z     ejecutar: python heuristica_intento3.py
import time
import numpy as np
import pandas as pd
import sys

def HeuristicaZ(site,N,D,P,K,V,simetria):
	#LECTURA DE DATOS-----------------------------------
	distancias = pd.read_csv('Ejemplo_cij.txt', sep=" ", header=None)
	distancias=distancias.as_matrix().reshape(N,N)
	print("distancias",distancias)

	dem = pd.read_csv('Ejemplo_dcp.txt', sep=" ", header=None)
	dem=dem.as_matrix().reshape(N,P)
	print("dem",dem)

	inventario=pd.read_csv('Ejemplo_sdp.txt', sep=" ", header=None)
	inventario=inventario.as_matrix().reshape(D,P)
	print("inventario",inventario)


	#Creo vectores con los nodos visitados y por visitar-------------------------------------------
	i=0
	nodos_visitados=[]
	for i in range(K):
		nodos_visitados.append(i+1)
	print("nodos_visitados=",nodos_visitados)
	
	i=0
	C=N-D
	nodos_por_visitar=[]
	for i in range(D,N):
		nodos_por_visitar.append(i+1)
	print("nodos_por_visitar=",nodos_por_visitar)

	#Creo diccionario de camiones--------------------------------------------------------------------
	capacidad_maxima=V 											#Capacidad maxima del camion
	carga_camiones=[0,0,0]
	diccionario_camiones={}
	i=0
	for i in range(K):
		diccionario_camiones[i+1]=0
	print("Diccionario camiones=",diccionario_camiones)
	camion_en_uso=list(diccionario_camiones.keys())
	camion_en_uso=camion_en_uso[0]
	carga_actual=carga_camiones[camion_en_uso - 1]
	posicion_actual=nodos_visitados[0]
	# Creo diccionario con las demandas de cada nodo--------------------------------------------------
	demanda_nodos={}
	i=0
	j=0
	for i in range(D,N):
		demanda_nodos[i+1]=list(dem[i])
	print("demanda_nodos",demanda_nodos)

	#Creo diccionario con rutas por camion -----------------------------------------------------------
	ruta_camion={}
	i=0
	for i in range(K):
		ruta_camion[i+1]=[0]
	print("ruta_camion=",ruta_camion)

	#Creo diccionario con el inventario de cada deposito
	inventario_depostios={}
	i=0
	for i in range(K):
		inventario_depostios[i+1]=list(inventario[i])
	print("inventario_depostios=",inventario_depostios)

	#iniciar iteración--------------------------------------------------------------------------------
	g=0
	while len(nodos_por_visitar)!=0:
		g=g+1
		print("INICIO ITERACION " + str(g) + "--------------------------------------------------------------------------------------------")
		red_nodos_dist={}									#creo diccionario con las distancias del nodo actual a los nodos que faltan por visitar
		i=0
		for i in range(len(nodos_por_visitar)):
			red_nodos_dist[posicion_actual,nodos_por_visitar[i]]=distancias[posicion_actual-1][nodos_por_visitar[i]-1] #Creo diccionario de distancia entre posicion actual y nodos que falta por visitar
		distancias_a_comparar=list(red_nodos_dist.values())
		distancia_menor=min(distancias_a_comparar)

		if distancias_a_comparar.count(distancia_menor)>=2:						#evaluo si se repite la distancia o no
			siguiente_nodo=distancia_repetida(red_nodos_dist,dem,distancia_menor)
		else:
			siguiente_nodo=distancia_sin_repetir(red_nodos_dist,dem,distancia_menor,posicion_actual)	

		(nodos_visitados,nodos_por_visitar,carga_camiones,carga_actual,camion_en_uso,dem,demanda_nodos,ruta_camion)=verificar_carga_camion(siguiente_nodo,diccionario_camiones,camion_en_uso,carga_camiones,V,dem,nodos_visitados,nodos_por_visitar,carga_actual,demanda_nodos,ruta_camion)	
		
		#Muestros soluciones de iteracion
		print("nodos_visitados=",nodos_visitados)
		print("nodos_por_visitar=",nodos_por_visitar)
		print("carga_camiones=",carga_camiones)
		print("carga_actual=",carga_actual)
		print("camion_en_uso=",camion_en_uso)
		print("dem=",dem)
		print("demanda nodos=",demanda_nodos)
		print("ruta camiones=",ruta_camion)
	

#Funcion Distnacia repetida-----------------------------------------------------------------------------		
def distancia_repetida(red_nodos_dist,dem,distancia_menor,posicion_actual):
	key_distancia_menor=[]
	for nodo,value in red_nodos_dist.items():
		if value==distancia_menor:
			key_distancia_menor.append(list(nodo))
	print("key_distancia_menor=",key_distancia_menor)
	key_distancia_menor=flatten(key_distancia_menor)
	key_distancia_menor.remove(posicion_actual)
	diccionario_demandas={}											#Creo diccionario solo con las demandas que se repiten, para poder tener un key asociado
	i=0
	for i in range(len(key_distancia_menor)):
		diccionario_demandas[key_distancia_menor[i]]=list(dem[key_distancia_menor[i]-1])
	print("diccionario_demandas=",diccionario_demandas)	
	i=0
	demandas_a_comparar=[]											#obtengo la mayor demanda entre los nodos con igual distancia
	for i in range(len(key_distancia_menor)):
		demandas_a_comparar.append(list(dem[key_distancia_menor[i]-1]))
	demandas_a_comparar=flatten(demandas_a_comparar)
	a=max(demandas_a_comparar)
	siguiente_nodo=[]
	print("diccionario_demandas.items=",diccionario_demandas.items())		#obtengo el siguiente nodo al que se deberia dirigir el vehiculo
	for nodo,value in diccionario_demandas.items():
		i=0
		print(type(list(diccionario_demandas.values())))
		for i in range(len(diccionario_demandas.values())):
			if value[i]==a:
				siguiente_nodo.append(nodo)
		print("siguiente_nodo=",siguiente_nodo)
	return(siguiente_nodo)


#Funcion Distnacia no repetida-----------------------------------------------------------------------------		
def distancia_sin_repetir(red_nodos_dist,dem,distancia_menor,posicion_actual):
	key_distancia_menor=[]
	for nodo,value in red_nodos_dist.items():
		if value==distancia_menor:
			key_distancia_menor.append(list(nodo))
	key_distancia_menor=flatten(key_distancia_menor)			
	key_distancia_menor.remove(posicion_actual)
	siguiente_nodo=[]
	siguiente_nodo=key_distancia_menor
	#print("dentro de funcion siguiente_nodo=",siguiente_nodo)
	return(siguiente_nodo)

#Funcion Verificar carga del camion-----------------------------------------------------------------------------	
def verificar_carga_camion(siguiente_nodo,diccionario_camiones,camion_en_uso,carga_camiones,V,dem,nodos_visitados,nodos_por_visitar,carga_actual,demanda_nodos,ruta_camion):
	print("Carga actual iniciando la funcion=",carga_actual)
	print("siguiente nodo dentro de la funcion=",siguiente_nodo)
	demanda_a_satisfacer=demanda_nodos.get(siguiente_nodo[0])
	if carga_actual < V:
		if carga_actual<V and sum(demanda_a_satisfacer)<(V - carga_actual):			#El camion puede satisfacer toda la demanda del nodo
			print("SE EJECUTO CASO 1")
			carga_actual=sum(demanda_a_satisfacer)
			carga_camiones[camion_en_uso - 1]=carga_actual
			demanda_nodos[siguiente_nodo[0]]=0
			nodos_visitados.append(siguiente_nodo)
			nodos_por_visitar.remove(siguiente_nodo[0])
			g=list(ruta_camion[camion_en_uso])	
			g.append(siguiente_nodo)									#Agrego nodo visitado a ruta del camion
			ruta_camion[camion_en_uso]=g
			print("nodos_visitados dentro de la funcion=",nodos_visitados)
			print("nodos_por_visitar dentro de la funcion=",nodos_por_visitar)
			print("carga_camiones dentro de la funcion=",carga_camiones)
		elif carga_actual<V and (V - carga_actual) <= sum(demanda_a_satisfacer):			#El camion solo puede satisfacer una parte de la demanda del nodo
			for j in range(len(demanda_a_satisfacer)):
				if carga_actual < V:
					if demanda_a_satisfacer[j]!=0 and (V - carga_actual)>=demanda_a_satisfacer[j]:	#El camion satisface toda la demanda del producto
						print("SE EJECUTO CASO 2")
						carga_actual= carga_actual + demanda_a_satisfacer[j]
						carga_camiones[camion_en_uso - 1]=carga_actual
						g=list(ruta_camion[camion_en_uso])	
						g.append(siguiente_nodo)									#Agrego nodo visitado a ruta del camion
						ruta_camion[camion_en_uso]=g
						demanda_a_satisfacer[j]=0
					elif demanda_a_satisfacer[j]!=0 and (V - carga_actual)<demanda_a_satisfacer[j]:	#El camion solo puede satisfacer una parte de la demanda del producto
						print("SE EJECUTO CASO 3")
						print(demanda_a_satisfacer)
						demanda_a_satisfacer[j]=demanda_a_satisfacer[j] - (V - carga_actual)
						print(demanda_a_satisfacer)
						demanda_nodos[siguiente_nodo[0]]=demanda_a_satisfacer
						g=list(ruta_camion[camion_en_uso])	
						g.append(siguiente_nodo)									#Agrego nodo visitado a ruta del camion
						ruta_camion[camion_en_uso]=g
						carga_actual = V
						carga_camiones[camion_en_uso - 1]=carga_actual
						print("demanda nodos dentro de caso 3=",demanda_nodos)

	else:
		if demanda_nodos[siguiente_nodo[0]]==0:
			print("SE EJECUTO CASO 4")
			camion_en_uso += 1
			carga_actual=0
			nodos_visitados.append(siguiente_nodo)
			nodos_por_visitar.remove(siguiente_nodo[0])
		else:
			print("SE EJECUTO CASO 5")
			camion_en_uso += 1
			carga_actual=0				
	return(nodos_visitados,nodos_por_visitar,carga_camiones,carga_actual,camion_en_uso,dem,demanda_nodos,ruta_camion)			



#Funcion para dejar en una dimension list de N dimensiones
def flatten(l):
    try:
        return flatten(l[0]) + (flatten(l[1:]) if len(l) > 1 else []) if type(l) is list else [l]
    except IndexError:
        return []



HeuristicaZ("Ejemplo",7,3,2,3,65,"Y")
#                     N,D,P,K ,V, simetria
