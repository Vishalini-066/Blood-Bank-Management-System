from people import Person, Donor, Recipient
from inventory import BloodInventory
from queue_ds import RequestQueue
from priority_queue import PriorityRequestQueue   # NEW
from expiry import BloodExpiry
from eligibility import EligibilityRegistry
from datetime import date

# ── setup
donors       = []        # list
inventory    = BloodInventory()
req_queue    = RequestQueue()
urgent_queue = PriorityRequestQueue()   # NEW — for emergency/urgent requests
expiry       = BloodExpiry()
eligibility  = EligibilityRegistry()    # tracks 90-day donor eligibility
history      = []        # list


def register_donor():
    print("\n--- REGISTER DONOR ---")
    name        = input("Enter Name        : ")
    age         = int(input("Enter Age         : "))
    phone       = input("Enter Phone       : ")
    blood_group = input("Enter Blood Group : ")
    city        = input("Enter City        : ")

    # Validation
    if age < 18 or age > 60:
        print("❌ Age must be 18–60!")
        return
    if len(phone) != 10 or not phone.isdigit():
        print("❌ Phone must be 10 digits!")
        return
    if blood_group not in BloodInventory.VALID_GROUPS:
        print("❌ Invalid blood group!")
        return

    result = eligibility.check_eligibility(phone)
    if not result["eligible"]:
        print(f"❌ Not Eligible to Donate. "
              f"Please wait {result['remaining_days']} more day(s).")
        return

    temp = Donor(0, name, age, phone, blood_group, city)
    donor_id = temp.generate_id(donors)
    donor    = Donor(donor_id, name, age, phone, blood_group, city)
    donors.append(donor)
    inventory.add_units(blood_group, 1)
    expiry.add_unit(blood_group)
    eligibility.record_donation(phone)
    history.append({
        'action'     : 'DONATED',
        'name'       : name,
        'blood_group': blood_group,
        'units'      : 1,
        'date'       : str(date.today()),
        'fulfilled'  : True
    })
    print(f"✅ Donor Registered! Donor ID: #D00{donor_id}")


def check_donor_eligibility():
    print("\n--- CHECK DONOR ELIGIBILITY ---")
    phone = input("Enter Phone Number: ").strip()
    if len(phone) != 10 or not phone.isdigit():
        print("❌ Phone must be 10 digits!")
        return
    result = eligibility.check_eligibility(phone)
    if result["eligible"]:
        print("✅ Eligible to Donate")
    else:
        print(f"❌ Not Eligible. Remaining Days: {result['remaining_days']}")


def request_blood():
    print("\n--- REQUEST BLOOD ---")
    name        = input("Enter Patient Name : ")
    blood_group = input("Enter Blood Group  : ")
    units       = int(input("Enter Units Needed: "))

    print("Select Urgency: 1=Emergency  2=Urgent  3=Normal")
    urgency = input("> ").strip()
    priority_map = {"1": 0, "2": 1, "3": 2}
    priority = priority_map.get(urgency, 2)   # default Normal

    request = {
        'name'       : name,
        'blood_group': blood_group,
        'units'      : units,
        'date'       : str(date.today())
    }

    if priority == 2:
        req_queue.enqueue(request)
        print("✅ Added to normal request queue.")
    else:
        urgent_queue.enqueue(request, priority)
        print("✅ Added to priority request queue.")


def dispatch_request():
    print("\n--- DISPATCH NEXT REQUEST ---")
    if not urgent_queue.is_empty():
        request = urgent_queue.dequeue()
        print("⚡ Serving URGENT request:")
    elif not req_queue.is_empty():
        request = req_queue.dequeue()
        print("Serving normal request:")
    else:
        print("No pending requests!")
        return

    print(request)

    # Fulfillment logic
    group = request['blood_group']
    units = request['units']
    if inventory.get_stock(group) >= units:
        inventory.remove_units(group, units)
        fulfilled = True
        print("✅ Request Fulfilled!")
    else:
        fulfilled = False
        print("❌ Insufficient stock. Request could not be fulfilled.")

    history.append({
        'action'     : 'REQUESTED',
        'name'       : request['name'],
        'blood_group': group,
        'units'      : units,
        'date'       : request['date'],
        'fulfilled'  : fulfilled
    })


def view_pending_requests():
    print("\n-- Urgent Requests --")
    urgent_queue.display_queue()
    print("\n-- Normal Requests --")
    req_queue.display_queue()


def view_donors():
    print("\n--- ALL DONORS ---")
    if not donors:
        print("No donors registered yet!")
        return
    for d in donors:
        print(d)


def view_history():
    print("\n--- DONATION / REQUEST HISTORY ---")
    if not history:
        print("No history yet!")
        return
    for h in history:
        print(h)


def search_by_group():
    print("\n--- SEARCH DONOR BY BLOOD GROUP ---")
    group = input("Enter Blood Group: ")
    found = [d for d in donors if d.blood_group == group]
    if not found:
        print("No donors found for this group!")
        return
    for d in found:
        print(d)


def admin_report():
    print("\n--- ADMIN REPORT ---")
    inventory.display_stock()
    print(f"Total Donors        : {len(donors)}")
    print(f"Pending Urgent Reqs : {urgent_queue.size()}")   # NEW
    print(f"Pending Normal Reqs : {req_queue.size()}")


def check_expiry():
    print("\n--- BLOOD EXPIRY STATUS ---")
    expiry.display_status()


def clean_expired():
    print("\n--- REMOVING EXPIRED UNITS ---")
    expiry.remove_expired(inventory)


# ── MAIN MENU LOOP
while True:
    print("\n============================================")
    print("     🩸 BLOOD BANK MANAGEMENT SYSTEM")
    print("============================================")
    print("1. Register Donor")
    print("2. Request Blood")
    print("3. Check Blood Availability")
    print("4. View All Donors")
    print("5. View Donation History")
    print("6. Search Donor by Blood Group")
    print("7. Admin Report")
    print("8. Check Blood Expiry Status")
    print("9. Remove Expired Units")
    print("10. Check Donor Eligibility")
    print("11. View Pending Requests")     # NEW
    print("12. Dispatch Next Request")     # NEW
    print("13. Exit")

    choice = input("\n> ")

    if   choice == "1": register_donor()
    elif choice == "2": request_blood()
    elif choice == "3": inventory.display_stock()
    elif choice == "4": view_donors()
    elif choice == "5": view_history()
    elif choice == "6": search_by_group()
    elif choice == "7": admin_report()
    elif choice == "8": check_expiry()
    elif choice == "9": clean_expired()
    elif choice == "10": check_donor_eligibility()
    elif choice == "11": view_pending_requests()
    elif choice == "12": dispatch_request()
    elif choice == "13":
        print("Goodbye! 👋")
        break
    else:
        print("❌ Invalid choice!")