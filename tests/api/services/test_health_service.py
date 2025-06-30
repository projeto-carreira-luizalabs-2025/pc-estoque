import pytest
from app.services.health_check.health_service import HealthCheckService
from app.services.health_check.base_health_check import BaseHealthCheck

class DummyChecker(BaseHealthCheck):
    async def check(self):
        return True

@pytest.fixture
def settings():
    class DummySettings:
        pass
    return DummySettings()

def test_health_check_service_init(settings):
    service = HealthCheckService(checkers={"dummy"}, settings=settings)
    assert isinstance(service, HealthCheckService)

def test_set_checkers(settings):
    service = HealthCheckService(checkers=set(), settings=settings)
    service._set_checkers({"dummy"})

def test_check_checker(settings):
    service = HealthCheckService(checkers=set(), settings=settings)
    service.checkers["dummy"] = DummyChecker
    service._check_checker("dummy")

@pytest.mark.asyncio
async def test_check_status(settings):
    service = HealthCheckService(checkers=set(), settings=settings)
    service.checkers["dummy"] = DummyChecker
    await service.check_status("dummy")