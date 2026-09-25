/**
 * LegalLens AI - Extension Content Script
 */

(function() {
  const url = window.location.href.toLowerCase();
  const title = document.title.toLowerCase();
  const isLegalPage = url.includes("terms") || url.includes("privacy") || url.includes("policy") || url.includes("tos") || url.includes("agreement") || title.includes("terms") || title.includes("privacy");

  if (isLegalPage) {
    if (document.getElementById("legallens-floating-badge")) return;
    const badge = document.createElement("div");
    badge.id = "legallens-floating-badge";
    badge.innerHTML = `
      <div style="position: fixed; bottom: 20px; right: 20px; z-index: 999999; background: #0B0F19; border: 1px solid #38BDF8; box-shadow: 0 10px 25px rgba(0,0,0,0.5); padding: 8px 14px; border-radius: 50px; display: flex; align-items: center; gap: 8px; font-family: sans-serif; color: #FFF; font-size: 12px;">
        <span style="background: linear-gradient(135deg, #06B6D4, #3B82F6); width: 20px; height: 20px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-weight: 800; font-size: 10px;">⚖️</span>
        <span><strong>LegalLens AI:</strong> Legal Policy Detected</span>
        <button id="legallensScanBtn" style="background: #38BDF8; color: #070B14; border: none; border-radius: 12px; padding: 4px 10px; font-weight: 700; cursor: pointer; font-size: 11px;">Scan</button>
        <span id="legallensCloseBadge" style="cursor: pointer; color: #94A3B8; margin-left: 4px;">&times;</span>
      </div>
    `;
    document.body.appendChild(badge);

    document.getElementById("legallensScanBtn").addEventListener("click", () => {
      chrome.runtime.sendMessage({ action: "open_popup" });
    });
    document.getElementById("legallensCloseBadge").addEventListener("click", () => {
      badge.remove();
    });
  }
})();
