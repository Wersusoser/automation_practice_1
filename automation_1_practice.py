#   Variant 2:
#   DFA: количество a РОВНО 2, количество b БОЛЬШЕ 2, алфавит {a,b}
#   NFA: последний символ цепочки раньше не встречался, алфавит {1,2,3}

from enum import Enum


class DFA:
    TOTAL_STATES = 13
    FINAL_STATES = 1
    ALPHABET_CHARCTERS = 2

    UNKNOWN_SYMBOL_ERR = 0
    NOT_REACHED_FINAL_STATE = 1
    REACHED_FINAL_STATE = 2

    class DFA_STATES(Enum):
        q0, q1, q2, q3, q4, q5, q6, q7, q8, q9, q10, q11, q12 = range(13)

    class Input(Enum):
        _A, _B = range(2)

    g_Accepted_states = [DFA_STATES.q11.value]                       # The set F
    g_alphabet = ['a', 'b']                                          # The set Sigma

    g_Transition_Table = []                                          # Transition function
    for _ in range(TOTAL_STATES):
        row = []
        for _ in range(ALPHABET_CHARCTERS):
            row.append(0)
        g_Transition_Table.append(row)

    g_Current_state = DFA_STATES.q0.value                            # Start state of DFA

    @classmethod
    def SetDFA_Transitions(cls):
        for i in range(0, 3):
            for j in range(0, 4):
                s = i * 4 + j
                cls.g_Transition_Table[s][cls.Input._A.value] = (i + 1) * 4 + j if i < 2 else 12
                cls.g_Transition_Table[s][cls.Input._B.value] = i * 4 + (j + 1) if j < 3 else i * 4 + 3
        cls.g_Transition_Table[12][cls.Input._A.value] = 12
        cls.g_Transition_Table[12][cls.Input._B.value] = 12

    @classmethod
    def DFA(cls, current_symbol):
        pos = 0
        while pos < cls.ALPHABET_CHARCTERS:
            if current_symbol == cls.g_alphabet[pos]:
                break
            pos += 1
        if cls.ALPHABET_CHARCTERS == pos:
            return cls.UNKNOWN_SYMBOL_ERR
        for i in range(cls.FINAL_STATES):
            cls.g_Current_state = cls.g_Transition_Table[cls.g_Current_state][pos]
            if cls.g_Current_state == cls.g_Accepted_states[i]:
                return cls.REACHED_FINAL_STATE
        return cls.NOT_REACHED_FINAL_STATE

    @classmethod
    def ResetDFA(cls):
        cls.g_Current_state = cls.DFA_STATES.q0.value


class NFA:
    TOTAL_STATES = 7
    FINAL_STATES = 3
    ALPHABET_CHARCTERS = 3

    UNKNOWN_SYMBOL_ERR = 0
    NOT_REACHED_FINAL_STATE = 1
    REACHED_FINAL_STATE = 2

    class NFA_STATES(Enum):
        q0, q1, q2, q3, f1, f2, f3 = range(7)

    class Input(Enum):
        _1, _2, _3 = range(3)

    g_Accepted_states = [NFA_STATES.f1.value, NFA_STATES.f2.value, NFA_STATES.f3.value]  # The set F
    g_alphabet = ['1', '2', '3']                                     # The set Sigma

    g_Transition_Table = []                                          # Transition function (set-valued)
    for _ in range(TOTAL_STATES):
        row = []
        for _ in range(ALPHABET_CHARCTERS):
            row.append([])
        g_Transition_Table.append(row)

    g_Epsilon_Transitions = []                                       # eps-переходы (доп. таблица)
    for _ in range(TOTAL_STATES):
        g_Epsilon_Transitions.append([])

    g_Current_states = [False] * TOTAL_STATES                        # Start "state" (множество) of NFA

    @classmethod
    def SetNFA_Transitions(cls):
        cls.g_Epsilon_Transitions[cls.NFA_STATES.q0.value] = [
            cls.NFA_STATES.q1.value, cls.NFA_STATES.q2.value, cls.NFA_STATES.q3.value
        ]

        cls.g_Transition_Table[cls.NFA_STATES.q1.value][cls.Input._2.value] = [cls.NFA_STATES.q1.value]
        cls.g_Transition_Table[cls.NFA_STATES.q1.value][cls.Input._3.value] = [cls.NFA_STATES.q1.value]
        cls.g_Transition_Table[cls.NFA_STATES.q1.value][cls.Input._1.value] = [cls.NFA_STATES.f1.value]

        cls.g_Transition_Table[cls.NFA_STATES.q2.value][cls.Input._1.value] = [cls.NFA_STATES.q2.value]
        cls.g_Transition_Table[cls.NFA_STATES.q2.value][cls.Input._3.value] = [cls.NFA_STATES.q2.value]
        cls.g_Transition_Table[cls.NFA_STATES.q2.value][cls.Input._2.value] = [cls.NFA_STATES.f2.value]

        cls.g_Transition_Table[cls.NFA_STATES.q3.value][cls.Input._1.value] = [cls.NFA_STATES.q3.value]
        cls.g_Transition_Table[cls.NFA_STATES.q3.value][cls.Input._2.value] = [cls.NFA_STATES.q3.value]
        cls.g_Transition_Table[cls.NFA_STATES.q3.value][cls.Input._3.value] = [cls.NFA_STATES.f3.value]

    @classmethod
    def EpsilonClosure(cls, states_set):
        changed = True
        while changed:
            changed = False
            for s in range(cls.TOTAL_STATES):
                if states_set[s]:
                    for t in cls.g_Epsilon_Transitions[s]:
                        if not states_set[t]:
                            states_set[t] = True
                            changed = True

    @classmethod
    def ResetNFA(cls):
        cls.g_Current_states = [False] * cls.TOTAL_STATES
        cls.g_Current_states[cls.NFA_STATES.q0.value] = True
        cls.EpsilonClosure(cls.g_Current_states)

    @classmethod
    def NFA(cls, current_symbol):
        pos = 0
        while pos < cls.ALPHABET_CHARCTERS:
            if current_symbol == cls.g_alphabet[pos]:
                break
            pos += 1
        if cls.ALPHABET_CHARCTERS == pos:
            return cls.UNKNOWN_SYMBOL_ERR
        next_states = [False] * cls.TOTAL_STATES
        for s in range(cls.TOTAL_STATES):
            if cls.g_Current_states[s]:
                for t in cls.g_Transition_Table[s][pos]:
                    next_states[t] = True
        cls.EpsilonClosure(next_states)
        cls.g_Current_states = next_states
        for i in range(cls.FINAL_STATES):
            if cls.g_Current_states[cls.g_Accepted_states[i]]:
                return cls.REACHED_FINAL_STATE
        return cls.NOT_REACHED_FINAL_STATE


class Main:

    @staticmethod
    def main():
        result = -1

        DFA.SetDFA_Transitions()   # Fill transition table

        print("Enter a string with 'a' s and 'b's:")
        print("Press Enter Key to stop")

        while True:
            input_line = input()
            if len(input_line) == 0:
                break

            DFA.ResetDFA()

            i = 0
            while i < len(input_line):
                c = input_line[i]
                if c == '\n':
                    break
                result = DFA.DFA(c)
                if DFA.REACHED_FINAL_STATE != result and DFA.NOT_REACHED_FINAL_STATE != result:
                    break
                i += 1

            if DFA.REACHED_FINAL_STATE == result:
                print("Accepted")
            else:
                print("Rejected")
            print()

        NFA.SetNFA_Transitions()   # Fill transition table

        print("Enter a string with '1' s, '2's and '3's:")
        print("Press Enter Key to stop")

        while True:
            input_line = input()
            if len(input_line) == 0:
                break

            NFA.ResetNFA()
            i = 0
            while i < len(input_line):
                c = input_line[i]
                if c == '\n':
                    break
                result = NFA.NFA(c)
                if NFA.REACHED_FINAL_STATE != result and NFA.NOT_REACHED_FINAL_STATE != result:
                    break
                i += 1

            if NFA.REACHED_FINAL_STATE == result:
                print("Accepted")
            else:
                print("Rejected")
            print()


if __name__ == "__main__":
    Main.main()
