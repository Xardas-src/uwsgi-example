from server import Application


def index_handler(env):
    return {
        'text': 'Hello world!',
        'extra_header': {'Content-Type': 'text/plain'},
    }


def contacts_handler(env):
    return {
        'json': {'City!': 'Moscow'},
    }


application = Application()
application.add_handler("/", index_handler)
application.add_handler("/contacts/", contacts_handler)
