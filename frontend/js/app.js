/**
 * LegalLens AI - Main Application & State Coordinator
 */

let activeDocumentText = "";
let activeDocumentTitle = "Residential Lease";
let activePlaybookRules = [];
let sessionApiKey = "";

// ----------------- Tab Navigation & Accessible State -----------------

function switchTab(tabId) {
  // Update all tab panels
  document.querySelectorAll(".tab-content").forEach(el => {
    el.classList.remove("active");
  });
  const targetPanel = document.getElementById(tabId);
  if (targetPanel) {
    targetPanel.classList.add("active");
  }

  // Update all tab buttons (ARIA attributes)
  document.querySelectorAll(".sidebar-menu .nav-item").forEach(btn => {
    btn.classList.remove("active");
    btn.setAttribute("aria-selected", "false");
  });

  const activeBtn = document.querySelector(`[aria-controls="${tabId}"]`);
  if (activeBtn) {
    activeBtn.classList.add("active");
    activeBtn.setAttribute("aria-selected", "true");
  }

  // Update breadcrumb title
  const titles = {
    "tab-landing": "Overview",
    "tab-upload": "Upload Document",
    "tab-analysis": "Analysis Dashboard",
    "tab-chat": "Ask the Document",
    "tab-compare": "Compare Documents",
    "tab-portfolio": "Due Diligence Hub",
    "tab-playbooks": "Negotiation Playbooks",
    "tab-settings": "Privacy & Safety"
  };
  const titleEl = document.getElementById("current-view-title");
  if (titleEl && titles[tabId]) {
    titleEl.innerText = titles[tabId];
  }

  // Close mobile sidebar if open
  const sidebar = document.getElementById("sidebarNav");
  if (sidebar && sidebar.classList.contains("mobile-open")) {
    sidebar.classList.remove("mobile-open");
    const mobileBtn = document.getElementById("mobileMenuBtn");
    if (mobileBtn) mobileBtn.setAttribute("aria-expanded", "false");
  }
}

function toggleMobileSidebar() {
  const sidebar = document.getElementById("sidebarNav");
  const mobileBtn = document.getElementById("mobileMenuBtn");
  if (!sidebar) return;

  const isOpen = sidebar.classList.toggle("mobile-open");
  if (mobileBtn) {
    mobileBtn.setAttribute("aria-expanded", isOpen ? "true" : "false");
  }
}

// ----------------- Document State & Analysis -----------------

function setActiveDocument(text, title) {
  activeDocumentText = text;
  activeDocumentTitle = title || "Contract.txt";
  
  const titleEl = document.getElementById("sidebar-doc-title");
  if (titleEl) {
    titleEl.innerText = activeDocumentTitle;
  }
}

async function executeAnalysis(text, filename) {
  const loadingIndicator = document.getElementById("analysisLoading");
  if (loadingIndicator) loadingIndicator.style.display = "block";

  try {
    const apiKey = getStoredApiKey();
    const res = await fetch("/api/analyze", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        text: text,
        filename: filename || "Contract.txt",
        playbook_rules: getActivePlaybookRules(),
        api_key: apiKey
      })
    });

    if (!res.ok) {
      const errText = await res.text();
      console.warn("Analysis API returned non-OK:", res.status, errText);
      throw new Error(`Analysis status ${res.status}: ${errText}`);
    }
    const data = await res.json();
    renderAnalysisDashboard(data);
  } catch (err) {
    console.error("Analysis Error:", err);
    // Display in dashboard without intrusive window.alert popups
    const container = document.getElementById("analysisResultsContainer");
    if (container) {
      container.innerHTML = `
        <div style="background: rgba(239, 68, 68, 0.1); border: 1px solid rgba(239, 68, 68, 0.3); border-radius: 8px; padding: 18px; margin: 20px 0; color: #FCA5A5;">
          <h4 style="margin-bottom: 6px; font-weight: 600; color: #FFF;">⚠️ Analysis Notice</h4>
          <p style="font-size: 13.5px; line-height: 1.5; margin: 0;">Could not complete server analysis for "${escapeHtml(filename)}". Please verify your network connection or try re-submitting.</p>
        </div>
      `;
    }
  } finally {
    if (loadingIndicator) loadingIndicator.style.display = "none";
  }
}

function analyzePastedText() {
  const text = document.getElementById("pasteContractText").value.trim();
  if (!text || text.length < 50) {
    alert("Please enter or paste at least 50 characters of contract text.");
    return;
  }

  setActiveDocument(text, "Pasted Contract.txt");
  switchTab("tab-analysis");
  executeAnalysis(text, "Pasted Contract.txt");
}

function clearUploadFields() {
  document.getElementById("pasteContractText").value = "";
  const fileInput = document.getElementById("singleFileInput");
  if (fileInput) fileInput.value = "";
}

async function handleSingleFileSelect(event) {
  const file = event.target.files[0];
  if (!file) return;

  if (file.size > 15 * 1024 * 1024) {
    alert(`File '${file.name}' exceeds the maximum allowable size of 15MB.`);
    return;
  }

  const formData = new FormData();
  formData.append("file", file);
  const pbRules = getActivePlaybookRules();
  if (pbRules && pbRules.length > 0) {
    formData.append("playbook_rules", JSON.stringify(pbRules));
  }
  const apiKey = getStoredApiKey();
  if (apiKey) {
    formData.append("api_key", apiKey);
  }

  try {
    const res = await fetch("/api/analyze-upload", {
      method: "POST",
      body: formData
    });

    if (!res.ok) throw new Error("File upload failed: " + (await res.text()));
    const data = await res.json();

    setActiveDocument(data.extracted_text, file.name);
    switchTab("tab-analysis");
    renderAnalysisDashboard(data);
  } catch (err) {
    alert("Upload Error: " + err.message);
  }
}

// ----------------- Playbooks & Presets -----------------

const PLAYBOOK_PRESETS = {
  "freelancer": [
    {
      regex_pattern: "assign(?:s|ment)?.*?(?:all rights|pre-existing|background)",
      title: "Broad IP Assignment & Pre-Existing Code Loss",
      severity: "High",
      category: "Intellectual Property",
      impact: "Risk of assigning your background developer tools and personal libraries.",
      recommendation: "Carve out pre-existing IP and limit assignment strictly to custom deliverables."
    },
    {
      regex_pattern: "net[\\s\\-]90",
      title: "Extended Net-90 Payment Terms",
      severity: "High",
      category: "Payment Terms",
      impact: "Payment delayed for 3 months after invoice receipt.",
      recommendation: "Negotiate standard Net-30 payment terms."
    }
  ],
  "startup": [
    {
      regex_pattern: "indemnif(?:y|ies|ication).*?(?:unlimited|sole|all claims)",
      title: "Uncapped Indemnity Liability",
      severity: "Critical",
      category: "Liability & Indemnity",
      impact: "Exposes organization to unlimited third-party damages.",
      recommendation: "Cap all indemnity liabilities to total fees paid in past 12 months."
    },
    {
      regex_pattern: "automatic(?:ally)? renew(?:s|al)?",
      title: "Automatic Multi-Year Renewal",
      severity: "High",
      category: "Term & Termination",
      impact: "Accidental lock-in without prior reminder notice.",
      recommendation: "Require 30-day advance written notice prior to renewal."
    }
  ],
  "tenant": [
    {
      regex_pattern: "security deposit.*?(?:60|90)\\s+days",
      title: "Delayed Deposit Return (Over 30 Days)",
      severity: "High",
      category: "Security Deposit",
      impact: "Excessive delay in returning tenant security funds.",
      recommendation: "Enforce statutory 30-day deposit return timeline."
    },
    {
      regex_pattern: "entry.*?(?:12|6)\\s+hours|without notice",
      title: "Short Notice Landlord Entry",
      severity: "Medium",
      category: "Property Access",
      impact: "Allows landlord inspections on short notice.",
      recommendation: "Require minimum 24 hours advance written notice for non-emergencies."
    }
  ]
};

function loadPlaybookPreset(presetName) {
  if (PLAYBOOK_PRESETS[presetName]) {
    activePlaybookRules = [...PLAYBOOK_PRESETS[presetName]];
    renderPlaybookRulesUI();
    alert(`Loaded '${presetName}' negotiation playbook preset with ${activePlaybookRules.length} rules.`);
  }
}

function saveCustomRule() {
  const title = document.getElementById("ruleTitleInput").value.trim();
  const pattern = document.getElementById("rulePatternInput").value.trim();
  const severity = document.getElementById("ruleSeverityInput").value;
  const category = document.getElementById("ruleCategoryInput").value.trim() || "Custom Playbook";

  if (!title || !pattern) {
    alert("Please enter both a Rule Title and a Keyword / Regex Pattern.");
    return;
  }

  activePlaybookRules.push({
    title: title,
    regex_pattern: pattern,
    severity: severity,
    category: category,
    impact: "Custom organization rule match.",
    recommendation: "Review terms against internal negotiation playbook standards."
  });

  document.getElementById("ruleTitleInput").value = "";
  document.getElementById("rulePatternInput").value = "";
  renderPlaybookRulesUI();
}

function clearPlaybookRules() {
  activePlaybookRules = [];
  renderPlaybookRulesUI();
}

function getActivePlaybookRules() {
  return activePlaybookRules;
}

function renderPlaybookRulesUI() {
  const container = document.getElementById("playbookRulesContainer");
  const countEl = document.getElementById("playbookRuleCount");
  if (!container) return;

  if (countEl) countEl.innerText = activePlaybookRules.length;
  container.innerHTML = "";

  if (activePlaybookRules.length === 0) {
    container.innerHTML = `<div style="font-size: 13px; color: var(--text-muted);">No custom rules active. Standard legal risk engine is active.</div>`;
    return;
  }

  activePlaybookRules.forEach((rule, idx) => {
    const div = document.createElement("div");
    div.style.cssText = "display: flex; justify-content: space-between; align-items: center; background: rgba(30, 41, 59, 0.7); padding: 10px 14px; border-radius: 6px; border: 1px solid var(--border-subtle);";
    div.innerHTML = `
      <div>
        <div style="font-weight: 600; color: #FFF; font-size: 13.5px;">${escapeHtml(rule.title)}</div>
        <div style="font-size: 11.5px; color: var(--accent-cyan); font-family: monospace;">Pattern: ${escapeHtml(rule.regex_pattern)}</div>
      </div>
      <div style="display: flex; gap: 8px; align-items: center;">
        <span class="badge ${rule.severity === 'Critical' || rule.severity === 'High' ? 'badge-danger' : 'badge-warning'}">${escapeHtml(rule.severity)}</span>
        <button class="btn btn-secondary btn-sm" onclick="removePlaybookRule(${idx})" style="color: #f87171; padding: 4px 8px;" aria-label="Delete rule">&times;</button>
      </div>
    `;
    container.appendChild(div);
  });
}

function removePlaybookRule(idx) {
  activePlaybookRules.splice(idx, 1);
  renderPlaybookRulesUI();
}

// ----------------- Privacy, Safety & Session Data -----------------

function saveApiKey() {
  const key = document.getElementById("geminiApiKeyInput").value.trim();
  const sessionOnly = document.getElementById("sessionOnlyKeyToggle").checked;

  if (!key) {
    sessionApiKey = "";
    localStorage.removeItem("legallens_gemini_key");
    alert("API Key cleared.");
    return;
  }

  if (sessionOnly) {
    sessionApiKey = key;
    localStorage.removeItem("legallens_gemini_key");
    alert("API Key saved for current session only. (Will be discarded when tab is closed)");
  } else {
    sessionApiKey = key;
    localStorage.setItem("legallens_gemini_key", key);
    alert("API Key saved securely in your browser's localStorage.");
  }
}

function getStoredApiKey() {
  if (sessionApiKey) return sessionApiKey;
  return localStorage.getItem("legallens_gemini_key") || null;
}

function purgeAllSessionData() {
  activeDocumentText = "";
  activeDocumentTitle = "Residential Lease";
  sessionApiKey = "";
  localStorage.clear();
  clearUploadFields();
  clearBatchQueue();
  activePlaybookRules = [];
  renderPlaybookRulesUI();
  alert("All local session data and document memory purged.");
  switchTab("tab-landing");
}

// ----------------- Modals Management (with Focus Trap & Escape) -----------------

function openModal(modalId) {
  const modal = document.getElementById(modalId);
  if (modal) {
    modal.classList.add("active");
    const closeBtn = modal.querySelector(".modal-close-btn");
    if (closeBtn) closeBtn.focus();
  }
}

function closeModal(modalId) {
  const modal = document.getElementById(modalId);
  if (modal) {
    modal.classList.remove("active");
  }
}

function openDisclaimerModal() {
  openModal("disclaimerModal");
}

// Global keyboard listeners (Escape to close modals)
document.addEventListener("keydown", (e) => {
  if (e.key === "Escape") {
    document.querySelectorAll(".modal-overlay.active").forEach(m => {
      m.classList.remove("active");
    });
  }
});

// ----------------- Utilities -----------------

function escapeHtml(str) {
  if (!str) return "";
  return String(str)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#039;");
}

// Handle Browser Extension / URL Query Handoff
document.addEventListener("DOMContentLoaded", () => {
  const params = new URLSearchParams(window.location.search);
  if (params.get("ext_scan") === "1" || params.get("text")) {
    const passedText = params.get("text") || "";
    if (passedText) {
      setActiveDocument(passedText, "Browser Scanned Terms.txt");
      switchTab("tab-analysis");
      executeAnalysis(passedText, "Browser Scanned Terms.txt");
    } else {
      switchTab("tab-upload");
    }
  } else {
    // Set default active document metadata cleanly
    const defaultSample = (typeof EMBEDDED_SAMPLES !== "undefined" && EMBEDDED_SAMPLES["residential_lease"]) 
      ? EMBEDDED_SAMPLES["residential_lease"] 
      : { text: "", title: "Residential Lease" };
    setActiveDocument(defaultSample.text, defaultSample.title);
  }
});
