from abc import abstractmethod,ABCMeta


class CustomizeHandleProcessNotFoundError(KeyError):
    pass


class BaseHandler(metaclass=ABCMeta):

    @abstractmethod
    def handle(self, content_type: str) -> callable:
        if content_type in self.__init__handle_dict:
            return self.__init__handle_dict[content_type]
        raise CustomizeHandleProcessNotFoundError(f'未找到自定义处理器{content_type}')

    def __init__(self, handle_dict: dict):
        self.__init__handle_dict = handle_dict
