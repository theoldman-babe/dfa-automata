# automata-lab
Implementation of a Deterministic Finite Automaton (DFA) and a Non-deterministic Finite Automaton (NFA) in Python, applying theoretical concepts from formal languages and automata theory.

# Deterministic Finite Automaton (DFA) — Python Implementation

This project comes directly from my **formal languages and automata** course this semester.
The goal was simple: go from the formal definition of a DFA to a concrete implementation, and verify that both describe exactly the same thing. The course gave me the theory — I just had to figure out how to make it run.

---

## What is a DFA?

Formally, an automaton is a **quintuplet** A = (Σ, E, I, F, T) where:

- **Σ** — an alphabet (the set of allowed symbols)
- **E** — a finite set of states
- **I ⊆ E** — the set of initial states
- **F ⊆ E** — the set of final states
- **T ⊆ E × Σ × E** — the set of transitions

A transition (p, a, q) means: *"from state p, reading symbol a, go to state q."*

**This is extracted from the course of my university*

---

A **concrete example** from the course:

```
A1 = (Σ = {a,b},  E = {p,q,r},  I = {p},  F = {r})

T = { (p,a,p), (p,b,p), (p,a,q), (q,b,r), (r,a,r), (r,b,r) }
```

Which gives the following diagram:

```
         a                    a
         ↙                    ↖
  --> ( p ) ---a---> ( q ) ---b---> (( r ))
         ↖                           ↙
          b                         b
```

State `p` = start, nothing significant read yet  
State `q` = just read an `a`, waiting for a `b`  
State `r` = recognized the pattern → final state

---

In Python, this translates directly to:

```python
transitions = {
    'p': {'a': 'q', 'b': 'p'},
    'q': {'a': 'p', 'b': 'r'},
    'r': {'a': 'r', 'b': 'r'}
}
```

The structure `dict[state][symbol] → next_state` is literally the function
**δ : E × Σ → E** from the formal definition.
The code and the theory say the same thing — just in two different languages.

---

## Features

* Deterministic Finite Automaton (DFA) implementation
* Generic and reusable class design
* Multiple example automata
* Direct mapping between theory (δ function) and code
* Simple and readable structure

---

## Project structure

```
dfa_project.py — DFA implementation
nfa_project.py — NFA implementation
```

---

## The DFA class

```python
class DFA:
    def __init__(self, etat_initial: int, transitions: dict, etats_finaux: set):
        ...
    def accepte(self, mot: str) -> bool:
        ...
```

Parameters:
* `etat_initial` — integer representing the starting state
* `transitions` — dictionary `{state: {symbol: next_state}}`
* `etats_finaux` — set of accepting states

---

## Example usage

```python
# DFA: words containing at least one 'a'
transitions = {
    0: {'a': 1, 'b': 0},
    1: {'a': 1, 'b': 1}
}

dfa = DFA(etat_initial=0, transitions=transitions, etats_finaux={1})

dfa.accepte("bbb")     # False
dfa.accepte("bbab")    # True
dfa.accepte("")        # False
```

```python
# DFA: words containing the substring "ab"
transitions_2 = {
    0: {'a': 1, 'b': 0},
    1: {'a': 1, 'b': 2},
    2: {'a': 2, 'b': 2}   # once "ab" is seen, always accepted
}

dfa2 = DFA(etat_initial=0, transitions=transitions_2, etats_finaux={2})

dfa2.accepte("ab")      # True
dfa2.accepte("aab")     # True
dfa2.accepte("ba")      # False
```

---

## What I learned

Implementing the automaton forced me to really understand what "deterministic" means:
for each state and each symbol, there is **exactly one possible transition**.

I also realized that the structure `dict[state][symbol] -> next_state` is literally the transition function
δ : Q × Σ → Q from the course — the code and the formal definition map one-to-one.

Refactoring the code into a class made sense naturally, a DFA has state, and so does an object.

---

---

# Non-deterministic Finite Automaton (NFA) — Python Implementation

After finishing the DFA, I went looking online to see what came next in automata theory.
That's when I found the concept of **non-deterministic finite automata**.
It took me a moment to really understand what "non-deterministic" meant in practice — so I dug into it, and then implemented it myself to make sure I actually got it.

---

## What is an NFA?

An NFA has the same structure as a DFA — states, an alphabet, transitions, a start state, final states.
The difference is in the transitions: **at the same state, reading the same letter, you can go to multiple states at once**. And on top of that, there are **epsilon (ε) transitions** — transitions that move to another state without reading any letter at all.

The way to think about it: instead of one cursor moving through the automaton, you have **a cloud of cursors** (clones). Every time there's a choice, all possibilities are explored simultaneously. If *at least one* clone ends up on a final state at the end of the word — the word is accepted.

---

## The key concept: epsilon-closure

When you're in a state that has epsilon transitions, you automatically follow them — for free, without reading anything. The **epsilon-closure** of a set of states is all the states you can reach just by following epsilon transitions (including the states you started from).

```
Example:
q0 --ε--> q1 --ε--> q2

epsilon_closure({q0}) = {q0, q1, q2}
```

This is computed at every step — before reading a letter and after moving.

---

## How `accepte` works

```
1. Start from the epsilon-closure of the initial state
2. For each letter in the word:
      a. Move all current states using that letter  → deplacement_simple
      b. Expand the result with epsilon-closure     → fermeture_epsilon
      c. If the cloud of states is empty: return False immediately
3. At the end: check if any current state is a final state
```

---

## The NFA class

```python
class NFA:
    def __init__(self, etat_initial, transitions: dict, etats_finaux: set):
        ...
    def fermeture_epsilon(self, etats_departs: set) -> set:
        ...
    def deplacement_simple(self, etats_actuel: set, lettre) -> set:
        ...
    def accepte(self, mot: str) -> bool:
        ...
```

Parameters:
* `etat_initial` — the starting state
* `transitions` — dictionary `{state: {symbol: set_of_next_states}}` — note: values are **sets**, not single states
* `etats_finaux` — set of accepting states

The key structural difference from DFA: `transitions[state][symbol]` returns a **set** of states, not just one.

---

## Example usage

```python
# NFA: words that contain "ab" — non-deterministic version
# At each 'a', the automaton clones itself: one clone stays on q0, one moves to q1
transitions = {
    'q0': {'a': {'q0', 'q1'}, 'b': {'q0'}},
    'q1': {'b': {'q2'}},
}

nfa = NFA(etat_initial='q0', transitions=transitions, etats_finaux={'q2'})

nfa.accepte("ab")    # True
nfa.accepte("aab")   # True  — loop on q0, then "ab"
nfa.accepte("b")     # False
nfa.accepte("")      # False
```

```python
# NFA with epsilon transitions: accepts either 'a' or 'b'
# q0 clones into q1 and q2 via epsilon, before reading anything
transitions = {
    'q0': {'': {'q1', 'q2'}},   # ε-transitions
    'q1': {'a': {'q3'}},
    'q2': {'b': {'q3'}},
}

nfa2 = NFA(etat_initial='q0', transitions=transitions, etats_finaux={'q3'})

nfa2.accepte("a")    # True
nfa2.accepte("b")    # True
nfa2.accepte("ab")   # False — q3 has no outgoing transitions
nfa2.accepte("")     # False — q3 never reached
```

---

## DFA vs NFA — what actually changes

| | DFA | NFA |
|---|---|---|
| Transitions | one next state | a set of next states |
| Epsilon transitions | no | yes |
| Reading a letter | move to one state | expand a cloud of states |
| Acceptance | one final state reached | at least one clone on a final state |
| Implementation | simple loop | epsilon-closure + set operations |

A DFA is a special case of an NFA where every transition goes to exactly one state and there are no epsilon transitions.

---

## What I learned

The hardest part wasn't the code — it was understanding what non-determinism actually means here.
It's not randomness. It's exploring all possible paths at once, and accepting if any of them works.

Once I understood the "cloud of clones" mental model, the implementation followed naturally:
- `fermeture_epsilon` → expand the cloud along epsilon transitions (DFS with a stack)
- `deplacement_simple` → move the whole cloud forward by one letter
- `accepte` → alternate between the two, check at the end

The `set` data structure does all the heavy lifting — merging possible states with `update`, checking intersection with `&`.

---

## Next steps

* [ ] Add alphabet validation at initialization
* [ ] NFA → DFA conversion (subset construction)
* [ ] DFA minimization (Hopcroft's algorithm)

---

## Run the project

No external dependencies required.

```bash
python dfa_project.py
python nfa_project.py
```

---

*Personal project — first-year Computer Science student, based on formal languages and automata coursework.*
