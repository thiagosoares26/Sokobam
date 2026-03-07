import numpy as np
import sys
import heapq
import copy

class No:
  def __init__(self, estado, no_pai=None, aresta=None, custo=0):
    self.estado = estado
    self.no_pai = no_pai
    self.aresta = aresta
    self.custo = custo

  def __lt__(self, other):
      return self.custo < other.custo


def vertice_caminho(no):
  caminho = []
  while no.no_pai is not None:
    if no.aresta is not None:
        caminho.append(no.aresta)
    no = no.no_pai
  caminho.reverse()
  return caminho

class Problema:
    def iniciar(self):
        raise NotImplementedError

    def testar_objetivo(self, no):
        raise  NotImplementedError

    def gerar_sucessores(self, no):
        raise NotImplementedError

def ler_entrada(arquivo):
    grid = []

    with open(arquivo, "r", encoding="utf-8") as f:
        for linha in f:
            grid.append(linha.strip().split())
    return grid

def extrair_elementos(grid):
    agente = None
    caixas = {}
    alvos = []

    for i in range(len(grid)):
        for j in range(len(grid[0])):
            cell = grid[i][j]

            if cell == "🙎":
                agente = (i, j)

            elif "️⃣" in cell:
                peso = int(cell[0])
                caixas[(i, j)] = peso

            elif cell == "🟢":
                alvos.append((i, j))

    return agente, caixas, alvos

class Sokoban(Problema):
    def __init__(self, grid):
        self.grid = grid
        self.linhas = len(grid)
        self.colunas = len(grid[0])
        self.agente, self.caixas, self.alvos = extrair_elementos(grid)
        self.direcoes = [
            (-1, 0, "⬆️"),
            (1, 0, "⬇️"),
            (0, -1, "⬅️"),
            (0, 1, "➡️")
        ]

    def iniciar(self):
        estado = (self.agente, tuple(self.caixas.items()), None)
        return No(estado)

    def testar_objetivo(self, no):
        agente, caixas, carregando = no.estado
        caixas = dict(caixas)

        if carregando is not None:
            return False

        return set(caixas.keys()) == set(self.alvos)

    def dentro_grid(self,x,y):
        return 0 <= x < self.linhas and 0 <= y < self.colunas

    def gerar_sucessores(self, no):
        sucessores = []
        agente, caixas, carregando = no.estado
        caixas = dict(caixas)

        for dx, dy, acao in self.direcoes:
            nx = agente[0] + dx
            ny = agente[1] + dy

            if not self.dentro_grid(nx, ny):
                continue

            if self.grid[nx][ny] == "🧱":
                continue

            custo = 1

            if carregando is not None:
                custo = 1 + carregando

            novo_estado = ((nx, ny), tuple(sorted(caixas.items())), carregando)
            sucessores.append(
                No(novo_estado, no, acao, custo)
            )

        if carregando is None and agente in caixas:
            peso = caixas[agente]
            novas_caixas = caixas.copy()
            del novas_caixas[agente]
            novo_estado = (
                agente,
                tuple(sorted(novas_caixas.items())),
                peso
            )
            sucessores.append(No(novo_estado, no, "P", 0))

        if carregando is not None and agente not in caixas:
            novas_caixas = caixas.copy()
            novas_caixas[agente] = carregando
            novo_estado = (
                agente,
                tuple(sorted(novas_caixas.items())),
                None
            )

            sucessores.append(No(novo_estado, no, "S", 0))

        return sucessores

def dijkstra(problema):
    raiz = problema.iniciar()
    fila = []
    heapq.heappush(fila, (0, raiz))
    visitados = {}

    while fila:
        custo, no = heapq.heappop(fila)

        if problema.testar_objetivo(no):
            return custo, no

        if no.estado in visitados and visitados[no.estado] <= custo:
            continue

        visitados[no.estado] = custo

        for sucessor in problema.gerar_sucessores(no):
            novo_custo = custo + sucessor.custo
            heapq.heappush(
                fila,
                (novo_custo,
                 No(
                    sucessor.estado,
                    no,
                    sucessor.aresta,
                    sucessor.custo
                 ))
            )
    return None, None

def gerar_grid_final(grid, estado):
    grid_final = copy.deepcopy(grid)
    agente, caixas, carregando = estado
    caixas = dict(caixas)

    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid_final[i][j] in ["🙎","1️⃣","2️⃣","3️⃣","4️⃣","5️⃣","6️⃣","7️⃣","8️⃣","9️⃣"]:
                grid_final[i][j] = "⚪️"

    for (x,y),peso in caixas.items():
        grid_final[x][y] = str(peso)+"️⃣"

    ax,ay = agente
    grid_final[ax][ay] = "🙎"

    return grid_final

def escrever_saida(nome, grid_final, movimentos):
    with open(nome,"w",encoding="utf-8") as f:
        f.write("Estado final\n")

        for linha in grid_final:
            f.write(" ".join(linha)+"\n")

        f.write("Movimentos\n")
        f.write("".join(movimentos)+"\n")
        f.write("Quantidades de movimentos\n")
        f.write(str(len(movimentos)))

if __name__ == "__main__":
    arquivo = sys.argv[1]
    grid = ler_entrada(arquivo)
    problema = Sokoban(grid)
    custo, no_solucao = dijkstra(problema)

    if no_solucao is None:
        print("Sem solução")
        exit()

    movimentos = vertice_caminho(no_solucao)
    grid_final = gerar_grid_final(grid, no_solucao.estado)
    escrever_saida("dijkstra.txt", grid_final, movimentos)
    print("Custo total:", custo)
    print("Movimentos:", len(movimentos))