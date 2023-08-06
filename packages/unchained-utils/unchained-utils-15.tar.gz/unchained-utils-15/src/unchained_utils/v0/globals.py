import contextvars


class Globals:
    def __setattr__(self, attr, value):
        try:
            super().__getattribute__(attr)
        except:
            super().__setattr__(attr, contextvars.ContextVar(attr))
        super().__getattribute__(attr).set(value)

    def __getattribute__(self, attr):
        try:
            if attr == '__dict__':
                return {k: v.get() for k, v in super(Globals, self).__getattribute__(attr).items()}
            else:
                return super().__getattribute__(attr).get()
        except:
            return None


g = Globals()


