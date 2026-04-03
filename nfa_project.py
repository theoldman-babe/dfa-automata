class NFA:
    def __init__(self,etat_initial,transitions,etats_finaux):
        self.etat_initial=etat_initial
        self.transitions=transitions
        self.etats_finaux=etats_finaux

    def fermeture_epsilon(self,etats_departs:set)-> set:
        """Retourne la fermeture epsilon d'un ensemble d'états.

        La fermeture epsilon d'un ensemble d'états est l'ensemble de tous les états
        accessibles à partir de ces états en suivant des transitions étiquetées par
        epsilon (c'est-à-dire des transitions qui ne consomment aucun symbole).

        """
        fermeture=set(etats_departs)   #les etats de depars sont touujours inclues dans la fermeture
        pile=list(etats_departs)      

        while pile:
            etat=pile.pop()  #je prends le dernier elet de ma pile

            transition_etat_actu=self.transitions.get(etat,{}) #ça renvoie set vide si c vide

            if '' in transition_etat_actu:
                for c in transition_etat_actu[''] :
                    if c not in fermeture:
                        fermeture.add(c)
                        pile.append(c)
        return fermeture

    # deifniton de la fonction de déplacement 
    def deplacement_simple(self,etats_actuel:set, lettre):
        nouveaux_etats=set()
        for e in etats_actuel:
            transitions_possibles=self.transitions.get(e,{})  # si notre e finit dans un puit il ignore simpleement
            if lettre in transitions_possibles:
                nouveaux_etats.update(transitions_possibles[lettre])   #j'utilse update pour fusionnner deux sets

        return nouveaux_etats

    # pour la fonction accpepte, on calcule d'abord la fermeture epsilon pour savoir où on est
    # et après je fais un deplacement simple avec une lettre et je recalcule la fermeture epsilon 
    # à la fin je véirifie si nos etats finaux inter ce que notre fonction renvoie est different du vide {}
    def accepte(self,mot):

        etats_actu=self.fermeture_epsilon({self.etat_initial}) #je transforme le type d'etat intial en set au lieu de laisser comme elt

        for l in mot:
            prochains_etats=self.deplacement_simple(etats_actu,l)   #on fait tous les déplacement possible avec la lettre
            etats_actu=self.fermeture_epsilon(prochains_etats)   #on déploie les clone via les transitions epsilon
            if not etats_actu:   #si le nuage d'états est vide, tous les clones ont disparu
                return False
        # victoire si au moins un clone termine sur un état final (on fait l'intersection)
        return len(etats_actu & self.etats_finaux) > 0
    
#  TESTS

#  TEST 1 : chaîne epsilon pure 
# q0 --ε--> q1 --ε--> q2 (final)
# Sans lire aucune lettre, on doit atteindre q2

nfa1 = NFA(
    etat_initial='q0',
    transitions={
        'q0': {'': {'q1'}},
        'q1': {'': {'q2'}},
    },
    etats_finaux={'q2'}
)

print(nfa1.fermeture_epsilon({'q0'}))  # {'q0', 'q1', 'q2'}
print(nfa1.accepte(''))   # True  — mot vide accepté avec epsilon
print(nfa1.accepte('a'))  # False — aucune transition sur 'a'


#  TEST 2 : NFA simple, plusieurs clones 
# Accepte tous les mots qui contiennent "ab"
# q0 boucle sur lui-même

nfa2 = NFA(
    etat_initial='q0',
    transitions={
        'q0': {'a': {'q0', 'q1'}, 'b': {'q0'}},
        'q1': {'b': {'q2'}},
    },
    etats_finaux={'q2'}
)

print(nfa2.accepte('ab'))   # True
print(nfa2.accepte('aab'))  # True  (boucle puis ab)
print(nfa2.accepte('abb'))  # True  ( ab trouvé, le b de fin finit sur q0)
print(nfa2.accepte('b'))    # False
print(nfa2.accepte('a'))    # False
print(nfa2.accepte(''))     # False


# TEST 3 :
# q0 se clone vers q1 et q2 via epsilon
# q1 lit 'a', q2 lit 'b' -> les deux mènent à q3 (final)

nfa3 = NFA(
    etat_initial='q0',
    transitions={
        'q0': {'': {'q1', 'q2'}},
        'q1': {'a': {'q3'}},
        'q2': {'b': {'q3'}},
    },
    etats_finaux={'q3'}
)

print(nfa3.accepte('a'))   # True
print(nfa3.accepte('b'))   # True
print(nfa3.accepte('ab'))  # False  (q3 n'a aucune transition)
print(nfa3.accepte(''))    # False  (q3 pas atteint) 


# TEST 4 : puit 
# q1 n'est pas dans les transitions -> le set des états sera vide

nfa4 = NFA(
    etat_initial='q0',
    transitions={
       'q0': {'a': {'q1'}, 'b': {'q2'}},   # q1 absent (il mène à un puit)
       
    },
    etats_finaux={'q2'}
)

print(nfa4.accepte('b'))   # True
print(nfa4.accepte('a'))   # False (on tombe dans le puit q1)
print(nfa4.accepte('ab'))  # False (après 'a' on est dans un puit)

# TEST 5
#  état initial = état final 
# q0 est final dès le départ -> mot vide accepté
# 'a' boucle sur q0, donc a* est accepté

nfa5 = NFA(
    etat_initial='q0',
    transitions={
        'q0': {'a': {'q0'}},
    },
    etats_finaux={'q0'}
)

print(nfa5.accepte(''))     # True  — q0 est déjà final
print(nfa5.accepte('a'))    # True  — boucle, reste sur q0
print(nfa5.accepte('aaa'))  # True
print(nfa5.accepte('b'))    # False —  c vide après'b'
print(nfa5.accepte('ab'))   # False
print(nfa5.accepte('abbbb'))    # False