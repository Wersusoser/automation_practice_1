# Вариант 2: а) ДКА #a==2 и #b>2 над {a,b}
#            б) НКА над {1,2,3}: последний символ раньше не встречался

import sys


def pad(text, width):
    while len(text) < width:
        text = text + " "
    return text


def ids_text(lst):
    text = ""
    for t in lst:
        text = text + "q" + str(t)
    return text if lst else "-"


def sym_index(SIGMA, c):
    for k, s in enumerate(SIGMA):
        if s == c:
            return k
    return -1


Q_DFA     = list(range(13))
SIGMA_DFA = ('a', 'b')
Q0_DFA    = 0
F_DFA     = {11}
DEAD_DFA  = 12

DELTA_DFA = [[DEAD_DFA, DEAD_DFA] for _ in Q_DFA]
for i in range(3):
    for j in range(4):
        s = i * 4 + j
        DELTA_DFA[s][0] = (i + 1) * 4 + j if i < 2 else DEAD_DFA
        DELTA_DFA[s][1] = i * 4 + (j + 1) if j < 3 else i * 4 + 3

DFA = (Q_DFA, SIGMA_DFA, DELTA_DFA, Q0_DFA, F_DFA)


def dfa_run(w, trace=False):
    Q, SIGMA, delta, q0, F = DFA
    s = q0
    if trace:
        sys.stdout.write("  q" + str(s))
    for c in w:
        k = sym_index(SIGMA, c)
        if k == -1:
            if trace:
                print("  (символ вне алфавита)")
            return 0
        s = delta[s][k]
        if trace:
            sys.stdout.write(" -" + c + "-> q" + str(s))
    if trace:
        print()
    return 1 if s in F else 0


def dfa_print_table():
    Q, SIGMA, delta, q0, F = DFA
    print("ДКА, таблица переходов delta:")
    print(" state |  a  |  b  | final")
    for s in Q:
        line = " " + pad("q" + str(s), 6) + "| " + pad("q" + str(delta[s][0]), 4)
        line += "| " + pad("q" + str(delta[s][1]), 4) + "|  "
        line += "+" if s in F else "-"
        print(line)
    print("(q0 - старт, q12 - ловушка, q11 - финал)\n")


Q_NFA     = list(range(7))
SIGMA_NFA = ('1', '2', '3')
Q0_NFA    = 0
F_NFA     = {4, 5, 6}

DELTA_NFA = [[set() for _ in range(len(SIGMA_NFA) + 1)] for _ in Q_NFA]

DELTA_NFA[0][0] = {1, 2, 3}

DELTA_NFA[1][1] = {4}; DELTA_NFA[1][2] = {1}; DELTA_NFA[1][3] = {1}
DELTA_NFA[2][1] = {2}; DELTA_NFA[2][2] = {5}; DELTA_NFA[2][3] = {2}
DELTA_NFA[3][1] = {3}; DELTA_NFA[3][2] = {3}; DELTA_NFA[3][3] = {6}

NFA = (Q_NFA, SIGMA_NFA, DELTA_NFA, Q0_NFA, F_NFA)


def eps_closure(delta, cur):
    stack = list(cur)
    while stack:
        s = stack.pop()
        for t in delta[s][0]:
            if t not in cur:
                cur.add(t)
                stack.append(t)
    return cur


def fmt_set(S):
    return "{" + " ".join("q" + str(s) for s in sorted(S)) + "}"


def nfa_run(w, trace=False):
    Q, SIGMA, delta, q0, F = NFA
    cur = eps_closure(delta, {q0})
    if trace:
        sys.stdout.write("  " + fmt_set(cur))
    for c in w:
        k = sym_index(SIGMA, c)
        if k == -1:
            if trace:
                print("  (символ вне алфавита)")
            return 0
        nxt = set()
        for s in cur:
            nxt |= delta[s][k + 1]
        cur = eps_closure(delta, nxt)
        if trace:
            sys.stdout.write(" -" + c + "-> " + fmt_set(cur))
    if trace:
        print()
    return 1 if cur & F else 0


def nfa_print_table():
    Q, SIGMA, delta, q0, F = NFA
    print("НКА, таблица переходов delta (столбец eps - часть delta):")
    print(" state | eps     |  1  |  2  |  3  | final")
    for s in Q:
        e  = ids_text(delta[s][0])
        c1 = ids_text(delta[s][1])
        c2 = ids_text(delta[s][2])
        c3 = ids_text(delta[s][3])
        line = " q" + str(s) + "     | " + pad(e, 8) + "| " + pad(c1, 4)
        line += "| " + pad(c2, 4) + "| " + pad(c3, 4) + "|  "
        line += "+" if s in F else "-"
        print(line)
    print("(q0 - старт, f1/f2/f3 = q4/q5/q6 - финалы)\n")


def run_suite(tests, func):
    print(" Input        | Result")
    print("--------------+---------")
    for w in tests:
        label = w if w else "(пусто)"
        print(" " + pad(label, 13) + "| " + ("Accept" if func(w) else "Reject"))
    print()


def interactive(auto_tuple, runner, name, allow_trace=True):
    Q, SIGMA, delta, q0, F = auto_tuple
    print(f"\n--- Интерактивный режим: {name} ---")
    print(f"  Алфавит: {SIGMA}")
    print(f"  Старт:   q{q0}")
    print(f"  Финал:   {{{', '.join('q' + str(s) for s in sorted(F))}}}")
    print("  Введите цепочку и Enter. Пустая строка — выход.")
    print("  Припишите '!' в конце, чтобы увидеть трассировку,")
    print("  например:  aabbb!")

    while True:
        try:
            w = input("> ")
        except EOFError:
            break

        if w == "":
            break

        trace = False
        if allow_trace and w.endswith("!"):
            trace = True
            w = w[:-1]

        bad = [c for c in w if c not in SIGMA]
        if bad:
            print(f"  Ошибка: символы {bad} не входят в алфавит {SIGMA}")
            continue

        label = w if w else "(пусто)"
        res = runner(w, trace=trace)
        print(f"  {label}: " + ("Accept" if res else "Reject"))


if __name__ == "__main__":
    print("=== ЧАСТЬ А: ДКА  #a=2 и #b>2 ===\n")
    dfa_print_table()
    run_suite(["aabbb", "aabb", "ab", "aaabbb", "bbbaa",
               "", "aabbbbbb", "bbbbb", "aa"], dfa_run)
    print("Трассировка \"aabbb\":")
    dfa_run("aabbb", trace=True)

    print("\n=== ЧАСТЬ Б: НКА над {1,2,3} ===\n")
    nfa_print_table()
    run_suite(["2321", "121", "3", "231", "1231",
               "233", "", "12", "13221"], nfa_run)
    print("Трассировка \"2321\":")
    nfa_run("2321", trace=True)

    interactive(DFA, dfa_run, "ДКА (#a=2, #b>2)")
    interactive(NFA, nfa_run, "НКА (последний символ новый)")