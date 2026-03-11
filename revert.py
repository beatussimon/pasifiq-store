import re

with open('static/css/main.css.bak', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Revert zoom-modal button
content = re.sub(r'\.zoom-modal img\s*\{.*?\}\s*\.zoom-modal button\s*\{.*?\}', 
                 '.zoom-modal img {\n  max-width: 100%;\n  max-height: 100%;\n  object-fit: contain;\n}', 
                 content, flags=re.DOTALL)

# 2. Revert review-header
content = re.sub(r'\.review-item\s*\{[^\}]+\}\s*\.review-header\s*\{[^\}]+\}\s*\.reviewer-info\s*\{',
                 '.review-item {\n  padding: 24px;\n  border-bottom: 1px solid var(--border);\n}\n\n.reviewer-info {',
                 content, flags=re.DOTALL)

# 3. Revert product-actions btn last-child
content = re.sub(r'\.product-actions\s*\{[^\}]+\}\s*\.product-actions \.btn:last-child:nth-child\(odd\)\s*\{[^\}]+\}',
                 '.product-actions {\n  display: grid;\n  grid-template-columns: 1fr 1fr;\n  gap: 16px;\n  margin-bottom: 16px;\n}',
                 content, flags=re.DOTALL)

# 4. Revert badge condition
content = re.sub(r'\.badge-featured.*?\.product-detail-title\s*\{',
                 '.badge-featured { background: var(--gold); color: white; }\n.badge-status-available { background: var(--success); color: white; }\n.badge-condition.badge-new { background: var(--brand-teal); color: white; }\n\n.product-detail-title {',
                 content, flags=re.DOTALL)

# 5. Revert stars
content = re.sub(r'\.product-rating-detail \.stars\s*\{[^\}]+\}',
                 '.product-rating-detail .stars {\n  color: var(--gold);\n  display: flex;\n  gap: 2px;\n}',
                 content, flags=re.DOTALL)

# 6. Revert inquiry section
old_inq = r'\.inquiry-section \{.*?\}\s*\.inquiry-form \{.*?\}\s*\.form-grid \{.*?\}\s*@media \(width <= 600px\) \{.*?\}\s*/\* Ratings & Reviews \*/\s*\.ratings-section \{.*?\}\s*\.ratings-header \{.*?\}\s*\.ratings-summary \{.*?\}\s*\.rating-login-prompt \{.*?\}\s*\.rating-login-prompt a \{.*?\}'
new_inq = '''.inquiry-section {
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: var(--radius-lg);
  padding: 32px;
  margin-bottom: 48px;
}

.inquiry-form {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
}

.inquiry-form .form-group:last-child {
  grid-column: span 2;
}

@media (width <= 600px) {
  .inquiry-form { grid-template-columns: 1fr; }
  .inquiry-form .form-group:last-child { grid-column: span 1; }
}

/* Ratings & Reviews */
.ratings-section {
  padding: 60px 0;
  border-top: 1px solid var(--border);
}

.ratings-summary {
  display: grid;
  grid-template-columns: auto 1fr auto;
  gap: 48px;
  align-items: center;
  background: var(--bg-surface);
  padding: 40px;
  border-radius: var(--radius-lg);
  margin-bottom: 48px;
}'''
content = re.sub(old_inq, new_inq, content, flags=re.DOTALL)

# 7. Revert price main
content = re.sub(r'\.price-main\s*\{[^\}]+\}\s*\.price-contact\s*\{[^\}]+\}\s*\[data-theme="dark"\] \.price-main\s*\{',
                 '.price-main {\n  font-size: 36px;\n  font-weight: 800;\n  color: var(--brand-ocean);\n  line-height: 1;\n}\n\n[data-theme="dark"] .price-main {',
                 content, flags=re.DOTALL)

# 8. Revert gallery-thumbs
content = re.sub(r'\.gallery-zoom-hint\s*\{[^\}]+\}\s*\.gallery-thumbs\s*\{[^\}]+\}\s*\.gallery-thumb\s*\{[^\}]+\}\s*\.gallery-thumb\.active\s*\{[^\}]+\}\s*\.gallery-thumb img\s*\{[^\}]+\}',
                 '.gallery-zoom-hint {\n  position: absolute;\n  bottom: 16px;\n  right: 16px;\n  background: rgb(0 0 0 / 50%);\n  color: white;\n  padding: 4px 12px;\n  border-radius: 20px;\n  font-size: 11px;\n  backdrop-filter: blur(4px);\n  pointer-events: none;\n}',
                 content, flags=re.DOTALL)

with open('static/css/main.css', 'w', encoding='utf-8') as f:
    f.write(content)
