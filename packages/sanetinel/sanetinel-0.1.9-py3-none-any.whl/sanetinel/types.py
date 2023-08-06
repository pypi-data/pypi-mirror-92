# (c) 2020 Simon Rovder and others.
# This file is subject to the terms provided in 'LICENSE'.
"""
File providing public types and interfaces.
"""
import abc
import typing as t


class Sanetinel(abc.ABC):
    """
    [TODO document what this actually does, give examples.]
    """
    @property
    @abc.abstractmethod
    def name(self) -> str:
        """
        Gets the name of the system that this Sanetinel is tracking.

        :returns: The name of the system that this Sanetinel is tracking.
        """

    @abc.abstractmethod
    def reset(self):
        """
        Rests the Sanetinel, clearing all data and returning to train mode.
        """

    @abc.abstractmethod
    def log(self, channel: str, value: float) -> float:
        """
        Logs the given value against the provided channel.

        When in train mode, the value will be recorded.
        When in test mode, the value will be checked.
        When in 'off' mode, the value will be ignored.

        .. code-block:: python

            s.test('experiment1')
            s.log('x', 1)
            s.log('x', 2)
            s.log('x', 1)
            s.test('experiment2')
            s.log('x', 1)
            s.log('x', 1)
            s.log('x', 1)

        :param channel: The data channel to which the value belongs.
        :param value: The value to log.
        """

    @abc.abstractmethod
    def train(self):
        """
        Enters train mode.

        In train mode, calls to `.log` record the given datum.
        The values are not checked, and no warnings are issued.

        In train mode, the `Sanetinel` assumes that the input is fine and the
        system ran as expected. Logging in this mode accumulates expected values
        against which subsequent logged data will be checked when in test mode.
        """

    @abc.abstractmethod
    def test(self):
        """
        Enters test mode.

        In train mode, calls to `.log` validate the given datum, issuing a
        warning where the value is outside the expected distribution.

        This can be used to check that the data being logged is sane.
        """

    @abc.abstractmethod
    def off(self):
        """
        Disables logging.

        After this method is called, the `Sanetinel` instance will enter the 'off'
        state and calls to `.log` will be ignored.
        """

    @abc.abstractmethod
    def load_from_file(self, file: t.Union[str, t.TextIO]):
        """
        Loads the Sanetinel data from the given file.

        This instance will be effectively reset before loading the data.

        :param file: The file or filename from which to load the `Sanetinel` data.
        """

    @abc.abstractmethod
    def load_from_dict(self, dictionary: t.Dict[str, t.List[float]]):
        """
        Loads the Sanetinel data from the given dictionary.

        This instance will be effectively reset before loading the data.

        :param dictionary: The dictionary from which to load the `Sanetinel` data.
        """

    @abc.abstractmethod
    def dump_to_file(self, file: t.Union[str, t.TextIO]):
        """
        Dumps the current Sanetinel data to the given file.

        :param file: The file or filename to which to dump the `Sanetinel` data.
        """

    @abc.abstractmethod
    def dump_to_dict(self) -> t.Dict[str, t.List[float]]:
        """
        Dumps the current Sanetinel data to a dictionary.

        :returns: A dictionary containing the `Sanetinel` data.
        """

    @abc.abstractmethod
    def mean(self, channel: str) -> t.Optional[float]:
        """
        Computes the mean of the values recorded in train mode for the given channel.

        If no values exist for the give channel, returns `None`.

        :param channel: The channel whose values to average.
        :returns: The mean of the recorded values, or `None` if no values were recorded.
        """

    @abc.abstractmethod
    def std(self, channel: str) -> t.Optional[float]:
        """
        Computes the standard deviation of the values recorded in train mode for the given channel.

        If no values exist for the give channel, returns `None`.

        :param channel: The channel for whose values to obtain the standard deviation.
        :returns: The standard deviation of the recorded values, or `None` if no values were recorded.
        """

    @abc.abstractmethod
    def plot(self):
        """
        Plots the recorded data (both training and experiment data)
        per-channel on a line graph using `matplotlib`.

        Use `matplotlib.pyplot.show()` to display.
        """

    @abc.abstractmethod
    def __contains__(self, channel: str) -> bool:
        """
        :param channel: The name of the channel whose presence to check.
        :returns: Whether the given channel has been logged during training.
        """
