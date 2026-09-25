/**
 * LegalLens AI - Analysis Dashboard Controller
 */

let activeAnalysisData = null;

function renderAnalysisDashboard(data) {
  activeAnalysisData = data;
  const meta = data.metadata || {};
  const risk = data.risk_assessment || {};

  // 1. Top Metrics
  document.getElementById("analysisRiskScore").innerText = `${risk.score}/100`;
  const riskLevelEl = document.getElementById("analysisRiskLevel");
  riskLevelEl.className = `badge ${risk.level === 'High' ? 'badge-danger' : risk.level === 'Medium' ? 'badge-warning' : 'badge-success'}`;
  riskLevelEl.innerText = `${risk.level} Risk`;
  document.getElementById("analysisRiskDesc").innerText = risk.description || "";
  document.getElementById("analysisDocType").innerText = meta.doc_type || "Commercial Contract";
  document.getElementById("analysisWordCount").innerText = `~${meta.word_count || 0} words • ${meta.governing_law || 'Jurisdiction not specified'}`;
  document.getElementById("analysisFlagCount").innerText = (data.risks_and_flags || []).length;
  document.getElementById("analysisActionCount").innerText = (data.checklist || []).length;

  // Update sidebar indicator
  const sideBadge = document.getElementById("sidebar-risk-badge");
  sideBadge.className = `nav-badge ${risk.level === 'High' ? 'badge-danger' : risk.level === 'Medium' ? 'badge-warning' : 'badge-success'}`;
  sideBadge.innerText = `${risk.level} Risk`;

  // 2. Executive Plain Summary
  const plainContainer = document.getElementById("plainSummaryContainer");
  plainContainer.innerHTML = "";
  (data.plain_language_summary || []).forEach(s => {
    const card = document.createElement("div");
    card.style.cssText = "background: rgba(15, 23, 42, 0.7); border: 1px solid var(--border-subtle); padding: 14px; border-radius: 8px;";
    card.innerHTML = `
      <h3 style="font-size: 14px; color: #FFF; font-weight: 700; margin-bottom: 6px;">${escapeHtml(s.title)}</h3>
      <p style="font-size: 13px; color: #CBD5E1; line-height: 1.5; margin-bottom: 8px;">${escapeHtml(s.simple_explanation)}</p>
      <div style="font-size: 12px; color: var(--accent-cyan);"><strong>Action:</strong> ${escapeHtml(s.what_to_do)}</div>
    `;
    plainContainer.appendChild(card);
  });

  // 3. Risks and Flags
  const flagsContainer = document.getElementById("riskFlagsContainer");
  flagsContainer.innerHTML = "";
  (data.risks_and_flags || []).forEach(flag => {
    const item = document.createElement("div");
    const sev = flag.severity || "Medium";
    const badgeClass = sev === "Critical" || sev === "High" ? "badge-danger" : sev === "Medium" ? "badge-warning" : "badge-secondary";
    item.style.cssText = "background: rgba(15, 23, 42, 0.7); border: 1px solid var(--border-subtle); padding: 14px; border-radius: 8px;";
    item.innerHTML = `
      <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
        <h3 style="font-size: 14px; color: #FFF; font-weight: 700;">${escapeHtml(flag.title)}</h3>
        <span class="badge ${badgeClass}">${escapeHtml(sev)}</span>
      </div>
      <p style="font-size: 13px; color: #CBD5E1; line-height: 1.5; margin-bottom: 8px;"><strong>Impact:</strong> ${escapeHtml(flag.impact)}</p>
      <div style="font-size: 12.5px; color: var(--accent-cyan); background: rgba(56, 189, 248, 0.08); padding: 8px 10px; border-radius: 6px;">
        <strong>Negotiation Advice:</strong> ${escapeHtml(flag.recommendation)}
      </div>
    `;
    flagsContainer.appendChild(item);
  });

  // 4. Proposed Redlines
  const redlinesContainer = document.getElementById("redlinesContainer");
  redlinesContainer.innerHTML = "";
  (data.redlines || []).forEach((red, idx) => {
    const card = document.createElement("div");
    card.style.cssText = "background: rgba(15, 23, 42, 0.7); border: 1px solid var(--border-subtle); padding: 16px; border-radius: 8px;";
    card.innerHTML = `
      <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
        <h3 style="font-size: 14px; color: #FFF; font-weight: 700;">${escapeHtml(red.title)}</h3>
        <button class="btn btn-secondary btn-sm" onclick="copyRedlineText(${idx})" id="copyRedBtn-${idx}">Copy Proposed Clause</button>
      </div>
      <p style="font-size: 12.5px; color: var(--text-muted); margin-bottom: 10px;">${escapeHtml(red.description || '')}</p>
      <div style="background: rgba(6, 78, 59, 0.2); border: 1px solid rgba(16, 185, 129, 0.4); padding: 12px; border-radius: 6px; font-family: monospace; font-size: 12.5px; color: #6EE7B7; line-height: 1.5;" id="redlineContent-${idx}">
        ${escapeHtml(red.proposed_clause)}
      </div>
    `;
    redlinesContainer.appendChild(card);
  });

  // 5. Annotated Document Viewer
  const docBody = document.getElementById("annotatedDocumentBody");
  docBody.innerHTML = data.annotated_html || escapeHtml(data.extracted_text || "");

  // 6. Checklist
  const chkContainer = document.getElementById("checklistContainer");
  chkContainer.innerHTML = "";
  (data.checklist || []).forEach(chk => {
    const div = document.createElement("div");
    div.style.cssText = "display: flex; align-items: center; gap: 8px; font-size: 13px; color: #CBD5E1;";
    const pBadge = chk.priority === "Urgent" ? "badge-danger" : chk.priority === "High" ? "badge-warning" : "badge-secondary";
    div.innerHTML = `
      <input type="checkbox" style="accent-color: var(--accent-cyan);">
      <span style="flex: 1;">${escapeHtml(chk.label)}</span>
      <span class="badge ${pBadge}" style="font-size: 10px;">${escapeHtml(chk.priority)}</span>
    `;
    chkContainer.appendChild(div);
  });

  // 7. Lawyer Questions
  const qContainer = document.getElementById("lawyerQuestionsContainer");
  qContainer.innerHTML = "";
  (data.lawyer_questions || []).forEach((q, i) => {
    const div = document.createElement("div");
    div.style.cssText = "font-size: 13px; color: #CBD5E1; padding: 6px 0; border-bottom: 1px solid rgba(255, 255, 255, 0.05);";
    div.innerHTML = `<strong>${i + 1}.</strong> ${escapeHtml(q)}`;
    qContainer.appendChild(div);
  });
}

function copyRedlineText(idx) {
  const content = document.getElementById(`redlineContent-${idx}`);
  if (content) {
    navigator.clipboard.writeText(content.innerText);
    const btn = document.getElementById(`copyRedBtn-${idx}`);
    if (btn) {
      btn.innerText = "Copied!";
      setTimeout(() => { btn.innerText = "Copy Proposed Clause"; }, 2000);
    }
  }
}

function generateClientMarkdownReport(data, title) {
  const meta = data.metadata || {};
  const risk = data.risk_assessment || {};
  const lines = [
    `# LegalLens AI Briefing Report: ${meta.title || title || 'Contract'}`,
    `**Date Generated:** ${meta.effective_date || new Date().toLocaleDateString()} | **Document Type:** ${meta.doc_type || 'Legal Agreement'}`,
    `**Overall Risk Profile:** ${risk.level || 'Moderate'} (${risk.score || 50}/100)`,
    `\n> **LEGAL DISCLAIMER:** LegalLens AI provides general legal information and is not a law firm or substitute for qualified legal advice.\n`,
    `## Executive Plain-Language Summary`
  ];
  (data.plain_language_summary || []).forEach(s => {
    lines.push(`### ${s.title}`);
    lines.push(`${s.simple_explanation}`);
    lines.push(`**Action:** ${s.what_to_do}\n`);
  });
  lines.push(`## Identified Risks & Contractual Asymmetries`);
  (data.risks_and_flags || []).forEach(r => {
    lines.push(`- **[${r.severity} Risk] ${r.title}** (${r.clause_ref || 'Clause'})`);
    lines.push(`  - *Impact:* ${r.impact}`);
    lines.push(`  - *Negotiation Tip:* ${r.recommendation}`);
  });
  lines.push(`\n## Proposed Counter-Language / Redlines`);
  (data.redlines || []).forEach(red => {
    lines.push(`### Proposed Redline: ${red.title}`);
    lines.push(`\`\`\`text\n${red.proposed_clause}\n\`\`\``);
  });
  lines.push(`\n## Questions for Your Attorney Consultation`);
  (data.lawyer_questions || []).forEach((q, i) => {
    lines.push(`${i + 1}. ${q}`);
  });
  lines.push(`\n## Pre-Signing Actionable Checklist`);
  (data.checklist || []).forEach(chk => {
    lines.push(`- [ ] **[${chk.priority}]** ${chk.label}`);
  });
  return lines.join("\n");
}

async function downloadLegalBriefMarkdown() {
  const textToUse = activeDocumentText || (typeof EMBEDDED_SAMPLES !== "undefined" && EMBEDDED_SAMPLES["residential_lease"] ? EMBEDDED_SAMPLES["residential_lease"].text : "");
  const titleToUse = activeDocumentTitle || "Residential Lease";

  // 1. Try Client-side instant export if activeAnalysisData is loaded
  if (activeAnalysisData) {
    const mdContent = generateClientMarkdownReport(activeAnalysisData, titleToUse);
    const blob = new Blob([mdContent], { type: "text/markdown;charset=utf-8" });
    const a = document.createElement("a");
    a.href = URL.createObjectURL(blob);
    a.download = `${titleToUse.replace(/\s+/g, '_')}_LegalLens_Report.md`;
    a.click();
    return;
  }

  // 2. Try Backend API
  try {
    const res = await fetch("/api/export-markdown", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        text: textToUse,
        filename: titleToUse,
        playbook_rules: getActivePlaybookRules()
      })
    });
    if (res.ok) {
      const data = await res.json();
      const blob = new Blob([data.markdown], { type: "text/markdown;charset=utf-8" });
      const a = document.createElement("a");
      a.href = URL.createObjectURL(blob);
      a.download = data.filename || "LegalLens_Report.md";
      a.click();
      return;
    }
  } catch (err) {
    console.warn("API export failed, generating basic fallback:", err);
  }

  // 3. Fallback direct download
  const fallbackContent = `# LegalLens AI Briefing: ${titleToUse}\n\n${textToUse}`;
  const blob = new Blob([fallbackContent], { type: "text/markdown;charset=utf-8" });
  const a = document.createElement("a");
  a.href = URL.createObjectURL(blob);
  a.download = `${titleToUse.replace(/\s+/g, '_')}_LegalLens_Report.md`;
  a.click();
}

async function downloadLegalBriefDocx() {
  const textToUse = activeDocumentText || (typeof EMBEDDED_SAMPLES !== "undefined" && EMBEDDED_SAMPLES["residential_lease"] ? EMBEDDED_SAMPLES["residential_lease"].text : "");
  const titleToUse = activeDocumentTitle || "Residential Lease";

  try {
    const res = await fetch("/api/export-docx", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        text: textToUse,
        filename: titleToUse,
        playbook_rules: getActivePlaybookRules()
      })
    });
    if (res.ok) {
      const blob = await res.blob();
      const a = document.createElement("a");
      a.href = URL.createObjectURL(blob);
      a.download = `${titleToUse.replace(/\s+/g, '_')}_LegalLens_Report.docx`;
      a.click();
      return;
    }
  } catch (err) {
    console.warn("DOCX backend export failed, falling back to Markdown export:", err);
  }

  // Fallback to Markdown download cleanly without intrusive alert dialogs
  downloadLegalBriefMarkdown();
}
