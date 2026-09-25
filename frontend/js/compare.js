/**
 * LegalLens AI - Document Comparator Controller
 */

async function loadSampleComparison() {
  try {
    const resA = await fetch("/api/samples/residential_lease");
    const resB = await fetch("/api/samples/freelance_contract");
    if (!resA.ok || !resB.ok) return;
    const docA = await resA.json();
    const docB = await resB.json();

    document.getElementById("compareDoc1Text").value = docA.text;
    document.getElementById("compareDoc2Text").value = docB.text;
    executeComparison();
  } catch (err) {
    alert("Error loading sample comparison: " + err.message);
  }
}

async function executeComparison() {
  const doc1 = document.getElementById("compareDoc1Text").value.trim();
  const doc2 = document.getElementById("compareDoc2Text").value.trim();

  if (!doc1 || !doc2) {
    alert("Please provide contract text for both Document A and Document B.");
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

    if (!res.ok) throw new Error("Comparison error");
    const data = await res.json();
    renderComparisonResults(data);
  } catch (err) {
    alert("Comparison Error: " + err.message);
  }
}

function renderComparisonResults(data) {
  const wrapper = document.getElementById("comparisonResultsWrapper");
  wrapper.style.display = "block";

  document.getElementById("compRiskShiftTitle").innerText = data.risk_shift_title;
  document.getElementById("compRiskShiftSummary").innerText = data.risk_shift_summary;

  const tbody = document.getElementById("comparisonMatrixBody");
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
