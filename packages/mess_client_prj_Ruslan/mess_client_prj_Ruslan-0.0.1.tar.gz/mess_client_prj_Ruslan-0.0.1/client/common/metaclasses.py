"""Server and client check by metaclasses"""
import dis


class ClientCheck(type):
    """Client check class"""

    def __init__(self, clsname, bases, clsdict):
        methods = []
        attrs = []
        variables = []
        class_methods = []

        for method in clsdict:
            try:
                ret = dis.get_instructions(clsdict[method])
            except TypeError:
                pass
            else:
                for i in ret:
                    if i.opname == 'LOAD_GLOBAL':
                        if i.argval not in methods:
                            methods.append(i.argval)
                    elif i.opname == 'LOAD_ATTR':
                        if i.argval not in attrs:
                            attrs.append(i.argval)
                    elif i.opname == 'LOAD_FAST':
                        if i.argval not in variables:
                            variables.append(i.argval)
                    elif i.opname == 'LOAD_METHOD':
                        if i.argval not in class_methods:
                            class_methods.append(i.argval)
        for command in ('accept', 'listen', 'socket'):
            if command in class_methods:
                raise TypeError(
                    'Использование listen и accept или socket недопустимо в классе клиента')
        if 'receive_message' in methods or 'send_message' in methods:
            pass
        else:
            raise TypeError('Отсутствуют вызовы функций, работающих с сокетами классе клиента')

        super().__init__(clsname, bases, clsdict)


class ServerCheck(type):
    """Server check class"""

    def __init__(self, clsname, bases, clsdict):
        methods = []
        attrs = []
        variables = []
        class_methods = []

        for method in clsdict:
            try:
                ret = dis.get_instructions(clsdict[method])
            except TypeError:
                pass
            else:
                for i in ret:
                    if i.opname == 'LOAD_GLOBAL':
                        if i.argval not in methods:
                            methods.append(i.argval)
                    elif i.opname == 'LOAD_ATTR':
                        if i.argval not in attrs:
                            attrs.append(i.argval)
                    elif i.opname == 'LOAD_FAST':
                        if i.argval not in variables:
                            variables.append(i.argval)
                    elif i.opname == 'LOAD_METHOD':
                        if i.argval not in class_methods:
                            class_methods.append(i.argval)
        if 'connect' in methods:
            raise TypeError('Использование listen и accept или socket недопустимо в классе клиента')
        if not ('AF_INET' in methods and 'SOCK_STREAM' in methods):
            raise TypeError('Некорректная инициализация сокета')

        super().__init__(clsname, bases, clsdict)
