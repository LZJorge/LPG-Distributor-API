from fastapi import Response
from app.core.application.response.base_response import Response as BaseResponse


def handle_service_result(result: BaseResponse, response: Response) -> Response:
    if not result or not result.success:
        response.status_code = result.status_code
