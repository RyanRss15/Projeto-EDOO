# Projeto-EDOO

Nosso projeto será reescrever o jogo "Purgatório" um jogo de campo minado em C++

A apresentação do projeto escolhido se encontra nesse [link](https://www.canva.com/design/DAG75EYGjEI/MPH-B5Er5jqhvPlAvkUcBg/edit)

E o repostório do jogo original é [esse](https://github.com/Elanosinho/projeto-ip)


## Migração de Arquitetura: Python para C++

Esta seção documenta as diretrizes gerais adotadas na transição do projeto e as adaptações específicas aplicadas a cada módulo.

#### Interface de Linha de Comando (CLI) -> main.cpp
Implementação do motor de jogo e interface visual operando integralmente no terminal, validando o total desacoplamento da classe `AbstractMinefield`.

* **Renderização via Referência (`const &`):** A função de desenho da grade recebe o estado do tabuleiro como uma referência constante, prevenindo cópias pesadas e desnecessárias de memória a cada frame, sem risco de alteração do estado original da matriz.
* **Injeção de Eventos via Lambdas:** O callback de eventos injetado na classe principal foi implementado utilizando expressões Lambda do C++ moderno. O escopo de captura por referência `[&]` permite que o evento (como explodir uma bomba) altere o estado da variável local `game_over` para interromper o loop, dispensando o uso de variáveis globais.
* **Entrada de Dados Tipada:** O parsing manual de strings (comum em linguagens dinâmicas) foi substituído pelo fluxo tipado do `std::cin`. Ele extrai sequencialmente o comando de ação (`char`) e as coordenadas (`int`) diretamente do buffer de entrada nativo.
* **Adaptação Síncrona de Tempo e Vidas:** O loop de jogo no terminal foi atualizado para suportar a classe `Timer` e um contador de vidas extraído do Pygame original. Devido à natureza bloqueante (síncrona) da entrada de dados no terminal (`std::cin`), o tempo é validado imediatamente antes de imprimir a grade e imediatamente após a submissão do comando pelo usuário.
* **Sobrevivência a Erros:** A injeção de dependência via Lambda foi modificada para interceptar eventos de erro (`MinefieldEvent::MISS`). O jogador agora perde uma vida progressivamente em vez de acionar a condição de derrota imediata, encerrando a partida apenas quando o limite de vidas chega a zero.

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

## 🎮 Como Jogar (Versão Terminal/CLI)

O jogo foi adaptado para rodar nativamente no terminal, transformando a ação em tempo real em uma experiência estratégica baseada em turnos, mas sem perder a pressão do tempo!

Para jogar você deve primeiramente compilar os arquivos a partir da seguinte linha de comando no terminal:
```g++ main.cpp AbstractMinefield.cpp Timer.cpp -o campominado -std=c++11```
E em seguida digitar:
```./campominado'''bash```

### A Interface
Durante a partida, você verá um painel (HUD) atualizado a cada rodada e a grade do campo minado:

**O Painel (HUD)**
Mostra suas **Vidas** restantes, o **Tempo** da rodada (limite de 60s), sua **Pontuação** atual e a **Nota** (Grade) correspondente.

**A Grade**
* **` . `** Ladrilho intocado e misterioso.
* **` - `** Ladrilho livre e seguro (zero bombas ao redor).
* **`1-8`** Quantidade de bombas nas casas adjacentes.
* **` F `** Bandeira plantada por você.
* **` * `** Bomba detonada (você pisou aqui e perdeu uma vida).

### Controles
O jogo aguardará o seu comando para processar cada turno. Para interagir, digite a letra da ação desejada, seguida das coordenadas da linha e da coluna (separadas por espaço), e aperte **Enter**:

* **Escavar (`e`):** Revela o conteúdo do ladrilho.
  * *Exemplo de uso:* Digite `e 4 5` para escavar a linha 4 e coluna 5.
* **Plantar/Remover Bandeira (`f`):** Marca um ladrilho suspeito com uma bandeira para evitar acidentes, ou remove uma bandeira existente.
  * *Exemplo de uso:* Digite `f 4 5` para colocar uma bandeira na linha 4 e coluna 5.

**💡 Dica Estratégica:** O relógio só começa a contar **após o seu primeiro movimento**. Aproveite esse tempo de respiro no início para decidir com calma onde dar o primeiro passo!
