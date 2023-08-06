from abc import ABC, abstractmethod

class Meal(ABC):
    @abstractmethod
    def create_starter(self):
        pass

    def create_main_course(self):
        pass

    def create_dessert(self):
        pass


class Asian_meal(Meal):
    def create_starter(self):
        return Dim_sum()

    def create_main_course(self):
        return Noodles()

    def create_dessert(self):
        return Fried_banana()


class Italian_meal(Meal):
    def create_starter(self):
        return Antipasto()

    def create_main_course(self):
        return Lasagna()

    def create_dessert(self):
        return Tiramisu()


class Starter(ABC):
    @abstractmethod
    def eatStarter(self):
        pass


class Main_course(ABC):
    @abstractmethod
    def eatMain(self):
        pass


class Dessert(ABC):
    @abstractmethod
    def eatDessert(self):
        pass


class Dim_sum(Starter):
    def eatStarter(self):
        return "dim-sum"


class Antipasto(Starter):
    def eatStarter(self):
        return "antipasto"


class Noodles(Main_course):
    def eatMain(self):
        return "noodles"


class Lasagna(Main_course):
    def eatMain(self):
        return "lasagna"


class Fried_banana(Dessert):
    def eatDessert(self):
        return "fried_banana"


class Tiramisu(Dessert):
    def eatDessert(self):
        return "tiramisu"


