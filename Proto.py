annual_income = float(input("Hi! I am your Tax Assistant. What is your annual income? "))
total_relief = 0
claimed_reliefs = [] #Keep track of what's been chosen to prevent double claims 

def claim_spouse_relief(): #Logic for spouse relief
    income = float(input("What is your spouse's annual income? "))
    if income <= 8000:
        handicapped = input("Is your spouse handicapped? (y/n): ").lower()
        if handicapped == "y":
            return 5500
        else:
            return 2000
        
    else:
        print("Spouse Income exceeds $8,000 limit. No relief granted.")
        return 0

def claim_qcr_relief(): #Logic for child relief
    try:
        num_children = int(input("How many children are you claiming for? "))
    except ValueError:
        print("Please enter a valid number.")
        return 0

    total_eligible_children = 0
    
    for i in range(1, num_children + 1):
        print("\nChecking Child",i)
        
        status = input("Is this child below 16? (y/n): ").lower()
        
        if status == "y":
            total_eligible_children += 1
        else:
            status1 = input("Is the child studying full-time and unmarried? (y/n): ").lower()
            if status1 == "y":
                status2 = input("Is the child's annual income $8k or less? (y/n): ").lower()
                if status2 == "y":
                    total_eligible_children += 1
                else:
                    print("Child not eligible due to income.")
            else:
                print("Child not eligible due to status.")
    print("Number of Children eligible for QCR:",total_eligible_children)
    return total_eligible_children 
    
while True:
    print("\n    Available Reliefs    ")
    if "1" not in claimed_reliefs: print("1. Spouse Relief")
    if "2" not in claimed_reliefs: print("2. Qualifying Child Relief")
    if "3" not in claimed_reliefs: print("3. Working Mother Child's Relief")
    if "4" not in claimed_reliefs: print("4. Grandparent Caregiver Relief")
    if "5" not in claimed_reliefs: print("5. Parent Relief")
    if "6" not in claimed_reliefs: print("6. Sibling Relief (Disability)")
    print("7. Finish and calculate")

    choice = input("Which relief would you like to claim? (Enter 1-6): ")

    
    if choice == "1" and "1" not in claimed_reliefs:
        total_relief+= claim_spouse_relief()
        claimed_reliefs.append("1") # Mark as "claimed"  

    elif choice == "2" and "2" not in claimed_reliefs:
        total_relief+= (claim_qcr_relief()*4000)
        claimed_reliefs.append("2")
        print("")

    elif choice == "7":
        break
    
    else:
        print("Invalid choice or relief already claimed. Try again.")

    # Show current status
    chargeable = annual_income - total_relief
    if chargeable < 0: chargeable = 0
    print("Current Relief: $" + str(total_relief))
    print("Current Chargeable Income: $" + str(chargeable))

# Final Result
print("\n--- FINAL SUMMARY ---")
# Apply the $80,000 Singapore tax relief cap
if total_relief > 80000:
    total_relief = 80000
    print("Note: Your total relief was capped at $80,000.")

final_chargeable = annual_income - total_relief
if final_chargeable < 0: final_chargeable = 0

print("Final Total Relief: $" + str(total_relief))
print("Final Chargeable Income: $" + str(final_chargeable))
print("Thank you for using the Tax Assistant!")
