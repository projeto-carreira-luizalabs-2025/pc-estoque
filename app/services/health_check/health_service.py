from app.settings import AppSettings

from .base_health_check import BaseHealthCheck


class HealthCheckService:
    # Não pronto XXX

    def __init__(self, checkers: set[str], settings: AppSettings) -> None:
        self.checkers: dict[str, type[BaseHealthCheck]] = {}
        self._settings = settings
        self._set_checkers(checkers)

    def _set_checkers(self, checkers: set[str]) -> None: ...

    def _check_checker(self, alias: str): ...

    async def check_status(self, alias: str) -> None: ...


__all__ = ["HealthCheckService"]
