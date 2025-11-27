import networkx as nx
import matplotlib.pyplot as plt

# ==========================================================
# ===== 1. ÁRVORE BINÁRIA RUBRO-NEGRA (RED-BLACK TREE) =====
# ==========================================================

# --- Definições de Cores e Classe de Nó BINÁRIO ---
RED = True
BLACK = False

class Node:
    def __init__(self, data, color=RED):
        self.data = data
        self.color = color
        self.parent = None
        self.left = None
        self.right = None

class RedBlackTree:
    def __init__(self):
        # O TNULL é o nó sentinela (folhas pretas virtuais)
        self.TNULL = Node(0, color=BLACK)
        self.TNULL.left = None
        self.TNULL.right = None
        self.root = self.TNULL

    # --- Operação 1: Busca ---
    def search(self, k):
        return self._search_helper(self.root, k)

    def _search_helper(self, node, key):
        if node == self.TNULL or key == node.data:
            return node
        if key < node.data:
            return self._search_helper(node.left, key)
        return self._search_helper(node.right, key)

    # --- Auxiliares de Rotação ---
    def left_rotate(self, x):
        y = x.right
        x.right = y.left
        if y.left != self.TNULL:
            y.left.parent = x
        y.parent = x.parent
        if x.parent is None:
            self.root = y
        elif x == x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y
        y.left = x
        x.parent = y

    def right_rotate(self, x):
        y = x.left
        x.left = y.right
        if y.right != self.TNULL:
            y.right.parent = x
        y.parent = x.parent
        if x.parent is None:
            self.root = y
        elif x == x.parent.right:
            x.parent.right = y
        else:
            x.parent.left = y
        y.right = x
        x.parent = y

    # --- Operação 2: Inserção ---
    def insert(self, key):
        node = Node(key)
        node.parent = None
        node.data = key
        node.left = self.TNULL
        node.right = self.TNULL
        node.color = RED 

        y = None
        x = self.root

        while x != self.TNULL:
            y = x
            if node.data < x.data:
                x = x.left
            elif node.data > x.data:
                x = x.right
            else:
                return 

        node.parent = y
        if y is None:
            self.root = node
        elif node.data < y.data:
            y.left = node
        else:
            y.right = node

        if node.parent is None:
            node.color = BLACK
            return

        if node.parent.parent is None:
            return

        self.insert_fix(node)

    def insert_fix(self, k):
        while k.parent.color == RED:
            if k.parent == k.parent.parent.right:
                u = k.parent.parent.left 
                if u.color == RED:
                    u.color = BLACK
                    k.parent.color = BLACK
                    k.parent.parent.color = RED
                    k = k.parent.parent
                else:
                    if k == k.parent.left:
                        k = k.parent
                        self.right_rotate(k)
                    k.parent.color = BLACK
                    k.parent.parent.color = RED
                    self.left_rotate(k.parent.parent)
            else:
                u = k.parent.parent.right 
                if u.color == RED:
                    u.color = BLACK
                    k.parent.color = BLACK
                    k.parent.parent.color = RED
                    k = k.parent.parent
                else:
                    if k == k.parent.right:
                        k = k.parent
                        self.left_rotate(k)
                    k.parent.color = BLACK
                    k.parent.parent.color = RED
                    self.right_rotate(k.parent.parent)
            if k == self.root:
                break
        self.root.color = BLACK

    # --- Operação 3: Exclusão ---
    def transplant(self, u, v):
        if u.parent is None:
            self.root = v
        elif u == u.parent.left:
            u.parent.left = v
        else:
            u.parent.right = v
        v.parent = u.parent

    def minimum(self, node):
        while node.left != self.TNULL:
            node = node.left
        return node

    def delete(self, key):
        z = self.TNULL
        node = self.root
        while node != self.TNULL:
            if node.data == key:
                z = node
                break 
            if node.data <= key:
                node = node.right
            else:
                node = node.left

        if z == self.TNULL:
            print(f"Chave {key} não encontrada para exclusão.")
            return

        y = z
        y_original_color = y.color
        if z.left == self.TNULL:
            x = z.right
            self.transplant(z, z.right)
        elif z.right == self.TNULL:
            x = z.left
            self.transplant(z, z.left)
        else:
            y = self.minimum(z.right)
            y_original_color = y.color
            x = y.right
            if y.parent == z:
                x.parent = y
            else:
                self.transplant(y, y.right)
                y.right = z.right
                y.right.parent = y

            self.transplant(z, y)
            y.left = z.left
            y.left.parent = y
            y.color = z.color

        if y_original_color == BLACK:
            self.delete_fix(x)

    def delete_fix(self, x):
        while x != self.root and x.color == BLACK:
            if x == x.parent.left:
                s = x.parent.right
                if s.color == RED:
                    s.color = BLACK
                    x.parent.color = RED
                    self.left_rotate(x.parent)
                    s = x.parent.right

                if s.left.color == BLACK and s.right.color == BLACK:
                    s.color = RED
                    x = x.parent
                else:
                    if s.right.color == BLACK:
                        s.left.color = BLACK
                        s.color = RED
                        self.right_rotate(s)
                        s = x.parent.right
                    s.color = x.parent.color
                    x.parent.color = BLACK
                    s.right.color = BLACK
                    self.left_rotate(x.parent)
                    x = self.root
            else:
                s = x.parent.left
                if s.color == RED:
                    s.color = BLACK
                    x.parent.color = RED
                    self.right_rotate(x.parent)
                    s = x.parent.left

                if s.right.color == BLACK and s.left.color == BLACK:
                    s.color = RED
                    x = x.parent
                else:
                    if s.left.color == BLACK:
                        s.right.color = BLACK
                        s.color = RED
                        self.left_rotate(s)
                        s = x.parent.left
                    s.color = x.parent.color
                    x.parent.color = BLACK
                    s.left.color = BLACK
                    self.right_rotate(x.parent)
                    x = self.root
        x.color = BLACK

    # --- Plotagem Gráfica (RB) ---
    def visualize(self):
        G = nx.DiGraph()
        if self.root == self.TNULL: 
            print("Árvore vazia.")
            return
        
        def build_graph(node):
            if node != self.TNULL:
                if node.left != self.TNULL:
                    G.add_edge(node.data, node.left.data)
                    build_graph(node.left)
                if node.right != self.TNULL:
                    G.add_edge(node.data, node.right.data)
                    build_graph(node.right)
                    
        build_graph(self.root)
        
        try:
            from networkx.drawing.nx_agraph import graphviz_layout
            pos = graphviz_layout(G, prog='dot')
        except:
            pos = nx.spring_layout(G)

        final_colors = []
        for n in G.nodes():
            node_obj = self.search(n)
            final_colors.append('red' if node_obj.color == RED else 'black')

        plt.figure(figsize=(10, 6))
        nx.draw(G, pos, with_labels=True, node_color=final_colors, font_color='white', node_size=600, font_weight='bold')
        plt.title("Visualização da Árvore Rubro-Negra")
        plt.show()

# ==========================================================
# ===== 2. ÁRVORE NÃO-BINÁRIA 2-3-4 (B-TREE ORDER 4) =====
# ==========================================================

class Node234:
    """Nó para a Árvore 2-3-4, capaz de armazenar 1, 2 ou 3 chaves e até 4 filhos."""
    def __init__(self, is_leaf=False):
        self.keys = [] 
        self.children = []
        self.is_leaf = is_leaf

class Tree234:
    def __init__(self):
        self.root = Node234(is_leaf=True)

    # --- Operação 1: Busca ---
    def search(self, key):
        return self._search_helper(self.root, key)

    def _search_helper(self, node, key):
        i = 0
        while i < len(node.keys) and key > node.keys[i]:
            i += 1
        
        if i < len(node.keys) and key == node.keys[i]:
            return (node, i)
        
        elif node.is_leaf:
            return None
        
        else:
            return self._search_helper(node.children[i], key)

    # --- Auxiliar de Inserção: Split Preventivo ---
    def split_child(self, parent, index):
        node_to_split = parent.children[index]
        new_node = Node234(is_leaf=node_to_split.is_leaf)

        mid_key = node_to_split.keys[1]
        
        new_node.keys.append(node_to_split.keys[2])

        if not node_to_split.is_leaf:
            new_node.children.append(node_to_split.children[2])
            new_node.children.append(node_to_split.children[3])
            node_to_split.children = node_to_split.children[:2]

        node_to_split.keys = node_to_split.keys[:1]

        parent.children.insert(index + 1, new_node)
        parent.keys.insert(index, mid_key)

    # --- Operação 2: Inserção com Balanceamento ---
    def insert(self, key):
        root = self.root
        
        if len(root.keys) == 3:
            new_root = Node234(is_leaf=False)
            new_root.children.append(self.root)
            self.root = new_root
            self.split_child(new_root, 0)
            self._insert_non_full(new_root, key)
        else:
            self._insert_non_full(root, key)

    def _insert_non_full(self, node, key):
        i = len(node.keys) - 1
        
        if node.is_leaf:
            if key in node.keys: return # Chaves Únicas
            
            node.keys.append(None) 
            while i >= 0 and key < node.keys[i]:
                node.keys[i+1] = node.keys[i]
                i -= 1
            node.keys[i+1] = key
        
        else:
            while i >= 0 and key < node.keys[i]:
                i -= 1
            i += 1
            
            if len(node.children[i].keys) == 3:
                self.split_child(node, i)
                if key > node.keys[i]:
                    i += 1 
            
            self._insert_non_full(node.children[i], key)
            
    # --- Operação 3: Exclusão com Balanceamento ---
    def delete(self, key):
        node, idx = self._find_node_and_index(self.root, key)

        if node is None:
            print(f"Chave {key} não encontrada para exclusão.")
            return

        if not node.is_leaf:
            try:
                predecessor_key = self._get_max_key(node.children[idx])
            except IndexError:
                print("Erro: Estrutura da árvore temporariamente inválida para predecessor.")
                return 

            node.keys[idx] = predecessor_key 
            self._delete_from_node_with_fix(node.children[idx], predecessor_key)
        else:
            self._delete_from_node_with_fix(node, key)

        if len(self.root.keys) == 0 and not self.root.is_leaf and self.root.children:
            self.root = self.root.children[0]
        elif len(self.root.keys) == 0:
            self.root = Node234(is_leaf=True)

    # --- Auxiliares de Exclusão (2-3-4) ---

    def _find_parent(self, current, target):
        """Busca o nó pai do target node."""
        if current.is_leaf:
            return None
        for child in current.children:
            if child is target:
                return current
            
        for child in current.children:
            result = self._find_parent(child, target)
            if result:
                return result
        return None

    def _find_node_and_index(self, node, key):
        i = 0
        while i < len(node.keys) and key > node.keys[i]:
            i += 1
        if i < len(node.keys) and key == node.keys[i]:
            return node, i
        elif node.is_leaf:
            return None, -1
        else:
            return self._find_node_and_index(node.children[i], key)
            
    def _get_max_key(self, node):
        current = node
        while not current.is_leaf:
            current = current.children[-1]
        return current.keys[-1]
        
    def _delete_from_node_with_fix(self, node, key):
        try:
            node.keys.remove(key)
        except ValueError:
            return 
            
        if len(node.keys) < 1 and node != self.root:
            self._fix_underflow_logic(node) 

    def _fix_underflow_logic(self, node):
        """
        IMPLEMENTAÇÃO COMPLETA: Lógica de balanceamento para Underflow (Empréstimo/Fusão).
        """
        parent = self._find_parent(self.root, node)
        if not parent: return 

        try:
            idx = parent.children.index(node)
        except ValueError:
            return 
        
        print(f"\n*** Underflow Detectado no nó com {node.keys}. Balanceamento ativado. ***")

        # --- Tenta Empréstimo do Irmão Direito ---
        if idx + 1 < len(parent.children) and len(parent.children[idx + 1].keys) > 1:
            right_sibling = parent.children[idx + 1]
            
            node.keys.append(parent.keys[idx]) # Desce a chave do pai para o nó underflow
            parent.keys[idx] = right_sibling.keys.pop(0) # Sobe a chave mínima do irmão para o pai
            
            if not node.is_leaf:
                node.children.append(right_sibling.children.pop(0)) # Move o ponteiro
            
            print(f"   -> EMPRÉSTIMO DO DIREITO: Nó balanceado. Chaves do pai: {parent.keys}")
            return
            
        # --- Tenta Empréstimo do Irmão Esquerdo ---
        elif idx - 1 >= 0 and len(parent.children[idx - 1].keys) > 1:
            left_sibling = parent.children[idx - 1]
            
            node.keys.insert(0, parent.keys[idx - 1]) # Desce a chave do pai para o nó underflow
            parent.keys[idx - 1] = left_sibling.keys.pop() # Sobe a chave máxima do irmão para o pai
            
            if not node.is_leaf:
                node.children.insert(0, left_sibling.children.pop()) # Move o ponteiro
            
            print(f"   -> EMPRÉSTIMO DO ESQUERDO: Nó balanceado. Chaves do pai: {parent.keys}")
            return

        # --- Realiza Fusão (Se Empréstimo Falhar) ---
        else:
            # Preferência de fusão: Irmão Direito (se não for o último filho)
            if idx + 1 < len(parent.children):
                merge_with = parent.children[idx + 1]
                key_to_move = parent.keys.pop(idx)
                
                # O nó underflow recebe a chave do pai e todas as chaves/filhos do irmão
                node.keys.append(key_to_move)
                node.keys.extend(merge_with.keys)
                node.children.extend(merge_with.children)
                
                parent.children.pop(idx + 1) # Remove o irmão da lista de filhos do pai
                
                print(f"   -> FUSÃO (DIREITO): Fundido. Nó Pai: {parent.keys}")
                
            # Fusão com Irmão Esquerdo (se for o último filho ou se o direito não existir)
            elif idx - 1 >= 0:
                merge_with = parent.children[idx - 1]
                key_to_move = parent.keys.pop(idx - 1)
                
                # A fusão ocorre no irmão esquerdo
                merge_with.keys.append(key_to_move)
                merge_with.keys.extend(node.keys)
                merge_with.children.extend(node.children)
                
                parent.children.pop(idx) # Remove o nó underflow da lista de filhos do pai
                node = merge_with # Ajusta a referência para o nó fundido
                
                print(f"   -> FUSÃO (ESQUERDO): Fundido. Nó Pai: {parent.keys}")

            # Verifica Underflow no Pai (recursão)
            if len(parent.keys) < 1 and parent != self.root:
                self._fix_underflow_logic(parent)


    # --- Plotagem Gráfica (2-3-4) ---
    def visualize(self):
        G = nx.DiGraph()
        if not self.root.keys and self.root.is_leaf: 
            print("Árvore vazia.")
            return

        def build_graph_234(node, parent_id=None, G=None):
            node_label = " | ".join(map(str, node.keys))
            node_id = id(node)

            G.add_node(node_id, label=node_label)
            if parent_id is not None:
                G.add_edge(parent_id, node_id)

            if not node.is_leaf:
                for child in node.children:
                    build_graph_234(child, node_id, G)

        G_plot = nx.DiGraph()
        build_graph_234(self.root, G=G_plot)
        
        try:
            from networkx.drawing.nx_agraph import graphviz_layout
            pos = graphviz_layout(G_plot, prog='dot')
        except ImportError:
            pos = nx.spring_layout(G_plot)

        labels = nx.get_node_attributes(G_plot, 'label')
        
        plt.figure(figsize=(12, 8))
        nx.draw(G_plot, pos, with_labels=True, labels=labels, 
                node_color='lightcoral', node_size=1800, font_size=10, 
                font_weight='bold', edge_color='black', arrows=True)
        plt.title("Visualização da Árvore 2-3-4 (Nós: Chave | Chave)")
        plt.show()

# ==========================================================
# ===== 3. EXECUÇÃO PRINCIPAL (MAIN) ATUALIZADA =====
# ==========================================================
if __name__ == "__main__":
    
    # ------------------------------------------------
    # A. Teste da ÁRVORE RUBRO-NEGRA (Binária)
    # ------------------------------------------------
    print("\n==============================================")
    print("===== TESTE 1: ÁRVORE RUBRO-NEGRA =====")
    print("==============================================")
    rbt = RedBlackTree()
    
    elementos = [10, 20, 30, 15, 25, 5, 1, 50, 40, 60, 70, 65, 80, 90, 100, 12, 45, 55, 35, 6, 8]
    print(f"-> Inserindo {len(elementos)} elementos (min. 21).")
    for el in elementos:
        rbt.insert(el)
    
    print(f"-> Raiz: {rbt.root.data} (Cor: {'Vermelho' if rbt.root.color else 'Preto'})")

    print("\n-> Teste de Exclusão (Removendo 10 e 50)")
    rbt.delete(10)
    rbt.delete(50)
    
    print("\n--- Gerando Visualização da Árvore Rubro-Negra Final (19 Nós) ---")
    rbt.visualize() 


    # ------------------------------------------------
    # B. Teste da ÁRVORE 2-3-4 (Não-Binária)
    # ------------------------------------------------
    print("\n==============================================")
    print("===== TESTE 2: ÁRVORE 2-3-4 =====")
    print("==============================================")
    t234 = Tree234()
    
    elementos = [10, 20, 30, 40, 50, 60, 70, 80, 5, 15, 25, 35, 45, 55, 65, 75, 85, 90, 95, 2, 99]
    print(f"-> Inserindo {len(elementos)} elementos (min. 21).")
    for el in elementos:
        t234.insert(el)
        
    print(f"-> Raiz final contém: {t234.root.keys}")
    
    print("\n-> Teste de Exclusão (Tentando forçar Underflow e balanceamento)")
    # Remove elementos que geralmente causam underflow nas folhas (depende da ordem de inserção)
    t234.delete(2) 
    t234.delete(5)
    t234.delete(10)
    t234.delete(15)
    t234.delete(20)
    
    t234.visualize()