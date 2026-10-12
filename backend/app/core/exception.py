from fastapi import status


class AppException(Exception):
    def __init__(
        self,
        message: str,
        status_code: int = status.HTTP_400_BAD_REQUEST,
        explanation: str | None = None,
    ):
        self.message = message
        self.status_code = status_code
        self.explanation = explanation or message


class NotFoundError(AppException):
    def __init__(self, resource_name: str):
        message = f"{resource_name} not found."
        super().__init__(message, status.HTTP_404_NOT_FOUND)
