class User():
    def __init__(self, name):
        self.name = name

    def  __repr__(self):
        return "{}".format(self.name)

q = User('q')
p = User('p')
print(User.query.all())
