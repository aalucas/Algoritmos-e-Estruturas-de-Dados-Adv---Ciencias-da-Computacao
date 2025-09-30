# ...existing code...
import heapq
import math

class Graph:
    def __init__(self):
        # O grafo é um dicionário: {nó: [(vizinho, peso), ...]}
        self.adj = {}

    def add_edge(self, source, destination, weight):
        """Adiciona uma aresta (com peso) ao grafo. Assumimos um grafo não-direcionado para simplicidade."""
        if source not in self.adj:
            self.adj[source] = []
        if destination not in self.adj:
            self.adj[destination] = []
            
        # Adiciona a aresta: (destino, peso)
        self.adj[source].append((destination, weight))
        
        # Para grafo não-direcionado, adicione a aresta de volta
        self.adj[destination].append((source, weight))

    def get_nodes(self):
        """Retorna todos os nós (vértices) do grafo."""
        return list(self.adj.keys())

    def __repr__(self):
        """Representação legível do grafo."""
        return f"Grafo com {len(self.adj)} nós: {self.adj}"
# ...existing code...

def dijkstra(graph, start_node):
    distances = {node: math.inf for node in graph.get_nodes()}
    predecessors = {node: None for node in graph.get_nodes()}

    if start_node not in distances:
        raise ValueError(f"Nó inicial '{start_node}' não existe no grafo.")

    distances[start_node] = 0

    # Fila de Prioridade (Min-Heap): armazena tuplas (distância, nó)
    priority_queue = [(0, start_node)]

    while priority_queue:
        # Extrai o nó com a menor distância (O(log V))
        current_distance, current_node = heapq.heappop(priority_queue)

        # Se a distância extraída for maior que a distância já conhecida (redundância da heap), ignore.
        if current_distance > distances[current_node]:
            continue

        # Explora os vizinhos
        for neighbor, weight in graph.adj.get(current_node, []):
            distance = current_distance + weight

            # Relaxamento: se um caminho mais curto for encontrado, atualiza a distância e o predecessor
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                predecessors[neighbor] = current_node

                # Adiciona o vizinho à fila de prioridade (O(log V))
                heapq.heappush(priority_queue, (distance, neighbor))

    return distances, predecessors

def find_and_visualize_shortest_path(graph, start_node, end_node):
    distances, predecessors = dijkstra(graph, start_node)

    if end_node not in distances:
        raise ValueError(f"Nó destino '{end_node}' não existe no grafo.")

    min_distance = distances[end_node]
    path = []
    current = end_node

    # 2. Reconstrução do Caminho
    if min_distance == math.inf:
        print(f"\n[Resultado] Não há caminho entre {start_node} e {end_node}.")
        return [], math.inf

    while current is not None:
        path.append(current)
        current = predecessors[current]

    path.reverse() # O caminho é reconstruído do destino para a origem, então precisa ser invertido.

    # 3. Visualização (Requisito 5)
    print(f"\n--- CAMINHO MÍNIMO ({start_node} -> {end_node}) ---")
    print(f"Distância Mínima: {min_distance}")
    print(f"Caminho: {' -> '.join(map(str, path))}")
    print("------------------------------------------")

    return path, min_distance

# --- Testes de Validação ---
if __name__ == "__main__":
    
    # Criação do Grafo de Teste (Exemplo de Mapa ou Rede)
    G = Graph()
    G.add_edge('A', 'B', 4)
    G.add_edge('A', 'C', 2)
    G.add_edge('B', 'E', 3)
    G.add_edge('C', 'D', 2)
    G.add_edge('C', 'F', 4)
    G.add_edge('D', 'E', 3)
    G.add_edge('D', 'F', 1)
    G.add_edge('E', 'Z', 1)
    G.add_edge('F', 'Z', 2)

    print("Grafo de Teste Criado:")
    print(G)
    
    # ----------------------------------------------------
    # Caso de Teste 1: Caminho Padrão
    # Esperado: A -> C -> D -> F -> Z (Distância: 2 + 2 + 1 + 2 = 7)
    # ----------------------------------------------------
    print("\n--- TESTE 1: Caminho Mais Curto (A para Z) ---")
    path1, dist1 = find_and_visualize_shortest_path(G, 'A', 'Z')
    assert dist1 == 7, f"Teste 1 falhou: Distância esperada 7, obtida {dist1}"
    assert path1 == ['A', 'C', 'D', 'F', 'Z'], "Teste 1 falhou: Caminho incorreto"
    print("Teste 1: Sucesso.")
    
    # ----------------------------------------------------
    # Caso de Teste 2: Caminho Intermediário
    # Esperado: B -> E (Distância: 3)
    # ----------------------------------------------------
    print("\n--- TESTE 2: Caminho Intermediário (B para E) ---")
    path2, dist2 = find_and_visualize_shortest_path(G, 'B', 'E')
    assert dist2 == 3, f"Teste 2 falhou: Distância esperada 3, obtida {dist2}"
    print("Teste 2: Sucesso.")

    # ----------------------------------------------------
    # Caso de Teste 3: Grafo Desconectado (Caso de Borda)
    # Adicionamos um nó 'K' sem arestas
    # ----------------------------------------------------
    G.adj['K'] = [] # Nó isolado
    
    print("\n--- TESTE 3: Grafo Desconectado (A para K) ---")
    path3, dist3 = find_and_visualize_shortest_path(G, 'A', 'K')
    assert dist3 == math.inf, f"Teste 3 falhou: Distância esperada inf, obtida {dist3}"
    print("Teste 3: Sucesso.")

    # ----------------------------------------------------
    # Caso de Teste 4: Origem e Destino são o mesmo nó
    # ----------------------------------------------------
    print("\n--- TESTE 4: Origem e Destino Iguais (A para A) ---")
    path4, dist4 = find_and_visualize_shortest_path(G, 'A', 'A')
    assert dist4 == 0, f"Teste 4 falhou: Distância esperada 0, obtida {dist4}"
    print("Teste 4: Sucesso.")