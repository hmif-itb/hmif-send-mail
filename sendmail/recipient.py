class Entity:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

class MailRecipientEntity(Entity):
    def __init__(self, **kwargs):
        Entity.__init__(self, **kwargs)
