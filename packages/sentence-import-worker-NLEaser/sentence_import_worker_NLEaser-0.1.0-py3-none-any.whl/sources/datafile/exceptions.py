class FileReadException(Exception):
    # Ocorreu um erro ao ler o arquivo, possivelmente por conta do formato incorreto.
    pass


class InvalidFormatException(Exception):
    # O formato informado não possui suporte, ainda.
    pass


class TextColumnNotFound(Exception):
    pass


class NotAuthorized(Exception):
    # O usuário não tem permissão para realizar algum acesso/modificação
    pass