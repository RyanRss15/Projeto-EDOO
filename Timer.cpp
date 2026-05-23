#include "Timer.h"

Timer::Timer() 
    : start_time(0), time_limit(0), current_time(0), activated(false) {
    // Registra o momento exato em que o Timer foi criado na memória
    initial_tick = std::chrono::steady_clock::now();
}

// SIMULA O COMPORTAMENTO DO PYGAME (Retorna milissegundos desde a criação)
long long Timer::get_ticks() const {
    auto now = std::chrono::steady_clock::now();
    return std::chrono::duration_cast<std::chrono::milliseconds>(now - initial_tick).count();
}

// PREPARA O TIMER COM UM DADO TEMPO EM SEGUNDOS
void Timer::set_timer_seconds(int time) {
    start_time = static_cast<long long>(time) * 1000;
}

// ADICIONA TEMPO AO TIMER
void Timer::add_time_seconds(int time) {
    time_limit += static_cast<long long>(time) * 1000;
}

int Timer::get_current_time_seconds() const {
    if (activated) {
        return static_cast<int>(current_time / 1000);
    }
    return 0; // C++ exige um retorno explícito, diferente do Python que retorna 'None' implicitamente
}

// ATIVA O TIMER
void Timer::activate() {
    activated = true;
    time_limit = start_time + get_ticks();
    current_time = start_time;
}

// CHECA SE O TIMER ATINGIU O LIMITE DE TEMPO
bool Timer::ring() {
    if (activated) {
        if (current_time > 0) {
            current_time = time_limit - get_ticks();
            return false;
        } else {
            activated = false;
            current_time = 0;
            return true;
        }
    }
    return false;
}