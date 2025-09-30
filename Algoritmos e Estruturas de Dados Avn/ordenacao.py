import random
import datetime
import time

# Configuração dos Requisitos Iniciais
# Número de produtos a serem gerados
N_PRODUTOS = 1000 # 1000 produtos exatamente como solicitado
print(f"Configuração: Gerando {N_PRODUTOS} produtos.")

# --- CLASSE PRODUTO ---
class Produto:
    def __init__(self, nome, preco, avaliacao, data_adicao, categoria):
        self.nome = nome
        self.preco = preco
        self.avaliacao = avaliacao
        self.data_adicao = data_adicao
        self.categoria = categoria

    def __repr__(self):
        # Formatando para melhor visualização
        return f"Produto(Preco:{self.preco:.2f}, Aval:{self.avaliacao:.2f}, Data:{self.data_adicao.date()}, Cat:{self.categoria})"

# --- GERAÇÃO DE DADOS (Requisito 1) ---
def gerar_produtos(n):
    nomes = ["Produto" + str(i) for i in range(n)]
    precos = [round(random.uniform(10, 1000), 2) for _ in range(n)]
    avaliacoes = [round(random.uniform(0, 5), 2) for _ in range(n)]
    # Datas no intervalo de 1 ano, incluindo segundos para garantir unicidade e ordenação fina
    datas = [datetime.datetime.now() - datetime.timedelta(days=random.randint(0, 365), seconds=random.randint(0, 86400)) for _ in range(n)]
    categorias = ["Categoria" + str(random.randint(1, 5)) for _ in range(n)]
    
    produtos = [Produto(nomes[i], precos[i], avaliacoes[i], datas[i], categorias[i]) for i in range(n)]
    return produtos

dataset_original = gerar_produtos(N_PRODUTOS)


## Implementação de Algoritmos de Ordenação 
# Bubble Sort, Quick Sort, Merge Sort, Heap Sort RESPECTIVAMENTE
# Cada função recebe a lista, uma função chave e um booleano para ordem reversa

def bubble_sort(arr, key=lambda x: x, reverse=False):
    n = len(arr)
    # Loop principal para passar por toda a lista
    for i in range(n - 1):
        swapped = False
        # Loop para as comparações e trocas
        for j in range(0, n - i - 1):
            # Obtém os valores de comparação
            val_j = key(arr[j])
            val_j1 = key(arr[j + 1])
            
            # Condição de troca
            should_swap = False
            if not reverse: # Ascendente (padrão)
                if val_j > val_j1:
                    should_swap = True
            else: # Descendente
                if val_j < val_j1:
                    should_swap = True
            
            if should_swap:
                arr[j], arr[j + 1] = arr[j + 1], arr[j] # Troca
                swapped = True
        
        # Se nenhuma troca ocorreu em um passo, a lista está ordenada
        if not swapped:
            break
    return arr


def quick_sort(arr, key=lambda x: x, reverse=False):
    # Função auxiliar para particionamento (Lomuto ou Hoare)
    def partition(items, low, high):
        # Escolhe o pivo como o elemento mais à direita
        pivot_val = key(items[high])
        i = low - 1  # Índice do menor elemento

        for j in range(low, high):
            current_val = key(items[j])
            
            # Condição de partição
            should_swap = False
            if not reverse: # Ascendente
                if current_val <= pivot_val:
                    should_swap = True
            else: # Descendente
                if current_val >= pivot_val:
                    should_swap = True

            if should_swap:
                i += 1
                items[i], items[j] = items[j], items[i] # Troca

        # Troca o pivo (items[high]) com o elemento items[i + 1]
        items[i + 1], items[high] = items[high], items[i + 1]
        return i + 1

    # Função auxiliar recursiva
    def _quick_sort(items, low, high):
        if low < high:
            # pi é o índice de partição, items[pi] está no lugar certo
            pi = partition(items, low, high)

            # Ordena recursivamente os elementos antes e depois da partição
            _quick_sort(items, low, pi - 1)
            _quick_sort(items, pi + 1, high)

    # Execução principal
    _quick_sort(arr, 0, len(arr) - 1)
    return arr

def merge_sort(arr, key=lambda x: x, reverse=False):
    if len(arr) > 1:
        mid = len(arr) // 2
        L = arr[:mid]  # Metade esquerda
        R = arr[mid:]  # Metade direita

        # Chamada recursiva em ambas as metades
        merge_sort(L, key=key, reverse=reverse)
        merge_sort(R, key=key, reverse=reverse)

        i = j = k = 0

        # Mesclagem (Merge)
        while i < len(L) and j < len(R):
            val_l = key(L[i])
            val_r = key(R[j])
            
            # Condição de comparação
            is_l_smaller = False
            if not reverse: # Ascendente
                if val_l < val_r:
                    is_l_smaller = True
            else: # Descendente
                if val_l > val_r:
                    is_l_smaller = True
                    
            if is_l_smaller:
                arr[k] = L[i]
                i += 1
            else:
                arr[k] = R[j]
                j += 1
            k += 1

        # Copia os elementos restantes de L[]
        while i < len(L):
            arr[k] = L[i]
            i += 1
            k += 1

        # Copia os elementos restantes de R[]
        while j < len(R):
            arr[k] = R[j]
            j += 1
            k += 1
            
    return arr

def heap_sort(arr, key=lambda x: x, reverse=False):
    n = len(arr)

    # 1. Função auxiliar para manter a propriedade Max-Heap (ou Min-Heap invertido)
    def heapify(items, n, i):
        root = i       # Inicializa a raiz
        left = 2 * i + 1
        right = 2 * i + 2
        
        # Define a condição de comparação
        def compare(idx1, idx2):
            val1 = key(items[idx1])
            val2 = key(items[idx2])
            
            if not reverse: # Max-Heap (para ordem ascendente)
                return val1 < val2 # Retorna True se val2 for maior (ou igual)
            else: # Min-Heap (para ordem descendente)
                return val1 > val2 # Retorna True se val2 for menor (ou igual)

        # Encontra o maior (ou menor, se reverse=True) entre a raiz e os filhos
        # Verifica o filho esquerdo
        if left < n and compare(root, left):
            root = left

        # Verifica o filho direito
        if right < n and compare(root, right):
            root = right

        # Troca se a raiz não for mais a maior (ou menor)
        if root != i:
            items[i], items[root] = items[root], items[i]
            # Chama recursivamente o heapify na subárvore afetada
            heapify(items, n, root)

    # 2. Construir o heap (reorganizar o array)
    # Começa do último nó pai e vai até a raiz
    for i in range(n // 2 - 1, -1, -1):
        heapify(arr, n, i)

    # 3. Extrair elementos um por um
    for i in range(n - 1, 0, -1):
        # Troca o elemento atual (raiz do heap) com o último elemento
        arr[i], arr[0] = arr[0], arr[i] 
        # Chama heapify na heap reduzida (excluindo o elemento extraído)
        heapify(arr, i, 0)
        
    return arr

# --- FUNÇÃO DE MEDIÇÃO E VERIFICAÇÃO ---
# Objetivo -> Medir tempo e verificar corretude
def medir_tempo_e_verificar(algoritmo, dados_originais, chave, reverso):
    # 1. Copia dos dados (fundamental para testes justos!)
    dados_para_ordenar = list(dados_originais)
    
    # 2. Medição do tempo
    inicio = time.perf_counter()
    lista_ordenada = algoritmo(dados_para_ordenar, key=chave, reverse=reverso)
    fim = time.perf_counter()
    tempo_execucao = fim - inicio
    
    # 3. Verificação de Corretude (Requisito 5)
    lista_correta = sorted(dados_originais, key=chave, reverse=reverso)
    
    # Compara apenas o atributo chave para verificar a ordenação
    chaves_ordenada = [chave(p) for p in lista_ordenada]
    chaves_correta = [chave(p) for p in lista_correta]
    
    # A verificação de corretude é crucial
    if chaves_ordenada != chaves_correta:
        print(f"\n--- ERRO: A ordenação por {algoritmo.__name__} falhou! ---")
        print(f"Primeiros 5 valores corretos: {chaves_correta[:5]}")
        print(f"Primeiros 5 valores do seu alg.: {chaves_ordenada[:5]}")
        return None
    
    return tempo_execucao

# --- Variáveis de Teste ---
algoritmos = {
    "Bubble Sort": bubble_sort,
    "Quick Sort": quick_sort,
    "Merge Sort": merge_sort,
    "Heap Sort": heap_sort,
}

# Requisito 3: Critérios de Ordenação
criterios = {
    "Preço (Asc)":         (lambda p: p.preco, False),
    "Preço (Desc)":        (lambda p: p.preco, True),
    "Avaliação (Asc)":     (lambda p: p.avaliacao, False),
    "Avaliação (Desc)":    (lambda p: p.avaliacao, True),
    "Data (Mais Recente)": (lambda p: p.data_adicao, True),
    "Data (Mais Antigo)":  (lambda p: p.data_adicao, False),
    "Categoria (Alfa)":    (lambda p: p.categoria, False),
}

# Estrutura para armazenar os resultados (Algoritmo: {Critério: Tempo})
resultados_tempos = {alg: {} for alg in algoritmos.keys()}

print("\n--- INICIANDO TESTE DE DESEMPENHO ---")
for nome_alg, alg_func in algoritmos.items():
    print(f"\nTestando {nome_alg}...")
    
    for nome_crit, (key, rev) in criterios.items():
        tempo = medir_tempo_e_verificar(alg_func, dataset_original, key, rev)
        
        if tempo is not None:
            resultados_tempos[nome_alg][nome_crit] = tempo
            # Imprime o resultado formatado
            print(f"  > {nome_crit:<20}: {tempo:.6f} segundos")

print("\n--- TESTE CONCLUÍDO ---")

# Exibição da Tabela de Resultados Finais
print("\nTABELA RESUMO DE TEMPOS DE EXECUÇÃO (em segundos):")
# Obtém a lista de nomes dos critérios para o cabeçalho
criterio_nomes = list(criterios.keys())
# Formata o cabeçalho
header = "{:<15}".format("Algoritmo") + "".join(["{:>16}".format(nome) for nome in criterio_nomes])
print(header)
print("-" * (15 + 16 * len(criterio_nomes)))

# Formata as linhas de dados
for alg, tempos in resultados_tempos.items():
    line = "{:<15}".format(alg)
    for nome_crit in criterio_nomes:
        tempo = tempos.get(nome_crit, 'N/A')
        line += "{:>16}".format(f"{tempo:.6f}" if tempo != 'N/A' else 'N/A')
    print(line)
