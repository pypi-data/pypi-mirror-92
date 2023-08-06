import typing as t


class ThresholdedLogger:
    def __init__(
        self,
        warning: t.Optional[float] = None,
        error: t.Optional[float] = None,
        critical: t.Optional[float] = None
    ):
        self._levels = (warning, error, critical)

    def log(self, logger, sigma: float, message: str, *args, **kwargs):
        warning, error, critical = self._levels
        func = logger.info
        if warning is not None and sigma >= warning:
            func = logger.warning
        if error is not None and sigma >= error:
            func = logger.error
        if critical is not None and sigma >= critical:
            func = logger.critical
        func(message, *args, **kwargs)
