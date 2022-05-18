class NameCondition:
    __slots__ = "lastName", "gender", "nameSource", "count"
    
    def __init__(self, lastName, gender, nameSource, count):
        self.lastName=lastName
        self.gender=gender
        self.nameSource=nameSource
        self.count=count