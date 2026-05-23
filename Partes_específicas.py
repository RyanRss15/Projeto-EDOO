# Ficará armazenado só as partes que precisaremos reescreever em c++(as partes importante da lógica do jogo)

# Arquivo main
import Game
from Constantes import GAME_TITLE, SCREEN_DIMENSIONS, FPS

if __name__ == '__main__':

    # ESTADOS E CLASSES DO ADMINISTRADOR DE ESTADOS
    BUNDLES = (('main menu', Game.MainMenu), ('main game', Game.MainGame), ('end screen', Game.EndScreen))

    # INICIALIZANDO O JOGO
    game = Game.Game(GAME_TITLE, SCREEN_DIMENSIONS, FPS)

    # CRIAÇÃO E INICIALIZAÇÃO DO ADMINISTRADOR DE ESTADOS
    game.gsm_init(BUNDLES, 'main menu')

    # INICIALIZAÇÃO DO JOGO
    game.run()

# Arquivo Algoritmos
import pygame
from random import shuffle
import Constantes as k

class AbstractMinefield:

    def __init__(self, size, density):
        self.size = size
        self.width, self.height = size
        self.minefield = [[] for _ in range(self.height)]
        self.minefield_mask = [[] for _ in range(self.height)]
        self.minefield_interface = [[0 for _ in range(self.width)] for _ in range(self.height)]
        self.tiles = self.width * self.height
        self.bombs = int(self.tiles * density)
        self.free_tiles = self.tiles - self.bombs
        self.discovered_tiles = 0
        self.win = False
        self.first_dig = True

    def fill_minefield(self):
        # PREENCHE UMA LISTA COM ESPAÇOS LIVRES (0) E BOMBAS (1)
        shallow_minefield = self.free_tiles * [0] + self.bombs * [1]

        # EMBARALHA-SE A LISTA
        shuffle(shallow_minefield)

        # TRANSFORMA-SE A LISTA EM UMA MATRIZ BIDIMENSIONAL
        self.minefield = [[] for _ in range(self.height)]
        for i in range(self.height):
            for j in range(self.width):
                self.minefield[i].append(shallow_minefield[i * self.height + j])

    # CONTA QUANTAS BOMBAS HÁ AO REDOR DE UM LADRILHO
    def count_tile(self, tile):
        i_tile, j_tile = tile
        count = 0
        for i, j in ((-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)):
            if self.height > i_tile + i >= 0 and self.width > j_tile + j >= 0 and self.minefield[i_tile + i][j_tile + j]:
                count += 1
        self.minefield_mask[i_tile].append(count)

    # FAZ A CONTAGEM DE BOMBAS PARA CADA LADRILHO NO CAMPO MINADO
    def count_all(self):
        for i in range(self.height):
            for j in range(self.width):
                self.count_tile((i, j))

    # REVELA UM LADRILHO NO CAMPO MINADO
    def dig(self, tile, primary_dig=True):

        # COORDENADAS DO LADRILHO
        i_tile, j_tile = tile

        # SÓ REVELA O LADRILHO SE NÃO HOUVER UMA BANDEIRA
        if not (self.minefield_interface[i_tile][j_tile] == 2 and primary_dig):

            # É IMPOSSÍVEL ERRAR NA PRIMEIRA ESCAVAÇÃO
            if self.first_dig:
                self.first_dig = False

                # A PRIMEIRA ESCAVAÇÃO ACERTOU UMA BOMBA
                if self.minefield[i_tile][j_tile]:
                    self.minefield[i_tile][j_tile] = 0
                    self.minefield_interface[i_tile][j_tile] = 1
                    self.bombs -= 1
                    self.free_tiles += 1
                    self.discovered_tiles += 1
                    post_event = pygame.event.Event(k.MINESWEEPER_HIT, {'coordinates': (i_tile, j_tile)})
                    pygame.event.post(post_event)
                    self.count_all()

                # A PRIMEIRA ESCAVAÇÃO ACERTOU UM LADRILHO LIVRE
                else:
                    self.count_all()
                    self.minefield_interface[i_tile][j_tile] = 1
                    self.discovered_tiles += 1
                    post_event = pygame.event.Event(k.MINESWEEPER_HIT, {'coordinates': (i_tile, j_tile)})
                    pygame.event.post(post_event)

                # A ESCAVAÇÃO NÃO FOI REALIZADA PELA CASCATA DE ESCAVAÇÃO
                if primary_dig:
                    post_event = pygame.event.Event(k.MINESWEEPER_PRIMARY_HIT, {'coordinates': (i_tile, j_tile)})
                    pygame.event.post(post_event)

                # OS LADRILHOS AO REDOR SERÃO ESCAVADOS CASO NÃO HAJAM BOMBAS POR PERTO
                for i, j in ((-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)):
                    if self.height > i_tile + i >= 0 and self.width > j_tile + j >= 0 and self.minefield_interface[i_tile + i][j_tile + j] != 1 and not self.minefield_mask[i_tile][j_tile]:
                        self.dig((i_tile + i, j_tile + j), False)

            # ACERTOU UMA MINA SEM SER A PRIMEIRA ESCAVAÇÃO
            elif self.minefield[i_tile][j_tile] and self.minefield_interface[i_tile][j_tile] != 3:
                self.minefield_interface[i_tile][j_tile] = 3
                post_event = pygame.event.Event(k.MINESWEEPER_MISS, {'coordinates': (i_tile, j_tile)})
                pygame.event.post(post_event)

            # REVELOU UM LADRILHO SEM SER A PRIMEIRA ESCAVAÇÃO
            elif self.minefield_interface[i_tile][j_tile] in (0, 2) and not self.minefield[i_tile][j_tile]:
                if primary_dig:
                    post_event = pygame.event.Event(k.MINESWEEPER_PRIMARY_HIT, {'coordinates': (i_tile, j_tile)})
                    pygame.event.post(post_event)
                self.minefield_interface[i_tile][j_tile] = 1
                self.discovered_tiles += 1
                post_event = pygame.event.Event(k.MINESWEEPER_HIT, {'coordinates': (i_tile, j_tile)})
                pygame.event.post(post_event)
                for i, j in ((-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)):
                    if self.height > i_tile + i >= 0 and self.width > j_tile + j >= 0 and self.minefield_interface[i_tile + i][j_tile + j] != 1 and not self.minefield_mask[i_tile][j_tile]:
                        self.dig((i_tile + i, j_tile + j), False)

    # INSERE UMA BANDEIRA NO CAMPO MINADO
    def flag(self, tile):
        i_tile, j_tile = tile
        view = self.minefield_interface[i_tile][j_tile]
        if view == 0:
            self.minefield_interface[i_tile][j_tile] = 2
            post_event = pygame.event.Event(k.MINESWEEPER_FLAG, {'coordinates': (i_tile, j_tile)})
            pygame.event.post(post_event)
        elif view == 2:
            self.minefield_interface[i_tile][j_tile] = 0
            post_event = pygame.event.Event(k.MINESWEEPER_UNFLAG, {'coordinates': (i_tile, j_tile)})
            pygame.event.post(post_event)

    # VERIFICA SE O CAMPO MINADO FOI COMPLETAMENTE LIMPO
    def win_check(self):
        if not self.win and self.discovered_tiles == self.free_tiles:
            self.win = True
            post_event = pygame.event.Event(k.MINESWEEPER_WIN)
            pygame.event.post(post_event)

#Aquivo Others

# UM TIMER QUE CONTA ATÉ ZERO
class Timer:

    def __init__(self):
        self.start_time = None
        self.time_limit = None
        self.current_time = None
        self.activated = False

    # PREPARA O TIMER COM UM DADO TEMPO EM SEGUNDOS
    def set_timer_seconds(self, time):
        self.start_time = time * 1000

    # ADICIONA TEMPO AO TIMER
    def add_time_seconds(self, time):
        self.time_limit += time * 1000

    def get_current_time_seconds(self):
        if self.activated:
            return self.current_time // 1000

    # ATIVA O TIMER
    def activate(self):
        self.activated = True
        self.time_limit = self.start_time + pygame.time.get_ticks()
        self.current_time = self.start_time

    # CHECA SE O TIMER ATINGIU O LIMITE DE TEMPO
    def ring(self):
        if self.activated:
            if self.current_time > 0:
                self.current_time = self.time_limit - pygame.time.get_ticks()
                return False
            else:
                self.activated = False
                self.current_time = 0
                return True

#Arquivo Constantes
# CALCULAR NOTA DO PLAYER
def score_grade(score):
    if score < 2000:
        return 'a'
    elif score < 4000:
        return 'b'
    elif score < 8000:
        return 'c'
    elif score < 16000:
        return 'd'
    elif score < 32000:
        return 'e'
    else:
        return 'f'

# DEFINIÇÕES DO CAMPO MINADO ABSTRATO
ABSTRACT_MINEFIELD_SIZE = (10, 10)
ABSTRACT_MINEFIELD_DENSITY = 0.12

# PROPORÇÕES DO CAMPO MINADO
MINEFIELD_SIZE = set_proportion((16/9), 1)
MINEFIELD_POSITION = set_proportion(4.5714, 10000)

# TEMPO LIMITE DE JOGO
TIME_LIMIT_SECONDS = 60

# TAMANHO DAS BANDEIRAS E DAS BOMBAS
SIZE_FLAGS = set_proportion(9.6, 5.4)
SIZE_BOMBS = set_proportion(9.6, 5.4)

  
