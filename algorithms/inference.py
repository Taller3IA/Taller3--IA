"""Punto 2. Inferencia exacta por enumeración."""
from algorithms.probability import normalize


def enumeration_ask(network, query: str, evidence: dict) -> dict:
    """Calcula P(query | evidence) sobre la conjunta factorizada.

    Entradas: network es la red; query es el nombre de la
    variable consultada; evidence es {nombre de variable: 0 o 1}.
    Salida: {0: probabilidad, 1: probabilidad}.

    Tips:
    - Recorra network.variables en orden topológico.
    - Para una variable fijada multiplique su probabilidad; para una oculta
      sume las dos alternativas 0 y 1. Normalice al terminar.
    - Use copias del evento y no modifique evidence.
    - network.probability(variable, valor, evento) consulta la CPT;
      el evento debe contener los valores de todos los padres.
    - Puede usar una función auxiliar recursiva. Al terminar el recorrido,
      el producto sin factores restantes vale 1.
    - Evidencia imposible: ValueError. Consulta observada: distribución puntual
      solo si la evidencia es posible.
    """
    # Valida nombres de variables y dominio de la evidencia.
    network.validate_query(query, evidence)

    def enumerate_all(variables, event):
        # Sin variables restantes el producto vale 1.
        if not variables:
            return 1.0
        var, rest = variables[0], variables[1:]
        if var in event:
            # Fijada -> multiplica su probabilidad dado el valor de sus padres.
            return network.probability(var, event[var], event) * enumerate_all(rest, event)
        # Oculta -> suma sobre sus dos valores, usando una copia del evento.
        total = 0.0
        for value in (0, 1):
            extended = dict(event)
            extended[var] = value
            total += network.probability(var, value, extended) * enumerate_all(rest, extended)
        return total

    weights = {}
    for value in (0, 1):
        # Si la consulta está observada con otro valor, ese peso es cero.
        if query in evidence and evidence[query] != value:
            weights[value] = 0.0
            continue
        event = dict(evidence)
        event[query] = value
        weights[value] = enumerate_all(network.variables, event)

    if sum(weights.values()) == 0:
        raise ValueError("Evidencia imposible")
    return normalize(weights)
    # FIN DEL BLOQUE DEL ESTUDIANTE
