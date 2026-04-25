"""
model_checking.py

Este modulo contiene las funciones de model checking proposicional.

Hint: Usa las funciones get_atoms() y evaluate() de logic_core.py.
"""

from __future__ import annotations

from src.logic_core import Formula, Atom, Not, And, Or, Implies, Iff, evaluate



def get_all_models(atoms: set[str]) -> list[dict[str, bool]]:
    """
    Genera todos los modelos posibles (asignaciones de verdad).
    Para n atomos, genera 2^n modelos.

    Args:
        atoms: Conjunto de nombres de atomos proposicionales.

    Returns:
        Lista de diccionarios, cada uno mapeando atomos a valores booleanos.

    Ejemplo:
        >>> get_all_models({'p', 'q'})
        [{'p': True, 'q': True}, {'p': True, 'q': False},
         {'p': False, 'q': True}, {'p': False, 'q': False}]

    Hint: Piensa en como representar los numeros del 0 al 2^n - 1 en binario.
          Cada bit corresponde al valor de verdad de un atomo.
    """
    # === YOUR CODE HERE ===
    atoms_list = sorted(atoms)
    n = len(atoms_list)
    models = []
    for i in range(2 ** n):          # de 0 a 2^n - 1
        model = {}
        for j, atom in enumerate(atoms_list):
            # el bit j del número i da el valor de verdad del átomo j
            model[atom] = bool((i >> (n - 1 - j)) & 1)
        models.append(model)
    return models
    
    # === END YOUR CODE ===


def check_satisfiable(formula: Formula) -> tuple[bool, dict[str, bool] | None]:
    """
    Determina si una formula es satisfacible.

    Args:
        formula: Formula logica a verificar.

    Returns:
        (True, modelo) si encuentra un modelo que la satisface.
        (False, None) si es insatisfacible.

    Ejemplo:
        >>> check_satisfiable(And(Atom('p'), Not(Atom('p'))))
        (False, None)

    Hint: Genera todos los modelos con get_all_models(), luego evalua
          la formula en cada uno usando evaluate().
    """
    # === YOUR CODE HERE ===
    atoms=formula.get_atoms()
    
    for model in get_all_models(atoms):
        if formula.evaluate(model):
            return (True, model)
    return (False, None)
       
    # === END YOUR CODE ===


def check_valid(formula: Formula) -> bool:
    """
    Determina si una formula es una tautologia (valida en todo modelo).

    Args:
        formula: Formula logica a verificar.

    Returns:
        True si la formula es verdadera en todos los modelos posibles.

    Ejemplo:
        >>> check_valid(Or(Atom('p'), Not(Atom('p'))))
        True

    Hint: Una formula es valida si y solo si su negacion es insatisfacible.
          Alternativamente, verifica que sea verdadera en TODOS los modelos.
    """
    # === YOUR CODE HERE ===
    satisfiable, _ = check_satisfiable(Not(formula)) #ver si su negación es insatisfacible
    return not satisfiable    #si lo anterior es False, entonces devuelve True

    # === END YOUR CODE ===


def check_entailment(kb: list[Formula], query: Formula) -> bool:
    """
    Determina si KB |= query (la base de conocimiento implica la consulta).

    Args:
        kb: Lista de formulas que forman la base de conocimiento.
        query: Formula que queremos verificar si se sigue de la KB.

    Returns:
        True si la query es verdadera en todos los modelos donde la KB es verdadera.

    Ejemplo:
        >>> kb = [Implies(Atom('p'), Atom('q')), Atom('p')]
        >>> check_entailment(kb, Atom('q'))
        True

    Hint: KB |= q  si y solo si  KB ^ ~q es insatisfacible.
          Es decir, no existe un modelo donde toda la KB sea verdadera
          y la query sea falsa.
    """
    # === YOUR CODE HERE ===
    if len(kb) == 0: #si no hay elementos en la base de conocimiento, se evalúa que el query sea satifacible
        kb_formula = query  
        satisfiable, _ = check_satisfiable(Not(query))
        return not satisfiable
    
    elif len(kb) == 1: #evitar errores con And()
        kb_formula = kb[0] 
    else:
        kb_formula = And(*kb)         #unir las proposiciones con And() 
        
    combined = And(kb_formula, Not(query)) #verificar el valor de verdad de KB ^ ~q
    satisfiable, _ = check_satisfiable(combined) #ver si lo anterior es insatisfacible
    return not satisfiable #si era insatisfacible, retorna True
    
    
    # === END YOUR CODE ===


def truth_table(formula: Formula) -> list[tuple[dict[str, bool], bool]]:
    """
    Genera la tabla de verdad completa de una formula.

    Args:
        formula: Formula logica.

    Returns:
        Lista de tuplas (modelo, resultado) para cada modelo posible.

    Ejemplo:
        >>> truth_table(And(Atom('p'), Atom('q')))
        [({'p': True, 'q': True}, True),
         ({'p': True, 'q': False}, False),
         ({'p': False, 'q': True}, False),
         ({'p': False, 'q': False}, False)]

    Hint: Combina get_all_models() y evaluate().
    """
# === YOUR CODE HERE ===
    atoms=formula.get_atoms()
    models=get_all_models(atoms)
    result=[]
    
    for i in models:
        value=formula.evaluate(i)
        tuplee=(i,value)
        result.append(tuplee)
    return result
    
    # === END YOUR CODE ===
