# Resolução EP1 - Sokoban

## Descrição do Problema

Este projeto implementa a resolução de um problema inspirado no jogo **Sokoban** utilizando três algoritmos de busca:

* **Dijkstra**
* **Busca Gananciosa (Greedy)**
* **A * (a_estrela)**

O objetivo do problema é mover caixas com pesos diferentes até posições alvo em um grid.

---

# Representação do Ambiente

O ambiente é representado por um **grid bidimensional** lido a partir de um arquivo `entrada.txt`.

Cada posição do grid pode ter:

| Símbolo         | Significado     |
| --------------- | --------------- |
| 🙎              | robo          |
| ⚪               | espaço livre    |
| 🧱              | parede          |
| 🟢              | posição alvo    |
| 1️⃣ 2️⃣ 3️⃣ ... | caixas com peso |

Exemplo de grid inicial:

```
🙎 ⚪ ⚪ ⚪ ⚪
🟢 📦 📦 ⚪ 8️⃣
⚪ ⚪ 📦 ⚪ ⚪
⚪ ⚪ 📦 ⚪ ⚪
⚪ 🟢 ⚪ ⚪ ⚪
```

---

# Representação dos Estados

Cada estado do problema é representado por uma tupla:

```
(agente, caixas, carregando)
```

Onde:

* **agente** → posição `(linha, coluna)`
* **caixas** → posições das caixas e seus pesos
* **carregando** → peso da caixa que o agente está carregando (ou `None`, caso não esteja carregando nada)

Exemplo:

```
((1,2), [((2,3),2),((3,1),1)], None)
```

Isso indica que:

* o agente está na posição `(1,2)`
* existem duas caixas
* o agente não está carregando nenhuma caixa
  
---

# Função Sucessora

A função sucessora é implementada no método:

```
gerar_sucessores()
```

Ela gera todos os estados possíveis a partir do estado atual.

## Movimentos possíveis

O agente pode se mover em quatro direções:

* ⬆️ cima
* ⬇️ baixo
* ⬅️ esquerda
* ➡️ direita

Um movimento só é permitido se:

* estiver dentro do grid
* não for uma parede

---

## Pegar caixa

Se o agente estiver na mesma posição de uma caixa e não estiver carregando nenhuma, ele pode executar a ação:

```
P
```

Essa ação remove a caixa do chão e o agente passa a carregá-la.

---

## Soltar caixa

Se o agente estiver carregando uma caixa e a posição atual não possuir outra caixa, ele pode executar:

```
S
```

Essa ação coloca a caixa no chão.

---

# Função Objetivo

A função objetivo verifica se todas as caixas estão nas posições alvo.

Ela é implementada em:

```
testar_objetivo()
```

A condição de sucesso é:

* todas as caixas devem estar nas posições alvo
* o agente não pode estar carregando nenhuma caixa.

Formalmente:

```
set(caixas.keys()) == set(alvos)
```

---

# Cálculo de Custo

O custo das ações depende da situação do agente.

### Movimento sem carregar caixa

```
custo = 1
```

### Movimento carregando caixa

```
custo = 1 + peso_da_caixa
```

Isso faz com que transportar caixas mais pesadas seja mais caro.

---

### Pegar ou soltar caixa

As ações:

* **P** (pegar caixa)
* **S** (soltar caixa)

possuem custo:

```
cucsto =0
```

---

# Função Heurística

A heurística utilizada é baseada na **distância de Manhattan** entre caixas e alvos.

Para cada caixa é calculada a distância até o alvo mais próximo:

```
|x_caixa - x_objetivo| + |y_caixa - y_objetivo|
```

A heurística total é a soma dessas distâncias.

Se o agente estiver carregando uma caixa, também é considerada a distância entre o agente e o alvo mais próximo.

---

# Admissibilidade da Heurística

A heurística é **admissível** porque a distância de Manhattan nunca superestima o custo real necessário para levar uma caixa até um alvo.

Isso ocorre porque:

* o agente só pode mover caixas em direções horizontais ou verticais
* cada movimento possui custo mínimo positivo

Portanto a heurística sempre fornece um valor menor ou igual ao custo real da solução.

Isso garante que o algoritmo **A*** encontre soluções ótimas.

---

# Algoritmos Utilizados

## Dijkstra

O algoritmo de Dijkstra expande os nós com base no **menor custo acumulado**.

Ele utiliza uma **fila de prioridade (heap)** para selecionar o próximo estado a ser explorado.

Esse algoritmo garante encontrar o caminho de menor custo, porém pode explorar muitos estados.

---

## Busca Gananciosa

A busca gananciosa utiliza apenas o valor da heurística para decidir qual nó expandir.

Ou seja, ela escolhe sempre o estado que parece mais próximo da solução.

Esse método costuma ser mais rápido, mas **não garante solução ótima**.

---

## A*

O algoritmo A* combina:

* custo acumulado `g(n)`
* heurística `h(n)`

Utilizando a função:

```
f(n) = g(n) + h(n)
```

Isso permite encontrar soluções ótimas explorando menos estados que Dijkstra.

---

# Arquivos de Saída

Cada algoritmo gera um arquivo de saída contendo:

* estado final do grid
* sequência de movimentos
* quantidade de movimentos

Arquivos gerados:

```
dijkstra.txt
ganancioso.txt
a_estrela.txt
```

---

# Resultados Obtidos a partir da entrada.txt (5x5)

## Dijkstra

Quantidade de movimentos:

```
25
```

---

## Busca Gananciosa

Quantidade de movimentos:

```
29
```

---

## A*

Quantidade de movimentos:

```
25
```

---

# Conclusão

Os resultados mostram que:

* **Dijkstra** encontra soluções ótimas, mas explora mais estados.
* **Busca Gananciosa** encontra soluções mais rapidamente, porém nem sempre ótimas.
* **A*** combina heurística e custo acumulado, encontrando soluções ótimas de forma mais eficiente.

Assim, o algoritmo **A*** apresenta o melhor equilíbrio entre qualidade da solução e desempenho.

# Estudo de caso grids(8, 16, 24 e 64)
# Estudo de caso grids(8, 16, 24 e 64)

## Grid 8x8(arquivo entrada_8x8.txt)

### Dijkstra
Custo total (Dijkstra): 127
Movimentos (Dijkstra): 37

### Ganancioso
Custo total (Ganancioso): 161
Movimentos (Ganancioso): 55

### A*
Custo total: 127
Movimentos: 37

## Grid 16x16(arquivo entrada_16x16.txt)

### Dijkstra
Custo total (Dijkstra): 333
Movimentos (Dijkstra): 80

### Ganancioso
Custo total (Ganancioso): 360
Movimentos (Ganancioso): 85

### A*
Custo total: 333
Movimentos: 80

## Grid 24x24(arquivo entrada_24x24.txt)

### Dijkstra
Custo total (Dijkstra): 593
Movimentos (Dijkstra): 131

### Ganancioso
Custo total (Ganancioso): 640
Movimentos (Ganancioso): 140

### A*
Custo total: 593
Movimentos: 131

## Grid 64x64(arquivo entrada_64x64.txt)

### Dijkstra
Custo total (Dijkstra): 1420
Movimentos (Dijkstra): 290

### Ganancioso
Custo total (Ganancioso): 1550
Movimentos (Ganancioso): 310

### A*
Custo total: 1420
Movimentos: 290
