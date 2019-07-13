class Var:
    """
    Makes string from var name and sets it to var
    """

    def __init__(self, value=None):
        self.value = value

    def __set_name__(self, owner, val):
        if not self.value:
            self.value = val

    def __get__(self, instance, owner):
        return self.value
