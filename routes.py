import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

# Definir un diccionario de reglas lógicas con datos ficticios de rutas en Santa Marta, Colombia
reglas = {
    "Conectado": {
        ("Playa Rodadero", "Parque Bolívar"): 5,
        ("Parque Bolívar", "Mercado Central"): 8,
        ("Mercado Central", "Malecón"): 6,
        ("Malecón", "Playa Blanca"): 12,
        ("Playa Blanca", "Quinta de San Pedro"): 10,
        ("Centro comercial buena vista", "Quinta de San Pedro"): 15,
        ("Quinta de San Pedro", "Centro Histórico"): 7,
        ("Centro Histórico", "Catedral Santa Marta"): 3,
        ("Catedral Santa Marta", "Muelle Turístico"): 5,
    }
}

# Crear grafo
grafo = nx.Graph()

# Agregar las conexiones al grafo
for conexion, distancia in reglas["Conectado"].items():
    ruta1, ruta2 = conexion
    grafo.add_edge(ruta1, ruta2, weight=distancia)

# Funcion para localizar mejor ruta
def encontrar_mejor_ruta(
    origen, destino, visitados=[], ruta_actual=[], distancia_actual=0
):
    # Agregar el destino actual a la ruta y marcarla como visitada
    ruta_actual.append(origen)
    visitados.append(origen)

    # Verificar si se ha llegado al destino
    if origen == destino:
        # Imprimir la ruta y la distancia total
        print("Destino encontrado", ruta_actual)
        print("Distancia total", distancia_actual)
        return ruta_actual

    # Obtener todas las conexiones de la estación actual desde las reglas
    conexiones = reglas["Conectado"].keys()

    # Inicializar la mejor ruta y distancia como null
    mejor_ruta = None
    mejor_distancia = float("inf")

    # Recorrer todas las conexiones de la ruta actual
    for conexion in conexiones:
        if origen == conexion[0] and conexion[1] not in visitados:
            # Calcular la distancia acumulada para esta conexión
            distancia = distancia_actual + reglas["Conectado"][conexion]

            # Realizar una llamada recursiva para encontrar el mejor destino desde el punto actual
            nueva_ruta = encontrar_mejor_ruta(
                conexion[1], destino, visitados[:], ruta_actual[:], distancia
            )

            # Actualizar la mejor ruta y distancia si se ha encontrado una ruta más corta
            if nueva_ruta and distancia < mejor_distancia:
                mejor_ruta = nueva_ruta
                mejor_distancia = distancia

    return mejor_ruta

ruta = encontrar_mejor_ruta("Parque Bolívar", "Malecón")

# Generar datos para la gráfica en forma de campana
mu, sigma = 0, 0.1 # Media y desviación estándar
datos = np.random.normal(mu, sigma, 1000)

# Colores personalizados para los nodos y las aristas
node_colors = ["blue" if node in ruta else "red" for node in grafo.nodes()]
edge_colors = ["blue" if edge in grafo.edges() else "black" for edge in grafo.edges()]

# Visualizar el grafo y la ruta encontrada
pos = nx.spring_layout(grafo)
nx.draw_networkx(grafo, pos, with_labels=True, node_size=500, font_size=10, node_color=node_colors, edge_color=edge_colors)
etiquetas = nx.get_edge_attributes(grafo, "weight")
nx.draw_networkx_edge_labels(grafo, pos, edge_labels=etiquetas, font_color="green")
ruta_aristas = [(ruta[i], ruta[i+1]) for i in range(len(ruta) -1)]
nx.draw_networkx_edges(grafo, pos, edgelist=ruta_aristas, edge_color="blue", width=2)

# Visualizar la gráfica en forma de campana
plt.hist(datos, bins=30, density=True, alpha=0.5)
plt.xlabel("Valores")
plt.ylabel("Densidad")
plt.title("Gráfica en forma de campana")
plt.grid(True)

plt.show()
