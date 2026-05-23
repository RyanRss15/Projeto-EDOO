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

#Aquivo game
# PARTE LÓGICA DO CAMPO MINADO
ABSTRACT_MINEFIELD = Algoritmos.AbstractMinefield(k.ABSTRACT_MINEFIELD_SIZE, k.ABSTRACT_MINEFIELD_DENSITY)

# PREENCHENDO CAMPO MINADO
MINEFIELD.fill_matrix()

# COMEÇO DO JOGO
GAME_START_VALUE = [None]

# DIÁLOGO DE PAUSE
PAUSE_DIALOGUE = FUZZY_BUBBLES_60.render('PRESSIONE ESC PARA RETORNAR AO JOGO', True, k.COLOR_WHITE)

# TIMER DO JOGO
GAME_TIMER = Others.Timer()

# TIMER DE DISPONIBILIDADE DOS LADRILHOS
AVAILABLE_TILE_TIMER = Others.Timer()

# PONTUAÇÃO PARA CONTAR NA TELA FINAL
COUNTING_SCORE = [0]

# PONTUAÇÃO FINAL
FINAL_SCORE = []
 def gsm_init(self, bundles, first_state):
        # INICIALIZANDO O GERENCIADOR DE ESTADOS
        self.gsm = GameStateManager()

        # CRIANDO ESTADOS
        for state_bundle in bundles:
            self.gsm.create_state(state_bundle)

        # ASSOCIANDO BOTÕES
        TO_MAIN_GAME_BUTTON.gsm = self.gsm

        # SELECIONANDO O PRIMEIRO ESTADO
        self.gsm.set_state(first_state)
        # GERAÇÃO ALEATÓRIA DE COLETÁVEIS
                    if randint(1, k.RNG_LIFE_COLLECTABLE) == 1:
                        LIFE_COLLECTABLE.generate((tile_x + tile_x_size * 0.5 - life_x_size * 0.5, tile_y + tile_y_size * 0.5 - life_y_size * 0.5), PURGATORY, 2)
                    if randint(1, k.RNG_TIME_COLLECTABLE) == 1:
                        TIME_COLLECTABLE.generate((tile_x + tile_x_size * 0.5 - life_x_size * 0.5, tile_y + tile_y_size * 0.5 - life_y_size * 0.5), PURGATORY, 2)
                    if randint(1, k.RNG_FLAG_COLLECTABLE) == 1:
                        FLAG_COLLECTABLE.generate((tile_x + tile_x_size * 0.5 - life_x_size * 0.5, tile_y + tile_y_size * 0.5 - life_y_size * 0.5), PURGATORY, 2)

                # ACERTOU UMA BOMBA NO CAMPO MINADO
                if event.type == k.MINESWEEPER_MISS:
                    tile_x, tile_y = event.coordinates
                    generation_tile = MINEFIELD.button_matrix[tile_x][tile_y]
                    tile_x, tile_y = generation_tile.rect.center
                    bomb_x_size, bomb_y_size = BOMB_OBJECT.rect.size

                    # GERA A BOMBA
                    BOMB_OBJECT.generate((tile_x - bomb_x_size // 2, tile_y - bomb_y_size // 1.3), PURGATORY, 0)
                # PLANTOU UMA BANDEIRA NO CAMPO MINADO
                if event.type == k.MINESWEEPER_FLAG:
                    SFX_STORAGE['FLAG'].play()
                    MIAUSMA_REACTS.set_animation(MIAUSMA_REACTS_BASE[0], k.MIAUSMA_REACT_POSITION, 3)
                    MIAUSMA.flag_down(1)
                    if not GAME_START_VALUE:
                        MIAUSMA.score_points(5)
         # REMOVEU UMA BANDEIRA DO CAMPO MINADO
                if event.type == k.MINESWEEPER_UNFLAG:

                    placed_flags = Sprites.Flag.placed_flags
                    if event.coordinates in placed_flags:
                        placed_flags[event.coordinates].kill()
                        del placed_flags[event.coordinates]
         # JOGADOR COLETOU UM COLETÁVEL
                if event.type == k.GET_COLLECTABLE:
                    SFX_STORAGE['ITEM'].play()
                    MIAUSMA_REACTS.set_animation(MIAUSMA_REACTS_BASE[0], k.MIAUSMA_REACT_POSITION, 3)

                    if event.caller.__class__ == Sprites.LifeCollectable:
                        MIAUSMA.heal(1)
                        SEVEN_LIVES.set_lives(MIAUSMA.lives)

                    if event.caller.__class__ == Sprites.TimeCollectable:
                        GAME_TIMER.add_time_seconds(3)

                    if event.caller.__class__ == Sprites.FlagCollectable:
                        MINEFIELD.set_flag_available()
                        MIAUSMA.flag_up(1)

                # PROTAGONISTA SE CUROU ALÉM DO NECESSÁRIO
                if event.type == k.OVERHEAL:
                    MIAUSMA.score_points(200)

                # PROTAGONISTA PEGOU MAIS BANDEIRAS QUE O NECESSÁRIO
                if event.type == k.OVERFLAG:
                    MIAUSMA.score_points(100)

                # O JOGO COMEÇOU
                if event.type == k.GAME_START:
                    PLAYLIST_MAIN_GAME.start()
                    GAME_TIMER.set_timer_seconds(k.TIME_LIMIT_SECONDS)
                    GAME_TIMER.activate()
class GameStateManager:

    def __init__(self):
        # INICIALIZA O OBJETO DO GERENCIADOR
        self.states = {}
        self.current_state = None

    def create_state(self, state_bundle):
        # CRIA UMA SÉRIE DE ESTADOS PARA O GERENCIADOR
        self.states[state_bundle[0]] = state_bundle[1]

    def set_state(self, state):
        # DEFINE O ESTADO ATUAL DO GERADOR
        self.current_state = self.states[state]

    def get_state(self):
        # RETORNA A CLASSE CORRESPONDENTE AO ESTADO DO GERENCIADOR
        return self.current_state

class MainMenu:

    def __init__(self, screen, gsm):
        # INICIALIZA O MENU PRINCIPAL
        self.screen = screen
        self.gsm = gsm

    def run(self):
        if not BACKGROUND_MAIN_MENU_DRAWN:
            # INSERE O PLANO DE FUNDO NA TELA
            BACKGROUND_MAIN_MENU_DRAWN.append(None)
            self.screen.put_inside(BACKGROUND_MAIN_MENU, (0, 0))

        # INSERE OS BOTÕES NA TELA
        self.screen.put_inside(TO_MAIN_GAME_BUTTON, TO_MAIN_GAME_BUTTON.rect.topleft)
        self.screen.put_inside(QUIT_GAME_BUTTON, QUIT_GAME_BUTTON.rect.topleft)

        BUTTON_MASKS.draw(self.screen.display)

        # CARREGA OS BOTÕES E A APARÊNCIA DELES NA TELA
        TO_MAIN_GAME_BUTTON.update()
        QUIT_GAME_BUTTON.update()
        BUTTON_MASKS.update()

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

  
