class Person:

    def __init__(self, name, age, phone):
        self._name  = name
        self._age   = age
        self._phone = phone

    def get_name(self):
        return self._name

    def get_age(self):
        return self._age

    def get_phone(self):
        return self._phone

    def display_info(self):
        print("Name  :", self._name)
        print("Age   :", self._age)
        print("Phone :", self._phone)


class Donor(Person):

    def __init__(self, donor_id, name, age, phone, blood_group, city):
        super().__init__(name, age, phone)   # calls Person
        self.donor_id     = donor_id    # int
        self.blood_group  = blood_group # str
        self.city         = city        # str
        self.is_active    = True        # bool

    # Recursion - find next donor ID
    def generate_id(self, donors, index=0):
        if index == len(donors):   # base case
            return index + 1
        return self.generate_id(donors, index + 1)

    # Tuple snapshot of donor
    def to_tuple(self):
        return (self.donor_id, self.get_name(),
                self.blood_group, self.city)

    def display_info(self):
        print("Donor ID    :", self.donor_id)
        print("Name        :", self.get_name())
        print("Age         :", self.get_age())
        print("Phone       :", self.get_phone())
        print("Blood Group :", self.blood_group)
        print("City        :", self.city)
        print("Active      :", self.is_active)


class Recipient(Person):

    def __init__(self, name, age, phone, blood_group, units):
        super().__init__(name, age, phone)  # calls Person
        self.blood_group  = blood_group  # str
        self.units_needed = units        # int
        self.fulfilled    = False        # bool

    def display_info(self):
        print("Name          :", self.get_name())
        print("Age           :", self.get_age())
        print("Phone         :", self.get_phone())
        print("Blood Group   :", self.blood_group)
        print("Units Needed  :", self.units_needed)
        print("Fulfilled     :", self.fulfilled)