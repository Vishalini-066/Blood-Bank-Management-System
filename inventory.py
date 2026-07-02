# inventory.py
# Encapsulation + dict + set + float + lambda

class BloodInventory:

    # set — all valid blood groups
    VALID_GROUPS = {'A+', 'A-', 'B+', 'B-',
                    'O+', 'O-', 'AB+', 'AB-'}

    def __init__(self):
        # dict — private (Encapsulation)
        self.__stock = {
            'A+': 0, 'A-': 0,
            'B+': 0, 'B-': 0,
            'O+': 0, 'O-': 0,
            'AB+': 0, 'AB-': 0
        }
        self.__threshold = 2.0   # float

    def add_units(self, group, units):
        if group in self.VALID_GROUPS:
            self.__stock[group] += units
            return True
        return False

    def deduct_units(self, group, units):
        if self.__stock.get(group, 0) >= units:
            self.__stock[group] -= units
            return True
        return False

    def check_stock(self, group):
        return self.__stock.get(group, 0)

    def display_stock(self):
        print("\n--- BLOOD AVAILABILITY ---")
        for group, units in self.__stock.items():
            if units == 0:
                status = "❌ Not Available"
            elif units <= self.__threshold:
                status = "⚠️  Low Stock"
            else:
                status = "✅ Available"
            print(f"{group:<4}: {units} units  {status}")

    # lambda — filter low stock
    def low_stock_groups(self):
        return list(filter(
            lambda g: 0 < self.__stock[g] <= self.__threshold,
            self.__stock
        ))

    # lambda — sort by units
    def sorted_stock(self):
        return sorted(
            self.__stock.items(),
            key=lambda x: x[1],
            reverse=True
        )