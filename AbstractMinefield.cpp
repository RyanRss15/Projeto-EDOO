#include "AbstractMinefield.h"
#include <random>
#include <algorithm>
#include <stdexcept>

AbstractMinefield::AbstractMinefield(std::pair<int, int> size, float density)
    : size(size), width(size.first), height(size.second),
      discovered_tiles(0), win(false), first_dig(true) {

    tiles = width * height;
    bombs = static_cast<int>(tiles * density);
    free_tiles = tiles - bombs;

    minefield.resize(height, std::vector<int>(width, 0));
    minefield_mask.resize(height, std::vector<int>(width, 0));
    minefield_interface.resize(height, std::vector<int>(width, 0));
}

void AbstractMinefield::set_event_callback(std::function<void(MinefieldEvent, std::pair<int, int>)> callback) {
    event_callback = callback;
}

void AbstractMinefield::fill_minefield() {
    // PREENCHE UM VETOR COM ESPAÇOS LIVRES (0) E BOMBAS (1)
    std::vector<int> shallow_minefield(tiles, 0);
    std::fill(shallow_minefield.begin() + free_tiles, shallow_minefield.end(), 1);

    // EMBARALHA-SE O VETOR
    std::random_device rd;
    std::mt19937 g(rd());
    std::shuffle(shallow_minefield.begin(), shallow_minefield.end(), g);

    // TRANSFORMA-SE O VETOR EM UMA MATRIZ BIDIMENSIONAL
    for (int i = 0; i < height; ++i) {
        for (int j = 0; j < width; ++j) {
            minefield[i][j] = shallow_minefield[i * width + j];
        }
    }
}

// CONTA QUANTAS BOMBAS HÁ AO REDOR DE UM LADRILHO
void AbstractMinefield::count_tile(std::pair<int, int> tile) {
    int i_tile = tile.first;
    int j_tile = tile.second;
    int count = 0;

    int offsets[8][2] = {{-1, -1}, {-1, 0}, {-1, 1}, {0, -1}, {0, 1}, {1, -1}, {1, 0}, {1, 1}};

    for (auto& offset : offsets) {
        int i = offset[0];
        int j = offset[1];
        if (i_tile + i >= 0 && i_tile + i < height &&
            j_tile + j >= 0 && j_tile + j < width &&
            minefield[i_tile + i][j_tile + j]) {
            count++;
        }
    }
    minefield_mask[i_tile][j_tile] = count;
}

// FAZ A CONTAGEM DE BOMBAS PARA CADA LADRILHO NO CAMPO MINADO
void AbstractMinefield::count_all() {
    for (int i = 0; i < height; ++i) {
        for (int j = 0; j < width; ++j) {
            count_tile({i, j});
        }
    }
}

// REVELA UM LADRILHO NO CAMPO MINADO
void AbstractMinefield::dig(std::pair<int, int> tile, bool primary_dig) {
    // COORDENADAS DO LADRILHO
    int i_tile = tile.first;
    int j_tile = tile.second;

    //Proteção contra crash a partir de uma exceção
    if (i_tile < 0 || i_tile >= height || j_tile < 0 || j_tile >= width) {
        throw std::out_of_range("Coordenadas informadas estao fora dos limites do tabuleiro!");
    }

    // SÓ REVELA O LADRILHO SE NÃO HOUVER UMA BANDEIRA
    if (minefield_interface[i_tile][j_tile] == 2 && primary_dig) {
        return;
    }

    int offsets[8][2] = {{-1, -1}, {-1, 0}, {-1, 1}, {0, -1}, {0, 1}, {1, -1}, {1, 0}, {1, 1}};

    // É IMPOSSÍVEL ERRAR NA PRIMEIRA ESCAVAÇÃO
    if (first_dig) {
        first_dig = false;

        // A PRIMEIRA ESCAVAÇÃO ACERTOU UMA BOMBA
        if (minefield[i_tile][j_tile]) {
            minefield[i_tile][j_tile] = 0;
            minefield_interface[i_tile][j_tile] = 1;
            bombs--;
            free_tiles++;
            discovered_tiles++;
            if (event_callback) event_callback(MinefieldEvent::HIT, {i_tile, j_tile});
            count_all();
        } 
        // A PRIMEIRA ESCAVAÇÃO ACERTOU UM LADRILHO LIVRE
        else {
            count_all();
            minefield_interface[i_tile][j_tile] = 1;
            discovered_tiles++;
            if (event_callback) event_callback(MinefieldEvent::HIT, {i_tile, j_tile});
        }

        // A ESCAVAÇÃO NÃO FOI REALIZADA PELA CASCATA DE ESCAVAÇÃO
        if (primary_dig) {
            if (event_callback) event_callback(MinefieldEvent::PRIMARY_HIT, {i_tile, j_tile});
        }

        // OS LADRILHOS AO REDOR SERÃO ESCAVADOS CASO NÃO HAJAM BOMBAS POR PERTO
        for (auto& offset : offsets) {
            int ni = i_tile + offset[0];
            int nj = j_tile + offset[1];
            if (ni >= 0 && ni < height && nj >= 0 && nj < width) {
                if (minefield_interface[ni][nj] != 1 && minefield_mask[i_tile][j_tile] == 0) {
                    dig({ni, nj}, false);
                }
            }
        }
    } 

    // ACERTOU UMA MINA SEM SER A PRIMEIRA ESCAVAÇÃO
    else if (minefield[i_tile][j_tile] && minefield_interface[i_tile][j_tile] != 3) {
        minefield_interface[i_tile][j_tile] = 3;
        if (event_callback) event_callback(MinefieldEvent::MISS, {i_tile, j_tile});
    } 
    // REVELOU UM LADRILHO SEM SER A PRIMEIRA ESCAVAÇÃO
    else if ((minefield_interface[i_tile][j_tile] == 0 || minefield_interface[i_tile][j_tile] == 2) && !minefield[i_tile][j_tile]) {
        if (primary_dig) {
            if (event_callback) event_callback(MinefieldEvent::PRIMARY_HIT, {i_tile, j_tile});
        }
        minefield_interface[i_tile][j_tile] = 1;
        discovered_tiles++;
        if (event_callback) event_callback(MinefieldEvent::HIT, {i_tile, j_tile});

        // OS LADRILHOS AO REDOR SERÃO ESCAVADOS CASO NÃO HAJAM BOMBAS POR PERTO
        for (auto& offset : offsets) {
            int ni = i_tile + offset[0];
            int nj = j_tile + offset[1];
            if (ni >= 0 && ni < height && nj >= 0 && nj < width) {
                if (minefield_interface[ni][nj] != 1 && minefield_mask[i_tile][j_tile] == 0) {
                    dig({ni, nj}, false);
                }
            }
        }
    }

    //Verificação de vitoria para caso o jogador já tenha vencido
    if (primary_dig) {
        win_check();
    }
}

// INSERE UMA BANDEIRA NO CAMPO MINADO
void AbstractMinefield::flag(std::pair<int, int> tile) {
    int i_tile = tile.first;
    int j_tile = tile.second;
    int view = minefield_interface[i_tile][j_tile];

    //Validação da entrada e lançamento de exceção
    if (i_tile < 0 || i_tile >= height || j_tile < 0 || j_tile >= width) {
        throw std::out_of_range("Coordenadas de bandeira estao fora dos limites!");
    }

    if (view == 0) {
        minefield_interface[i_tile][j_tile] = 2;
        if (event_callback) event_callback(MinefieldEvent::FLAG, {i_tile, j_tile});
    } else if (view == 2) {
        minefield_interface[i_tile][j_tile] = 0;
        if (event_callback) event_callback(MinefieldEvent::UNFLAG, {i_tile, j_tile});
    }
}

// VERIFICA SE O CAMPO MINADO FOI COMPLETAMENTE LIMPO
void AbstractMinefield::win_check() {
    if (!win && discovered_tiles == free_tiles) {
        win = true;
        if (event_callback) event_callback(MinefieldEvent::WIN, {-1, -1});
    }
}

// Adaptando à mudança dos métodos get interface e mask para retornar a referencia por constante e não por valor
const std::vector<std::vector<int>> &AbstractMinefield::get_interface() const {
    return minefield_interface;
}

const std::vector<std::vector<int>> &AbstractMinefield::get_mask() const {
    return minefield_mask;
}