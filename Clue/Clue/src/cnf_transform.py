"""
cnf_transform.py — Transformaciones a Forma Normal Conjuntiva (CNF).
El pipeline completo to_cnf() llama a todas las transformaciones en orden.
"""

from __future__ import annotations

from logic_core import And, Atom, Formula, Not, Or, Implies, Iff


# --- FUNCION GUÍA SUMINISTRADA COMPLETA ---


def eliminate_double_negation(formula: Formula) -> Formula:
    """
    Elimina dobles negaciones recursivamente.

    Transformacion:
        Not(Not(a)) -> a

    Se aplica recursivamente hasta que no queden dobles negaciones.

    Ejemplo:
        >>> eliminate_double_negation(Not(Not(Atom('p'))))
        Atom('p')
        >>> eliminate_double_negation(Not(Not(Not(Atom('p')))))
        Not(Atom('p'))
    """
    if isinstance(formula, Atom):
        return formula
    if isinstance(formula, Not):
        if isinstance(formula.operand, Not):
            return eliminate_double_negation(formula.operand.operand)
        return Not(eliminate_double_negation(formula.operand))
    if isinstance(formula, And):
        return And(*(eliminate_double_negation(c) for c in formula.conjuncts))
    if isinstance(formula, Or):
        return Or(*(eliminate_double_negation(d) for d in formula.disjuncts))
    return formula


# --- FUNCIONES QUE DEBEN IMPLEMENTAR ---


def eliminate_iff(formula: Formula) -> Formula:
    if isinstance(formula, Atom):
        return formula
    if isinstance(formula, Not):
        return Not(eliminate_iff(formula.operand))
    if isinstance(formula, And):
        return And(*(eliminate_iff(c) for c in formula.conjuncts))
    if isinstance(formula, Or):
        return Or(*(eliminate_iff(d) for d in formula.disjuncts))
    if isinstance(formula, Implies):
        return Implies(
            eliminate_iff(formula.antecedent),
            eliminate_iff(formula.consequent),
        )
    if isinstance(formula, Iff):
        left = eliminate_iff(formula.left)
        right = eliminate_iff(formula.right)
        return And(Implies(left, right), Implies(right, left))
    return formula


def eliminate_implication(formula: Formula) -> Formula:
    if isinstance(formula, Atom):
        return formula
    if isinstance(formula, Not):
        return Not(eliminate_implication(formula.operand))
    if isinstance(formula, And):
        return And(*(eliminate_implication(c) for c in formula.conjuncts))
    if isinstance(formula, Or):
        return Or(*(eliminate_implication(d) for d in formula.disjuncts))
    if isinstance(formula, Implies):
        antecedent = eliminate_implication(formula.antecedent)
        consequent = eliminate_implication(formula.consequent)
        return Or(Not(antecedent), consequent)
    if isinstance(formula, Iff):
        return Iff(
            eliminate_implication(formula.left),
            eliminate_implication(formula.right),
        )
    return formula


def push_negation_inward(formula: Formula) -> Formula:
    if isinstance(formula, Atom):
        return formula
    if isinstance(formula, Not):
        operand = formula.operand
        if isinstance(operand, Atom):
            return formula
        if isinstance(operand, Not):
            return push_negation_inward(operand.operand)
        if isinstance(operand, And):
            return Or(*(push_negation_inward(Not(c)) for c in operand.conjuncts))
        if isinstance(operand, Or):
            return And(*(push_negation_inward(Not(d)) for d in operand.disjuncts))
        return Not(push_negation_inward(operand))
    if isinstance(formula, And):
        return And(*(push_negation_inward(c) for c in formula.conjuncts))
    if isinstance(formula, Or):
        return Or(*(push_negation_inward(d) for d in formula.disjuncts))
    return formula


def distribute_or_over_and(formula: Formula) -> Formula:
    if isinstance(formula, (Atom, Not)):
        return formula
    if isinstance(formula, And):
        return And(*(distribute_or_over_and(c) for c in formula.conjuncts))
    if isinstance(formula, Or):
        distributed_children = [distribute_or_over_and(d) for d in formula.disjuncts]

        and_child = None
        for child in distributed_children:
            if isinstance(child, And):
                and_child = child
                break

        if and_child is None:
            return Or(*distributed_children)

        others = [child for child in distributed_children if child is not and_child]

        new_conjuncts = []
        for conjunct in and_child.conjuncts:
            new_disjuncts = others + [conjunct]
            if len(new_disjuncts) == 1:
                new_formula = new_disjuncts[0]
            else:
                new_formula = Or(*new_disjuncts)
            new_conjuncts.append(distribute_or_over_and(new_formula))

        if len(new_conjuncts) == 1:
            return new_conjuncts[0]
        return And(*new_conjuncts)

    return formula


def flatten(formula: Formula) -> Formula:
    if isinstance(formula, Atom):
        return formula
    if isinstance(formula, Not):
        return Not(flatten(formula.operand))
    if isinstance(formula, And):
        flat_conjuncts = []
        for conjunct in formula.conjuncts:
            flattened = flatten(conjunct)
            if isinstance(flattened, And):
                flat_conjuncts.extend(flattened.conjuncts)
            else:
                flat_conjuncts.append(flattened)

        if len(flat_conjuncts) == 1:
            return flat_conjuncts[0]
        return And(*flat_conjuncts)

    if isinstance(formula, Or):
        flat_disjuncts = []
        for disjunct in formula.disjuncts:
            flattened = flatten(disjunct)
            if isinstance(flattened, Or):
                flat_disjuncts.extend(flattened.disjuncts)
            else:
                flat_disjuncts.append(flattened)

        if len(flat_disjuncts) == 1:
            return flat_disjuncts[0]
        return Or(*flat_disjuncts)

    return formula



# --- PIPELINE COMPLETO ---


def to_cnf(formula: Formula) -> Formula:
    """
    [DADO] Pipeline completo de conversion a CNF.

    Aplica todas las transformaciones en el orden correcto:
    1. Eliminar bicondicionales (Iff)
    2. Eliminar implicaciones (Implies)
    3. Mover negaciones hacia adentro (Not)
    4. Eliminar dobles negaciones (Not Not)
    5. Distribuir Or sobre And
    6. Aplanar conjunciones/disyunciones

    Ejemplo:
        >>> to_cnf(Implies(Atom('p'), And(Atom('q'), Atom('r'))))
        And(Or(Not(Atom('p')), Atom('q')), Or(Not(Atom('p')), Atom('r')))
    """
    formula = eliminate_iff(formula)
    formula = eliminate_implication(formula)
    formula = push_negation_inward(formula)
    formula = eliminate_double_negation(formula)
    formula = distribute_or_over_and(formula)
    formula = flatten(formula)
    return formula
