#include <stdexcept>
#include <iostream>
#include <vector>
#include "AbstractMinefield.h"
#include "Timer.h"
#include "Constantes.h"

// Função responsável por desenhar a matriz no terminal.
// Recebe os dados por referência (const &) para evitar cópias desnecessárias de memória.
void print_board(const std::vector<std::vector<int>>& board, const std::vector<std::vector<int>>& mask) {
    std::cout << "\n   ";
    for (size_t j = 0; j < board[0].size(); ++j) std::cout << j << " ";
    std::cout << "\n";

    for (size_t i = 0; i < board.size(); ++i) {
        std::cout << i << " |";
        for (size_t j = 0; j < board[i].size(); ++j) {
            int state = board[i][j];
            
            if (state == 0) {
                std::cout << ". ";
            } else if (state == 1) {
                // Se o bloco foi revelado (1), lê a máscara para saber quantas bombas há em volta
                int bombs_around = mask[i][j];
                if (bombs_around == 0) std::cout << "- ";
                else std::cout << bombs_around << " ";
            } else if (state == 2) {
                std::cout << "F ";
            } else if (state == 3) {
                std::cout << "* "; // Representação visual de uma bomba detonada
            }
        }
        std::cout << "|\n";
    }
    std::cout << "\n";
}

int main() {
    // Variáveis de estado do jogo (replicando os atributos do Game.py)
    bool game_over = false;
    bool game_started = false; // Garante que o tempo só corra após o primeiro movimento
    int lives = 7;
    int score = 0;
    
    // Inicialização do núcleo lógico do Campo Minado
    AbstractMinefield game({10, 10}, 0.12f);
    game.fill_minefield();

    // Configuração do temporizador independente de engine gráfica
    Timer game_timer;
    game_timer.set_timer_seconds(60); 

    // INJEÇÃO DE DEPENDÊNCIA (Callbacks)
    // A função lambda [&] captura as variáveis locais (como 'score' e 'lives') por referência,
    // permitindo que o núcleo do jogo atualize o estado da partida sem conhecer o terminal.
    game.set_event_callback([&](MinefieldEvent e, std::pair<int, int> coords) {
        switch (e) {
            case MinefieldEvent::PRIMARY_HIT:
                score += 15; // Bônus do primeiro acerto seguro
                break;
            case MinefieldEvent::HIT:
                score += 5;  // Bônus padrão por escavar
                break;
            case MinefieldEvent::FLAG:
                score += 5;  // Bônus por colocar bandeira
                break;
            case MinefieldEvent::MISS:
                lives--; // Penalidade por atingir bomba
                if (lives > 0) {
                    std::cout << "\n>>> KABOOM! Voce perdeu uma vida! Restam: " << lives << "\n";
                } else {
                    std::cout << "\n>>> KABOOM! Fim das vidas! Game Over.\n";
                    game_over = true; // Aciona o fim do loop principal
                }
                break;
            case MinefieldEvent::WIN:
                // Cálculo de pontuação final baseado em tempo e vidas restantes
                score += 1000 + (lives * 100) + (game_timer.get_current_time_seconds() * 100);
                std::cout << "\n>>> PARABENS! Voce limpou o campo!\n";
                game_over = true;
                break;
            default: 
                break;
        }
    });

    std::cout << "=== CAMPO MINADO ===\n";

    // GAME LOOP PRINCIPAL
    while (!game_over) {
        // Validação de tempo pré-renderização
        if (game_started && game_timer.ring()) {
            std::cout << "\n>>> TEMPO ESGOTADO! Game Over.\n";
            break;
        }

        print_board(game.get_interface(), game.get_mask());

        // Se o jogo não começou, crava a exibição em 60s. Caso contrário, busca o tempo real.
        int display_time = game_started ? game_timer.get_current_time_seconds() : 60;
        char grade = Constantes::score_grade(score); // Avalia a nota baseada no score atual
        
        std::cout << "[ Vidas: " << lives << " | Tempo: " << display_time << "s | Pontos: " << score << " | Nota: " << grade << " ]\n";
        std::cout << "Acao (e=escavar, f=bandeira) e Coordenadas (linha coluna): ";
        
        char action;
        int row, col;
        
        // Operação síncrona: O terminal pausa o programa aqui esperando a digitação.
        // O relógio da classe Timer continua rodando internamente graças à biblioteca <chrono>.
        std::cin >> action >> row >> col; 

        // Ativa o temporizador do jogo somente após a primeira entrada de dados válida
        if (!game_started && (action == 'e' || action == 'f')) {
            game_started = true;
            game_timer.activate();
        }

        // Validação de tempo pós-renderização: Checa se o jogador demorou tempo demais na tela do std::cin
        if (game_started && game_timer.ring()) {
            std::cout << "\n>>> TEMPO ESGOTADO! O tempo acabou enquanto voce pensava.\n";
            break;
        }

        // ROTEAMENTO DE COMANDOS PROTEGIDO POR TRATAMENTO DE ERRO
        try {
            if (action == 'e') {
                game.dig({row, col});
            } 
            else if (action == 'f') {
                // É altamente recomendável colocar a validação de limites no método flag() também,
                // assim este mesmo bloco catch vai proteger o seu jogo se o usuário tentar colocar uma bandeira fora do mapa.
                game.flag({row, col});
            } 
            else {
                std::cout << "Acao invalida.\n";
            }
        } 
        catch (const std::out_of_range& e) {
            // O código entra aqui APENAS se alguma coordenada inválida disparar o throw
            std::cout << "\n======================================================\n";
            std::cout << ">>> ERRO: " << e.what() << "\n";
            std::cout << "======================================================\n\n";

            // O loop não é quebrado (não usamos break), portanto ele avança para a próxima
            // iteração e solicita uma nova jogada válida para o jogador.
        }
    }

    // Tela de Resultados Final
    print_board(game.get_interface(), game.get_mask());
    std::cout << ">>> RESULTADO FINAL: " << score << " PONTOS (Nota: " << Constantes::score_grade(score) << ")\n";
    return 0;
}