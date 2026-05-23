# Projeto-EDOO

Nosso projeto será reescrever o jogo "Purgatório" um jogo de campo minado em C++

A apresentação do projeto escolhido se encontra nesse [link](https://www.canva.com/design/DAG75EYGjEI/MPH-B5Er5jqhvPlAvkUcBg/edit)

E o repostório do jogo original é [esse](https://github.com/Elanosinho/projeto-ip)


## Migração de Arquitetura: Python para C++

Esta seção documenta as diretrizes gerais adotadas na transição do projeto e as adaptações específicas aplicadas a cada módulo.

### 1. Diretrizes Gerais do Projeto
* **Separação entre Interface e Implementação:** Adoção do modelo de compilação separada. Arquivos de cabeçalho (`.h`) atuam como contratos com declarações protegidas por *Include Guards*, enquanto os arquivos de código-fonte (`.cpp`) encapsulam a complexidade da lógica.
* **Tipagem e Estruturas de Dados:** Substituição das tipagens dinâmicas do Python por estruturas estáticas da Standard Template Library (STL) do C++.
* **Encapsulamento Restrito:** Transição de atributos implicitamente públicos (`self.atributo`) para modificadores de acesso rígidos (`private` e `public`), garantindo o princípio de Information Hiding.
* **Otimização de Construtores:** Uso padrão de *Member Initialization Lists* para garantir a construção e alocação segura das variáveis de classe antes da execução do construtor.

---

### 2. Módulos Refatorados

#### Algoritmos.py -> AbstractMinefield.h / AbstractMinefield.cpp
O núcleo lógico do campo minado foi convertido para operar de forma totalmente desacoplada de bibliotecas gráficas ou de interface.

* **Alocação do Tabuleiro:** A grade bidimensional construída com `lists` no Python foi convertida para `std::vector<std::vector<int>>` para garantir alocação contígua, e as coordenadas de posição passaram a utilizar `std::pair<int, int>`.
* **Desacoplamento de Eventos (Callbacks):** A dependência direta e global do `pygame.event` foi eliminada. A comunicação do estado do jogo (como revelar mina, marcar bandeira ou vencer) agora utiliza injeção de dependência através de ponteiros de função (`std::function`) e um enumerador estrito (`enum class MinefieldEvent`).
* **Proteção de Estado:** Propriedades críticas do jogo como contagem de bombas e tiles livres foram isoladas no escopo `private`.

#### Timer.py -> Timer.h / Timer.cpp
A classe de temporização foi convertida com foco na remoção de dependências de bibliotecas gráficas, tornando-a agnóstica.

* **Desacoplamento do Pygame:** A dependência direta da função `pygame.time.get_ticks()` foi substituída por uma implementação nativa utilizando a biblioteca padrão `<chrono>` do C++. O uso de `std::chrono::steady_clock` garante uma contagem de tempo monotônica e precisa.
* **Segurança de Tipos e Overflow:** O rastreio de tempo em milissegundos foi definido como `long long` (int64) para prevenir estouros de limite (*overflows*) que ocorreriam com inteiros tradicionais em sessões longas.
* **Const Correctness:** Métodos de leitura de tempo (como `get_current_time_seconds`) foram assinalados com o modificador `const`, garantindo a nível de compilação que chamadas de leitura não alterem o estado interno do temporizador.