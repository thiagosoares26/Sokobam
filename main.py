import numpy as np

class No:
  def __init__(self, estado, no_pai=None, aresta=None):
    self.estado = estado
    self.no_pai = no_pai
    self.aresta = aresta

  def __repr__(self):
    return str(self.estado)

def no_caminho(no):
  caminho = [no.estado]
  while no.no_pai is not None:
    caminho.append(no.estado)
    no = no.no_pai
  caminho.reverse()
  return caminho

def vertice_caminho(no):
  caminho = []
  while no.no_pai is not None:
    if no.aresta is not None: caminho.append(no.aresta)
    no = no.no_pai
  caminho.reverse()
  return caminho

class Visitados:
  def __init__(self):
    self.visitados = set({})

  def adicionar(self, no):
    self.visitados.add(tuple(no.estado))

  def foi_visitado(self, no):
    return tuple(no.estado) in self.visitados

  def tamanho(self):
    return len(self.visitados)

  # Breadth-First Search - Busca em Largura
def bfs(problema):
    no = problema.iniciar()

    fila = Fila()
    fila.push(no)

    visitados = Visitados()

    while not fila.esta_vazio():
        no = fila.pop()
        visitados.adicionar(no)

          # faz o teste objetivo. Se chegou no resultado final
          # retorna o No correspondente
        if (problema.testar_objetivo(no)):
            return (visitados.tamanho(), no)

          # função sucessores define os Nós sucessores
        nos_sucessores = problema.gerar_sucessores(no)

          # para cada sucessor, se armazena se ainda não visitado
        for no_sucessor in nos_sucessores:
              # pula estado_filho se já foi expandido
            if not visitados.foi_visitado(no_sucessor): fila.push(no_sucessor)

    return (visitados.tamanho(), None)

class Fila:
    def __init__(self):
        self.fila = []

    def push(self, item):
        self.fila.append(item)

    def pop(self):
        if (self.esta_vazio()):
            return None
        else:
            return self.fila.pop(0)

    def esta_vazio(self):
        return len(self.fila) == 0

def dfs(problema):
  no = problema.iniciar()

  pilha = Pilha()
  pilha.push(no)

  visitados = Visitados()
  visitados.adicionar(no)

  while not pilha.esta_vazio():
    no = pilha.pop()
    visitados.adicionar(no)

    # faz o teste objetivo. Se chegou no resultado final
    # retorna o No correspondente
    resultado = problema.testar_objetivo(no)
    if(resultado):
      return (visitados.tamanho(), no)

    # função sucessores define os Nós sucessores
    nos_sucessores = problema.gerar_sucessores(no)

    # para cada sucessor, se armazena se ainda não visitado
    for no_sucessor in nos_sucessores:
      # pula estado_filho se já foi expandido
      if not visitados.foi_visitado(no_sucessor):
        pilha.push(no_sucessor)

  return (visitados.tamanho(), None)

class Pilha:
  def __init__(self):
    self.pilha = []

  def push(self, item):
    self.pilha.append(item)

  def pop(self):
    if(self.esta_vazio()):
      return None
    else:
      return self.pilha.pop()

  def esta_vazio(self):
    return len(self.pilha) == 0

  def tamanho(self):
    return len(self.pilha)

class Problema:
  # Função auxiliar para imprimir
  # deve retornar o nó raiz
  def iniciar(self):
     raise NotImplementedError

  # Função auxiliar para imprimir
  # deve retornar uma string de como
  # imprimir cada estado
  def imprimir(self, no):
    estado = no.estado
    return estado

  # Função booleana que verifica se o estado atual
  # é o estado objetivo do problema
  def testar_objetivo(self, no):
    raise NotImplementedError

  # Função que gera os sucessores válidos
  # a partir de um estado válido
  # deve retornar uma lista de nós sucessores
  def gerar_sucessores(self, no):
    raise NotImplementedError

import copy
class BracoRobotico:
  # Função auxiliar para imprimir
  # deve retornar o nó raiz
  def iniciar(self):
    self.estado_inicial = [0, None, 10, 20, 15, None, None, None]
    self.no_raiz = No(self.estado_inicial)
    return self.no_raiz

  # Função auxiliar para imprimir
  # deve retornar uma string de como
  # imprimir cada estado
  def imprimir(self, no):
    return f"Posição do braço: {no.estado[0]}\nCaixa no braço: {no.estado[1]}\nPosicoes no braço: {no.estado[2:]}"

  # Função auxiliar para imprimir
  # deve retornar uma string de como
  # imprimir cada estado
  # def imprimir(self, no):
  #   estado = no.estado
  #   return estado

  # Função booleana que verifica se o estado atual
  # é o estado objetivo do problema
  def testar_objetivo(self, no):
    estado = no.estado
    if estado[1] is not None: return False # se o braço tem uma caixa

    i = 2
    # verifica se todos os itens estão em ordem
    while estado[i] is not None and estado[i+1] is not None:
      if estado[i] > estado[i+1]: return False
      i += 1

    # verifica se o restante é nulo (não há caixas)
    i += 1
    final = len(estado) - 1
    while i <= final:
      if estado[i] is not None: return False
      i += 1

    return True

  # Função que gera os sucessores válidos
  # a partir de um estado válido
  # deve retornar uma lista de nós sucessores
  def gerar_sucessores(self, no):
    nos_sucessores = []
    posicao = no.estado[0]
    i = 2 # espaços começam aqui no array
    while(i < 8):
      index_braco = i - 2
      if posicao != index_braco: # não está onde o braço está
        novo_estado = copy.copy(no.estado)
        novo_estado[0] = index_braco
        nos_sucessores.append(No(novo_estado, no, f"M{index_braco}"))
      i += 1

    # verifica o Pega
    if no.estado[1] is None: # verifica se braço está vazio
      novo_estado = copy.copy(no.estado)
      indice = novo_estado[0] + 2 # onde o braço está
      braco = novo_estado[1] # o que o braço está carregando
      espaco_com_caixa = novo_estado[indice] # espaço com caixa
      if espaco_com_caixa is not None: # sem tem caixa lá
        novo_estado[1] = espaco_com_caixa # braço pega a caixa
        novo_estado[indice] = None # retira caixa do local
        nos_sucessores.append(No(novo_estado, no, f"P{indice - 2}"))

    # verifica o solta
    if no.estado[1] is not None: # verifica se há algo no braço
      novo_estado = copy.copy(no.estado)
      indice = novo_estado[0] + 2 # onde o braço está
      braco = novo_estado[1] # o que o braço está carregando
      espaco_com_caixa = novo_estado[indice] # espaço com caixa
      if espaco_com_caixa is None: # espaço precisa estar vazio
        novo_estado[indice] = braco # solta
        novo_estado[1] = None # braço fica vazio
        nos_sucessores.append(No(novo_estado, no, f"S{indice - 2}"))

    return nos_sucessores

if __name__ == "__main__":
  problema = BracoRobotico()
  no_raiz = problema.iniciar()
  print(problema.imprimir(no_raiz))
  raiz = problema.iniciar()

  (qtd_estados_visitados, no_solucao) = dfs(problema)
 # (qtd_estados_visitados, no_solucao) = bfs(problema)

  if(no_solucao is None):
    print("Não houve solução ao problema")
  else:
    #caminho = no_caminho(no_solucao)
    caminho = vertice_caminho(no_solucao)
    print("Solução:")
    print(caminho)
  print(f"Transições: {len(caminho)}")
  print(f"Estados visitados: {qtd_estados_visitados}")
  print("Estado Inicial:")
  print(problema.imprimir(no_solucao))