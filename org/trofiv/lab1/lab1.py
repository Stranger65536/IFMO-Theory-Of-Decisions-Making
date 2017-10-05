# coding=utf-8
from qprompt import ask_int

from org.trofiv.lab1 import MontyHallSimulation


def main():
    """
    Entry point
    """
    doors_range = ask_int("Doors range", dft=20)
    prizes_range = ask_int("Prizes range", dft=20)
    games_number = ask_int("Games number", dft=1000)
    simulation = MontyHallSimulation(doors_range=range(doors_range),
                                     prizes_range=range(prizes_range),
                                     games_number=games_number)
    simulation.run()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass
