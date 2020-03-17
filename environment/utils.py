def get_logistic_growth_rate(r, N, K):
    """
    Logistic growth equation, 2.14
    :param r: growth rate
    :param N: Population size
    :param K: Carrying capacity
    :return: growth rate
    """
    return r * N * (1-(N/K))