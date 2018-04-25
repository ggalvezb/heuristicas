#Ubicación C:\Users\Gonzalo\Google Drive\Respaldo\TESIS\Heuristica para Z     ejecutar: python heuristica_z_diccionario.py
import time
import numpy as np
import sys

def HeuristicaZ(site,N,D,P,K,V,simetria):
#LECTURA DE DATOS-----------------------------------
	content1 = []
	with open(site+"_dcp.txt") as f:
	    for i in f.readline().split():
	        content1.append(int(i))
	dem = np.resize(content1,(N,P))
	print(dem)
	print(range(N))

	content = []
	with open(site+"_cij.txt") as f:
	    for i in f.readline().split():
	        content.append(int(i))
	c = np.resize(content,(N,N))
	print(c)
	print(range(N))

#Elimino los valores si la matriz es simetrica
	if simetria=="Y":
		i=0
		j=0
		for i in range(N):
			for j in range(N):
				if i>j:
					c[i][j]=0
	print("distancias=",c)				


#Creo diccionario con red de nodos con sus demandas-------------------
	red_nodos_dem={}
	i=0
	for i in range(N):
		red_nodos_dem[i+1]=dem[i]
		#red_nodos_dem.update(dem[i])
	print("red_nodos_dem=",red_nodos_dem)
	#print("Rango=",range(len(list(red_nodos_dem.keys()))))

#Creo diccionario con red de nodos con sus distancias-------------------
	red_nodos_dist={}
	i=0
	j=0
	for i in range(N):
		for j in range(N):
			red_nodos_dist[i+1,j+1]=c[i][j]
			#red_nodos_dist.update(dem[i])
	print("red_nodos_dist=",red_nodos_dist)
#Creo diccionario con red de camiones-----------------
	ruta_camiones={}
	i=0
	for i in range(K):
		ruta_camiones[i+1]=0
	print(ruta_camiones)

	carga_camiones={}
	i=0
	for i in range(K):
		carga_camiones[i+1]=0
	print(ruta_camiones)

#Encuentro menor distancia desde cualquier deposito a cualquier ciudad----------------
	nodos_visitados=[]
	for k in range(K):
		lista_distancias=[]
		for n in range(N):
			lista_distancias.append(red_nodos_dist[(k+1,n+1)])
		print(lista_distancias)
		lista_distancias.sort()
		print(lista_distancias)
		i=1
		for i in range(len(lista_distancias)):
			a=lista_distancias[i]													#Valor i de la lista
			if a not in nodos_visitados and a!=0 and a!=999999 :					#si el nodo no fue visitado avanzara
				print("a=",a)
				b=lista_distancias.count(a)											#veces que se repite el valor a
				if b>=2:
					keys_demanda_repetida = []
					demandas_para_comparar=[]
					for nodo,dist in red_nodos_dist.items():
						if dist==a:
							keys_demanda_repetida.append(list(nodo))				#lleno vector con todos los nodos donde se repite la demanda
							print(range(len(keys_demanda_repetida)))
					for c in range(len(keys_demanda_repetida)):
						demandas_para_comparar.append(list(red_nodos_dem[keys_demanda_repetida[c][1]]))		#creo vector con las demandas de los nodos que se repite
					d=max(max(demandas_para_comparar))								#asigno la mayor demanda a d	
					print((demandas_para_comparar.index([])))				
							
					
					print("keys_demanda_repetida=",keys_demanda_repetida)
					print("demandas_para_comparar=",demandas_para_comparar)
					print("maxima demanda=",max(max(demandas_para_comparar)))
					sys.exit()







HeuristicaZ("Ejemplo",7,3,2,3,65,"Y")
#                     N,D,P,K ,V, simetria
