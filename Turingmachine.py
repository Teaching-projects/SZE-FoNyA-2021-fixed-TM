import time
from collections import defaultdict
from dataclasses import dataclass, field


@dataclass
class TuringMachine:
    states: set[str]
    symbols: set[str]
    blank_symbol: str
    input_symbols: set[str]
    initial_state: str
    accepting_states: set[str]
    transitions: dict[tuple[str, str], tuple[str, str, int]]
    # state, symbol -> new state, new symbol, direction

    head: int = field(init=False)
    tape: defaultdict[int, str] = field(init=False)
    current_state: str = field(init=False)
    halted: bool = field(init=False, default=True)

    def initialize(self, input_symbols: dict[int, str]):
        self.head = 0
        self.halted = False
        self.current_state = self.initial_state
        self.tape = defaultdict(lambda: self.blank_symbol, input_symbols)

    def step(self):
        if self.halted:
            raise RuntimeError('A megallitott gepet nem lehet leptetni')

        try:
            state, symbol, direction = self.transitions[(self.current_state, self.tape[self.head])]
        except KeyError:
            self.halted = True
            return
        self.tape[self.head] = symbol
        self.current_state = state
        self.head += direction


    def accepted_input(self):
        if not self.halted:
            raise RuntimeError('A gep meg fut')
        return self.current_state in self.accepting_states

    def print(self, window=10):
        print('... ', end='')
        print(' '.join(self.tape[i] for i in range(self.head - window, self.head + window + 1)), end='')
        print(f' ... Allapot={self.current_state}')
        print(f'{" " * (2 * window + 4)}^')


if __name__ == '__main__':
    tm = TuringMachine(states={'s', 'a', 'b', 'c', 'H'},
                       symbols={'0', '1'},
                       blank_symbol='#',
                       input_symbols={'0', '1'},
                       initial_state='s',
                       accepting_states={'H'},
                       transitions={
                           ('s', '0'): ('s', '0', 1),
                           ('s', '1'): ('s', '1', 1),
                           ('s', '#'): ('a', '#', -1),
                           ('a', '0'): ('b', '1', 1),
                           ('a', '1'): ('c', '0', -1),
                           ('b', '0'): ('b', '0', 1),
                           ('b', '1'): ('b', '1', 1),
                           ('b', '#'): ('H', '#', 1),
                           ('c', '0'): ('b', '1', 1),
                           ('c', '1'): ('c', '0', -1),
                           ('c', '#'): ('b', '1', 1),
                       })
    
    print("Turing gep, amely az inputhoz hozzaad egyet 2-es szamrendszerben")
    value = input("Irja be a szamot!: ")
    tm.initialize(dict(enumerate(value)))

    while not tm.halted:
        tm.print()
        tm.step()
        time.sleep(1)

    print(f'Az input elfogadva: {tm.accepted_input()}')

    def to_infinity():
        index = 0
        while True:
            yield index
            index += 1

for i in to_infinity():
    value = input("Irja be a szamot!: ")
    tm.initialize(dict(enumerate(value)))

    while not tm.halted:
        tm.print()
        tm.step()
        time.sleep(1)

    print(f'Az input elfogadva: {tm.accepted_input()}')
