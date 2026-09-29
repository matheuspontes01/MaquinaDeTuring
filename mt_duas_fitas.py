"""
Simulador de Maquina de Turing deterministica de DUAS fitas
Operacoes logicas bit a bit (AND, OR, XOR) sobre cadeias binarias.

Entrada (fita 1):  op w1#w2   com op em {A, O, X}, w1, w2 em {0,1}+, |w1| = |w2|
Saida   (fita 2):  resultado da operacao, bit a bit.

Toda a computacao e feita pelas transicoes de delta (dicionario `transicoes`).
O Python apenas SIMULA a maquina: le (estado, simbolo fita 1, simbolo fita 2),
consulta delta, escreve, move as cabecas e troca de estado.
Nenhum operador logico do Python e usado para calcular o resultado.

Formato: delta(q, X1, X2) = (p, Y1, Y2, D1, D2), com D em {L, R, S}.
Marcas usadas na fita 1:  x = bit 0 ja processado,  y = bit 1 ja processado.
"""

BRANCO = "B"
ESTADO_INICIAL = "q0"
ESTADOS_FINAIS = {"q_aceita"}

# ---------------------------------------------------------------------------
# Funcao de transicao delta
# ---------------------------------------------------------------------------
transicoes = {
    # --- Identificacao da operacao (1o simbolo da fita 1) ---
    ('q0', 'A', 'B')              : ('q_and', 'A', 'B', 'R', 'S'),
    ('q0', 'O', 'B')              : ('q_or', 'O', 'B', 'R', 'S'),
    ('q0', 'X', 'B')              : ('q_xor', 'X', 'B', 'R', 'S'),
    # --- Operacao AND (simbolo A) ---
    # q_and: seleciona o proximo bit nao marcado de w1
    ('q_and', '0', 'B')           : ('q_and_0', 'x', 'B', 'R', 'S'),
    ('q_and', '1', 'B')           : ('q_and_1', 'y', 'B', 'R', 'S'),
    ('q_and', '#', 'B')           : ('q_rest_dir', '#', 'B', 'R', 'S'),
    # q_and_0: guarda o bit 0 de w1 e anda ate o #
    ('q_and_0', '0', 'B')         : ('q_and_0', '0', 'B', 'R', 'S'),
    ('q_and_0', '1', 'B')         : ('q_and_0', '1', 'B', 'R', 'S'),
    ('q_and_0', '#', 'B')         : ('q_and_0w2', '#', 'B', 'R', 'S'),
    # q_and_0w2: pula bits ja marcados de w2 e processa o primeiro nao marcado
    ('q_and_0w2', 'x', 'B')       : ('q_and_0w2', 'x', 'B', 'R', 'S'),
    ('q_and_0w2', 'y', 'B')       : ('q_and_0w2', 'y', 'B', 'R', 'S'),
    ('q_and_0w2', '0', 'B')       : ('q_and_volta2', 'x', '0', 'L', 'R'),
    ('q_and_0w2', '1', 'B')       : ('q_and_volta2', 'y', '0', 'L', 'R'),
    # q_and_1: guarda o bit 1 de w1 e anda ate o #
    ('q_and_1', '0', 'B')         : ('q_and_1', '0', 'B', 'R', 'S'),
    ('q_and_1', '1', 'B')         : ('q_and_1', '1', 'B', 'R', 'S'),
    ('q_and_1', '#', 'B')         : ('q_and_1w2', '#', 'B', 'R', 'S'),
    # q_and_1w2: pula bits ja marcados de w2 e processa o primeiro nao marcado
    ('q_and_1w2', 'x', 'B')       : ('q_and_1w2', 'x', 'B', 'R', 'S'),
    ('q_and_1w2', 'y', 'B')       : ('q_and_1w2', 'y', 'B', 'R', 'S'),
    ('q_and_1w2', '0', 'B')       : ('q_and_volta2', 'x', '0', 'L', 'R'),
    ('q_and_1w2', '1', 'B')       : ('q_and_volta2', 'y', '1', 'L', 'R'),
    # q_and_volta2 / q_and_volta1: retorno ao proximo bit de w1
    ('q_and_volta2', 'x', 'B')    : ('q_and_volta2', 'x', 'B', 'L', 'S'),
    ('q_and_volta2', 'y', 'B')    : ('q_and_volta2', 'y', 'B', 'L', 'S'),
    ('q_and_volta2', '#', 'B')    : ('q_and_volta1', '#', 'B', 'L', 'S'),
    ('q_and_volta1', '0', 'B')    : ('q_and_volta1', '0', 'B', 'L', 'S'),
    ('q_and_volta1', '1', 'B')    : ('q_and_volta1', '1', 'B', 'L', 'S'),
    ('q_and_volta1', 'x', 'B')    : ('q_and', 'x', 'B', 'R', 'S'),
    ('q_and_volta1', 'y', 'B')    : ('q_and', 'y', 'B', 'R', 'S'),
    ('q_and_volta1', 'A', 'B')    : ('q_and', 'A', 'B', 'R', 'S'),
    # --- Operacao OR (simbolo O) ---
    # q_or: seleciona o proximo bit nao marcado de w1
    ('q_or', '0', 'B')            : ('q_or_0', 'x', 'B', 'R', 'S'),
    ('q_or', '1', 'B')            : ('q_or_1', 'y', 'B', 'R', 'S'),
    ('q_or', '#', 'B')            : ('q_rest_dir', '#', 'B', 'R', 'S'),
    # q_or_0: guarda o bit 0 de w1 e anda ate o #
    ('q_or_0', '0', 'B')          : ('q_or_0', '0', 'B', 'R', 'S'),
    ('q_or_0', '1', 'B')          : ('q_or_0', '1', 'B', 'R', 'S'),
    ('q_or_0', '#', 'B')          : ('q_or_0w2', '#', 'B', 'R', 'S'),
    # q_or_0w2: pula bits ja marcados de w2 e processa o primeiro nao marcado
    ('q_or_0w2', 'x', 'B')        : ('q_or_0w2', 'x', 'B', 'R', 'S'),
    ('q_or_0w2', 'y', 'B')        : ('q_or_0w2', 'y', 'B', 'R', 'S'),
    ('q_or_0w2', '0', 'B')        : ('q_or_volta2', 'x', '0', 'L', 'R'),
    ('q_or_0w2', '1', 'B')        : ('q_or_volta2', 'y', '1', 'L', 'R'),
    # q_or_1: guarda o bit 1 de w1 e anda ate o #
    ('q_or_1', '0', 'B')          : ('q_or_1', '0', 'B', 'R', 'S'),
    ('q_or_1', '1', 'B')          : ('q_or_1', '1', 'B', 'R', 'S'),
    ('q_or_1', '#', 'B')          : ('q_or_1w2', '#', 'B', 'R', 'S'),
    # q_or_1w2: pula bits ja marcados de w2 e processa o primeiro nao marcado
    ('q_or_1w2', 'x', 'B')        : ('q_or_1w2', 'x', 'B', 'R', 'S'),
    ('q_or_1w2', 'y', 'B')        : ('q_or_1w2', 'y', 'B', 'R', 'S'),
    ('q_or_1w2', '0', 'B')        : ('q_or_volta2', 'x', '1', 'L', 'R'),
    ('q_or_1w2', '1', 'B')        : ('q_or_volta2', 'y', '1', 'L', 'R'),
    # q_or_volta2 / q_or_volta1: retorno ao proximo bit de w1
    ('q_or_volta2', 'x', 'B')     : ('q_or_volta2', 'x', 'B', 'L', 'S'),
    ('q_or_volta2', 'y', 'B')     : ('q_or_volta2', 'y', 'B', 'L', 'S'),
    ('q_or_volta2', '#', 'B')     : ('q_or_volta1', '#', 'B', 'L', 'S'),
    ('q_or_volta1', '0', 'B')     : ('q_or_volta1', '0', 'B', 'L', 'S'),
    ('q_or_volta1', '1', 'B')     : ('q_or_volta1', '1', 'B', 'L', 'S'),
    ('q_or_volta1', 'x', 'B')     : ('q_or', 'x', 'B', 'R', 'S'),
    ('q_or_volta1', 'y', 'B')     : ('q_or', 'y', 'B', 'R', 'S'),
    ('q_or_volta1', 'O', 'B')     : ('q_or', 'O', 'B', 'R', 'S'),
    # --- Operacao XOR (simbolo X) ---
    # q_xor: seleciona o proximo bit nao marcado de w1
    ('q_xor', '0', 'B')           : ('q_xor_0', 'x', 'B', 'R', 'S'),
    ('q_xor', '1', 'B')           : ('q_xor_1', 'y', 'B', 'R', 'S'),
    ('q_xor', '#', 'B')           : ('q_rest_dir', '#', 'B', 'R', 'S'),
    # q_xor_0: guarda o bit 0 de w1 e anda ate o #
    ('q_xor_0', '0', 'B')         : ('q_xor_0', '0', 'B', 'R', 'S'),
    ('q_xor_0', '1', 'B')         : ('q_xor_0', '1', 'B', 'R', 'S'),
    ('q_xor_0', '#', 'B')         : ('q_xor_0w2', '#', 'B', 'R', 'S'),
    # q_xor_0w2: pula bits ja marcados de w2 e processa o primeiro nao marcado
    ('q_xor_0w2', 'x', 'B')       : ('q_xor_0w2', 'x', 'B', 'R', 'S'),
    ('q_xor_0w2', 'y', 'B')       : ('q_xor_0w2', 'y', 'B', 'R', 'S'),
    ('q_xor_0w2', '0', 'B')       : ('q_xor_volta2', 'x', '0', 'L', 'R'),
    ('q_xor_0w2', '1', 'B')       : ('q_xor_volta2', 'y', '1', 'L', 'R'),
    # q_xor_1: guarda o bit 1 de w1 e anda ate o #
    ('q_xor_1', '0', 'B')         : ('q_xor_1', '0', 'B', 'R', 'S'),
    ('q_xor_1', '1', 'B')         : ('q_xor_1', '1', 'B', 'R', 'S'),
    ('q_xor_1', '#', 'B')         : ('q_xor_1w2', '#', 'B', 'R', 'S'),
    # q_xor_1w2: pula bits ja marcados de w2 e processa o primeiro nao marcado
    ('q_xor_1w2', 'x', 'B')       : ('q_xor_1w2', 'x', 'B', 'R', 'S'),
    ('q_xor_1w2', 'y', 'B')       : ('q_xor_1w2', 'y', 'B', 'R', 'S'),
    ('q_xor_1w2', '0', 'B')       : ('q_xor_volta2', 'x', '1', 'L', 'R'),
    ('q_xor_1w2', '1', 'B')       : ('q_xor_volta2', 'y', '0', 'L', 'R'),
    # q_xor_volta2 / q_xor_volta1: retorno ao proximo bit de w1
    ('q_xor_volta2', 'x', 'B')    : ('q_xor_volta2', 'x', 'B', 'L', 'S'),
    ('q_xor_volta2', 'y', 'B')    : ('q_xor_volta2', 'y', 'B', 'L', 'S'),
    ('q_xor_volta2', '#', 'B')    : ('q_xor_volta1', '#', 'B', 'L', 'S'),
    ('q_xor_volta1', '0', 'B')    : ('q_xor_volta1', '0', 'B', 'L', 'S'),
    ('q_xor_volta1', '1', 'B')    : ('q_xor_volta1', '1', 'B', 'L', 'S'),
    ('q_xor_volta1', 'x', 'B')    : ('q_xor', 'x', 'B', 'R', 'S'),
    ('q_xor_volta1', 'y', 'B')    : ('q_xor', 'y', 'B', 'R', 'S'),
    ('q_xor_volta1', 'X', 'B')    : ('q_xor', 'X', 'B', 'R', 'S'),
    # --- Restauracao da fita 1 (desfaz as marcacoes) ---
    ('q_rest_dir', 'x', 'B')      : ('q_rest_dir', '0', 'B', 'R', 'S'),
    ('q_rest_dir', 'y', 'B')      : ('q_rest_dir', '1', 'B', 'R', 'S'),
    ('q_rest_dir', 'B', 'B')      : ('q_rest_esq', 'B', 'B', 'L', 'S'),
    ('q_rest_esq', 'x', 'B')      : ('q_rest_esq', '0', 'B', 'L', 'S'),
    ('q_rest_esq', 'y', 'B')      : ('q_rest_esq', '1', 'B', 'L', 'S'),
    ('q_rest_esq', '0', 'B')      : ('q_rest_esq', '0', 'B', 'L', 'S'),
    ('q_rest_esq', '1', 'B')      : ('q_rest_esq', '1', 'B', 'L', 'S'),
    ('q_rest_esq', '#', 'B')      : ('q_rest_esq', '#', 'B', 'L', 'S'),
    ('q_rest_esq', 'A', 'B')      : ('q_aceita', 'A', 'B', 'S', 'S'),
    ('q_rest_esq', 'O', 'B')      : ('q_aceita', 'O', 'B', 'S', 'S'),
    ('q_rest_esq', 'X', 'B')      : ('q_aceita', 'X', 'B', 'S', 'S'),
}


# ---------------------------------------------------------------------------
# Simulador
# ---------------------------------------------------------------------------
class MaquinaTuringDuasFitas:
    def __init__(self, transicoes, estado_inicial, estados_finais, branco=BRANCO):
        self.delta = transicoes
        self.estado_inicial = estado_inicial
        self.estados_finais = estados_finais
        self.branco = branco

    def carregar(self, entrada):
        """Coloca a entrada na fita 1; a fita 2 comeca totalmente em branco."""
        self.fita1 = list(entrada) if entrada else [self.branco]
        self.fita2 = [self.branco]
        self.cabeca1 = 0
        self.cabeca2 = 0
        self.estado = self.estado_inicial
        self.passo = 0

    # -- acesso as fitas (fitas infinitas a direita, completadas com B) --
    @staticmethod
    def _ler(fita, pos, branco):
        if pos >= len(fita):
            fita.extend([branco] * (pos - len(fita) + 1))
        return fita[pos]

    @staticmethod
    def _mover(pos, direcao):
        if direcao == "R":
            return pos + 1
        if direcao == "L":
            return max(pos - 1, 0)
        return pos  # "S": permanece

    # -- exibicao --
    def _fita_str(self, fita, cabeca):
        fim = max(len(fita), cabeca + 1)
        while fim > cabeca + 1 and fim > 1 and fita[fim - 1] == self.branco:
            fim -= 1
        celulas = [self._ler(fita, i, self.branco) for i in range(fim + 1)]
        return "".join(f"[{s}]" if i == cabeca else f" {s} " for i, s in enumerate(celulas)).rstrip()

    def mostrar(self):
        print(f"Passo {self.passo:>3} | estado: {self.estado}")
        print(f"   Fita 1: {self._fita_str(self.fita1, self.cabeca1)}   (cabeca 1 na posicao {self.cabeca1})")
        print(f"   Fita 2: {self._fita_str(self.fita2, self.cabeca2)}   (cabeca 2 na posicao {self.cabeca2})")

    # -- um passo da maquina --
    def passo_unico(self):
        x1 = self._ler(self.fita1, self.cabeca1, self.branco)
        x2 = self._ler(self.fita2, self.cabeca2, self.branco)
        chave = (self.estado, x1, x2)
        if chave not in self.delta:
            return False  # delta indefinida: a maquina para
        p, y1, y2, d1, d2 = self.delta[chave]
        self.fita1[self.cabeca1] = y1
        self.fita2[self.cabeca2] = y2
        self.cabeca1 = self._mover(self.cabeca1, d1)
        self.cabeca2 = self._mover(self.cabeca2, d2)
        self.estado = p
        self.passo += 1
        return True

    def executar(self, entrada, mostrar_passos=True, limite=100000):
        self.carregar(entrada)
        if mostrar_passos:
            self.mostrar()
        while self.estado not in self.estados_finais and self.passo < limite:
            if not self.passo_unico():
                break
            if mostrar_passos:
                self.mostrar()
        aceitou = self.estado in self.estados_finais
        return aceitou, self.conteudo(self.fita1), self.conteudo(self.fita2)

    def conteudo(self, fita):
        return "".join(fita).strip(self.branco)


# ---------------------------------------------------------------------------
# Testes
# ---------------------------------------------------------------------------
TESTES = [
    # (entrada na fita 1, resultado esperado na fita 2)
    ("A0#0",        "0"),
    ("A101#110",    "100"),
    ("A11010#10011", "10010"),
    ("O01#11",      "11"),
    ("O101#110",    "111"),
    ("O0000#0000",  "0000"),
    ("X01#11",      "10"),
    ("X101#110",    "011"),
    ("X1100#1010",  "0110"),
]


def main():
    import sys
    mt = MaquinaTuringDuasFitas(transicoes, ESTADO_INICIAL, ESTADOS_FINAIS)

    # Uso opcional:  python mt_duas_fitas.py X101#110
    if len(sys.argv) > 1:
        casos = [(e, None) for e in sys.argv[1:]]
    else:
        casos = TESTES

    resumo = []
    for entrada, esperado in casos:
        print("=" * 78)
        print(f"ENTRADA: {entrada}")
        print("=" * 78)
        aceitou, f1, f2 = mt.executar(entrada)
        status = "ACEITA" if aceitou else "REJEITADA (delta indefinida)"
        print(f"-> Maquina parou em {mt.estado} apos {mt.passo} passos: {status}")
        print(f"-> Fita 1 final: {f1}")
        print(f"-> Fita 2 final: {f2}\n")
        resumo.append((entrada, esperado, f2 if aceitou else "-", mt.passo))

    print("=" * 78)
    print("RESUMO DOS TESTES: entrada -> resultado esperado -> resultado obtido")
    print("=" * 78)
    for entrada, esperado, obtido, passos in resumo:
        if esperado is None:
            print(f"{entrada:<14} -> {'?':<8} -> {obtido:<8} ({passos} passos)")
        else:
            ok = "OK" if obtido == esperado else "FALHOU"
            print(f"{entrada:<14} -> {esperado:<8} -> {obtido:<8} [{ok}] ({passos} passos)")


if __name__ == "__main__":
    main()