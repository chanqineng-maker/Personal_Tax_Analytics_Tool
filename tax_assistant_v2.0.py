import streamlit as st

st.set_page_config(page_title="Singapore Tax Assistant", layout="wide")

st.title("🇸🇬 Singapore Tax Relief Calculator")
st.markdown("Calculate your personal tax reliefs and chargeable income")

# Initialize session state
if "annual_income" not in st.session_state:
    st.session_state.annual_income = 0.0
if "total_relief" not in st.session_state:
    st.session_state.total_relief = 0.0
if "claimed_reliefs" not in st.session_state:
    st.session_state.claimed_reliefs = []
if "configuring_relief" not in st.session_state:
    st.session_state.configuring_relief = None
if "failed_claims" not in st.session_state:
    st.session_state.failed_claims = {}

# Input Section
st.header("Step 1: Enter Your Annual Income")
income_input = st.number_input(
    "What is your annual income? ($)",
    value="" if st.session_state.annual_income == 0.0 else str(st.session_state.annual_income),
    placeholder="0.0"
)
try:
    annual_income = float(income_input) if income_input else 0.0
except ValueError:
    annual_income = 0.0
    st.error("Please enter a valid number")
st.session_state.annual_income = annual_income

st.divider()
st.header("Step 2: Claim Your Reliefs")

# Spouse Relief
if "1" not in st.session_state.claimed_reliefs:
    with st.expander("1️⃣ Spouse Relief", expanded=(st.session_state.configuring_relief == "1")):
        spouse_income_input = st.number_input(
            "Spouse's annual income ($)",
            value="" if st.session_state.get("spouse_income", 0.0) == 0.0 else str(st.session_state.get("spouse_income", 0.0)),
            placeholder="0.0",
            key="spouse_income_input"
        )
        try:
            spouse_income = float(spouse_income_input) if spouse_income_input else 0.0
        except ValueError:
            spouse_income = 0.0
            st.error("Please enter a valid number")
        
        st.session_state.spouse_income = spouse_income
        col_sp1, col_sp2 = st.columns(2)
        
        with col_sp1:
            if spouse_income <= 8000:
                handicapped = st.radio("Is your spouse handicapped?", ["Yes", "No"], key="spouse_handicap_input")
                if st.button("✅ Confirm Spouse Relief", key="confirm_spouse"):
                    relief = 5500 if handicapped == "Yes" else 2000
                    st.session_state.total_relief += relief
                    st.session_state.claimed_reliefs.append("1")
                    st.session_state.configuring_relief = None
                    st.success(f"Spouse Relief claimed: ${relief:,.2f}")
                    st.rerun()
            else:
                st.error("❌ Unable to claim: Spouse income exceeds $8,000 limit")
                st.session_state.failed_claims["1"] = "Spouse income exceeds $8,000 limit"
        
        with col_sp2:
            if st.button("❌ Cancel", key="cancel_spouse"):
                st.session_state.configuring_relief = None
                st.rerun()
else:
    st.success("✅ Spouse Relief - Claimed")

# Qualifying Child Relief
if "2" not in st.session_state.claimed_reliefs:
    with st.expander("2️⃣ Qualifying Child Relief (QCR)", expanded=(st.session_state.configuring_relief == "2")):
        num_children = st.number_input("How many children are you claiming for?", min_value=1, step=1, key="qcr_num_children", placeholder="1")
        total_eligible = 0
        
        for i in range(1, int(num_children) + 1):
            col_child1, col_child2, col_child3 = st.columns(3)
            with col_child1:
                st.markdown(f"**Child {i}**")
            with col_child2:
                below_16 = st.radio(f"Below 16?", ["Yes", "No"], key=f"qcr_child_{i}_age")
                
                if below_16 == "Yes":
                    total_eligible += 1
            with col_child3:
                if below_16 == "No":
                    studying = st.radio(f"Studying full-time & unmarried?", ["Yes", "No"], key=f"qcr_child_{i}_study")
                    if studying == "Yes":
                        income_ok = st.radio(f"Income ≤ $8k?", ["Yes", "No"], key=f"qcr_child_{i}_income")
                        if income_ok == "Yes":
                            total_eligible += 1
        
        col_qcr1, col_qcr2 = st.columns(2)
        with col_qcr1:
            if st.button("✅ Confirm QCR", key="confirm_qcr"):
                relief = total_eligible * 4000
                st.session_state.total_relief += relief
                st.session_state.claimed_reliefs.append("2")
                st.session_state.configuring_relief = None
                st.success(f"QCR claimed for {total_eligible} children: ${relief:,.2f}")
                st.rerun()
        with col_qcr2:
            if st.button("❌ Cancel", key="cancel_qcr"):
                st.session_state.configuring_relief = None
                st.rerun()
else:
    st.success("✅ Qualifying Child Relief (QCR) - Claimed")

# Working Mother Child Relief
if "3" not in st.session_state.claimed_reliefs:
    with st.expander("3️⃣ Working Mother Child Relief (WMCR)", expanded=(st.session_state.configuring_relief == "3")):
        is_mother = st.radio("Are you a working mother (married/widowed/divorced)?", ["Yes", "No"], key="wmcr_is_mother")
        
        if is_mother == "Yes":
            num_kids = st.number_input("How many children for WMCR?", min_value=1, step=1, key="wmcr_num_kids", placeholder="1")
            wmcr_total = 0
            
            for i in range(1, int(num_kids) + 1):
                col_wmcr1, col_wmcr2, col_wmcr3 = st.columns(3)
                with col_wmcr1:
                    st.markdown(f"**Child {i}**")
                with col_wmcr2:
                    born_after = st.radio(f"Born on/after 1 Jan 2024?", ["Yes", "No"], key=f"wmcr_{i}_born")
                with col_wmcr3:
                    if born_after == "Yes":
                        if i == 1: wmcr_total += 8000
                        elif i == 2: wmcr_total += 10000
                        else: wmcr_total += 12000
                        st.write(f"Fixed amount")
                    else:
                        if i == 1: wmcr_total += (st.session_state.annual_income * 0.15)
                        elif i == 2: wmcr_total += (st.session_state.annual_income * 0.20)
                        else: wmcr_total += (st.session_state.annual_income * 0.25)
                        st.write(f"% of income")
            
            col_wmcr_btn1, col_wmcr_btn2 = st.columns(2)
            with col_wmcr_btn1:
                if st.button("✅ Confirm WMCR", key="confirm_wmcr"):
                    st.session_state.total_relief += wmcr_total
                    st.session_state.claimed_reliefs.append("3")
                    st.session_state.configuring_relief = None
                    st.success(f"WMCR claimed: ${wmcr_total:,.2f}")
                    st.rerun()
            with col_wmcr_btn2:
                if st.button("❌ Cancel", key="cancel_wmcr"):
                    st.session_state.configuring_relief = None
                    st.rerun()
        else:
            st.error("❌ Unable to claim: Not a working mother")
            st.session_state.failed_claims["3"] = "Not a working mother"
else:
    st.success("✅ Working Mother Child Relief (WMCR) - Claimed")

# Grandparent Caregiver Relief
if "4" not in st.session_state.claimed_reliefs:
    with st.expander("4️⃣ Grandparent Caregiver Relief", expanded=(st.session_state.configuring_relief == "4")):
        eligible = st.radio("Working with parent/grandparent caring for child?", ["Yes", "No"], key="gp_eligible_input")
        
        if eligible == "Yes":
            income_check = st.radio("Caregiver's annual income $4,000 or less?", ["Yes", "No"], key="gp_income_input")
            col_gp1, col_gp2 = st.columns(2)
            
            with col_gp1:
                if income_check == "Yes":
                    if st.button("✅ Confirm Grandparent Relief", key="confirm_gp"):
                        st.session_state.total_relief += 3000
                        st.session_state.claimed_reliefs.append("4")
                        st.session_state.configuring_relief = None
                        st.success("Grandparent Caregiver Relief claimed: $3,000.00")
                        st.rerun()
            with col_gp2:
                if st.button("❌ Cancel", key="cancel_gp"):
                    st.session_state.configuring_relief = None
                    st.rerun()
        else:
            st.error("❌ Unable to claim: Does not meet eligibility criteria")
            st.session_state.failed_claims["4"] = "Does not meet eligibility criteria"
else:
    st.success("✅ Grandparent Caregiver Relief - Claimed")

# Parent Relief
if "5" not in st.session_state.claimed_reliefs:
    with st.expander("5️⃣ Parent Relief", expanded=(st.session_state.configuring_relief == "5")):
        col_pr1, col_pr2 = st.columns(2)
        
        with col_pr1:
            handicapped = st.radio("Is the parent handicapped?", ["Yes", "No"], key="parent_handicap_input")
        with col_pr2:
            staying = st.radio("Are you living with the parent?", ["Yes", "No"], key="parent_stay_input")
        
        col_pr_btn1, col_pr_btn2 = st.columns(2)
        with col_pr_btn1:
            if st.button("✅ Confirm Parent Relief", key="confirm_parent"):
                if handicapped == "Yes":
                    relief = 9000 if staying == "Yes" else 5500
                else:
                    relief = 5500 if staying == "Yes" else 4500
                st.session_state.total_relief += relief
                st.session_state.claimed_reliefs.append("5")
                st.session_state.configuring_relief = None
                st.success(f"Parent Relief claimed: ${relief:,.2f}")
                st.rerun()
        with col_pr_btn2:
            if st.button("❌ Cancel", key="cancel_parent"):
                st.session_state.configuring_relief = None
                st.rerun()
else:
    st.success("✅ Parent Relief - Claimed")

# Sibling Relief
if "6" not in st.session_state.claimed_reliefs:
    with st.expander("6️⃣ Sibling Relief (Disability)", expanded=(st.session_state.configuring_relief == "6")):
        col_sib1, col_sib2 = st.columns(2)
        
        with col_sib1:
            handicapped = st.radio("Sibling handicapped & living in Singapore?", ["Yes", "No"], key="sibling_handicap_input")
        
        with col_sib2:
            if handicapped == "Yes":
                income_check = st.radio("Sibling's annual income $8,000 or less?", ["Yes", "No"], key="sibling_income_input")
            else:
                income_check = "No"
        
        col_sib_btn1, col_sib_btn2 = st.columns(2)
        with col_sib_btn1:
            if income_check == "Yes":
                if st.button("✅ Confirm Sibling Relief", key="confirm_sibling"):
                    st.session_state.total_relief += 5500
                    st.session_state.claimed_reliefs.append("6")
                    st.session_state.configuring_relief = None
                    st.success("Sibling Relief claimed: $5,500.00")
                    st.rerun()
            else:
                st.error("❌ Unable to claim: Sibling income exceeds $8,000 or not handicapped")
                st.session_state.failed_claims["6"] = "Sibling income exceeds $8,000 or not handicapped"
        with col_sib_btn2:
            if st.button("❌ Cancel", key="cancel_sibling"):
                st.session_state.configuring_relief = None
                st.rerun()
else:
    st.success("✅ Sibling Relief (Disability) - Claimed")

st.divider()

# Results Section
st.header("Step 3: Your Summary")

col_summary1, col_summary2 = st.columns(2)

with col_summary1:
    st.metric("Annual Income", f"${st.session_state.annual_income:,.2f}")

with col_summary2:
    st.metric("Total Relief Claimed", f"${st.session_state.total_relief:,.2f}")

# Apply relief cap
total_relief_capped = st.session_state.total_relief
if total_relief_capped > 80000:
    total_relief_capped = 80000
    st.warning("⚠️ Your total relief has been capped at $80,000 (Singapore tax relief limit)")

final_chargeable = max(0, st.session_state.annual_income - total_relief_capped)

col_final1, col_final2 = st.columns(2)

with col_final1:
    st.metric("Final Total Relief", f"${total_relief_capped:,.2f}")

with col_final2:
    st.metric("Final Chargeable Income", f"${final_chargeable:,.2f}", delta=None, delta_color="off")

# Claimed reliefs summary
if st.session_state.claimed_reliefs:
    st.subheader("Reliefs Claimed")
    relief_names = {
        "1": "Spouse Relief",
        "2": "Qualifying Child Relief (QCR)",
        "3": "Working Mother Child Relief (WMCR)",
        "4": "Grandparent Caregiver Relief",
        "5": "Parent Relief",
        "6": "Sibling Relief (Disability)"
    }
    for relief_id in st.session_state.claimed_reliefs:
        st.write(f"✅ {relief_names.get(relief_id, 'Unknown Relief')}")

# Failed claims summary
if st.session_state.failed_claims:
    st.subheader("Unable to Claim")
    relief_names = {
        "1": "Spouse Relief",
        "2": "Qualifying Child Relief (QCR)",
        "3": "Working Mother Child Relief (WMCR)",
        "4": "Grandparent Caregiver Relief",
        "5": "Parent Relief",
        "6": "Sibling Relief (Disability)"
    }
    for relief_id, reason in st.session_state.failed_claims.items():
        st.write(f"❌ {relief_names.get(relief_id, 'Unknown Relief')}: {reason}")

# Reset button
if st.button("Reset Calculator"):
    st.session_state.annual_income = 0.0
    st.session_state.total_relief = 0.0
    st.session_state.claimed_reliefs = []
    st.session_state.configuring_relief = None
    st.session_state.failed_claims = {}
    st.rerun()

st.divider()
st.markdown("**Disclaimer:** This calculator is for informational purposes. Please consult the IRAS (Inland Revenue Authority of Singapore) for official tax advice.")
