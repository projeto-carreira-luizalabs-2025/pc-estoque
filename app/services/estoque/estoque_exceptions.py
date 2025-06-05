from app.common.exceptions import ConflictException
from app.api.common.schemas.response import ErrorDetail


class EstoqueAlreadyExistsException(ConflictException):
    def __init__(self):
        details = [
            ErrorDetail(
                field="estoque",
                location="body",
                message="Estoque já existe",
                slug="codigo-xxx-yyy",
                ctx={},
            )
        ]
        super().__init__(details)

