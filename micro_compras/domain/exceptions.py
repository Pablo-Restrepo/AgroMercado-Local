class DomainError(Exception):
    """Base para errores de dominio con código y status HTTP."""
    def __init__(self, message: str, code: str = "DOMAIN_ERROR", status_code: int = 400):
        super().__init__(message)
        self.code = code
        self.status_code = status_code