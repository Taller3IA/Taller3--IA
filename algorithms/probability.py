"""Punto 1. Distribuciones discretas y decisiones de respuesta."""
import math 


def normalize(weights: dict) -> dict:
    """Retorna un diccionario nuevo cuyas probabilidades suman uno.

    Entrada: weights = {resultado: peso}.
    Salida: {resultado: probabilidad}, con las mismas claves.

    Tips:
    - Conserve las claves y su orden; no modifique weights.
    - Rechace pesos negativos, no finitos, diccionarios vacíos y suma cero.
    """

    if not weights:
        raise ValueError("Diccionario vacío")

    for peso in weights.values():
        if peso < 0:
            raise ValueError("Peso negativo")

        elif not math.isfinite(peso):
            raise ValueError("Peso no finito")

        elif sum(weights.values()) == 0:
            raise ValueError("Suma da 0")

    else:

        rta = {}

        sumas_pesos = sum(weights.values())

        for clave in weights:
            rta[clave] = weights[clave] / sumas_pesos

        return rta


def expected_utility(distribution: dict, utilities: dict) -> float:
    """Calcula sum_s P(s) U(s) para una acción.

    Entradas: distribution = {resultado: probabilidad} y
    utilities = {resultado: utilidad} para una sola acción.
    Salida: un número con la utilidad esperada.

    Tips:
    - distribution ya debe estar normalizada; no normalice utilidades.
    - Ambas tablas deben contener los mismos resultados posibles.
    """
    # Validación de las entradas; no modificar.
    if set(distribution) != set(utilities) or not distribution:
        raise ValueError("Probabilidades y utilidades deben tener las mismas claves")
    if any(not math.isfinite(p) or p < 0 for p in distribution.values()):
        raise ValueError("Distribución inválida")
    if not math.isclose(sum(distribution.values()), 1, abs_tol=1e-9):
        raise ValueError("La distribución debe sumar uno")
    if any(not math.isfinite(u) for u in utilities.values()):
        raise ValueError("Utilidades no finitas")

    utilidad = 0

    for d in distribution:
        utilidad += distribution[d]*utilities[d]

    return utilidad


def best_action(distribution: dict, actions: dict) -> tuple[str, dict]:
    """Retorna (nombre de acción, utilidades esperadas por acción).

    Entradas: distribution = {resultado: probabilidad} y
    actions = {acción: {resultado: utilidad}}.
    Salida: (acción elegida, {acción: utilidad esperada}).

    Tips:
    - actions asocia cada acción con su tabla de utilidades.
    - Reutilice expected_utility y conserve la primera acción en los empates.
    """
    # Validación de las acciones; no modificar.
    if not actions:
        raise ValueError("Se requiere al menos una acción")

    mejor = None
    utilidades = {}

    for a, t in actions.items():
        utilidades[a] = expected_utility(distribution, t)
        

    mejor = max(utilidades, key=utilidades.get)

    return (mejor, utilidades)

    
        

    
    
