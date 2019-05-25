class A:
    def __init__(self, a):
        self.a = 1000+a
        self.b = a**a

ob1 = A(8)
ob2 = ob1
print(ob1.a, ob2.a)