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
}

#endif