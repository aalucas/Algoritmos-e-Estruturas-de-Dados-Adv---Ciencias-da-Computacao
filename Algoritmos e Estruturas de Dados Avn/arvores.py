class Node:
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None
        self.height = 1 # Inicialmente, o nó tem altura 1

class AVLTree:
    def __init__(self):
        self.root = None
    
    # --- Funções Auxiliares de Altura e Fator de Balanceamento ---
    
    def _get_height(self, node):
        """Retorna a altura do nó (ou 0 se for None)."""
        if not node:
            return 0
        return node.height

    def _get_balance(self, node):
        """Calcula o Fator de Balanceamento (Fb) de um nó."""
        if not node:
            return 0
        return self._get_height(node.left) - self._get_height(node.right)
    
    def _update_height(self, node):
        """Recalcula a altura do nó com base em seus filhos."""
        node.height = 1 + max(self._get_height(node.left), 
                              self._get_height(node.right))
        
    # --- Rotações para Balanceamento ---
    # --- Rotações ---
    
    def _rotate_left(self, z):
        """Rotação Simples à Esquerda (Left-Left)"""
        y = z.right
        T2 = y.left
        
        # Executa a rotação
        y.left = z
        z.right = T2
        
        # Atualiza as alturas (a ordem é importante: z antes de y)
        self._update_height(z)
        self._update_height(y)
        
        return y # Retorna a nova raiz da subárvore

    def _rotate_right(self, y):
        """Rotação Simples à Direita (Right-Right)"""
        x = y.left
        T2 = x.right
        
        # Executa a rotação
        x.right = y
        y.left = T2
        
        # Atualiza as alturas (a ordem é importante: y antes de x)
        self._update_height(y)
        self._update_height(x)
        
        return x # Retorna a nova raiz da subárvore
    
    # --- Balanceamento Geral ---
    
    def _balance_tree(self, root, key):
        """
        Verifica o Fator de Balanceamento (Fb) e executa as rotações 
        (simples ou duplas) necessárias.
        """
        self._update_height(root)
        balance = self._get_balance(root)

        # 1. Caso Left-Left (Fb > 1 e a chave inserida está na subárvore esquerda do filho esquerdo)
        if balance > 1 and key < root.left.key:
            return self._rotate_right(root)

        # 2. Caso Right-Right (Fb < -1 e a chave inserida está na subárvore direita do filho direito)
        if balance < -1 and key > root.right.key:
            return self._rotate_left(root)

        # 3. Caso Left-Right (Fb > 1 e a chave inserida está na subárvore direita do filho esquerdo)
        if balance > 1 and key > root.left.key:
            root.left = self._rotate_left(root.left) # Rotação Simples à Esquerda no filho
            return self._rotate_right(root)          # Rotação Simples à Direita na raiz

        # 4. Caso Right-Left (Fb < -1 e a chave inserida está na subárvore esquerda do filho direito)
        if balance < -1 and key < root.right.key:
            root.right = self._rotate_right(root.right) # Rotação Simples à Direita no filho
            return self._rotate_left(root)              # Rotação Simples à Esquerda na raiz

        return root
    
    # --- Inserção com Balanceamento ---
    def insert(self, key):
        """Insere um nó e garante que a AVL permaneça balanceada."""
        self.root = self._insert_node(self.root, key)
        
    def _insert_node(self, root, key):
        # 1. Caso base: Inserção de uma BST normal
        if not root:
            return Node(key)
        
        if key < root.key:
            root.left = self._insert_node(root.left, key)
        elif key > root.key:
            root.right = self._insert_node(root.right, key)
        else:
            # Chaves duplicadas não são permitidas em uma BST padrão (ou AVL)
            return root
        
        # 2. Balanceamento
        return self._balance_tree(root, key)
    

    # --- Busca ---
    def search(self, key):
        """Busca por uma chave na árvore. Complexidade O(log N)."""
        return self._search_node(self.root, key)

    def _search_node(self, root, key):
        if root is None or root.key == key:
            return root # Retorna o nó (ou None se não encontrado)
        
        if key < root.key:
            return self._search_node(root.left, key)
        else:
            return self._search_node(root.right, key)
        

    # --- Remoção com Balanceamento ---
    def get_min_value_node(self, node):
        """Função auxiliar para encontrar o nó com o menor valor na subárvore (sucessor)."""
        current = node
        while current.left is not None:
            current = current.left
        return current

    def delete(self, key):
        """Remove um nó e garante que a AVL permaneça balanceada."""
        self.root = self._delete_node(self.root, key)

    def _delete_node(self, root, key):
        # 1. BST Delete: Encontra e remove o nó
        if not root:
            return root
        
        if key < root.key:
            root.left = self._delete_node(root.left, key)
        elif key > root.key:
            root.right = self._delete_node(root.right, key)
        else: # O nó com a chave correspondente foi encontrado
            
            # Caso 1 ou 2: Nó com 0 ou 1 filho
            if root.left is None:
                temp = root.right
                root = None
                return temp
            elif root.right is None:
                temp = root.left
                root = None
                return temp
                
            # Caso 3: Nó com 2 filhos
            temp = self.get_min_value_node(root.right) # Encontra o sucessor in-order (menor na subárvore direita)
            root.key = temp.key # Copia a chave do sucessor para este nó
            
            # Deleta o sucessor in-order
            root.right = self._delete_node(root.right, temp.key)

        if root is None:
            return root
        
        # 2. Balanceamento após a remoção (mesma lógica usada na inserção)
        self._update_height(root)
        balance = self._get_balance(root)

        # Rebalanceamento: é um pouco diferente da inserção, pois o desbalanceamento
        # pode ocorrer após a remoção de *qualquer* subárvore.

        # Left-Left Case
        if balance > 1 and self._get_balance(root.left) >= 0:
            return self._rotate_right(root)

        # Left-Right Case
        if balance > 1 and self._get_balance(root.left) < 0:
            root.left = self._rotate_left(root.left)
            return self._rotate_right(root)

        # Right-Right Case
        if balance < -1 and self._get_balance(root.right) <= 0:
            return self._rotate_left(root)

        # Right-Left Case
        if balance < -1 and self._get_balance(root.right) > 0:
            root.right = self._rotate_right(root.right)
            return self._rotate_left(root)

        return root
    
    
    # --- Impressão da Árvore ---
    def inorder_traversal(self, root):
        """Imprime a árvore Inorder: Left -> Root -> Right."""
        if root:
            self.inorder_traversal(root.left)
            fb = self._get_balance(root)
            print(f"[{root.key}] (H:{root.height}, Fb:{fb})", end=" ")
            self.inorder_traversal(root.right)

    def print_tree(self):
        """Função para iniciar a impressão."""
        print("\n--- Estrutura da Árvore AVL (Inorder) ---")
        self.inorder_traversal(self.root)
        print("\n-------------------------------------------")

    # --- Validação da Propriedade AVL ---
    # --- Testes de Validação ---
if __name__ == "__main__":
    avl = AVLTree()
    
    # 1. Teste de Inserção e Rotações (caso de borda: ordem ascendente)
    print("--- Teste 1: Inserção Sequencial (Verificar Balanceamento) ---")
    keys_asc = [10, 20, 30, 40, 50, 25]
    print(f"Inserindo: {keys_asc}")
    
    for key in keys_asc:
        avl.insert(key)
        # Se for inserido 10, 20, 30, a raiz deve ser 20 (após Rotação RR em 10).
    
    # O nó 50 deve ter sido rotacionado para cima
    avl.print_tree()
    # Raiz deve ser 30 ou 40 dependendo da ordem e rotações duplas/simples

    # 2. Teste de Busca
    print("\n--- Teste 2: Busca ---")
    print(f"Busca por 40: {'Encontrado' if avl.search(40) else 'Não Encontrado'}") # Deve ser Encontrado
    print(f"Busca por 99: {'Encontrado' if avl.search(99) else 'Não Encontrado'}") # Deve ser Não Encontrado

    # 3. Teste de Remoção
    print("\n--- Teste 3: Remoção (Verificar Balanceamento) ---")
    
    # Remove uma folha
    print("Removendo 50...")
    avl.delete(50)
    avl.print_tree()

    # Remove a raiz (força a substituição e possivelmente um rebalanceamento)
    if avl.root:
        root_key = avl.root.key
        print(f"Removendo a raiz ({root_key})...")
        avl.delete(root_key)
        avl.print_tree()