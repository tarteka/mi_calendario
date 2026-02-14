class LoginError(Exception):
    """Error cuando las credenciales son incorrectas"""
    pass


class DownloadError(Exception):
    """Error cuando no se pueden descargar los datos"""
    pass