"""Regras comuns às duas implementações."""
from paa.models import Instance, Solution


def validate_instance(instance: Instance) -> None:
    """Rejeitar entradas fora do domínio do problema com ValueError."""
    raise NotImplementedError("Definir domínio e restrições do problema em conjunto.")


def validate_solution(instance: Instance, solution: Solution) -> None:
    """Verificar viabilidade e recalcular o objetivo; rejeitar com ValueError.

    A otimalidade deve ser demonstrada separadamente.
    """
    raise NotImplementedError("Definir restrições e função objetivo em conjunto.")
