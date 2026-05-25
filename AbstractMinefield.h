#ifndef ABSTRACTMINEFIELD_H
#define ABSTRACTMINEFIELD_H

#include <vector>
#include <utility>
#include <functional>

enum class MinefieldEvent {
    HIT,
    PRIMARY_HIT,
    MISS,
    FLAG,
    UNFLAG,
    WIN
};

class AbstractMinefield {
private:
    std::pair<int, int> size;
    int width, height;
    std::vector<std::vector<int>> minefield;
    std::vector<std::vector<int>> minefield_mask;
    std::vector<std::vector<int>> minefield_interface;

    int tiles;
    int bombs;
    int free_tiles;
    int discovered_tiles;
    bool win;
    bool first_dig;

    std::function<void(MinefieldEvent, std::pair<int, int>)> event_callback;

public:
    AbstractMinefield(std::pair<int, int> size, float density);

    //Métodos adaptados para retornar a o valor por uma referência constante ao inves de ser por valor
    // (o que fazia uma alocação desnecessária de memoria)
    const std::vector<std::vector<int>>& get_mask() const;
    const std::vector<std::vector<int>>& get_interface() const;
    
    void set_event_callback(std::function<void(MinefieldEvent, std::pair<int, int>)> callback);
    void fill_minefield();
    void count_tile(std::pair<int, int> tile);
    void count_all();
    void dig(std::pair<int, int> tile, bool primary_dig = true);
    void flag(std::pair<int, int> tile);
    void win_check();
};

#endif // ABSTRACTMINEFIELD_H