"""Main module."""


class meursingCode:
    
    def __init__(self, **kwargs):
        self.name = "Meursing version at 24 January 2021"
        for kwarg in kwargs:
            setatt(self, kwarg, kwargs[kwarg])
    
    def encode(self):
        pass

    def decode(self):
        pass

    def __repr__(self):
        pass