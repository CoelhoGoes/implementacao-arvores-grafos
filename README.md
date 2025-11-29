# Implementação e Visualização de Árvores e Grafos

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

Projeto acadêmico desenvolvido para a disciplina de **Algoritmos e Estruturas de Dados**, focado na implementação e visualização interativa de estruturas de dados avançadas: **Árvore Rubro-Negra** e **Árvore 2-3-4**.

## 📋 Índice

- [Sobre o Projeto](#-sobre-o-projeto)
- [Estruturas Implementadas](#-estruturas-implementadas)
- [Recursos](#-recursos)
- [Instalação](#-instalação)
- [Como Usar](#-como-usar)
- [Exemplos](#-exemplos)
- [Documentação](#-documentação)
- [Tecnologias](#️-tecnologias)
- [Autores](#-autores)

## 🎯 Sobre o Projeto

Este projeto implementa do zero (sem bibliotecas prontas) duas estruturas de dados fundamentais em Ciência da Computação:

1. **Árvore Rubro-Negra (Red-Black Tree)** - Árvore binária de busca auto-balanceada
2. **Árvore 2-3-4** - Árvore de busca não-binária (B-Tree de ordem 4)

O projeto inclui:

- ✅ Implementação completa das estruturas com todas as operações (inserção, remoção, busca)
- ✅ Interface gráfica (GUI) para visualização interativa em tempo real
- ✅ Código totalmente comentado em português
- ✅ Sistema de log para acompanhamento das operações

## 🌳 Estruturas Implementadas

### Árvore Rubro-Negra (Red-Black Tree)

Árvore binária de busca balanceada que mantém as seguintes propriedades:

- Cada nó é vermelho ou preto
- A raiz é sempre preta
- Nós folhas (NIL/TNULL) são pretos
- Nós vermelhos têm apenas filhos pretos
- Todos os caminhos da raiz até as folhas contêm o mesmo número de nós pretos

**Complexidade:**

- Busca: O(log n)
- Inserção: O(log n)
- Remoção: O(log n)

### Árvore 2-3-4

Árvore de busca não-binária onde cada nó pode ter:

- 1 chave e 2 filhos (nó 2)
- 2 chaves e 3 filhos (nó 3)
- 3 chaves e 4 filhos (nó 4)

Todas as folhas estão no mesmo nível, garantindo balanceamento perfeito.

**Complexidade:**

- Busca: O(log n)
- Inserção: O(log n)
- Remoção: O(log n)

## 🚀 Recursos

### Interface Gráfica (`grafosRBe234.py`)

- **Seleção de Árvore**: Alterne entre Rubro-Negra e 2-3-4
- **Operações Interativas**:
  - Inserir valores
  - Remover valores
  - Buscar elementos
- **Visualização Dinâmica**: Atualização em tempo real da estrutura
- **Log de Execução**: Acompanhe todas as operações realizadas
- **Carga Inicial**: Botão para popular com 21 nós para testes rápidos
- **Cores Personalizadas**: Visualização clara com nós vermelhos/pretos (RB) e nós organizados (2-3-4)

## 📦 Instalação

### Pré-requisitos

- Python 3.8 ou superior
- pip (gerenciador de pacotes Python)

### Passos

1. **Clone o repositório:**

   ```bash
   git clone https://github.com/CoelhoGoes/implementacao-arvores-grafos.git
   cd implementacao-arvores-grafos
   ```

2. **Instale as dependências:**

```bash
pip install networkx matplotlib
```

**Nota:** O Tkinter já vem pré-instalado com Python. Se não estiver disponível:

```bash
# Windows: reinstale o Python marcando a opção "tcl/tk and IDLE"
# Linux/Ubuntu:
sudo apt-get install python3-tk
# macOS:
brew install python-tk
```

## 💻 Como Usar

### Executando a Interface Gráfica

```bash
python grafosRBe234.py
```

**Instruções:**

1. Selecione o tipo de árvore (Rubro-Negra ou 2-3-4)
2. Digite um valor no campo "Valor"
3. Clique em **Inserir**, **Remover** ou **Buscar**
4. Observe a visualização atualizar automaticamente
5. Use "Gerar 21 Nós" para teste rápido
6. Acompanhe as operações no log em tempo real

## 📊 Exemplos

### Exemplo 1: Inserção Básica (Python)

```python
from grafosRBe234 import RedBlackTree

# Criar árvore
rbt = RedBlackTree()

# Inserir valores
valores = [20, 15, 25, 10, 5, 1, 30]
for v in valores:
    rbt.insert(v)

# Buscar elemento
resultado = rbt.search(15)
if resultado != rbt.TNULL:
    print(f"Encontrado! Cor: {'Vermelho' if resultado.color else 'Preto'}")
```

### Exemplo 2: Árvore 2-3-4

```python
from grafosRBe234 import Tree234

# Criar árvore
tree = Tree234()

# Inserir valores
valores = [10, 20, 30, 15, 25, 5]
for v in valores:
    tree.insert(v)

# Buscar elemento
resultado = tree.search(25)
if resultado:
    print(f"Elemento 25 encontrado no nó {id(resultado[0])}")
```

### Exemplo 3: Remoção com Rebalanceamento

```python
# Remover elemento e rebalancear automaticamente
rbt.delete(15)
print("Árvore rebalanceada após remoção!")
```

## 📚 Documentação

### Estrutura do Projeto

```text
implementacao-arvores-grafos/
│
├── grafosRBe234.py              # Aplicação principal (GUI + implementações)
├── README.md                    # Este arquivo
└── .gitignore
```

### Principais Classes

#### `RedBlackTree`

- `insert(key)` - Insere um valor na árvore
- `delete(key)` - Remove um valor da árvore
- `search(key)` - Busca um valor na árvore
- `left_rotate(x)` - Rotação à esquerda
- `right_rotate(x)` - Rotação à direita

#### `Tree234`

- `insert(key)` - Insere um valor na árvore
- `delete(key)` - Remove um valor da árvore
- `search(key)` - Busca um valor na árvore
- `split_child(parent, index)` - Divide nó cheio

## 🛠️ Tecnologias

- **Python 3.8+** - Linguagem principal
- **Tkinter** - Interface gráfica nativa do Python
- **NetworkX** - Representação e manipulação de grafos
- **Matplotlib** - Visualização dinâmica das estruturas de árvores

## 👨‍💻 Autores

### Gabriel Góes

- GitHub: [@CoelhoGoes](https://github.com/CoelhoGoes)

### Cauê Barroso

- GitHub: [@cauebarroso](https://github.com/cauebarroso)

### Bernardo Lins

- GitHub: [@Bernard0Lins](https://github.com/Bernard0Lins)

## 📝 Licença

Este projeto foi desenvolvido para fins educacionais como parte da disciplina de Algoritmos e Estruturas de Dados.

---

⭐ Se este projeto foi útil para você, considere dar uma estrela no repositório!
