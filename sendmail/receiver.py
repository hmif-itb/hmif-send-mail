class Entity:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

class MailReceiverEntity(Entity):
    def __init__(self, **kwargs):
        Entity.__init__(self, **kwargs)
