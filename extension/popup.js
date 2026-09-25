/**
 * LegalLens AI - Extension Popup Controller
 */

let activeExtractedText = "";
let activePageTitle = "";
const API_BASE = "http://localhost:8000";

document.addEventListener("DOMContentLoaded", async () => {
  const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
  if (tab) {
    document.getElementById("pageUrl").innerText = tab.url || "Active Tab";
    activePageTitle = tab.title || "Web Contract";
  }

  document.getElementById("btnScanPage").addEventListener("click", scanCurrentPage);
  document.getElementById("btnOpenStudio").addEventListener("click", openInFullStudio);
});

async function scanCurrentPage() {
  const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
  if (!tab || !tab.id) return;

  document.getElementById("initialView").style.display = "none";
  document.getElementById("loadingView").style.display = "block";

  try {
    const results = await chrome.scripting.executeScript({
      target: { tabId: tab.id },
      func: () => {
        const selection = window.getSelection().toString();
        if (selection && selection.length > 50) return selection;
        const mainEl = document.querySelector("main") || document.querySelector("article") || document.body;
        return mainEl ? mainEl.innerText : "";
      }
    });

    const pageText = results && results[0] ? results[0].result : "";
    if (!pageText || pageText.trim().length < 50) {
      throw new Error("Could not extract enough text. Please highlight the terms or open the studio directly.");
    }

    activeExtractedText = pageText;

    const res = await fetch(`${API_BASE}/api/analyze`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        text: pageText.slice(0, 25000),
        filename: `${activePageTitle.slice(0, 30)}.txt`
      })
    });

    if (!res.ok) throw new Error("Server error");
    const data = await res.json();
    renderResults(data);
  } catch (err) {
    alert("Scan Error: " + err.message);
    document.getElementById("initialView").style.display = "block";
    document.getElementById("loadingView").style.display = "none";
  }
}

function renderResults(data) {
  document.getElementById("loadingView").style.display = "none";
  document.getElementById("resultsView").style.display = "block";

  const risk = data.risk_assessment || {};
  document.getElementById("resRiskScore").innerText = `${risk.score || 0}/100`;
  const badgeEl = document.getElementById("resRiskBadge");
  badgeEl.className = `badge-${risk.level === 'High' ? 'danger' : risk.level === 'Medium' ? 'warning' : 'success'}`;
  badgeEl.innerText = `${risk.level || 'Evaluated'} Risk`;

  const flagsList = document.getElementById("resFlagsList");
  flagsList.innerHTML = "";
  const flags = data.risks_and_flags || [];
  document.getElementById("resFlagCount").innerText = flags.length;

  flags.slice(0, 3).forEach(f => {
    const div = document.createElement("div");
    div.style.cssText = "font-size: 11.5px; border-bottom: 1px solid rgba(255,255,255,0.05); padding-bottom: 4px;";
    div.innerHTML = `<strong style="color:#FFF;">⚠️ ${escapeHtml(f.title)}:</strong> <span style="color:#94A3B8;">${escapeHtml(f.impact)}</span>`;
    flagsList.appendChild(div);
  });
}

function openInFullStudio() {
  // Pass scraped text to web studio
  const encodedText = encodeURIComponent(activeExtractedText.slice(0, 15000));
  const url = `${API_BASE}/?ext_scan=1&text=${encodedText}`;
  chrome.tabs.create({ url });
}

function escapeHtml(str) {
  if (!str) return "";
  return String(str).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
}
