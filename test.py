from typing_extensions import Self


class Test:

    a : Self

a = Test.a


class Sub(Test):

    a : "Sub"
    ...

a = Sub.a