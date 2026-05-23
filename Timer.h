#ifndef TIMER_H
#define TIMER_H

#include <chrono>

class Timer {
private:
    long long start_time;
    long long time_limit;
    long long current_time;
    bool activated;

    // Variável para marcar o "início" do programa e simular o get_ticks()
    std::chrono::time_point<std::chrono::steady_clock> initial_tick;

    // Método privado interno para substituir o pygame.time.get_ticks()
    long long get_ticks() const;

public:
    Timer();

    void set_timer_seconds(int time);
    void add_time_seconds(int time);
    
    // O const garante que este método não altera o estado do objeto
    int get_current_time_seconds() const; 
    
    void activate();
    bool ring();
};

#endif // TIMER_H