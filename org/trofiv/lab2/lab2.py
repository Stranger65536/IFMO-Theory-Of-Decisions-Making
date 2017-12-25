# coding=utf-8
from colorama import Fore, Style
from nash import Game
from numpy import array


def nash_equilibrium(*args):
    """
    Calculates the Nash equilibrium
    :param arr: game matrix
    """
    if len(args) == 1:
        rps = Game(args[0])
    elif len(args) == 2:
        rps = Game(args[0], args[1])
    else:
        raise ValueError('Invalid game matrix!')

    for fun in [rps.support_enumeration,
                rps.vertex_enumeration,
                rps.lemke_howson_enumeration]:
        print('Equilibriums by {}:'.format(fun))
        equilibrium = set((tuple(p1.tolist()),
                           tuple(p2.tolist()))
                          for p1, p2 in fun())

        for solution in equilibrium:
            print(solution)


def prisoners_dilemma():
    """
    Prisoner's dilemma nash equilibrium
    """
    print('{}{}{}{}'.format(
        Style.BRIGHT, Fore.GREEN, 'Prisoner\'s dilemma',
        Style.RESET_ALL))
    a = array([[2, 2], [0, 3]])
    b = array([[3, 0], [1, 1]])
    nash_equilibrium(a, b)


def rock_paper_scissors():
    """
    Rock-Paper-Scissors nash equilibrium
    """
    print('{}{}{}{}'.format(
        Style.BRIGHT, Fore.GREEN, 'Rock-Paper-Scissors',
        Style.RESET_ALL))
    a = array([[0, -1, 1], [1, 0, -1], [-1, 1, 0]])
    nash_equilibrium(a)


def main():
    """
    Entry point
    """
    prisoners_dilemma()
    rock_paper_scissors()


if __name__ == '__main__':
    main()
