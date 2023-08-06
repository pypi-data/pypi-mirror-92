import dis


class ServerVerifier(type):
    """
    Метакласс, проверяющий что в результирующем классе нет клиентских
    вызовов таких как: connect. Также проверяется, что серверный
    сокет является TCP и работает по IPv4 протоколу.
    """

    def __init__(cls, cls_name, bases, cls_dict):
        methods = []
        attrs = []
        for func in cls_dict:
            try:
                data = dis.get_instructions(cls_dict[func])
            except TypeError:
                pass
            else:
                for i in data:
                    # print(i)
                    if i.opname == 'LOAD_GLOBAL' and i.argval not in methods:
                        methods.append(i.argval)
                        # print(i)
                    elif i.opname == 'LOAD_ATTR' and i.argval not in attrs:
                        attrs.append(i.argval)

        if 'connect' in methods:
            raise TypeError(
                'Метод \"connect\" модуля socket недопустим в классе Server.')
        if not ('SOCK_STREAM' in attrs and 'AF_INET' in attrs):
            raise TypeError(
                'Сокет был инициализирован с некорректными параметрами.')
        super().__init__(cls_name, bases, cls_dict)


class ClientVerifier(type):
    """
    Метакласс, проверяющий что в результирующем классе нет серверных
    вызовов таких как: accept, listen. Также проверяется, что сокет не
    создаётся внутри конструктора класса.
    """

    def __init__(cls, cls_name, bases, cls_dict):
        methods = []
        for func in cls_dict:
            try:
                data = dis.get_instructions(cls_dict[func])
            except TypeError:
                pass
            else:
                for i in data:
                    if i.opname == 'LOAD_GLOBAL' and i.argval not in methods:
                        methods.append(i.argval)

        # print(methods)
        if 'accept' in methods or 'listen' in methods:
            raise TypeError(
                'Методы \"accept\" или \"listen\" модуля '
                'socket недопустимы в классе .')
        if 'receive_message' in methods or 'send_message' in methods:
            pass
        else:
            raise TypeError('Отсутствуют методы, работающие с сокетами.')

        super().__init__(cls_name, bases, cls_dict)
