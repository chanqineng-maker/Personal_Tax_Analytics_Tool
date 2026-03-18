annual_income = float(input("Hi! I am your Tax Assistant. What is your annual income? "))
total_relief = 0
claimed_reliefs = [] # list to store claimed releifs to prevent double claims 

def claim_spouse_relief(): #function for spouse relief
    income = float(input("\nWhat is your spouse's annual income? "))
    if income <= 8000:    # income threshold cannot exceed 8k 
        handicapped = input("Is your spouse handicapped? (y/n): ").lower() # to claim spouse relief for spouses with disability
        if handicapped == "y":
            return 5500
        else:
            return 2000
        
    else:
        print("Spouse Income exceeds $8,000 limit. No relief granted.")
        return 0



def claim_qcr_relief(): # function for child relief
    try:
        num_children = int(input("How many children are you claiming for? ")) # in case user tries to input non-number values
    except ValueError:
        print("Please enter a valid number.")
        return 0

    total_elig_children = 0 #counter for total no. of eligible children
    
    for i in range(1, num_children + 1): # loop cycles based on number of children being claimed
        print("\nChecking Child",i)
        
        status = input("Is this child below 16? (y/n): ").lower()
        
        if status == "y":
            total_elig_children += 1
        else:
            status1 = input("Is the child studying full-time and unmarried? (y/n): ").lower()
            if status1 == "y":
                status2 = input("Is the child's annual income $8k or less? (y/n): ").lower()
                if status2 == "y":
                    total_elig_children += 1 # meets condition
                else:
                    print("Child not eligible due to their income exceeding the threshold.")
            else:
                print("Child not eligible due to status.")
    return total_elig_children


def claim_wmcr_relief(): # function for Working Mother's Child Relief
    is_mother = input("Are you a working mother who is married, widowed, or divorced? (y/n): ").lower()
    if is_mother == "y":
        num_child = int(input("How many children are you claiming WMCR for? "))
        wmcr_total = 0
        for i in range(1, num_child + 1):
            born_after_2024 = input("Was Child " + str(i) + " born on or after 1 Jan 2024? (y/n): ").lower()
            if born_after_2024 == "y":
                # Fixed dollar amount calc for children born after 2024
                if i == 1: wmcr_total += 8000
                elif i == 2: wmcr_total += 10000
                else: wmcr_total += 12000
            else:
                # Percentage based calc for children born before 2024
                if i == 1: wmcr_total += (annual_income * 0.15)
                elif i == 2: wmcr_total += (annual_income * 0.20)
                else: wmcr_total += (annual_income * 0.25)
        return wmcr_total
    else:
        print("WMCR is only applicable to working mothers.")
        return 0


def claim_grandparent_relief(): #Logic for Grandparent Caregiver Relief
    eligible = input("Are you working and have a parent/grandparent looking after your child? (y/n): ").lower()
    if eligible == "y":
        income_check = input("Is the caregiver's annual income $4,000 or less? (y/n): ").lower()
        if income_check == "y":
            return 3000
    return 0


def claim_parent_relief(): #Logic for Parent Relief
    handicapped = input("Is the parent handicapped? (y/n): ").lower()
    staying_together = input("Are you living with the parent? (y/n): ").lower()
    
    if handicapped == "y":
        if staying_together == "y": return 9000
        else: return 5500
    else:
        if staying_together == "y": return 5500
        else: return 4500


def claim_sibling_relief(): #Logic for Sibling Relief
    is_handicapped = input("Is the sibling handicapped and living in Singapore? (y/n): ").lower()
    if is_handicapped == "y":
        income_check = input("Is the sibling's annual income $8,000 or less? (y/n): ").lower()
        if income_check == "y":
            return 5500
    return 0

    
while True:
    print(" ")
    print("\n    Available Reliefs    ")
    if "1" not in claimed_reliefs: print("1. Spouse Relief")
    if "2" not in claimed_reliefs: print("2. Qualifying Child Relief")
    if "3" not in claimed_reliefs: print("3. Working Mother Child's Relief")
    if "4" not in claimed_reliefs: print("4. Grandparent Caregiver Relief")
    if "5" not in claimed_reliefs: print("5. Parent Relief")
    if "6" not in claimed_reliefs: print("6. Sibling Relief (Disability)")
    print("7. Finish and calculate")

    choice = input("Which relief would you like to claim? (Enter 1-7): ")

    
    if choice == "1" and "1" not in claimed_reliefs:
        total_relief+= claim_spouse_relief()
        claimed_reliefs.append("1") # Mark as "claimed"  

    elif choice == "2" and "2" not in claimed_reliefs:
        total_relief+= (claim_qcr_relief()*4000)
        claimed_reliefs.append("2")
        print(".")

    elif choice == "3" and "3" not in claimed_reliefs:
        total_relief += claim_wmcr_relief()
        claimed_reliefs.append("3")

    elif choice == "4" and "4" not in claimed_reliefs:
        total_relief += claim_grandparent_relief()
        claimed_reliefs.append("4")

    elif choice == "5" and "5" not in claimed_reliefs:
        total_relief += claim_parent_relief()
        claimed_reliefs.append("5")

    elif choice == "6" and "6" not in claimed_reliefs:
        total_relief += claim_sibling_relief()
        claimed_reliefs.append("6")

    elif choice == "7":
        break
    
    else:
        print("Invalid choice or relief already claimed. Try again.")

    # Show current status
    chargeable = annual_income - total_relief
    if chargeable < 0: chargeable = 0
    print(f"\nCurrent Total Relief: ${total_relief:,.2f}")
    print(f"Current Chargeable Income: ${chargeable:,.2f}")

# Final Result
print("\n--- FINAL SUMMARY ---")
# Apply the $80,000 Singapore tax relief cap
if total_relief > 80000:
    total_relief = 80000
    print("Note: Your total relief was capped at $80,000.")

final_chargeable = annual_income - total_relief
if final_chargeable < 0: final_chargeable = 0

print(f"Final Total Relief: ${total_relief:,.2f}")
print(f"Final Chargeable Income: ${final_chargeable:,.2f}")
print("Thank you for using the Tax Assistant!")
