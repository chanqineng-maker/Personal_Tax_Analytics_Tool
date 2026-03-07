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

# --- Step 1: Annual Income ---
st.header("Step 1: Enter Your Annual Income")

# Using number_input with min_value=0.0 prevents text and negative numbers
annual_income = st.number_input(
    "What is your annual income? ($)",
    min_value=0.0,
    value=st.session_state.annual_income,
    step=1000.0,
    format="%.2f",
    help="Enter your total gross annual income before reliefs."
)
st.session_state.annual_income = annual_income

st.divider()
st.header("Step 2: Claim Your Reliefs")

# --- Spouse Relief ---
if "1" not in st.session_state.claimed_reliefs:
    with st.expander("1️⃣ Spouse Relief", expanded=(st.session_state.configuring_relief == "1")):
        # Forced numeric input for spouse income
        spouse_income = st.number_input(
            "Spouse's annual income ($)",
            min_value=0.0,
            value=st.session_state.get("spouse_income", 0.0),
            step=100.0,
            format="%.2f",
            key="spouse_income_num"
        )
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

# --- Qualifying Child Relief (QCR) ---
if "2" not in st.session_state.claimed_reliefs:
    with st.expander("2️⃣ Qualifying Child Relief (QCR)", expanded=(st.session_state.configuring_relief == "2")):
        # min_value=1 ensures they can't claim for 0 or negative children
        num_children = st.number_input("How many children are you claiming for?", min_value=1, step=1, key="qcr_num_children")
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

# --- Working Mother Child Relief (WMCR) ---
if "3" not in st.session_state.claimed_reliefs:
    with st.expander("3️⃣ Working Mother Child Relief (WMCR)", expanded=(st.session_state.configuring_relief == "3")):
        is_mother = st.radio("Are you a working mother (married/widowed/divorced)?", ["Yes", "No"], key="wmcr_is_mother")
        
        if is_mother == "Yes":
            num_kids = st.number_input("How many children for WMCR?", min_value=1, step=1, key="wmcr_num_kids")
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
                        st.write(f"Fixed amount applied")
                    else:
                        if i == 1: wmcr_total += (st.session_state.annual_income * 0.15)
                        elif i == 2: wmcr_total += (st.session_state.annual_income * 0.20)
                        else: wmcr_total += (st.session_state.annual_income * 0.25)
                        st.write(f"% of income applied")
            
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
else:
    st.success("✅ Working Mother Child Relief (WMCR) - Claimed")

# --- Results Section ---
st.divider()
st.header("Step 3: Your Summary")

# Apply relief cap
total_relief_raw = st.session_state.total_relief
total_relief_capped = min(total_relief_raw, 80000.0)

col_summary1, col_summary2 = st.columns(2)
with col_summary1:
    st.metric("Total Relief (Before Cap)", f"${total_relief_raw:,.2f}")
with col_summary2:
    if total_relief_raw > 80000:
        st.metric("Final Total Relief (Capped)", "$80,000.00", delta="-"+f"${total_relief_raw-80000:,.2f}", delta_color="inverse")
    else:
        st.metric("Final Total Relief", f"${total_relief_raw:,.2f}")

final_chargeable = max(0.0, st.session_state.annual_income - total_relief_capped)
st.metric("Final Chargeable Income", f"${final_chargeable:,.2f}")

# Reset button
if st.button("Reset Calculator"):
    st.session_state.annual_income = 0.0
    st.session_state.total_relief = 0.0
    st.session_state.claimed_reliefs = []
    st.session_state.configuring_relief = None
    st.session_state.failed_claims = {}
    st.rerun()
