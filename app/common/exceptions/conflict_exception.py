from typing import TYPE_CHECKING

from app.common.error_codes import ErrorCodes

from . import ApplicationException

if TYPE_CHECKING:
    from app.api.common.schemas.response import ErrorDetail


class ConflictException(ApplicationException):
    def __init__(
        self,
        details: list["ErrorDetail"] | None = None,
    ):
        super().__init__(
            error_info=ErrorCodes.CONFLICT.value,
            details=details,
        )