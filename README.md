# Singapore Tax Relief Assistant (Python)

## Project Overview
While working at **IRAS**, I developed this Python chatbot to bridge the gap between complex tax relief logic and taxpayer understanding. The tool automates the logic for several Singaporean tax reliefs, helping taxpayers calculate their **Total Personal Reliefs** and **Final Assessable Income**.

## Key Features
* **Checks eligibility of reliefs:** Spouse, QCR, WMCR, Parent, and Sibling reliefs.
* **Up-to-date logic:**
* 1. Accounts for the 2024/2025 change in WMCR (Fixed-dollar vs. Percentage-based).
  2.  Applies the **S$80,000 personal relief cap** and ensures non-negative chargeable income.
  3.  Prevents double-claiming of the same relief.

 ## Test run
 This test case will validate the most complex part of my code: the WMCR (Working Mother's Child Relief) and the $80,000 cap.
### User Profile:

Annual Income: $150,000

Status: Working Mother

Claims: 
1. Spouse Relief: $2,000 (Non-handicapped)
2. Qualifying Child Relief (QCR): 3 Children ($4,000 x 3 = $12,000)
3. WMCR: * Child 1 (Born 2022): 15% of $150k = $22,500
* Child 2 (Born 2023): 20% of $150k = $30,000
* Child 3 (Born 2025): Fixed $12,000 (New Rule)
* Total WMCR: $64,500

### Expected Mathematical Outcome:

**Raw Total Relief**: $2,000 (Spouse) + $12,000 (QCR) + $64,500 (WMCR) = **$78,500**

**System Check**: Since $78,500 < $80,000, the full amount is granted.

**Final Assessable Income**: $150,000 - $78,500 = **$71,500**
