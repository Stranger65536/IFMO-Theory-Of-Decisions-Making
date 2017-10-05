# coding=utf-8
from multiprocessing import cpu_count
from multiprocessing.pool import ThreadPool
from random import choice, sample
from time import sleep

from numpy import asarray, empty
from preconditions import PreconditionError, preconditions

from org.trofiv.common import LoggingUtils, PlotUtils

logger = LoggingUtils.get_logger('MontyHallSimulation')


class MontyHallSimulation(object):
    """
    Monty-Hall game simulation
    """

    class MontyHallSimulationRunnable(object):
        """
        Thread for Monty-Hall game simulation with the specified doors
        and prizes number. Performs specified number of games and
        records number of wins for both door change and same door
        strategies
        """

        @property
        def same_door_choose_wins(self):
            """
            Returns number of winning games using same door strategy
            :return: number
            """
            return self._same_door_wins

        @property
        def another_door_choose_wins(self):
            """
            Returns number of winning games using another door strategy
            :return: number
            """
            return self._another_door_wins

        @preconditions(lambda games_number: games_number >= 0,
                       lambda doors_number: doors_number > 1,
                       lambda prizes_number: prizes_number > 0,
                       lambda prizes_number, doors_number:
                       prizes_number < doors_number - 1)
        def __init__(self, doors_number, prizes_number, games_number):
            self._doors_number = doors_number
            self._prizes_number = prizes_number
            self._games_number = games_number
            self._same_door_wins = 0
            self._another_door_wins = 0

        def run(self):
            """
            Starts the thread
            """
            for game in range(self._games_number):
                all_doors = set(range(self._doors_number))
                winning_doors = set(
                    sample(all_doors, self._prizes_number))
                losing_doors = all_doors - winning_doors
                original_choice = choice(list(all_doors))
                opened_door = choice(list(losing_doors))
                another_choice = choice(list(all_doors - {opened_door}))

                if original_choice in winning_doors:
                    self._same_door_wins += 1
                if another_choice in winning_doors:
                    self._another_door_wins += 1

    def __init__(self, doors_range, prizes_range, games_number):
        self._doors = list(doors_range)
        self._prizes = list(prizes_range)
        self._games_number = games_number
        self._thread_pool = ThreadPool(cpu_count())
        self._futures = {}
        self._runnables = {}
        combinations = len(self._doors) * len(self._prizes)
        self._progressbar = LoggingUtils \
            .get_progressbar(label='Combinations',
                             maxvalue=combinations)

    # noinspection PyUnusedLocal
    def _update_progressbar(self, args=None):
        """
        Increments progressbar's value
        """
        self._progressbar.update()

    def wait_futures(self):
        """
        Waits until all running futures completes
        """
        while any((True for future
                   in self._futures.values()
                   if future and not future.ready())):
            sleep(1)

    def run(self):
        """
        Runs simulation
        """

        self.submit_tasks()
        self.wait_futures()
        self._progressbar.close()
        self._futures.clear()
        another_choice_probs, same_choice_probs = \
            self.calculate_probabilities()

        probs_compare = another_choice_probs - same_choice_probs

        PlotUtils.plot_surface(
            asarray(self._doors),
            asarray(self._prizes),
            same_choice_probs,
            title='Same door probabilities surface')
        PlotUtils.plot_heatmap(
            asarray(self._doors),
            asarray(self._prizes),
            same_choice_probs,
            title='Same door probabilities heatmap')
        PlotUtils.plot_surface(
            asarray(self._doors),
            asarray(self._prizes),
            another_choice_probs,
            title='Another door probabilities surface')
        PlotUtils.plot_heatmap(
            asarray(self._doors),
            asarray(self._prizes),
            another_choice_probs,
            title='Another door probabilities heatmap')
        PlotUtils.plot_surface(
            asarray(self._doors),
            asarray(self._prizes),
            probs_compare,
            title='When to choose another door surface')
        PlotUtils.plot_heatmap(
            asarray(self._doors),
            asarray(self._prizes),
            probs_compare,
            title='When to choose another door heatmap')

    def calculate_probabilities(self):
        """
        Calculates probabilities based on finished runnables
        :return: tuple of numpy array, numpy array
        """
        same_choice_probs = empty(shape=[len(self._doors),
                                         len(self._prizes)],
                                  dtype=float)
        another_choice_probs = empty(shape=[len(self._doors),
                                            len(self._prizes)],
                                     dtype=float)
        for doors_number, prizes_number in \
                ((doors_number, prizes_number)
                 for prizes_number in self._prizes
                 for doors_number in self._doors):
            combination = (doors_number, prizes_number)
            runnable = self._runnables[combination]
            same_choice_wins = \
                runnable.same_door_choose_wins if runnable else 0
            another_choice_wins = \
                runnable.another_door_choose_wins if runnable else 0

            same_choice_probs[doors_number][prizes_number] = \
                same_choice_wins / self._games_number
            another_choice_probs[doors_number][prizes_number] = \
                another_choice_wins / self._games_number
        return another_choice_probs, same_choice_probs

    def submit_tasks(self):
        """
        Submits tasks
        """
        for doors_number, prizes_number in \
                ((doors_number, prizes_number)
                 for prizes_number in self._prizes
                 for doors_number in self._doors):
            try:
                runnable = \
                    MontyHallSimulation.MontyHallSimulationRunnable(
                        doors_number,
                        prizes_number,
                        self._games_number)
                future = self._thread_pool.apply_async(
                    func=runnable.run,
                    callback=self._update_progressbar,
                    error_callback=print)
                combination = (doors_number, prizes_number)
                self._futures[combination] = future
                self._runnables[combination] = runnable
            except PreconditionError:
                self._futures[(doors_number, prizes_number)] = None
                self._runnables[(doors_number, prizes_number)] = None
                self._update_progressbar()

