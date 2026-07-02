# expiry.py
# Concepts: Abstraction, Polymorphism,
#           Encapsulation, Lambda, datetime
#           List, Dict, Bool, Int

from datetime import date
from abc import ABC, abstractmethod

# ── ABSTRACT BASE CLASS — Abstraction
class BloodUnit(ABC):

    def __init__(self, blood_group, packed_date):
        self._blood_group  = blood_group   # str
        self._packed_date  = packed_date   # date
        self._is_valid     = True          # bool

    # Abstract method — MUST be overridden
    # This is Abstraction — subclass decides 
    # how to check expiry
    @abstractmethod
    def check_expiry(self):
        pass

    # Abstract method — Polymorphism
    # Each subclass displays differently
    @abstractmethod
    def display_info(self):
        pass

    def get_group(self):
        return self._blood_group

    def get_packed_date(self):
        return self._packed_date

    def get_age(self):
        return (date.today() - self._packed_date).days


# ── SUBCLASS 1 — Regular Blood Unit
class RegularUnit(BloodUnit):

    EXPIRY_DAYS = 35   # int

    def __init__(self, blood_group, packed_date):
        super().__init__(blood_group, packed_date)

    # Polymorphism — overrides abstract method
    def check_expiry(self):
        age       = self.get_age()
        remaining = self.EXPIRY_DAYS - age

        if age > self.EXPIRY_DAYS:
            self._is_valid = False
            return "❌ Expired"
        elif remaining <= 7:
            return "⚠️  Expiring Soon"
        else:
            return "✅ Fresh"

    # Polymorphism — own version of display_info
    def display_info(self):
        status = self.check_expiry()
        age    = self.get_age()
        print(f"  [REGULAR] {self._blood_group} | "
              f"Packed: {self._packed_date} | "
              f"Age: {age} days | {status}")


# ── SUBCLASS 2 — Emergency Blood Unit
# (shorter expiry — must be used in 24 hours)
class EmergencyUnit(BloodUnit):

    EXPIRY_DAYS = 1   # int — emergency use only

    def __init__(self, blood_group, packed_date):
        super().__init__(blood_group, packed_date)

    # Polymorphism — different expiry logic
    def check_expiry(self):
        age = self.get_age()

        if age > self.EXPIRY_DAYS:
            self._is_valid = False
            return "❌ Expired (Emergency unit)"
        else:
            return "🚨 Active Emergency Unit"

    # Polymorphism — different display
    def display_info(self):
        status = self.check_expiry()
        age    = self.get_age()
        print(f"  [EMERGENCY] {self._blood_group} | "
              f"Packed: {self._packed_date} | "
              f"Age: {age} days | {status}")


# ── MANAGER CLASS — Encapsulation
class BloodExpiry:

    def __init__(self):
        # dict of lists — private (Encapsulation)
        self.__units = {}   # dict

    # Add regular unit
    def add_unit(self, blood_group, unit_type="regular"):
        if blood_group not in self.__units:
            self.__units[blood_group] = []

        if unit_type == "emergency":
            unit = EmergencyUnit(blood_group, date.today())
        else:
            unit = RegularUnit(blood_group, date.today())

        self.__units[blood_group].append(unit)

    # Remove one unit when allocated
    def remove_unit(self, blood_group):
        if blood_group in self.__units:
            if self.__units[blood_group]:
                self.__units[blood_group].pop(0)

    # Remove all expired units — uses Lambda
    def remove_expired(self):
        expired_count = 0   # int
        for group in self.__units:
            before = len(self.__units[group])
            # lambda — keep only valid units
            self.__units[group] = list(filter(
                lambda u: u.check_expiry() != "❌ Expired"
                and u.check_expiry() != "❌ Expired (Emergency unit)",
                self.__units[group]
            ))
            after = len(self.__units[group])
            expired_count += (before - after)
        return expired_count   # int

    # Display all — Polymorphism in action!
    # display_info() behaves differently for
    # RegularUnit vs EmergencyUnit
    def display_expiry(self):
        print("\n--- BLOOD EXPIRY STATUS ---")
        found = False   # bool
        for group, units in self.__units.items():
            if units:
                found = True
                print(f"\nBlood Group : {group}")
                for unit in units:
                    unit.display_info()  # Polymorphism!
        if not found:
            print("No blood units tracked yet!")

    # Count only fresh units — Lambda
    def fresh_count(self, blood_group):
        units = self.__units.get(blood_group, [])
        # lambda — filter fresh units only
        fresh = list(filter(
            lambda u: "✅" in u.check_expiry()
                   or "🚨" in u.check_expiry(),
            units
        ))
        return len(fresh)   # int