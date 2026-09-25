/**
 * LegalLens AI - Document-Grounded Chat Controller
 */

async function fetchSuggestedQuestions() {
  try {
    const res = await fetch("/api/suggested-questions");
    if (!res.ok) return;
    const data = await res.json();
    renderSuggestionChips(data.categories);
  } catch (err) {
    console.error("Failed to load suggested questions:", err);
  }
}

function renderSuggestionChips(categories) {
  const container = document.getElementById("chatSuggestionChips");
  if (!container || !categories) return;

  container.innerHTML = "";
  categories.forEach(cat => {
    (cat.questions || []).forEach(q => {
      const chip = document.createElement("button");
      chip.className = "btn btn-secondary btn-sm";
      chip.style.fontSize = "12px";
      chip.style.padding = "4px 10px";
      chip.innerText = q;
      chip.onclick = () => {
        document.getElementById("chatQuestionInput").value = q;
        sendChatQuestion();
      };
      container.appendChild(chip);
    });
  });
}

async function sendChatQuestion() {
  const input = document.getElementById("chatQuestionInput");
  const question = input.value.trim();
  if (!question) return;

  if (!activeDocumentText) {
    alert("Please upload or select an active contract first.");
    return;
  }

  // Render user question
  appendChatMessage("user", question);
  input.value = "";

  try {
    const apiKey = getStoredApiKey();
    const res = await fetch("/api/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        question: question,
        document_text: activeDocumentText,
        document_title: activeDocumentTitle,
        api_key: apiKey
      })
    });

    if (!res.ok) throw new Error("Server error during Q&A");
    const data = await res.json();
    appendChatMessage("assistant", data.answer, data.citation, data.excerpt, data.explanation, data.is_grounded);
  } catch (err) {
    appendChatMessage("assistant", "Error: " + err.message, null, null, null, false);
  }
}

function appendChatMessage(sender, text, citation, excerpt, explanation, isGrounded) {
  const container = document.getElementById("chatHistoryContainer");
  const msgDiv = document.createElement("div");
  msgDiv.style.cssText = sender === "user" 
    ? "align-self: flex-end; background: rgba(56, 189, 248, 0.15); border: 1px solid rgba(56, 189, 248, 0.3); color: #FFF; padding: 10px 14px; border-radius: 8px; max-width: 80%; font-size: 13.5px;"
    : "align-self: flex-start; background: rgba(30, 41, 59, 0.8); border: 1px solid var(--border-subtle); color: #E2E8F0; padding: 12px 16px; border-radius: 8px; max-width: 85%; font-size: 13.5px; line-height: 1.5;";

  if (sender === "user") {
    msgDiv.innerText = text;
  } else {
    let citationHtml = "";
    if (citation && isGrounded) {
      citationHtml = `
        <div style="margin-top: 8px; display: flex; gap: 8px; align-items: center;">
          <button class="badge badge-cyan" style="cursor: pointer; border: 1px solid rgba(56, 189, 248, 0.4);" onclick="openCitationModal('${escapeJsString(citation)}', '${escapeJsString(excerpt)}', '${escapeJsString(explanation)}')">
            <span>📑 Verified: ${escapeHtml(citation)}</span>
          </button>
        </div>
      `;
    } else if (citation === "Out of Scope" || !isGrounded) {
      citationHtml = `
        <div style="margin-top: 6px;">
          <span class="badge badge-secondary" style="font-size: 10.5px;">Out of Document Scope</span>
        </div>
      `;
    }
    msgDiv.innerHTML = `<div>${escapeHtml(text)}</div>${citationHtml}`;
  }

  container.appendChild(msgDiv);
  container.scrollTop = container.scrollHeight;
}

function openCitationModal(citation, excerpt, explanation) {
  document.getElementById("citationModalTitle").innerText = citation || "Clause Reference";
  document.getElementById("citationModalExcerpt").innerText = excerpt || "Excerpt not available";
  document.getElementById("citationModalSummary").innerText = explanation || "";
  openModal("citationModal");
}

function escapeJsString(str) {
  if (!str) return "";
  return str.replace(/'/g, "\\'").replace(/"/g, '\\"').replace(/\n/g, " ");
}

document.addEventListener("DOMContentLoaded", fetchSuggestedQuestions);
