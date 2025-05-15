def epsilon_closure(transitions, state_set):
    stack = list(state_set)
    closure = set(state_set)

    while stack:
        state = stack.pop()
        if state in transitions and 'ε' in transitions[state]:
            for next_state in transitions[state]['ε']:
                if next_state not in closure:
                    closure.add(next_state)
                    stack.append(next_state)

    return closure

def move(transitions, state_set, symbol):
    result = set()
    for state in state_set:
        result.update(transitions.get(state, {}).get(symbol, []))
    return result

def nfa_to_dfa(nfa_states, alphabet, transitions, start_state, final_states):
    alphabet = [a for a in alphabet if a != 'ε']  # any alphabet without ε

    dfa_states = []  
    dfa_transitions = {}
    dfa_final_states = set()

    start_closure = frozenset(epsilon_closure(transitions, {start_state}))
    print(f"{start_closure}/n")
    unmarked_states = [start_closure]

    state_name_map = {start_closure: 'A'}
    state_counter = 1

    while unmarked_states:
        current = unmarked_states.pop(0)
        current_name = state_name_map[current]
        dfa_transitions[current_name] = {}

        for symbol in alphabet:
            move_result = move(transitions, current, symbol)
            closure = frozenset(epsilon_closure(transitions, move_result))
            if not closure:
                continue
            if closure not in state_name_map:
                state_name_map[closure] = chr(65 + state_counter)
                unmarked_states.append(closure)
                state_counter += 1
            dfa_transitions[current_name][symbol] = state_name_map[closure]

    for state_set, name in state_name_map.items():
        if any(s in final_states for s in state_set):
            dfa_final_states.add(name)

    return {
        'states': list(state_name_map.values()),
        'start_state': 'A',
        'accept_states': list(dfa_final_states),
        'transitions': dfa_transitions
    }



nfa_states = {'s', 'p', 'q','r'}
alphabet = ['0', '1', 'ε']
transitions = {
    's': {'ε': {'r'},'0':{'q'}},
    'p': {'0': {'s','r'},'1':{'p'}},
    'r': {'ε': {'p'},'1': {'q'}},
    'q': {'ε': {'r'},'0': {'q'}}

}
start_state = 's'
final_states = {'q'}

dfa = nfa_to_dfa(nfa_states, alphabet, transitions, start_state, final_states)

print("DFA States:", dfa['states'])
print("Start State:", dfa['start_state'])
print("Accept States:", dfa['accept_states'])
print("Transitions:")
for state, trans in dfa['transitions'].items():
    for sym, dest in trans.items():
        print(f"        {state} --{sym}--> {dest}")
