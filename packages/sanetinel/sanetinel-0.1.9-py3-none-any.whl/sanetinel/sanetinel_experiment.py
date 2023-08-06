# (c) 2020 Simon Rovder and others.
# This file is subject to the terms provided in 'LICENSE'.

import typing as t
import contextvars

from numbers import Number


class SanetinelExperiment:
    def __init__(self, experiment_id: str):
        self._id = experiment_id
        self._previous = None

        # TODO: Add something with more type hints because this is just sad.
        self._channel_logs: t.Optional[
            t.Dict[str, t.List[t.Dict[str, t.Union[str, Number]]]]
        ] = None

    def __enter__(self):
        self._channel_logs = dict()
        self._previous = current_experiment.set(self)

    def __exit__(self, *_, **__):
        self._channel_logs = None
        current_experiment.reset(self._previous)

    def log(self, sanetinel_name: str, channel: str, value: Number):
        if self._channel_logs is not None:
            self._channel_logs.setdefault(sanetinel_name, list()).append(
                dict(channel=channel, value=value)
            )

    def iterate_sanetinel(self, sanetinel_name):
        if self._channel_logs is not None:
            for i in self._channel_logs.get(sanetinel_name, list()):
                yield i

    @property
    def experiment_id(self) -> str:
        return self._id


"""
The current_experiment holds a reference to the current SanetinelExperiment.
Being a ContextVar allows us to have individual experiment scopes even in
an async environment. The SanetinelExperiment sets this variable itself
when its scope is entered.
"""
current_experiment = contextvars.ContextVar(
    'sanetinel_experiment',
    default=SanetinelExperiment('experiment')
)
