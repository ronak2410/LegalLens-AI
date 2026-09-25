/**
 * LegalLens AI - Sample Contracts Catalog Controller
 * Includes embedded local fallback for zero-latency offline & serverless resilience.
 */

"use strict";

const EMBEDDED_SAMPLES = {
  "residential_lease": {
    "id": "residential_lease",
    "title": "Residential Lease Agreement (Austin, TX)",
    "doc_type": "Residential Lease Agreement",
    "parties": ["Apex Property Management LLC (Landlord)", "Jane Doe (Tenant)"],
    "effective_date": "2026-08-01",
    "summary": "12-month residential apartment lease containing several one-sided tenant obligations, automatic 60-day renewal notice trap, non-negotiable monthly utility portal fees, and severe early termination liquidated damages.",
    "text": `RESIDENTIAL LEASE AGREEMENT

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
8.2 Waiver of Jury Trial: Tenant and Landlord knowingly and voluntarily waive any right to trial by jury in any action or proceeding arising out of or related to this Lease. Any legal fees incurred by Landlord in enforcing this Agreement shall be reimbursed by Tenant.`
  },

  "freelance_contract": {
    "id": "freelance_contract",
    "title": "Freelance Master Services Agreement & SOW",
    "doc_type": "Independent Contractor Agreement",
    "parties": ["Titan Digital Media Inc. (Client)", "Alex Rivera / AR Creative Solutions (Contractor)"],
    "effective_date": "2026-09-01",
    "summary": "Independent contractor agreement featuring aggressive un-capped client indemnification, 90-day deferred payment terms, full intellectual property assignment prior to payment, and an unreasonable 24-month non-compete.",
    "text": `MASTER SERVICES & INDEPENDENT CONTRACTOR AGREEMENT

This Master Services Agreement ("Agreement") is executed as of September 1, 2026, by and between Titan Digital Media Inc., a Delaware corporation ("Client"), and Alex Rivera d/b/a AR Creative Solutions ("Contractor").

1. SERVICES AND DELIVERABLES
1.1 Scope of Work: Contractor agrees to provide custom software engineering and UI/UX design deliverables as specified in applicable Statements of Work ("SOW").
1.2 Revisions and Acceptance: Client shall have forty-five (45) business days following receipt of any deliverable to evaluate and request unlimited modifications. If Client does not formally approve in writing, deliverables shall be deemed rejected without obligation of payment.

2. PAYMENT TERMS AND EXPENSES
2.1 Invoicing: Contractor may submit invoices on the final day of each calendar month.
2.2 Payment Window: Client agrees to remit payment within ninety (90) calendar days following receipt of a valid, undisputed invoice (Net-90 Payment Terms).
2.3 Expenses: All travel, hardware, and third-party software license costs are included in the agreed fixed project price and shall not be separately reimbursed.

3. INTELLECTUAL PROPERTY AND WORK FOR HIRE
3.1 Assignment of Rights: Contractor irrevocably agrees that all works of authorship, designs, software, inventions, source code, and improvements developed by Contractor in connection with this Agreement shall be deemed "Work Made for Hire". Contractor assigns all worldwide rights, copyright, patents, and trademarks to Client immediately upon creation, regardless of whether invoice amounts have been disbursed.
3.2 Moral Rights: Contractor irrevocably waives all moral rights, rights of attribution, and integrity in the Deliverables.
3.3 Pre-existing IP: Contractor retains no rights to pre-existing background libraries incorporated into the deliverables without prior written disclosure.

4. INDEMNIFICATION AND LIABILITY
4.1 Contractor Indemnification: Contractor shall defend, indemnify, and hold harmless Client, its officers, directors, and clients against any and all losses, claims, damages, liabilities, and legal defense costs arising from (i) any alleged infringement of third-party intellectual property, (ii) breach of this Agreement, or (iii) any negligent act or omission. This indemnity is uncapped and not subject to any limitation of liability.
4.2 Client Liability Cap: Client's total aggregate liability arising out of this Agreement shall not exceed $100.00 USD.

5. RESTRICTIVE COVENANTS
5.1 Non-Compete: During the term of this Agreement and for a period of twenty-four (24) months following termination, Contractor shall not directly or indirectly provide services, consult with, or be employed by any entity operating in competition with Client's digital media business within North America.
5.2 Non-Solicitation: Contractor shall not solicit any Client employee or client for a period of twelve (12) months.

6. GOVERNING LAW AND DISPUTE RESOLUTION
6.1 Governing Law: This Agreement is governed by the laws of the State of Delaware.
6.2 Arbitration: Any dispute shall be resolved through binding arbitration in Wilmington, Delaware. Each party shall bear its own arbitration costs.`
  },

  "saas_agreement": {
    "id": "saas_agreement",
    "title": "CloudMetrics B2B Subscription Agreement",
    "doc_type": "Software-as-a-Service (SaaS) Agreement",
    "parties": ["CloudMetrics Analytics Ltd. (Vendor)", "Enterprise Customer Inc. (Subscriber)"],
    "effective_date": "2026-07-15",
    "summary": "Commercial B2B SaaS agreement with mutual liability caps equal to 12 months fees, standard 99.9% uptime SLA service credit remedies, GDPR/CCPA data privacy protection, and mutual 30-day breach cure windows.",
    "text": `ENTERPRISE SOFTWARE-AS-A-SERVICE SUBSCRIPTION AGREEMENT

This Enterprise SaaS Agreement ("Agreement") is made on July 15, 2026, between CloudMetrics Analytics Ltd., a UK limited company ("Vendor"), and Enterprise Customer Inc., a Delaware corporation ("Subscriber").

1. SUBSCRIPTION SERVICES & ACCESS
1.1 Cloud Services: Vendor grants Subscriber a non-exclusive, non-transferable subscription to access and use the CloudMetrics analytics platform in accordance with the Order Form.
1.2 Service Level Agreement: Vendor shall use commercially reasonable efforts to make the Service available with an uptime percentage of at least 99.9% during each calendar month, excluding scheduled maintenance. If Vendor fails to meet this SLA, Subscriber is entitled to proportional service fee credits as sole and exclusive remedy.

2. DATA PRIVACY AND SECURITY
2.1 Customer Data: Subscriber retains all ownership rights, title, and interest in and to all data, information, or materials submitted by Subscriber ("Customer Data").
2.2 Data Protection: Vendor shall maintain appropriate technical and organizational safeguards adhering to SOC 2 Type II and ISO 27001 standards to protect Customer Data against unauthorized access, loss, or alteration.
2.3 Compliance: Both parties agree to comply with applicable data protection regulations including GDPR and CCPA.

3. FEES AND PAYMENT
3.1 Subscription Fees: Subscriber agrees to pay the fees set forth in the Order Form within thirty (30) days from invoice date.
3.2 Taxes: Fees are exclusive of sales, value-added, or withholding taxes.

4. LIMITATION OF LIABILITY
4.1 Mutual Liability Cap: Except for breaches of confidentiality or gross negligence, neither party's total aggregate liability arising out of or related to this Agreement shall exceed the total amount paid by Subscriber under the applicable Order Form in the twelve (12) months preceding the incident giving rise to liability.
4.2 Consequential Damages Waiver: Neither party shall be liable for indirect, incidental, special, punitive, or consequential damages.

5. TERM AND TERMINATION
5.1 Term: The initial subscription term is twelve (12) months from the Effective Date, renewing annually unless either party provides thirty (30) days' written notice prior to term expiration.
5.2 Termination for Cause: Either party may terminate this Agreement immediately upon written notice if the other party materially breaches any provision and fails to cure such breach within thirty (30) days.
5.3 Data Retrieval: Upon termination, Vendor shall provide Subscriber with thirty (30) days to export Customer Data before secure cryptographic erasure.

6. GOVERNING LAW
6.1 Governing Law: This Agreement shall be governed by and construed in accordance with the laws of the State of New York.`
  },

  "nda_agreement": {
    "id": "nda_agreement",
    "title": "Bilateral Mutual Non-Disclosure Agreement",
    "doc_type": "Mutual Non-Disclosure Agreement",
    "parties": ["Vanguard Robotics Inc.", "Aether Dynamics LLC"],
    "effective_date": "2026-06-01",
    "summary": "Standard mutual NDA protecting technical diagrams, financial projections, and proprietary algorithms with a 3-year confidentiality period, standard exclusions for public information, and trade secret protections.",
    "text": `MUTUAL NON-DISCLOSURE AND CONFIDENTIALITY AGREEMENT

This Mutual Non-Disclosure Agreement ("Agreement") is made effective as of June 1, 2026 ("Effective Date"), by and between Vanguard Robotics Inc. ("Party A") and Aether Dynamics LLC ("Party B").

1. PURPOSE
The parties wish to explore a potential strategic business collaboration regarding autonomous navigation technologies ("Purpose") and in connection with this Purpose, each party may disclose Confidential Information to the other.

2. DEFINITION OF CONFIDENTIAL INFORMATION
2.1 "Confidential Information" means all non-public information disclosed by one party ("Disclosing Party") to the other party ("Receiving Party"), whether orally or in writing, that is designated as confidential or that reasonably should be understood to be confidential given the nature of the information and the circumstances of disclosure.
2.2 Exclusions: Confidential Information does not include information that: (a) is or becomes publicly known through no breach by Receiving Party; (b) was already known to Receiving Party prior to disclosure; (c) is independently developed by Receiving Party without reference to Disclosing Party's information; or (d) is rightfully received from a third party without duty of confidentiality.

3. OBLIGATIONS OF RECEIVING PARTY
3.1 Standard of Care: Receiving Party shall use the same degree of care to protect Disclosing Party's Confidential Information as it uses for its own confidential information of like nature, but in no event less than reasonable care.
3.2 Restricted Use: Receiving Party shall use Confidential Information solely for the Purpose and shall disclose it only to employees, contractors, and legal advisors who need to know such information and are bound by confidentiality obligations at least as restrictive as those herein.

4. DURATION AND TERM
4.1 Term: This Agreement governs disclosures made within one (1) year from the Effective Date.
4.2 Confidentiality Period: The obligations of non-disclosure and non-use shall survive for a period of three (3) years from the date of disclosure; provided that with respect to trade secrets, obligations shall continue for as long as such information remains a trade secret under applicable law.

5. RETURN OR DESTRUCTION
Upon written request by Disclosing Party, Receiving Party shall promptly return or certify destruction of all documents, prototypes, and copies containing Confidential Information.

6. GOVERNING LAW AND INJUNCTIVE RELIEF
6.1 Governing Law: This Agreement shall be governed by the laws of the State of California.
6.2 Equitable Remedies: Both parties acknowledge that unauthorized disclosure of Confidential Information may cause irreparable harm for which monetary damages are inadequate, and agree that Disclosing Party shall be entitled to seek injunctive relief in addition to any other remedies available at law.`
  }
};

async function fetchSampleDocuments() {
  try {
    const res = await fetch("/api/samples");
    if (res.ok) {
      const data = await res.json();
      if (data && data.samples && data.samples.length > 0) {
        renderSampleCards(data.samples);
        return;
      }
    }
  } catch (err) {
    console.warn("API sample fetch failed, using embedded fallback:", err);
  }

  // Fallback to embedded catalog
  const fallbackList = Object.values(EMBEDDED_SAMPLES).map(doc => ({
    id: doc.id,
    title: doc.title,
    doc_type: doc.doc_type,
    parties: doc.parties,
    effective_date: doc.effective_date,
    summary: doc.summary,
    word_count: doc.text.split(/\s+/).length
  }));
  renderSampleCards(fallbackList);
}

function renderSampleCards(samples) {
  const container = document.getElementById("sampleCardsContainer");
  if (!container || !samples) return;

  container.innerHTML = "";
  samples.forEach(s => {
    const card = document.createElement("div");
    card.className = "card-container";
    card.style.display = "flex";
    card.style.flexDirection = "column";
    card.style.justifyContent = "space-between";

    card.innerHTML = `
      <div>
        <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 8px;">
          <span class="badge badge-cyan">${escapeHtml(s.doc_type)}</span>
          <span style="font-size: 11px; color: var(--text-muted);">${s.word_count} words</span>
        </div>
        <h3 style="font-family: var(--font-heading); font-size: 16px; color: #FFF; margin-bottom: 6px;">${escapeHtml(s.title)}</h3>
        <p style="font-size: 13px; color: var(--text-muted); line-height: 1.5; margin-bottom: 12px;">${escapeHtml(s.summary)}</p>
      </div>
      <button class="btn btn-secondary btn-sm" onclick="loadSampleContract('${s.id}')" style="width: 100%;">
        <span>Analyze This Sample &rarr;</span>
      </button>
    `;
    container.appendChild(card);
  });
}

async function loadSampleContract(sampleId) {
  let doc = null;

  try {
    const res = await fetch(`/api/samples/${sampleId}`);
    if (res.ok) {
      doc = await res.json();
    }
  } catch (err) {
    console.warn("API load failed, using embedded doc:", err);
  }

  // Use embedded sample if API didn't return JSON
  if (!doc && EMBEDDED_SAMPLES[sampleId]) {
    doc = EMBEDDED_SAMPLES[sampleId];
  }

  if (doc && doc.text) {
    setActiveDocument(doc.text, doc.title);
    switchTab("tab-analysis");
    executeAnalysis(doc.text, doc.title);
  } else {
    console.error("Sample contract could not be loaded:", sampleId);
  }
}

document.addEventListener("DOMContentLoaded", fetchSampleDocuments);
