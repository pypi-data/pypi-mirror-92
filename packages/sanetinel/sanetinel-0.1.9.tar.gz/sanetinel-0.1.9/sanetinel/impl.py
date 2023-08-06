# (c) 2020 Simon Rovder and others.
# This file is subject to the terms provided in 'LICENSE'.
"""
File providing the implementation of `Sanetinel`.
"""
import copy
import json
import math
import enum
import logging
import statistics
import typing as t

from .math import linspace, pdf
from .types import Sanetinel
from .errors import UnknownChannelException
from .sanetinel_experiment import current_experiment


_logger: logging.Logger = logging.getLogger('sanetinel')


class _SanetinelMode(enum.IntEnum):
    OFF = 0  # Indicates that no logging or checking is being performed
    TRAIN = 1  # Indicates that the values are being logged
    TEST = 2  # Indicates that the values are being checked


class _Sanetinel(Sanetinel):

    # Dictionary holding all current Sanetinels by name.
    _instances: t.Dict[str, Sanetinel] = dict()

    def __init__(self, name: str):
        """
        Internal use only.

        :param name: The name of the system that this Sanetinel is tracking.
        :type name: str
        """
        self._name = name
        self._logger: logging.Logger = _logger.getChild(suffix=name)
        self._dict = dict()
        self._mode: _SanetinelMode = _SanetinelMode.TEST

    @property
    def name(self):
        return self._name

    def reset(self):
        self._dict = dict()
        self._mode = _SanetinelMode.TEST

    def log(self, channel: str, value: float) -> float:
        current_experiment.get().log(self._name, channel, value)
        if self._mode == _SanetinelMode.TRAIN:
            return self._train(channel=channel, value=value)
        elif self._mode == _SanetinelMode.TEST:
            return self._test(channel=channel, value=value)
        else:
            return 0

    def train(self):
        self._mode = _SanetinelMode.TRAIN

    def test(self):
        self._mode = _SanetinelMode.TEST

    def off(self):
        self._mode = _SanetinelMode.OFF

    def load_from_file(self, file: t.Union[str, t.TextIO]):
        if isinstance(file, str):
            with open(file, 'rb') as f:
                self._dict = json.load(f)
        else:
            self._dict = json.load(file)

    def load_from_dict(self, dictionary: t.Dict[str, t.List[float]]):
        self._dict = copy.deepcopy(dictionary)

    def dump_to_file(self, file: t.Union[str, t.TextIO]):
        if isinstance(file, str):
            with open(file, 'w') as f:
                json.dump(self._dict, f, ensure_ascii=False)
        else:
            json.dump(self._dict, file, ensure_ascii=False)

    def dump_to_dict(self) -> t.Dict[str, t.List[float]]:
        return copy.deepcopy(self._dict)

    def mean(self, channel: str) -> t.Optional[float]:
        if channel not in self:
            return None
        return statistics.mean([i['value'] for i in self._dict[channel]])

    def std(self, channel: str) -> t.Optional[float]:
        if channel not in self:
            return None
        return statistics.stdev([i['value'] for i in self._dict[channel]])

    def __contains__(self, channel: str) -> bool:
        return channel in self._dict

    def _iter_ordered_channels(self):
        """
        Method iterates over channels sorted as follows:
        First all channels that were logged to during the current experiment (in the
        order in which they were logged)
        Then all remaining channels in alphabetical order.
        """
        channels = set(self._dict.keys())
        for event in current_experiment.get().iterate_sanetinel(self._name):
            c = event['channel']
            if c in channels:
                channels.remove(c)
                yield c
        channels = list(sorted(channels))
        for c in channels:
            yield c

    def _train(self, channel: str, value: float) -> float:
        logger = self._logger.getChild(channel)
        record = dict(
            experiment=current_experiment.get().experiment_id,
            channel=channel,
            value=value
        )
        if channel not in self:
            self._dict[channel] = list()
        elif isinstance(self._dict[channel], dict):
            raise NotImplementedError("Cannot log into a compacted channel!")

        self._dict[channel].append(record)

        # This allows for numpy values to be logged into sanetinels
        if hasattr(value, 'item'):
            value = value.item()

        logger.info(
            f"[{current_experiment.get().experiment_id}] "
            f"Adding value {value} to channel {channel}",
            extra=dict(
                training=True,
                sanetinel=self._name,
                channel=channel,
                value=value,
                experiment=current_experiment.get().experiment_id
            )
        )

        return 0

    def _test(self, channel: str, value: float) -> float:
        logger = self._logger.getChild(channel)
        if channel not in self:
            # This is the case when we see a value for this channel at test time
            # but the channel was never seen at train time.
            logger.critical(
                f"[{current_experiment.get().experiment_id}] "
                f"Missing test values for channel {channel}!",
                extra=dict(
                    sanetinel=self._name,
                    channel=channel,
                    value=value,
                    missing=True,
                    experiment=current_experiment.get().experiment_id,
                )
            )
            raise UnknownChannelException(
                sanetinel_name=self.name,
                channel_name=channel,
            )
        elif len({i['value'] for i in self._dict[channel]}) == 1:
            # This is the case when we only saw a single value for this channel
            # at training time but we now received a different one.
            only = self._dict[channel][0]['value']
            if only == value:
                return 0
            else:
                logger.info(
                    f"[{current_experiment.get().experiment_id}] "
                    f"Received value '{value}' for channel '{channel}' but the "
                    f"only value ever observed at training time was '{only}'!",
                    extra=dict(
                        sanetinel=self._name,
                        channel=channel,
                        value=value,
                        mean=only,
                        only=True,
                        experiment=current_experiment.get().experiment_id,
                    )
                )
                return math.inf
        else:
            m = self.mean(channel)
            s = self.std(channel)
            deviation = abs(value - m)
            sigmas = deviation / s
            logger.info(
                f"[{current_experiment.get().experiment_id}] "
                f"Channel={channel}, Mean={m:.2f}, Std={s:.2f} Value={value:.2f}, Sigmas={sigmas:.2f}",
                extra=dict(
                    sanetinel=self._name,
                    channel=channel,
                    value=value,
                    sigmas=sigmas,
                    mean=m,
                    std=s,
                    experiment=current_experiment.get().experiment_id,
                )
            )

            return sigmas

    @staticmethod
    def _plot_row_cols(n):
        """
        If you wanted to plot n plots onto a page in either a square (x by x) or a
        rectangle (x-1 by x) shape, this function will return the (rows, cols) tuple
        that best achieves this. Basically, it solves the x*x>=n and x*(x-1)>=n
        quadratic equations and returns the one that exceeds n by the least.
        """
        x1 = math.ceil(n**0.5)
        x2 = math.ceil(0.5 + math.sqrt(1 + 4*n)/2)
        if x1*x1 < x2*(x2-1):
            return x1, x1
        else:
            return x2-1, x2

    def plot(self):
        try:
            import matplotlib
            import matplotlib.pyplot as plt
            from matplotlib.collections import LineCollection
        except ImportError as err:
            _error = "To use the Sanetinel.plot() function you must install Sanetinel with " \
                     "the plotting requirements like this: `pip install sanetinel[plotting]`."

            self._logger.critical(_error)

            raise ImportError(_error) from err

        rows, cols = _Sanetinel._plot_row_cols(len(self._dict.keys()))

        plt.suptitle(
            f"Sanetinel: {self._name} | Experiment: {current_experiment.get().experiment_id}"
        )

        channel_mapping = dict()

        for i, channel in enumerate(self._iter_ordered_channels()):
            channel_mapping[channel] = i + 1
            ax = matplotlib.pyplot.subplot(rows, cols, i + 1)
            ax.get_yaxis().set_ticks([])

            mean = self.mean(channel)
            std = self.std(channel)

            ax.set_xlabel(
                f"{channel}\n{mean:.3f} +- {std:.3f} ({(std / mean * 100):.2f}%)"
            )

            highest = pdf(mean, mean, std)

            xs = linspace(mean - 3 * std, mean + 3 * std, 100)
            ys = [pdf(x, mean, std) for x in xs]
            ax.plot(xs, ys)

            lines = list()
            colors = list()

            for experiment in self._dict[channel]:
                val = experiment['value']
                lines.append([(val, 0), (val, highest / 2)])
                colors.append('k')

            for event in current_experiment.get().iterate_sanetinel(self._name):
                c, v = event['channel'], event['value']
                if c != channel:
                    continue
                lines.append([(v, 0), (v, highest)])
                colors.append('r')

            ax.add_collection(LineCollection(lines, colors=colors))
            ax.autoscale()
            plt.subplots_adjust(wspace=0.1, hspace=0.5)

    @staticmethod
    def get_or_create_sanetinel(name):
        s = _Sanetinel._instances.get(name)
        if not s:
            s = _Sanetinel(name)
            _Sanetinel._instances[name] = s
        return s


def sanetinel(name: str) -> Sanetinel:
    """
    Gets or creates the `Sanetinel` for the given system.

    .. code-block:: python

        s = sanetinel('algorithm1')
        s.train()

        s = sanetinel('algorithm1')
        s.test()

    :param name: The name to assign to the `Sanetinel`.
    :returns: The corresponding `Sanetinel` instance.
    """
    return _Sanetinel.get_or_create_sanetinel(name)
