import tkinter as tk
from tkinter import ttk, messagebox
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import random

# ==========================================================
# ===== 1. ÁRVORE BINÁRIA RUBRO-NEGRA (RED-BLACK TREE) =====
# ==========================================================

RED = True
BLACK = False

class NodeRB:
    def __init__(self, data, color=RED):
        self.data = data
        self.color = color
        self.parent = None
        self.left = None
        self.right = None

class RedBlackTree:
    def __init__(self):
        self.TNULL = NodeRB(0, color=BLACK)
        self.TNULL.left = None
        self.TNULL.right = None
        self.root = self.TNULL

    # --- Busca ---
    def search(self, k):
        return self._search_helper(self.root, k)

    def _search_helper(self, node, key):
        if node == self.TNULL or key == node.data:
            return node
        if key < node.data:
            return self._search_helper(node.left, key)
        return self._search_helper(node.right, key)

    # --- Rotações ---
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

    # --- Inserção ---
    def insert(self, key):
        if self.search(key) != self.TNULL:
            return False # Duplicado

        node = NodeRB(key)
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
                return False

        node.parent = y
        if y is None:
            self.root = node
        elif node.data < y.data:
            y.left = node
        else:
            y.right = node

        if node.parent is None:
            node.color = BLACK
            return True

        if node.parent.parent is None:
            return True

        self.insert_fix(node)
        return True

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

    # --- Remoção ---
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
            return False # Não encontrado

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
        return True

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

# ==========================================================
# ===== 2. ÁRVORE NÃO-BINÁRIA 2-3-4 (B-TREE ORDER 4) =====
# ==========================================================

class Node234:
    def __init__(self, is_leaf=False):
        self.keys = [] 
        self.children = []
        self.is_leaf = is_leaf

class Tree234:
    def __init__(self):
        self.root = Node234(is_leaf=True)

    # --- Busca ---
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

    # --- Inserção ---
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

    def insert(self, key):
        if self.search(key) is not None:
            return False # Duplicado

        root = self.root
        if len(root.keys) == 3:
            new_root = Node234(is_leaf=False)
            new_root.children.append(self.root)
            self.root = new_root
            self.split_child(new_root, 0)
            self._insert_non_full(new_root, key)
        else:
            self._insert_non_full(root, key)
        return True

    def _insert_non_full(self, node, key):
        i = len(node.keys) - 1
        if node.is_leaf:
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

    # --- Remoção Completa (B-Tree Logic) ---
    def delete(self, key):
        if self.search(key) is None:
            return False # Chave não existe
        
        self._delete_recursive(self.root, key)

        # Se a raiz ficar vazia após exclusões e não for folha, reduz a altura
        if len(self.root.keys) == 0 and not self.root.is_leaf:
            self.root = self.root.children[0]
        
        return True

    def _delete_recursive(self, node, key):
        idx = 0
        while idx < len(node.keys) and key > node.keys[idx]:
            idx += 1
        
        # CASO 1: A chave está neste nó
        if idx < len(node.keys) and node.keys[idx] == key:
            if node.is_leaf:
                node.keys.pop(idx)
            else:
                # Nó interno: substitui pelo predecessor ou sucessor
                child_left = node.children[idx]
                child_right = node.children[idx+1]
                
                if len(child_left.keys) >= 2:
                    pred = self._get_predecessor(child_left)
                    node.keys[idx] = pred
                    self._delete_recursive(child_left, pred)
                elif len(child_right.keys) >= 2:
                    succ = self._get_successor(child_right)
                    node.keys[idx] = succ
                    self._delete_recursive(child_right, succ)
                else:
                    # Merge (fusão)
                    self._merge(node, idx)
                    self._delete_recursive(child_left, key)
        
        # CASO 2: A chave não está neste nó
        else:
            if node.is_leaf:
                return 
            
            child = node.children[idx]
            if len(child.keys) < 2:
                self._fill_child(node, idx)
                if idx > len(node.keys):
                    idx = len(node.keys)
                    
            if idx < len(node.keys) and key > node.keys[idx]:
                idx += 1
            
            self._delete_recursive(node.children[idx], key)

    def _get_predecessor(self, node):
        curr = node
        while not curr.is_leaf:
            curr = curr.children[-1]
        return curr.keys[-1]

    def _get_successor(self, node):
        curr = node
        while not curr.is_leaf:
            curr = curr.children[0]
        return curr.keys[0]

    def _fill_child(self, parent, idx):
        if idx != 0 and len(parent.children[idx-1].keys) >= 2:
            self._borrow_from_prev(parent, idx)
        elif idx != len(parent.keys) and len(parent.children[idx+1].keys) >= 2:
            self._borrow_from_next(parent, idx)
        else:
            if idx != len(parent.keys):
                self._merge(parent, idx)
            else:
                self._merge(parent, idx-1)

    def _borrow_from_prev(self, parent, idx):
        child = parent.children[idx]
        sibling = parent.children[idx-1]
        
        child.keys.insert(0, parent.keys[idx-1])
        parent.keys[idx-1] = sibling.keys.pop()
        
        if not child.is_leaf:
            child.children.insert(0, sibling.children.pop())
            
    def _borrow_from_next(self, parent, idx):
        child = parent.children[idx]
        sibling = parent.children[idx+1]
        
        child.keys.append(parent.keys[idx])
        parent.keys[idx] = sibling.keys.pop(0)
        
        if not child.is_leaf:
            child.children.append(sibling.children.pop(0))

    def _merge(self, parent, idx):
        child = parent.children[idx]
        sibling = parent.children[idx+1]
        
        child.keys.append(parent.keys.pop(idx))
        child.keys.extend(sibling.keys)
        if not child.is_leaf:
            child.children.extend(sibling.children)
            
        parent.children.pop(idx+1)

# ==========================================================
# ===== 3. INTERFACE GRÁFICA (GUI) =====
# ==========================================================

class TreeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Visualizador de Árvores - Projeto de Grafos")
        self.root.geometry("1200x700")
        
        style = ttk.Style()
        style.theme_use('clam')
        
        self.rb_tree = RedBlackTree()
        self.tree_234 = Tree234()
        self.current_tree_type = "RB" 

        main_frame = ttk.Frame(root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        left_panel = ttk.Frame(main_frame, width=300)
        left_panel.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        
        right_panel = ttk.Frame(main_frame)
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        self.setup_controls(left_panel)
        self.setup_canvas(right_panel)

    def setup_controls(self, parent):
        lbl_tipo = ttk.Label(parent, text="Selecione a Árvore:", font=("Arial", 12, "bold"))
        lbl_tipo.pack(pady=(0, 5), anchor="w")
        
        self.tree_var = tk.StringVar(value="RB")
        rb_btn1 = ttk.Radiobutton(parent, text="Árvore Rubro-Negra", variable=self.tree_var, 
                                  value="RB", command=self.on_tree_change)
        rb_btn2 = ttk.Radiobutton(parent, text="Árvore 2-3-4", variable=self.tree_var, 
                                  value="234", command=self.on_tree_change)
        rb_btn1.pack(anchor="w")
        rb_btn2.pack(anchor="w")

        ttk.Separator(parent, orient='horizontal').pack(fill='x', pady=15)

        lbl_ops = ttk.Label(parent, text="Operações:", font=("Arial", 12, "bold"))
        lbl_ops.pack(pady=(0, 5), anchor="w")

        frame_entry = ttk.Frame(parent)
        frame_entry.pack(fill='x', pady=5)
        ttk.Label(frame_entry, text="Valor:").pack(side=tk.LEFT)
        self.entry_val = ttk.Entry(frame_entry)
        self.entry_val.pack(side=tk.LEFT, fill='x', expand=True, padx=5)

        btn_insert = ttk.Button(parent, text="Inserir", command=self.action_insert)
        btn_insert.pack(fill='x', pady=2)
        
        btn_delete = ttk.Button(parent, text="Remover", command=self.action_delete)
        btn_delete.pack(fill='x', pady=2)
        
        btn_search = ttk.Button(parent, text="Buscar", command=self.action_search)
        btn_search.pack(fill='x', pady=2)

        ttk.Separator(parent, orient='horizontal').pack(fill='x', pady=15)

        lbl_extra = ttk.Label(parent, text="Atalhos:", font=("Arial", 12, "bold"))
        lbl_extra.pack(pady=(0, 5), anchor="w")
        
        btn_populate = ttk.Button(parent, text="Gerar 21 Nós (Carga Inicial)", command=self.action_populate)
        btn_populate.pack(fill='x', pady=5)

        ttk.Label(parent, text="Log de Execução:", font=("Arial", 10, "bold")).pack(pady=(20, 0), anchor="w")
        self.log_box = tk.Text(parent, height=15, width=30, state='disabled', bg="#f0f0f0", font=("Consolas", 9))
        self.log_box.pack(fill='both', expand=True, pady=5)

    def setup_canvas(self, parent):
        self.fig = plt.Figure(figsize=(5, 5), dpi=100)
        self.ax = self.fig.add_subplot(111)
        self.ax.axis('off')

        self.canvas = FigureCanvasTkAgg(self.fig, master=parent)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    def log(self, message):
        self.log_box.config(state='normal')
        self.log_box.insert(tk.END, f"> {message}\n")
        self.log_box.see(tk.END)
        self.log_box.config(state='disabled')

    def get_value(self):
        try:
            return int(self.entry_val.get())
        except ValueError:
            messagebox.showerror("Erro", "Por favor, digite um número inteiro válido.")
            return None

    def on_tree_change(self):
        self.current_tree_type = self.tree_var.get()
        self.log(f"Trocado para {self.current_tree_type}")
        self.entry_val.delete(0, tk.END)
        self.update_plot()

    def action_populate(self):
        vals = [10, 20, 30, 15, 25, 5, 1, 50, 40, 60, 70, 65, 80, 90, 100, 12, 45, 55, 35, 6, 8]
        tree = self.rb_tree if self.current_tree_type == "RB" else self.tree_234
        
        count = 0
        for v in vals:
            if tree.insert(v):
                count += 1
        
        self.log(f"Carga inicial: inseridos {count} nós na {self.current_tree_type}.")
        self.update_plot()

    def action_insert(self):
        val = self.get_value()
        if val is None: return

        tree = self.rb_tree if self.current_tree_type == "RB" else self.tree_234
        if tree.insert(val):
            self.log(f"Inserido: {val}")
            self.entry_val.delete(0, tk.END)
            self.update_plot()
        else:
            self.log(f"Falha: {val} já existe ou erro.")

    def action_delete(self):
        val = self.get_value()
        if val is None: return
        
        tree = self.rb_tree if self.current_tree_type == "RB" else self.tree_234
        
        if tree.delete(val):
            self.log(f"Removido: {val}")
            self.update_plot()
            messagebox.showinfo("Sucesso", f"O valor {val} foi removido e a árvore foi rebalanceada.")
        else:
            self.log(f"Erro: {val} não encontrado.")
            messagebox.showwarning("Erro", f"O valor {val} não foi encontrado na árvore.")

    def action_search(self):
        val = self.get_value()
        if val is None: return
        
        if self.current_tree_type == "RB":
            res = self.rb_tree.search(val)
            if res != self.rb_tree.TNULL:
                self.log(f"Encontrado: {val} (Cor: {'Vermelho' if res.color else 'Preto'})")
                messagebox.showinfo("Busca", f"Elemento {val} encontrado!\nCor: {'VERMELHO' if res.color else 'PRETO'}")
            else:
                self.log(f"Não encontrado: {val}")
                messagebox.showwarning("Busca", "Elemento não encontrado.")
        else:
            res = self.tree_234.search(val)
            if res:
                self.log(f"Encontrado: {val} no nó {id(res[0])}")
                messagebox.showinfo("Busca", f"Elemento {val} encontrado no nó interno.")
            else:
                self.log(f"Não encontrado: {val}")

    def update_plot(self):
        self.ax.clear()
        self.ax.axis('off')
        
        if self.current_tree_type == "RB":
            self.draw_rb_tree()
        else:
            self.draw_234_tree()
            
        self.canvas.draw()

    def draw_rb_tree(self):
        G = nx.DiGraph()
        root = self.rb_tree.root
        tnull = self.rb_tree.TNULL

        if root == tnull:
            self.ax.text(0.5, 0.5, "Árvore Vazia", ha='center')
            return

        def add_edges(node):
            if node.left != tnull:
                G.add_edge(node.data, node.left.data)
                add_edges(node.left)
            if node.right != tnull:
                G.add_edge(node.data, node.right.data)
                add_edges(node.right)
            if node.left == tnull and node.right == tnull:
                pass # Folha

        add_edges(root)
        
        if len(G.nodes) == 0:
            G.add_node(root.data)

        try:
            from networkx.drawing.nx_agraph import graphviz_layout
            pos = graphviz_layout(G, prog='dot')
        except:
            pos = self.hierarchy_pos(G, root.data)

        colors = []
        for n_val in G.nodes():
            node_obj = self.rb_tree.search(n_val)
            colors.append('red' if node_obj.color else 'black')

        nx.draw(G, pos, ax=self.ax, with_labels=True, node_color=colors, 
                font_color='white', node_size=500, font_weight='bold')
        self.ax.set_title("Visualização Árvore Rubro-Negra", fontsize=14)

    def draw_234_tree(self):
        root = self.tree_234.root
        if not root.keys:
            self.ax.text(0.5, 0.5, "Árvore Vazia", ha='center')
            return

        G = nx.DiGraph()
        labels = {}

        def traverse(node, parent_id=None):
            node_id = id(node)
            lbl = " | ".join(map(str, node.keys))
            labels[node_id] = lbl
            G.add_node(node_id)
            
            if parent_id:
                G.add_edge(parent_id, node_id)
            
            if not node.is_leaf:
                for child in node.children:
                    traverse(child, node_id)

        traverse(root)
        
        pos = self.hierarchy_pos(G, id(root))

        nx.draw(G, pos, ax=self.ax, labels=labels, with_labels=True, 
                node_shape="s", node_color="skyblue", node_size=2000, 
                font_size=8, font_weight='bold')
        self.ax.set_title("Visualização Árvore 2-3-4", fontsize=14)

    def hierarchy_pos(self, G, root=None, width=1., vert_gap = 0.2, vert_loc = 0, xcenter = 0.5):
        pos = self._hierarchy_pos_impl(G, root, width, vert_gap, vert_loc, xcenter)
        return pos

    def _hierarchy_pos_impl(self, G, root, width=1., vert_gap = 0.2, vert_loc = 0, xcenter = 0.5, pos = None, parent = None):
        if pos is None:
            pos = {root:(xcenter,vert_loc)}
        else:
            pos[root] = (xcenter, vert_loc)
        children = list(G.neighbors(root))
        if not isinstance(G, nx.DiGraph) and parent is not None:
            children.remove(parent)  
        if len(children)!=0:
            dx = width/len(children) 
            nextx = xcenter - width/2 - dx/2
            for child in children:
                nextx += dx
                pos = self._hierarchy_pos_impl(G,child, width = dx, vert_gap = vert_gap, 
                                    vert_loc = vert_loc-vert_gap, xcenter=nextx,
                                    pos=pos, parent = root)
        return pos

if __name__ == "__main__":
    root = tk.Tk()
    app = TreeApp(root)
    root.mainloop()
