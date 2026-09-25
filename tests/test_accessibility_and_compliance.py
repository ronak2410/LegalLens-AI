"""
LegalLens AI - Accessibility (WCAG 2.1 AA) and Frontend Quality Test Suite.
Tests semantic landmarks, ARIA tablist patterns, modal accessibility, and absence of blocking alerts.
"""

import sys
import re
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
FRONTEND_DIR = BASE_DIR / "frontend"
PUBLIC_DIR = BASE_DIR / "public"

def test_html_semantic_landmarks():
    html_content = (FRONTEND_DIR / "index.html").read_text(encoding="utf-8")
    assert "<main" in html_content
    assert 'id="main-content"' in html_content
    assert "<nav" in html_content
    assert "<aside" in html_content
    assert "<header" in html_content
    assert 'lang="en"' in html_content

def test_aria_tablist_compliance():
    html_content = (FRONTEND_DIR / "index.html").read_text(encoding="utf-8")
    # All buttons in the tablist must have aria-controls matching an existing section
    tab_buttons = re.findall(r'<button\s+role="tab"[^>]+aria-controls="([^"]+)"', html_content)
    assert len(tab_buttons) >= 8
    for target_id in tab_buttons:
        assert f'id="{target_id}"' in html_content
        assert f'aria-labelledby="tab-btn-{target_id.replace("tab-", "")}"' in html_content or f'id="{target_id}"' in html_content

def test_modal_accessibility_attributes():
    html_content = (FRONTEND_DIR / "index.html").read_text(encoding="utf-8")
    modals = re.findall(r'<div\s+class="modal-overlay"[^>]+id="([^"]+)"([^>]*)>', html_content)
    assert len(modals) >= 2
    for modal_id, attrs in modals:
        assert 'role="dialog"' in attrs
        assert 'aria-modal="true"' in attrs
        assert 'aria-labelledby=' in attrs

def test_css_reduced_motion_support():
    css_content = (FRONTEND_DIR / "css" / "styles.css").read_text(encoding="utf-8")
    assert "prefers-reduced-motion" in css_content
    assert ":focus-visible" in css_content
    assert "--border-focus" in css_content

def test_no_blocking_window_alerts_in_js():
    js_files = list((FRONTEND_DIR / "js").glob("*.js"))
    assert len(js_files) >= 5
    for js_file in js_files:
        content = js_file.read_text(encoding="utf-8")
        # Ensure raw blocking alert() calls are replaced with non-intrusive showToast
        raw_alerts = re.findall(r'\balert\(', content)
        assert len(raw_alerts) == 0, f"Blocking window.alert() found in {js_file.name}"

def test_toast_notification_container_present():
    html_content = (FRONTEND_DIR / "index.html").read_text(encoding="utf-8")
    assert 'id="toastContainer"' in html_content
    assert 'role="status"' in html_content or 'aria-live="polite"' in html_content
