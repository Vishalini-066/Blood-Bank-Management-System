# eligibility.py
# Donor Eligibility Tracking (90-day gap rule)
# Concepts: Class, Encapsulation, datetime, Recursion, Dict

from datetime import date

class EligibilityRegistry:

    MIN_GAP_DAYS = 90  # int — minimum days required between donations

    def __init__(self):
        # dict — private (Encapsulation)
        # { phone: last_donation_date }
        self.__last_donation = {}

    # Record today as the last donation date for this phone
    def record_donation(self, phone):
        self.__last_donation[phone] = date.today()

    # Recursive search through phone keys (kept for recursion requirement)
    def __recursive_search(self, phone, keys=None, index=0):
        if keys is None:
            keys = list(self.__last_donation.keys())
        if index >= len(keys):
            return None
        if keys[index] == phone:
            return self.__last_donation[keys[index]]
        return self.__recursive_search(phone, keys, index + 1)

    # Check eligibility for a given phone number
    def check_eligibility(self, phone):
        last_date = self.__recursive_search(phone)

        if last_date is None:
            return {"eligible": True, "remaining_days": 0}

        days_since = (date.today() - last_date).days  # int

        if days_since >= self.MIN_GAP_DAYS:
            return {"eligible": True, "remaining_days": 0}
        else:
            remaining = self.MIN_GAP_DAYS - days_since
            return {"eligible": False, "remaining_days": remaining}