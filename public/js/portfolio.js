/**
 * LegalLens AI - Multi-Document Due Diligence Portfolio Controller
 * Batch audits 2 to 10 contracts concurrently to surface cross-contract contradictions and milestones.
 * @file portfolio.js
 */

"use strict";

let queuedBatchFiles = [];
let activePortfolioData = null;

function handleBatchFileSelect(event) {
  const files = Array.from(event.target.files);
  if (!files || files.length === 0) return;

  for (const file of files) {
    if (file.size > 15 * 1024 * 1024) {
      showToast(`File '${file.name}' exceeds the 15MB limit and was skipped.`, "warning");
      continue;
    }
    if (!queuedBatchFiles.some(f => f.name === file.name)) {
      queuedBatchFiles.push(file);
    }
  }
  updateBatchFileListUI();
  showToast(`Added ${files.length} document(s) to portfolio queue.`, "info");
}

function updateBatchFileListUI() {
  const container = document.getElementById("batchFileItemsContainer");
  const listWrapper = document.getElementById("batchSelectedFilesList");
  const countEl = document.getElementById("batchFileCount");

  if (!container || !listWrapper) return;

  if (queuedBatchFiles.length === 0) {
    listWrapper.style.display = "none";
    return;
  }

  listWrapper.style.display = "block";
  countEl.innerText = queuedBatchFiles.length;
  container.innerHTML = "";

  queuedBatchFiles.forEach((file, index) => {
    const sizeStr = file.size ? `${(file.size / 1024).toFixed(1)} KB` : 'Sample Text';
    const item = document.createElement("div");
    item.style.cssText = "display: flex; justify-content: space-between; align-items: center; background: rgba(30, 41, 59, 0.7); border: 1px solid var(--border-subtle); padding: 10px 14px; border-radius: 8px;";
    
    item.innerHTML = `
      <div style="display: flex; align-items: center; gap: 10px;">
        <svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="#c084fc" stroke-width="2" aria-hidden="true"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/></svg>
        <div>
          <div style="font-weight: 600; color: #FFF; font-size: 13.5px;">${escapeHtml(file.name)}</div>
          <div style="font-size: 11.5px; color: var(--text-muted);">${sizeStr}</div>
        </div>
      </div>
      <button class="btn btn-secondary btn-sm" onclick="removeBatchFile(${index})" style="padding: 4px 8px; color: #f87171;" aria-label="Remove ${escapeHtml(file.name)} from batch">
        &times;
      </button>
    `;
    container.appendChild(item);
  });
}

function removeBatchFile(index) {
  queuedBatchFiles.splice(index, 1);
  updateBatchFileListUI();
  showToast("File removed from queue.", "info");
}

function clearBatchQueue() {
  queuedBatchFiles = [];
  updateBatchFileListUI();
  document.getElementById("batchResultsDashboard").style.display = "none";
  showToast("Portfolio queue cleared.", "info");
}

async function loadSamplePortfolio() {
  try {
    queuedBatchFiles = [];
    if (typeof EMBEDDED_SAMPLES !== "undefined") {
      Object.keys(EMBEDDED_SAMPLES).forEach(k => {
        const doc = EMBEDDED_SAMPLES[k];
        queuedBatchFiles.push({
          name: `${doc.title}.txt`,
          text: doc.text,
          isVirtual: true,
          size: doc.text.length
        });
      });
    } else {
      const res = await fetch("/api/samples");
      const data = await res.json();
      for (const s of data.samples) {
        const detailRes = await fetch(`/api/samples/${s.id}`);
        const doc = await detailRes.json();
        queuedBatchFiles.push({
          name: `${doc.title}.txt`,
          text: doc.text,
          isVirtual: true,
          size: doc.text.length
        });
      }
    }

    updateBatchFileListUI();
    showToast("Loaded 4 pre-configured contracts into Due Diligence Hub.", "success");
    executeBatchAnalysis();
  } catch (err) {
    showToast("Error loading sample portfolio: " + err.message, "error");
  }
}

async function executeBatchAnalysis() {
  if (queuedBatchFiles.length === 0) {
    showToast("Please upload or select at least one document for portfolio analysis.", "warning");
    return;
  }

  const dashboard = document.getElementById("batchResultsDashboard");
  dashboard.style.display = "none";

  try {
    const playbookRules = getActivePlaybookRules();
    let result = null;
    const hasRealFiles = queuedBatchFiles.some(f => f instanceof File);

    if (hasRealFiles) {
      const formData = new FormData();
      queuedBatchFiles.forEach(f => {
        if (f instanceof File) {
          formData.append("files", f);
        } else if (f.text) {
          const blob = new Blob([f.text], { type: "text/plain" });
          formData.append("files", blob, f.name);
        }
      });
      if (playbookRules && playbookRules.length > 0) {
        formData.append("playbook_rules", JSON.stringify(playbookRules));
      }

      const res = await fetch("/api/upload-batch", { method: "POST", body: formData });
      if (!res.ok) throw new Error(await res.text());
      result = await res.json();
    } else {
      const payload = {
        documents: queuedBatchFiles.map(f => ({ text: f.text, filename: f.name })),
        playbook_rules: playbookRules
      };

      const res = await fetch("/api/analyze-batch", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload)
      });
      if (!res.ok) throw new Error(await res.text());
      result = await res.json();
    }

    activePortfolioData = result;
    renderPortfolioDashboard(result);
    showToast("Portfolio due diligence analysis complete.", "success");
  } catch (err) {
    showToast("Batch Due Diligence Error: " + err.message, "error");
  }
}

function renderPortfolioDashboard(data) {
  const dashboard = document.getElementById("batchResultsDashboard");
  dashboard.style.display = "block";

  const summary = data.summary || {};
  document.getElementById("batchKpiScore").innerText = `${summary.average_risk_score || 0}/100`;
  const badgeEl = document.getElementById("batchKpiBadge");
  badgeEl.className = `badge ${summary.portfolio_badge === 'critical' ? 'badge-danger' : summary.portfolio_badge === 'warning' ? 'badge-warning' : 'badge-success'}`;
  badgeEl.innerText = summary.portfolio_status || "Evaluated";
  document.getElementById("batchKpiDocCount").innerText = summary.total_documents || 0;

  const highCriticalCount = (summary.risk_distribution?.Critical || 0) + (summary.risk_distribution?.High || 0);
  document.getElementById("batchKpiHighCount").innerText = highCriticalCount;

  // Conflicts
  const conflictsContainer = document.getElementById("batchConflictsContainer");
  conflictsContainer.innerHTML = "";
  if (!data.cross_contract_conflicts || data.cross_contract_conflicts.length === 0) {
    conflictsContainer.innerHTML = `<div style="font-size: 13px; color: #10b981;">No direct jurisdictional contradictions or compounding indemnity concentrations detected.</div>`;
  } else {
    data.cross_contract_conflicts.forEach(c => {
      const div = document.createElement("div");
      div.style.cssText = "background: rgba(15, 23, 42, 0.6); border: 1px solid rgba(239, 68, 68, 0.2); padding: 12px; border-radius: 8px;";
      div.innerHTML = `
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 4px;">
          <strong style="color: #fca5a5; font-size: 13.5px;">${escapeHtml(c.type)}</strong>
          <span class="badge badge-danger">${escapeHtml(c.severity)} Exposure</span>
        </div>
        <p style="color: #CBD5E1; font-size: 13px; margin-bottom: 6px;">${escapeHtml(c.description)}</p>
        <div style="font-size: 11.5px; color: var(--text-muted);">Impacted Contracts: <em>${escapeHtml(c.impacted_contracts.join(', '))}</em></div>
      `;
      conflictsContainer.appendChild(div);
    });
  }

  // Risk Matrix
  const matrixBody = document.getElementById("batchRiskMatrixBody");
  matrixBody.innerHTML = "";
  (data.risk_matrix || []).forEach(cat => {
    const tr = document.createElement("tr");
    const highBadge = cat.critical_high_count > 0 
      ? `<span class="badge badge-danger">${cat.critical_high_count} High</span>`
      : `<span class="badge badge-secondary">0 High</span>`;
    tr.innerHTML = `
      <td style="font-weight: 600; color: #FFF;">${escapeHtml(cat.category)}</td>
      <td style="text-align: center; color: #CBD5E1;">${cat.total_flags}</td>
      <td style="text-align: center;">${highBadge}</td>
      <td style="font-size: 12.5px; color: var(--accent-cyan);">${escapeHtml(cat.affected_contracts.join(', '))}</td>
    `;
    matrixBody.appendChild(tr);
  });

  // Timeline
  const timelineContainer = document.getElementById("batchTimelineContainer");
  timelineContainer.innerHTML = "";
  (data.timeline_milestones || []).forEach(m => {
    const item = document.createElement("div");
    item.style.cssText = "display: flex; justify-content: space-between; align-items: center; background: rgba(30, 41, 59, 0.5); padding: 10px 14px; border-radius: 8px; border-left: 3px solid var(--accent-cyan);";
    item.innerHTML = `
      <div>
        <div style="font-weight: 600; color: #FFF; font-size: 13.5px;">${escapeHtml(m.event)}</div>
        <div style="font-size: 12px; color: var(--text-muted); margin-top: 2px;">${escapeHtml(m.date_detail)}</div>
      </div>
      <span class="badge badge-cyan">${escapeHtml(m.contract)}</span>
    `;
    timelineContainer.appendChild(item);
  });
}

function exportBatchMarkdown() {
  if (!activePortfolioData) return;
  const d = activePortfolioData;
  const s = d.summary;

  const lines = [
    `# LegalLens AI Due Diligence Portfolio Briefing`,
    `**Audited Contracts:** ${s.total_documents} | **Portfolio Health:** ${s.portfolio_status} (${s.average_risk_score}/100)`,
    `**Total Risk Flags Identified:** ${s.total_risk_flags}`,
    `\n> **LEGAL DISCLAIMER:** LegalLens AI provides general legal information and is not a law firm or substitute for qualified legal advice.\n`,
    `## Cross-Contract Contradictions & Exposures`
  ];

  (d.cross_contract_conflicts || []).forEach(c => {
    lines.push(`### [${c.severity} Exposure] ${c.type}`);
    lines.push(`${c.description}`);
    lines.push(`*Impacted Contracts:* ${c.impacted_contracts.join(', ')}\n`);
  });

  lines.push(`## Consolidated Risk Matrix by Category`);
  (d.risk_matrix || []).forEach(r => {
    lines.push(`- **${r.category}:** ${r.total_flags} flags (${r.critical_high_count} Critical/High) across [${r.affected_contracts.join(', ')}]`);
  });

  const blob = new Blob([lines.join('\n')], { type: 'text/markdown' });
  const a = document.createElement('a');
  a.href = URL.createObjectURL(blob);
  a.download = `LegalLens_Due_Diligence_Portfolio_Report.md`;
  a.click();
  showToast("Downloaded portfolio briefing report (.md)", "success");
}
