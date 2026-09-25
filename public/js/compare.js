/**
 * LegalLens AI - Document Comparator Controller
 * Side-by-side contract comparison and quantifiable Risk Shift Delta calculation.
 * @file compare.js
 */

"use strict";

async function loadSampleComparison() {
  try {
    let docAText = "";
    let docBText = "";

    if (typeof EMBEDDED_SAMPLES !== "undefined" && EMBEDDED_SAMPLES["residential_lease"] && EMBEDDED_SAMPLES["freelance_contract"]) {
      docAText = EMBEDDED_SAMPLES["residential_lease"].text;
      docBText = EMBEDDED_SAMPLES["freelance_contract"].text;
    } else {
      const resA = await fetch("/api/samples/residential_lease");
      const resB = await fetch("/api/samples/freelance_contract");
      if (resA.ok && resB.ok) {
        const docA = await resA.json();
        const docB = await resB.json();
        docAText = docA.text;
        docBText = docB.text;
      }
    }

    document.getElementById("compareDoc1Text").value = docAText;
    document.getElementById("compareDoc2Text").value = docBText;
    showToast("Loaded sample comparison drafts.", "info");
    executeComparison();
  } catch (err) {
    showToast("Error loading sample comparison: " + err.message, "error");
  }
}

async function executeComparison() {
  const doc1 = document.getElementById("compareDoc1Text").value.trim();
  const doc2 = document.getElementById("compareDoc2Text").value.trim();

  if (!doc1 || !doc2) {
    showToast("Please provide contract text for both Document A and Document B.", "warning");
    return;
  }

  try {
    const res = await fetch("/api/compare", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        doc1_text: doc1,
        doc2_text: doc2,
        doc1_name: "Document A",
        doc2_name: "Document B"
      })
    });

    if (!res.ok) throw new Error("Comparison calculation failed on server.");
    const data = await res.json();
    renderComparisonResults(data);
    showToast("Comparison analysis complete.", "success");
  } catch (err) {
    showToast("Comparison Error: " + err.message, "error");
  }
}

function renderComparisonResults(data) {
  const wrapper = document.getElementById("comparisonResultsWrapper");
  if (!wrapper) return;
  wrapper.style.display = "block";

  document.getElementById("compRiskShiftTitle").innerText = data.risk_shift_title || "Comparison Matrix";
  document.getElementById("compRiskShiftSummary").innerText = data.risk_shift_summary || "";

  const tbody = document.getElementById("comparisonMatrixBody");
  if (!tbody) return;
  tbody.innerHTML = "";

  (data.comparison_matrix || []).forEach(row => {
    const tr = document.createElement("tr");
    const badgeClass = row.status === "Unfavorable Shift" ? "badge-danger" : row.status === "Favorable Protection" ? "badge-success" : "badge-secondary";
    tr.innerHTML = `
      <td style="font-weight: 600; color: #FFF;">${escapeHtml(row.category)}</td>
      <td style="font-size: 13px; color: #CBD5E1;">${escapeHtml(row.doc1_summary)}</td>
      <td style="font-size: 13px; color: #CBD5E1;">${escapeHtml(row.doc2_summary)}</td>
      <td><span class="badge ${badgeClass}">${escapeHtml(row.status)}</span></td>
    `;
    tbody.appendChild(tr);
  });
}
