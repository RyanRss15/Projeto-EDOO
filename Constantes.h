#ifndef CONSTANTES_H
#define CONSTANTES_H

#include <utility>

namespace Constantes {

    inline char score_grade(int score) {
        if (score < 2000) return 'a';
        if (score < 4000) return 'b';
        if (score < 8000) return 'c';
        if (score < 16000) return 'd';
        if (score < 32000) return 'e';
        return 'f';
    }

    constexpr std::pair<int, int> ABSTRACT_MINEFIELD_SIZE = {10, 10};
    constexpr float ABSTRACT_MINEFIELD_DENSITY = 0.12f;
    constexpr int TIME_LIMIT_SECONDS = 60;

    // A implementação inline resolve o erro de "undefined reference"
    inline std::pair<float, float> set_proportion(float a, float b) {
        return {a, b}; 
    }

    const std::pair<float, float> MINEFIELD_SIZE = set_proportion(16.0f / 9.0f, 1.0f);
    const std::pair<float, float> MINEFIELD_POSITION = set_proportion(4.5714f, 10000.0f);
    const std::pair<float, float> SIZE_FLAGS = set_proportion(9.6f, 5.4f);
    const std::pair<float, float> SIZE_BOMBS = set_proportion(9.6f, 5.4f);

}

#endif