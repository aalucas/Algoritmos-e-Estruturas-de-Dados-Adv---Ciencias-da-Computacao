# Estruturas de Dados — Implementações em Python

Repositório com implementações didáticas de estruturas e algoritmos em Python:
- ordenacao.py — algoritmos de ordenação e benchmark
- grafos.py — grafo simples e Dijkstra (caminhos mínimos)
- arvores.py — árvore AVL (inserção, remoção, busca, impressão)
- heap.py — fila de prioridade baseada em heap (com atualização de prioridade)

## Objetivo
Código educacional para estudar e demonstrar comportamento, complexidade e correção de algoritmos clássicos. Projetado para execução local (Windows) e publicação em GitHub como material didático.

## Requisitos
- Python 3.8+ recomendado
- Módulos da biblioteca padrão: random, datetime, time, heapq, itertools, math

## Estrutura do Repositório
- ordenacao.py — geração de dados (classe Produto) e 4 algoritmos de ordenação (Bubble, Quick, Merge, Heap). Inclui medição de tempo e verificação de corretude.
- grafos.py — classe Graph (dicionário de adjacência), dijkstra() e find_and_visualize_shortest_path(). Testes no bloco __main__.
- arvores.py — implementação completa de AVL (Node, AVLTree) com testes no bloco __main__.
- heap.py — PriorityQueue (heapq + entry_finder + contador) e rotina test_priority_queue().

## Como executar (Windows)
Abra um terminal no diretório do repositório e rode:

- Ordenação / benchmark:
  python ordenacao.py

- Grafos / Dijkstra:
  python grafos.py

- Árvores AVL:
  python arvores.py

- Fila de prioridade (Heap):
  python heap.py

Nota: para módulos com geração de dados/benchmarks (ordenacao.py), o tempo de execução pode variar. Evite aumentar N_PRODUTOS acima de limites razoáveis para algoritmos O(n^2) (Bubble Sort).

## Resumo das APIs (uso rápido)

ordenacao.py
- Classe Produto(nome, preco, avaliacao, data_adicao, categoria)
- Funções de ordenação:
  - bubble_sort(arr, key=lambda x: x, reverse=False)
  - quick_sort(arr, key=lambda x: x, reverse=False)
  - merge_sort(arr, key=lambda x: x, reverse=False)
  - heap_sort(arr, key=lambda x: x, reverse=False)
- medir_tempo_e_verificar(algoritmo, dados_originais, chave, reverso)

grafos.py
- class Graph:
  - add_edge(source, destination, weight)
  - get_nodes()
  - adj (dicionário público)
- dijkstra(graph, start_node) -> (distances, predecessors)
- find_and_visualize_shortest_path(graph, start_node, end_node) -> (path, min_distance)

arvores.py
- class Node(key)
- class AVLTree:
  - insert(key)
  - delete(key)
  - search(key) -> bool/Node
  - print_tree() — impressão (inorder)

heap.py
- class PriorityQueue:
  - add_task(task, priority=0)
  - pop_task() -> (task, priority)
  - change_priority(task, new_priority)
  - __len__(), __repr__()
- test_priority_queue() — exemplo e verificação

## Testes e Verificação
Cada módulo contém um bloco `if __name__ == "__main__":` com cenários de teste/demonstração:
- ordenacao.py: gera N_PRODUTOS = 1000 e executa comparativos contra sorted()
- grafos.py: cria um grafo de exemplo e valida caminhos/mensagens
- arvores.py: insere chaves para forçar rotações, testa busca e remoções
- heap.py: adiciona/atualiza/remove tarefas e verifica ordem de remoção

Para testes automáticos (sugestão):
- Extrair funções puras e criar testes com pytest em `tests/`:
  - tests/test_ordenacao.py
  - tests/test_grafos.py
  - tests/test_arvores.py
  - tests/test_heap.py

## Complexidade (resumo)
- Bubble Sort: O(n^2)
- Quick Sort: O(n log n) médio, O(n^2) pior caso
- Merge Sort: O(n log n)
- Heap Sort: O(n log n)
- Dijkstra (com heap): O((V + E) log V)
- AVL (inserção/remoção/busca): O(log n)
- PriorityQueue (heap + lazy deletion): add/pop O(log n) amortizado

## Boas práticas e notas
- Mantenha geração de dados e execução de testes sob `if __name__ == "__main__":` para permitir importação segura dos módulos.
- Use random.seed(...) nos scripts de benchmark para reprodutibilidade.
- Evite rodar Bubble Sort em conjuntos grandes ao fazer benchmarking.
- Para cargas altas na PriorityQueue, implemente limpeza (reconstrução do heap) se entradas obsoletas se acumularem.

## Licença
Sugestão: adicionar LICENSE (por exemplo MIT) ao repositório antes de publicar.

## Contribuição
- Abra issues para bugs e melhorias.
- Envie Pull Requests com testes e documentação.
- Mantenha estilo consistente e docstrings claros.

## Exemplo rápido (ordenacao.py)
No terminal:
```
python ordenacao.py
```
Saída esperada: tabela com tempos por algoritmo/critério e mensagens de verificação de corretude.

---

Se quiser, gero automaticamente:
- README traduzido para inglês,
- arquivos de testes pytest para cada módulo,
- docstrings/typing e pequenos patches para garantir importação sem executar geração pesada.  
