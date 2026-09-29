# Operações lógicas sobre cadeias binárias com Máquina de Turing de duas fitas

Este trabalho da disciplina de **Teoria de Computação** (UFT – Ciência da Computação) apresenta uma Máquina de Turing **determinística de duas fitas**. Ela calcula, bit a bit, as operações **AND**, **OR** e **XOR** entre duas palavras binárias de mesmo comprimento.

O projeto tem quatro partes:

- o **projeto formal** da máquina: alfabetos, estados, função de transição δ e diagrama;
- um **simulador em Python**, em que toda a computação ocorre pelas transições de δ;
- o arquivo da máquina para o **JFLAP**;
- o **relatório em PDF**, feito em LateX no modelo `uftreport` da UFT.

---

## Problema

A entrada é escrita na **fita 1** no formato:

```
op w1#w2
```

| Símbolo `op` | Operação |
|:---:|:---:|
| `A` | AND |
| `O` | OR |
| `X` | XOR |

Aqui, `w1, w2 ∈ {0,1}+` e `|w1| = |w2|`. Quem identifica a operação é a própria máquina, pelo primeiro símbolo da fita 1. A operação não é passada ao programa por nenhum outro meio.

A **fita 2** começa em branco. Ao final ela contém **somente** o resultado:

| Fita 1 | Fita 2 (resultado) |
|---|---|
| `A101#110` | `100` |
| `O101#110` | `111` |
| `X101#110` | `011` |

---

## Como a máquina funciona

**Alfabeto de entrada:** `Σ = {A, O, X, 0, 1, #}`
**Alfabeto das fitas:** `Γ = Σ ∪ {x, y, B}`

- `x` marca um bit `0` já processado e `y` marca um bit `1` já processado. As marcas são usadas **somente na fita 1**.
- `B` é o símbolo branco.

**Algoritmo:**

1. Em `q0` a máquina lê `A`, `O` ou `X` e vai para `q_and`, `q_or` ou `q_xor`. A partir daí, a operação fica guardada no estado.
2. A máquina marca o próximo bit não processado de `w1` (`0→x`, `1→y`) e guarda o valor dele no estado (`q_op_0` ou `q_op_1`).
3. Anda até o `#` e pula os bits já marcados de `w2`.
4. No primeiro bit não marcado de `w2`, marca esse bit e **escreve o resultado na fita 2**. O valor escrito vem da própria transição, que codifica a tabela-verdade da operação.
5. Volta até o próximo bit de `w1` e repete o processo.
6. Quando não há mais bits em `w1`, desfaz as marcas da fita 1 e para em `q_aceita`.

**Números da máquina:**
- 25 estados e 89 transições;
- custo de O(n²) passos;
- ao final, a fita 1 volta a ser igual à entrada original;
- a fita 2 nunca é usada como memória auxiliar: a cabeça 2 sempre lê `B`.

Entradas inválidas levam a uma transição indefinida, e a máquina rejeita. Isso vale para palavras de tamanhos diferentes, símbolo de operação desconhecido e ausência de `#`.

---

## Executando o simulador

**Requisito:** Python 3.8 ou superior. Não há dependências externas.

Para executar todos os casos de teste:

```bash
python3 mt_duas_fitas.py
```

Para executar uma entrada específica:

```bash
python3 mt_duas_fitas.py "X101#110"
```

Para executar várias entradas:

```bash
python3 mt_duas_fitas.py "A0#0" "O01#11" "X01#11"
```

Para salvar a saída em arquivo:

```bash
python3 mt_duas_fitas.py > saida.txt
```

> No Windows, use `python` ou `py` no lugar de `python3`. Coloque a entrada entre aspas por causa do símbolo `#`.

A cada passo, o programa mostra o estado atual, o conteúdo das duas fitas e a posição de cada cabeça. A célula sob a cabeça aparece entre colchetes:

```
Passo   0 | estado: q0
   Fita 1: [X] 0  1  #  1  1  B   (cabeca 1 na posicao 0)
   Fita 2: [B] B   (cabeca 2 na posicao 0)
Passo   1 | estado: q_xor
   Fita 1:  X [0] 1  #  1  1  B   (cabeca 1 na posicao 1)
   Fita 2: [B] B   (cabeca 2 na posicao 0)
...
```

Ao final, o programa imprime um resumo no formato **entrada → resultado esperado → resultado obtido**.

### Estrutura do código

| Elemento | Onde está |
|---|---|
| Função de transição δ | dicionário `transicoes`, no formato `(q, X1, X2) → (p, Y1, Y2, D1, D2)` |
| Fita 1 e fita 2 | `self.fita1`, `self.fita2` |
| Estado atual | `self.estado` |
| Posição das cabeças | `self.cabeca1`, `self.cabeca2` |
| Um passo da máquina | método `passo_unico()` |
| Casos de teste | lista `TESTES` |

O simulador **não usa operadores lógicos do Python** (`and`, `or`, `^`, `&`, `|`) para calcular o resultado. Ele apenas consulta δ, escreve nas fitas, move as cabeças e troca de estado.

---

## Casos de teste

| Entrada (fita 1) | Esperado (fita 2) | Obtido | Passos |
|---|---|---|---|
| `A0#0` | `0` | `0` ✅ | 13 |
| `A101#110` | `100` | `100` ✅ | 41 |
| `A11010#10011` | `10010` | `10010` ✅ | 85 |
| `O01#11` | `11` | `11` ✅ | 25 |
| `O101#110` | `111` | `111` ✅ | 41 |
| `O0000#0000` | `0000` | `0000` ✅ | 61 |
| `X01#11` | `10` | `10` ✅ | 25 |
| `X101#110` | `011` | `011` ✅ | 41 |
| `X1100#1010` | `0110` | `0110` ✅ | 61 |

---

## Abrindo no JFLAP

1. Abra o JFLAP 7 e use **File → Open** para abrir `mt_duas_fitas.jff`.
2. Para rodar passo a passo, use **Input → Step…**. Informe a entrada na fita 1 (ex.: `A101#110`) e deixe a fita 2 vazia.
3. Para testar vários casos de uma vez, use **Input → Multiple Run**.

No JFLAP, os rótulos aparecem como `lido ; escrito , movimento`, com uma parte para cada fita. O branco aparece como `□`.

---

### Conteúdo do relatório

1. **Projeto da Máquina de Turing:** definição formal, alfabetos, algoritmo, identificação da operação, localização dos bits, estados, tabela δ completa e diagramas.
2. **Implementação em Python:** estrutura do simulador e código-fonte.
3. **Testes e Resultados:** tabela de testes e prints da execução passo a passo.

A tabela δ e os diagramas do relatório foram gerados a partir do mesmo dicionário `transicoes` do simulador. Assim, a máquina apresentada no projeto é exatamente a máquina executada pelo programa.

---

## Autores

- Matheus Silva Pontes
- Lucas Monteiro de Carvalho

Universidade Federal do Tocantins – Curso de Ciência da Computação – 2026.
