"""
LegalLens AI - High-fidelity Realistic Sample Legal Contracts.
Provides realistic, full-text legal agreements across everyday scenarios:
1. Residential Lease Agreement (Tenant-unfriendly terms, hidden fees, notice traps)
2. Freelance MSA & SOW (One-sided IP ownership, unlimited indemnity, net-90 payment)
3. Enterprise SaaS Subscription Agreement (Balanced commercial B2B terms)
4. Mutual Non-Disclosure Agreement (Standard protective NDA)
"""

SAMPLE_DOCUMENTS = {
    "residential_lease": {
        "id": "residential_lease",
        "title": "Residential Lease Agreement (Austin, TX)",
        "doc_type": "Residential Lease Agreement",
        "parties": ["Apex Property Management LLC (Landlord)", "Jane Doe (Tenant)"],
        "effective_date": "2026-08-01",
        "summary": "12-month residential apartment lease containing several one-sided tenant obligations, automatic 60-day renewal notice trap, non-negotiable monthly utility portal fees, and severe early termination liquidated damages.",
        "text": """RESIDENTIAL LEASE AGREEMENT

This Residential Lease Agreement ("Agreement") is made and entered into this 1st day of August, 2026, by and between Apex Property Management LLC ("Landlord"), and Jane Doe ("Tenant").

1. PREMISES AND TERM
1.1 Premises: Landlord hereby leases to Tenant, and Tenant hereby leases from Landlord, the residential apartment located at Unit 4B, 1400 Congress Avenue, Austin, Texas 78701 ("Premises").
1.2 Term: The lease term shall commence on September 1, 2026 ("Commencement Date") and shall expire on August 31, 2027 ("Expiration Date"), unless terminated earlier or extended in accordance with the terms herein.
1.3 Automatic Renewal: Tenant must provide written notice of intent not to renew at least sixty (60) days prior to the Expiration Date. Failure to deliver such notice sixty (60) calendar days in advance shall result in an automatic twelve (12) month renewal at Landlord's prevailing market rate plus a ten percent (10%) administrative surcharge.

2. RENT AND PAYMENT OBLIGATIONS
2.1 Monthly Rent: Tenant agrees to pay Landlord a base monthly rent of $2,450.00 USD, due on or before the first (1st) day of each calendar month.
2.2 Mandatory Utility & Technology Fees: In addition to the base rent, Tenant shall pay a mandatory monthly Community Technology Fee of $85.00, a Valet Trash Fee of $45.00, and a Building Maintenance Fee of $65.00, totaling $195.00 in non-negotiable monthly surcharges.
2.3 Late Charges: Rent received after 11:59 PM on the third (3rd) calendar day of the month shall incur an immediate late charge of $125.00, plus an additional daily penalty of $15.00 per day until all delinquent balances are settled in full.
2.4 Returned Payments: A fee of $75.00 will be assessed for any returned electronic check or insufficient funds transaction.

3. SECURITY DEPOSIT
3.1 Deposit Amount: Tenant shall deposit with Landlord the sum of $2,450.00 upon execution of this Agreement as a Security Deposit.
3.2 Deductions & Return: Landlord shall return the security deposit within sixty (60) days after complete surrender of the Premises. Landlord reserves unilateral authority to deduct repair costs, professional cleaning fees ($350 mandatory deduction upon move-out), and any outstanding surcharges.

4. EARLY TERMINATION AND LIQUIDATED DAMAGES
4.1 Tenant Early Termination: Tenant may not terminate this Agreement prior to the Expiration Date without express written consent. If Tenant vacates prior to lease conclusion, Tenant shall be liable for an Early Termination Fee equal to two (2) months' rent ($4,900.00), forfeiture of the entire Security Deposit ($2,450.00), and continued liability for monthly rent until a replacement tenant commences occupancy.
4.2 Military Deployment: Early termination rights under the Servicemembers Civil Relief Act (SCRA) remain subject to thirty (30) days' written notice and official orders.

5. USE, GUESTS, AND RESTRICTIONS
5.1 Guest Limitations: No guest or visitor may remain on the Premises for more than three (3) consecutive nights or more than seven (7) total nights within any calendar month without prior written approval of Landlord. Any unauthorized guest staying beyond this threshold shall be deemed an unauthorized subtenant, subjecting Tenant to an immediate $500.00 unauthorized occupant fine and potential eviction proceedings.
5.2 Pets: Pets are strictly prohibited without a separate Pet Addendum, a non-refundable $400.00 pet fee, and monthly pet rent of $50.00 per approved animal.
5.3 Quiet Enjoyment & Noise: Noise complaints verified by building security will incur a $150 penalty on the second occurrence.

6. MAINTENANCE AND REPAIRS
6.1 Minor Repairs: Tenant shall be solely responsible for the cost and execution of any maintenance or repair where the total cost is under $150.00, including but not limited to clogged drains, HVAC filter replacements, light bulbs, and smoke detector batteries.
6.2 Right of Entry: Landlord and Landlord's authorized agents may enter the Premises at any time between 8:00 AM and 7:00 PM for inspections, repairs, or showing the unit to prospective tenants with twelve (12) hours prior electronic notice, or without notice in emergency circumstances.

7. INDEMNIFICATION AND LIABILITY
7.1 Limitation of Landlord Liability: Landlord and its agents shall not be liable for any personal injury, property damage, loss of personal items, or theft occurring within the Premises, common areas, parking facilities, or storage rooms, regardless of whether caused by plumbing failures, weather events, vandalism, or negligence, unless caused by gross negligence or willful misconduct of Landlord.
7.2 Mandatory Renter's Insurance: Tenant shall maintain general liability insurance with coverage of at least $300,000.00 naming Landlord as an additional insured.

8. GOVERNING LAW AND DISPUTES
8.1 Governing Law: This Agreement shall be governed by and construed under the laws of the State of Texas.
8.2 Waiver of Jury Trial: Tenant and Landlord knowingly and voluntarily waive any right to trial by jury in any action or proceeding arising out of or related to this Lease. Any legal fees incurred by Landlord in enforcing this Agreement shall be reimbursed by Tenant.
"""
    },

    "freelance_contract": {
        "id": "freelance_contract",
        "title": "Master Freelance Software Services Agreement",
        "doc_type": "Independent Contractor Agreement",
        "parties": ["HyperScale Media Inc. (Client)", "Alex Rivera (Contractor)"],
        "effective_date": "2026-06-15",
        "summary": "Freelance development contract with heavy contractual asymmetries: assignment of all pre-existing IP, unlimited indemnification of client, net-90 payment terms with unilateral fee dispute withholdings, and broad non-compete clauses.",
        "text": """MASTER FREELANCE SOFTWARE SERVICES AGREEMENT

This Master Services Agreement ("Agreement") is executed on June 15, 2026, between HyperScale Media Inc. ("Client"), a Delaware corporation, and Alex Rivera ("Contractor"), an independent software engineer.

1. SERVICES AND DELIVERABLES
1.1 Scope of Work: Contractor agrees to develop, test, and deliver custom web applications, API integrations, and software components as detailed in subsequent Statements of Work ("SOW").
1.2 Standard of Performance: Contractor shall perform all work with the highest level of professional care, skill, and diligence. All deliverables must satisfy Client's subjective satisfaction before payment is released.

2. PAYMENT TERMS AND INVOICING
2.1 Compensation: Client shall pay Contractor at the fixed rate of $95.00 per hour for approved working hours.
2.2 Payment Schedule: Contractor shall submit invoices on the last day of each calendar month. Client shall pay undisputed invoice amounts within ninety (90) calendar days of invoice receipt ("Net-90").
2.3 Unilateral Dispute Right: Client reserves the right to withhold up to fifty percent (50%) of any invoice amount if Client determines, in its sole discretion, that deliverables require revision or fail to meet specifications.

3. INTELLECTUAL PROPERTY ASSIGNMENT
3.1 Work for Hire & Universal Assignment: Contractor agrees that all code, scripts, designs, discoveries, patents, copyrights, and intellectual property conceived, created, or reduced to practice by Contractor during the term of this Agreement shall be deemed "works made for hire" and shall become the sole and exclusive property of Client worldwide in perpetuity.
3.2 Pre-Existing IP Overreach: Contractor hereby assigns, transfers, and conveys to Client all rights, title, and interest in any background tools, open-source libraries, frameworks, or pre-existing code incorporated into or utilized in the deliverables, without reservation of license or residual ownership.

4. INDEMNIFICATION AND LIABILITY
4.1 Contractor Unlimited Indemnity: Contractor agrees to defend, indemnify, and hold harmless Client, its officers, directors, employees, and affiliates from and against any and all claims, damages, liabilities, losses, judgments, costs, and expenses (including reasonable attorneys' fees) arising out of or relating to: (a) any breach of this Agreement by Contractor; (b) any claim that deliverables infringe third-party intellectual property; or (c) any acts or omissions of Contractor.
4.2 Limitation of Client Liability: Client's maximum cumulative aggregate liability under this Agreement for any and all claims shall be limited to the total fees paid by Client to Contractor in the preceding thirty (30) days. In no event shall Client be liable for indirect, incidental, special, or consequential damages.

5. NON-COMPETITION AND NON-SOLICITATION
5.1 Non-Compete: During the term of this Agreement and for a period of twenty-four (24) months following termination, Contractor shall not directly or indirectly provide software engineering, consulting, or advisory services to any entity operating in digital media, SaaS marketing, or content distribution in North America.
5.2 Non-Solicitation of Personnel: Contractor shall not solicit, recruit, or hire any employee or contractor of Client for twenty-four (24) months after termination.

6. TERM AND TERMINATION
6.1 Termination for Convenience: Client may terminate this Agreement or any SOW at any time, for any reason or no reason, upon twenty-four (24) hours' written notice to Contractor. Contractor may terminate only upon sixty (60) days' prior written notice.
6.2 Effect of Termination: Upon termination, Contractor shall immediately deliver all work-in-progress to Client. Client shall not be liable for compensation for unapproved hours or post-termination wind-down.

7. GOVERNING LAW AND JURISDICTION
7.1 Governing Law: This Agreement shall be governed by and construed under the laws of the State of Delaware.
7.2 Dispute Venue: Any dispute, claim, or controversy shall be resolved exclusively in the state or federal courts located in Wilmington, Delaware. Contractor irrevocably waives any objection to inconvenient forum.
"""
    },

    "saas_agreement": {
        "id": "saas_agreement",
        "title": "Enterprise Cloud SaaS Terms of Service",
        "doc_type": "Cloud Services Agreement",
        "parties": ["NexusCloud Inc. (Provider)", "Enterprise Customer (Subscriber)"],
        "effective_date": "2026-03-01",
        "summary": "Commercial enterprise software agreement with standard balanced provisions: mutual confidentiality, 99.9% uptime SLA, 30-day termination notice, data protection compliance (GDPR/CCPA), and mutual liability caps.",
        "text": """ENTERPRISE CLOUD SOFTWARE-AS-A-SERVICE AGREEMENT

This Enterprise Cloud Software-as-a-Service Agreement ("Agreement") is made effective as of March 1, 2026, between NexusCloud Inc. ("Provider"), a California corporation, and Customer ("Subscriber").

1. SUBSCRIPTION SERVICES
1.1 Access Rights: Provider grants Subscriber a non-exclusive, non-transferable, worldwide right to access and utilize the NexusCloud Data Platform in accordance with the subscribed Tier and Documentation.
1.2 Service Level Agreement (SLA): Provider warrants that the Production Cloud Service shall maintain a monthly Service Availability of at least 99.9% uptime, excluding scheduled maintenance. If Provider fails to meet the SLA, Subscriber shall be eligible for Service Fee Credits calculated proportionally.

2. FEES AND BILLING
2.1 Subscription Fees: Subscriber shall pay subscription fees according to the executed Order Form. Invoices are payable within thirty (30) days of receipt ("Net-30").
2.2 Price Adjustments: Provider may adjust subscription pricing upon annual contract renewal upon giving at least sixty (60) days' advance written notice.

3. DATA PRIVACY AND SECURITY
3.1 Customer Data Ownership: Subscriber retains all right, title, and ownership in all data, records, and files uploaded or processed through the Service ("Customer Data"). Provider acquires no ownership rights.
3.2 Security Measures: Provider shall implement and maintain rigorous administrative, technical, and physical safeguards conforming to SOC 2 Type II and ISO 27001 standards to protect Customer Data against unauthorized access or disclosure.

4. CONFIDENTIALITY
4.1 Mutual Protection: Each party agrees to protect the Confidential Information of the other party with the same degree of care it uses for its own confidential materials, but not less than reasonable care.

5. LIMITATION OF LIABILITY
5.1 Mutual Cap on Damages: Except for breaches of confidentiality or gross negligence, each party's total aggregate liability arising out of or related to this Agreement shall be limited to the total amounts paid or payable by Subscriber in the twelve (12) months preceding the incident.

6. TERM AND TERMINATION
6.1 Term: The initial subscription term shall be twelve (12) months and shall renew for successive one-year periods unless either party provides written notice of non-renewal at least thirty (30) days prior to the expiration of the current term.
6.2 Termination for Cause: Either party may terminate upon thirty (30) days' written notice if the other party materially breaches any provision and fails to cure such breach within the notice period.

7. GOVERNING LAW
7.1 Governing Law: This Agreement is governed by the laws of the State of California, without regard to conflicts of law principles.
"""
    },

    "nda_mutual": {
        "id": "nda_mutual",
        "title": "Mutual Non-Disclosure & Confidentiality Agreement",
        "doc_type": "Non-Disclosure Agreement (NDA)",
        "parties": ["Apex Ventures Inc. (Party A)", "Innovatech Labs LLC (Party B)"],
        "effective_date": "2026-05-10",
        "summary": "Standard bilateral non-disclosure agreement with 2-year confidentiality duration, standard trade secret carve-outs, clear non-use restrictions, and equitable injunctive relief.",
        "text": """MUTUAL NON-DISCLOSURE AND CONFIDENTIALITY AGREEMENT

This Mutual Non-Disclosure Agreement ("Agreement") is entered into on May 10, 2026, by and between Apex Ventures Inc. ("Party A") and Innovatech Labs LLC ("Party B").

1. PURPOSE
The parties wish to explore a potential strategic commercial partnership, joint technology venture, or investment opportunity ("Purpose"). In connection with the Purpose, each party may disclose proprietary and confidential technical, business, and financial information.

2. CONFIDENTIAL INFORMATION DEFINITION
"Confidential Information" refers to any non-public information disclosed by one party ("Disclosing Party") to the other party ("Receiving Party"), whether orally, visually, electronically, or in writing, that is marked as confidential or that reasonably should be understood to be confidential given the nature of the information.

3. OBLIGATIONS AND STANDARD OF CARE
3.1 Protection: Receiving Party agrees to hold Disclosing Party's Confidential Information in strict confidence and not to disclose such information to any third party, except to employees, consultants, and legal advisors who have a need to know for the Purpose and are bound by confidentiality obligations at least as restrictive as those herein.
3.2 Standard of Care: Receiving Party shall use at least the degree of care it uses to protect its own sensitive information, but not less than a reasonable degree of care.
3.3 Non-Use: Receiving Party shall not use Confidential Information for any purpose other than evaluating or pursuing the Purpose.

4. EXCLUSIONS FROM CONFIDENTIAL TREATMENT
Confidential Information does not include information that: (a) is or becomes publicly known through no breach of this Agreement; (b) was already known to Receiving Party prior to disclosure; (c) is independently developed by Receiving Party without reference to Disclosing Party's information; or (d) is received from a third party without breach of duty.

5. DURATION OF OBLIGATIONS
The obligations of confidentiality shall remain in effect for a period of two (2) years from the date of disclosure, provided that trade secrets shall remain confidential for as long as they qualify as trade secrets under applicable law.

6. RETURN OR DESTRUCTION OF MATERIALS
Upon written request of Disclosing Party, Receiving Party shall promptly return or certify the destruction of all documents, files, copies, and extracts containing Confidential Information within fourteen (14) days.

7. INJUNCTIVE RELIEF AND GOVERNING LAW
7.1 Injunctive Relief: Receiving Party acknowledges that unauthorized disclosure may cause irreparable harm for which damages alone are inadequate, and Disclosing Party shall be entitled to seek equitable injunctive relief.
7.2 Governing Law: This Agreement shall be governed by and construed under the laws of the State of New York.
"""
    }
}
