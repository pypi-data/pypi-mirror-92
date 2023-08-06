from cement import App


__APP = None


def app(app: App=None):
    global __APP

    if app is not None:
        __APP = app

    return __APP