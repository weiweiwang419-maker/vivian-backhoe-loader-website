#!/usr/bin/env python3
"""Add 5 new sections to index.html: B(How I Work), C(Comparison Table), D(Where We Ship), F(FAQ Preview), H(CTA Box)"""

import re

INDEX_PATH = "/Users/vivianwang/WorkBuddy/2026-07-01-16-58-56/vivian_website/index.html"

with open(INDEX_PATH, "r", encoding="utf-8") as f:
    html = f.read()

# ============================================================
# 1. CSS for all 5 new sections (insert before </style>)
# ============================================================
NEW_CSS = """
  /* === B. How I Work === */
  .how-section { background: #fff; }
  .how-steps {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 0;
    position: relative;
    counter-reset: step;
  }
  .how-steps::before {
    content: '';
    position: absolute;
    top: 40px;
    left: 12.5%;
    right: 12.5%;
    height: 2px;
    background: var(--border);
    z-index: 0;
  }
  .how-step {
    text-align: center;
    padding: 0 20px;
    position: relative;
    z-index: 1;
  }
  .how-step-num {
    width: 80px;
    height: 80px;
    margin: 0 auto 24px;
    border-radius: 50%;
    background: #fff;
    border: 3px solid var(--primary);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 28px;
    font-weight: 800;
    color: var(--primary);
    transition: all 0.3s;
  }
  .how-step:hover .how-step-num {
    background: var(--primary);
    color: #fff;
    transform: scale(1.05);
  }
  .how-step h3 {
    font-size: 18px;
    font-weight: 700;
    margin-bottom: 10px;
  }
  .how-step p {
    font-size: 14px;
    color: var(--text-light);
    line-height: 1.6;
  }

  /* === C. Comparison Table === */
  .compare-section { background: var(--cream); }
  .compare-table-wrap {
    overflow-x: auto;
    border-radius: 8px;
    box-shadow: 0 4px 20px rgba(0,0,0,0.06);
  }
  .compare-table {
    width: 100%;
    border-collapse: collapse;
    background: #fff;
    min-width: 760px;
  }
  .compare-table th {
    background: var(--primary);
    color: #fff;
    padding: 18px 16px;
    text-align: left;
    font-size: 13px;
    font-weight: 600;
    letter-spacing: 0.5px;
    white-space: nowrap;
  }
  .compare-table th:first-child { border-radius: 8px 0 0 0; }
  .compare-table th:last-child { border-radius: 0 8px 0 0; }
  .compare-table td {
    padding: 16px;
    border-bottom: 1px solid var(--border);
    font-size: 14px;
    color: var(--text);
  }
  .compare-table td:first-child {
    font-weight: 700;
    color: var(--primary);
  }
  .compare-table tr:last-child td { border-bottom: none; }
  .compare-table tr:nth-child(even) { background: #faf8f3; }
  .compare-table tr:hover { background: #f0ede4; }
  .compare-table .model-link {
    color: var(--primary);
    text-decoration: none;
    font-weight: 700;
  }
  .compare-table .model-link:hover { text-decoration: underline; }
  .compare-table .best-for {
    font-size: 12px;
    color: var(--text-light);
    font-style: italic;
  }

  /* === D. Where We Ship === */
  .ship-section { background: #fff; }
  .ship-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 24px;
  }
  .ship-card {
    background: var(--cream);
    border-radius: 8px;
    padding: 36px 28px;
    text-align: center;
    border: 1px solid var(--border);
    transition: transform 0.3s, box-shadow 0.3s;
  }
  .ship-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 12px 32px rgba(0,0,0,0.08);
  }
  .ship-emoji {
    font-size: 40px;
    margin-bottom: 16px;
  }
  .ship-card h3 {
    font-size: 18px;
    font-weight: 700;
    margin-bottom: 12px;
    color: var(--primary);
  }
  .ship-card .ship-countries {
    font-size: 13px;
    color: var(--text);
    margin-bottom: 12px;
    line-height: 1.7;
  }
  .ship-card .ship-time {
    font-size: 12px;
    color: var(--accent);
    font-weight: 600;
    background: rgba(239, 159, 39, 0.1);
    padding: 6px 14px;
    border-radius: 20px;
    display: inline-block;
  }

  /* === F. FAQ Preview === */
  .faq-preview-section { background: var(--cream); }
  .faq-preview-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 20px;
    margin-bottom: 40px;
  }
  .faq-preview-item {
    background: #fff;
    border-radius: 8px;
    padding: 28px 32px;
    border: 1px solid var(--border);
    cursor: pointer;
    transition: all 0.3s;
  }
  .faq-preview-item:hover {
    box-shadow: 0 8px 24px rgba(0,0,0,0.06);
    border-color: var(--primary);
  }
  .faq-preview-item .fp-q {
    font-size: 16px;
    font-weight: 700;
    color: var(--text);
    margin-bottom: 12px;
    display: flex;
    align-items: flex-start;
    gap: 10px;
  }
  .faq-preview-item .fp-q::before {
    content: 'Q';
    flex-shrink: 0;
    width: 24px;
    height: 24px;
    background: var(--primary);
    color: #fff;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 12px;
    font-weight: 700;
    margin-top: 1px;
  }
  .faq-preview-item .fp-a {
    font-size: 14px;
    color: var(--text-light);
    line-height: 1.7;
    padding-left: 34px;
  }
  .faq-preview-item .fp-a strong { color: var(--text); }
  .faq-preview-cta {
    text-align: center;
  }
  .faq-preview-cta a {
    color: var(--primary);
    font-weight: 600;
    font-size: 15px;
    text-decoration: none;
    border-bottom: 2px solid var(--primary);
    padding-bottom: 2px;
    transition: color 0.2s;
  }
  .faq-preview-cta a:hover { color: var(--primary-dark); }

  /* === H. CTA Box === */
  .cta-box-section {
    background: var(--primary-dark);
    padding: 100px 40px;
    text-align: center;
    position: relative;
    overflow: hidden;
  }
  .cta-box-section::before {
    content: '';
    position: absolute;
    top: -50%;
    right: -10%;
    width: 500px;
    height: 500px;
    background: radial-gradient(circle, rgba(239, 159, 39, 0.08), transparent);
    border-radius: 50%;
  }
  .cta-box-inner {
    max-width: 900px;
    margin: 0 auto;
    position: relative;
    z-index: 1;
  }
  .cta-box-section h2 {
    font-size: clamp(32px, 4vw, 48px);
    font-weight: 800;
    color: #fff;
    margin-bottom: 20px;
    letter-spacing: -0.5px;
    line-height: 1.2;
  }
  .cta-box-section .cta-subtitle {
    font-size: 18px;
    color: rgba(255,255,255,0.8);
    margin-bottom: 48px;
    line-height: 1.6;
    max-width: 680px;
    margin-left: auto;
    margin-right: auto;
  }
  .cta-box-buttons {
    display: flex;
    gap: 20px;
    justify-content: center;
    flex-wrap: wrap;
    margin-bottom: 40px;
  }
  .cta-box-btn {
    display: inline-flex;
    align-items: center;
    gap: 10px;
    padding: 18px 36px;
    text-decoration: none;
    font-weight: 700;
    font-size: 16px;
    border-radius: 6px;
    transition: all 0.2s;
  }
  .cta-box-btn.whatsapp {
    background: #25D366;
    color: #fff;
  }
  .cta-box-btn.whatsapp:hover {
    background: #1da851;
    transform: translateY(-2px);
    box-shadow: 0 12px 32px rgba(37, 211, 102, 0.3);
  }
  .cta-box-btn.quote {
    background: var(--accent);
    color: var(--primary-dark);
  }
  .cta-box-btn.quote:hover {
    background: #e08e15;
    transform: translateY(-2px);
    box-shadow: 0 12px 32px rgba(239, 159, 39, 0.3);
  }
  .cta-box-btn.email {
    background: transparent;
    color: #fff;
    border: 2px solid rgba(255,255,255,0.3);
  }
  .cta-box-btn.email:hover {
    border-color: #fff;
    background: rgba(255,255,255,0.05);
  }
  .cta-trust-row {
    display: flex;
    gap: 40px;
    justify-content: center;
    flex-wrap: wrap;
    padding-top: 40px;
    border-top: 1px solid rgba(255,255,255,0.1);
  }
  .cta-trust-item {
    text-align: center;
  }
  .cta-trust-item .trust-num {
    font-size: 28px;
    font-weight: 800;
    color: var(--accent);
    margin-bottom: 4px;
  }
  .cta-trust-item .trust-label {
    font-size: 13px;
    color: rgba(255,255,255,0.6);
    letter-spacing: 0.5px;
  }

  /* === Responsive for new sections === */
  @media (max-width: 1024px) {
    .how-steps { grid-template-columns: repeat(2, 1fr); gap: 40px; }
    .how-steps::before { display: none; }
    .ship-grid { grid-template-columns: repeat(2, 1fr); }
    .faq-preview-grid { grid-template-columns: 1fr; }
  }
  @media (max-width: 768px) {
    .how-steps { grid-template-columns: 1fr; gap: 32px; }
    .ship-grid { grid-template-columns: 1fr; }
    .cta-box-buttons { flex-direction: column; align-items: stretch; }
    .cta-box-btn { justify-content: center; }
    .cta-trust-row { gap: 24px; }
  }
"""

# Insert CSS before </style>
html = html.replace("  .footer-logo-row {\n    display: flex;\n    align-items: center;\n    margin-bottom: 12px;\n  }\n</style>", 
                    "  .footer-logo-row {\n    display: flex;\n    align-items: center;\n    margin-bottom: 12px;\n  }\n" + NEW_CSS + "</style>")

# ============================================================
# 2. Insert B (How I Work) after Vivian Video section, before Why Me
# ============================================================
SECTION_B = """
<!-- How I Work -->
<section class="how-section">
  <div class="container">
    <div class="section-eyebrow">How it works</div>
    <h2 class="section-title">From first message to your port — 4 steps.</h2>
    <p class="section-subtitle">No middlemen, no mystery. Here's exactly what happens when you message me.</p>
    <div class="how-steps">
      <div class="how-step">
        <div class="how-step-num">1</div>
        <h3>Tell me your needs</h3>
        <p>What's your job? Budget? Site conditions? I listen first, sell second.</p>
      </div>
      <div class="how-step">
        <div class="how-step-num">2</div>
        <h3>I recommend models</h3>
        <p>Based on your needs, I pick 1-2 models that fit. Not the most expensive — the right one.</p>
      </div>
      <div class="how-step">
        <div class="how-step-num">3</div>
        <h3>Factory inspection</h3>
        <p>Before it ships, I walk the line. I send you photos and video of YOUR machine.</p>
      </div>
      <div class="how-step">
        <div class="how-step-num">4</div>
        <h3>Ship to your port</h3>
        <p>I handle export docs, loading, and shipping. You pick it up at your port.</p>
      </div>
    </div>
  </div>
</section>

<!-- Why Me -->"""

html = html.replace("<!-- Why Me -->", SECTION_B, 1)

# ============================================================
# 3. Insert C (Comparison Table) after Products section, before From the Floor
# ============================================================
SECTION_C = """
<!-- Product Comparison Table -->
<section class="compare-section">
  <div class="container">
    <div class="section-eyebrow">Compare at a glance</div>
    <h2 class="section-title">All 7 models, side by side.</h2>
    <p class="section-subtitle">Don't know which one fits? Start here. Tap any model name for full specs.</p>
    <div class="compare-table-wrap">
      <table class="compare-table">
        <thead>
          <tr>
            <th>Model</th>
            <th>Operating Weight</th>
            <th>Engine</th>
            <th>Dig Depth</th>
            <th>Max Speed</th>
            <th>Best For</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td><a href="product-bl105-25.html" class="model-link">BL 105-25</a></td>
            <td>10,870 kg</td>
            <td>73 kW Weichai</td>
            <td>4,000 mm</td>
            <td>40 km/h</td>
            <td class="best-for">Heavy duty, road construction</td>
          </tr>
          <tr>
            <td><a href="product-bl90-25.html" class="model-link">BL 90-25</a></td>
            <td>9,000 kg</td>
            <td>73 kW Weichai</td>
            <td>3,800 mm</td>
            <td>40 km/h</td>
            <td class="best-for">All-round, most popular</td>
          </tr>
          <tr>
            <td><a href="product-bl80-25.html" class="model-link">BL 80-25</a></td>
            <td>8,000 kg</td>
            <td>73 kW Weichai</td>
            <td>3,600 mm</td>
            <td>40 km/h</td>
            <td class="best-for">Balanced power and price</td>
          </tr>
          <tr>
            <td><a href="product-bl70-25.html" class="model-link">BL 70-25</a></td>
            <td>6,300 kg</td>
            <td>55 kW Yuchai</td>
            <td>3,400 mm</td>
            <td>35 km/h</td>
            <td class="best-for">Farms, orchards, small sites</td>
          </tr>
          <tr>
            <td><a href="product-bl45-18.html" class="model-link">BL 45-18</a></td>
            <td>4,500 kg</td>
            <td>48 kW Xinchai</td>
            <td>3,000 mm</td>
            <td>30 km/h</td>
            <td class="best-for">Compact, tight job sites</td>
          </tr>
          <tr>
            <td><a href="product-bl35-12.html" class="model-link">BL 35-12</a></td>
            <td>3,500 kg</td>
            <td>37 kW Xinchai</td>
            <td>2,800 mm</td>
            <td>25 km/h</td>
            <td class="best-for">Entry-level, light work</td>
          </tr>
          <tr>
            <td><a href="product-bl15-06.html" class="model-link">BL 15-06</a></td>
            <td>1,500 kg</td>
            <td>72V/120V Electric</td>
            <td>1,580 mm</td>
            <td>&mdash;</td>
            <td class="best-for">Electric, indoor & urban</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</section>

<!-- From the Floor -->"""

html = html.replace("<!-- From the Floor -->", SECTION_C, 1)

# ============================================================
# 4. Insert D (Where We Ship) after From the Floor, before Contact
# ============================================================
SECTION_D = """
<!-- Where We Ship -->
<section class="ship-section">
  <div class="container">
    <div class="section-eyebrow">Where I ship</div>
    <h2 class="section-title">Shipping to 95% of ports worldwide.</h2>
    <p class="section-subtitle">I specialize in emerging markets. These are the regions I ship to most. Tell me your port — I'll find the route.</p>
    <div class="ship-grid">
      <div class="ship-card">
        <div class="ship-emoji">🌍</div>
        <h3>Africa</h3>
        <div class="ship-countries">Nigeria, Kenya, Ghana, South Africa, Egypt, Tanzania, Morocco</div>
        <div class="ship-time">20-45 days by sea</div>
      </div>
      <div class="ship-card">
        <div class="ship-emoji">🌏</div>
        <h3>Southeast Asia</h3>
        <div class="ship-countries">Philippines, Indonesia, Vietnam, Thailand, Malaysia, Myanmar</div>
        <div class="ship-time">7-15 days by sea</div>
      </div>
      <div class="ship-card">
        <div class="ship-emoji">🕌</div>
        <h3>Middle East</h3>
        <div class="ship-countries">UAE, Saudi Arabia, Qatar, Turkey, Iran, Iraq, Kuwait</div>
        <div class="ship-time">20-30 days by sea</div>
      </div>
      <div class="ship-card">
        <div class="ship-emoji">🌎</div>
        <h3>South America</h3>
        <div class="ship-countries">Brazil, Chile, Peru, Colombia, Argentina, Ecuador</div>
        <div class="ship-time">30-45 days by sea</div>
      </div>
    </div>
  </div>
</section>

<!-- Contact -->"""

html = html.replace("<!-- Contact -->", SECTION_D, 1)

# ============================================================
# 5. Insert F (FAQ Preview) before CTA Box, and replace Contact with H (CTA Box)
# ============================================================
SECTION_F_H = """
<!-- FAQ Preview -->
<section class="faq-preview-section">
  <div class="container">
    <div class="section-eyebrow">Quick answers</div>
    <h2 class="section-title">Things buyers ask me most.</h2>
    <p class="section-subtitle">The 4 questions I get on WhatsApp every week. For the full list, visit the FAQ page.</p>
    <div class="faq-preview-grid">
      <div class="faq-preview-item">
        <div class="fp-q">How long does delivery take to my country?</div>
        <div class="fp-a">Sea freight transit time depends on your destination: <strong>Asia 7-15 days</strong>, Middle East 20-30 days, Africa 20-45 days, South America 30-45 days. I'll confirm the exact time in your quotation.</div>
      </div>
      <div class="faq-preview-item">
        <div class="fp-q">What warranty do you offer?</div>
        <div class="fp-a"><strong>12-month warranty or 1,500-2,000 working hours</strong>, whichever comes first. Exact terms vary by model and are confirmed in the quotation.</div>
      </div>
      <div class="faq-preview-item">
        <div class="fp-q">What payment methods do you accept?</div>
        <div class="fp-a"><strong>T/T (wire transfer)</strong>: 30% deposit in advance, 70% balance before shipment. Minimum order is 1 unit. Bulk orders get discounted pricing.</div>
      </div>
      <div class="faq-preview-item">
        <div class="fp-q">Can the machine be customized?</div>
        <div class="fp-a">All backhoe loaders can be customized with your preferred color at <strong>no extra cost</strong>. Over 40 attachments available. Customization lead time is 35-40 days.</div>
      </div>
    </div>
    <div class="faq-preview-cta">
      <a href="faq.html">See all 18 questions →</a>
    </div>
  </div>
</section>

<!-- CTA Box -->
<section class="cta-box-section" id="contact">
  <div class="cta-box-inner">
    <h2>Ready to find your machine?</h2>
    <p class="cta-subtitle">Text me on WhatsApp. Tell me what you're building. I'll tell you which machine fits — no pressure, no markup, no BS. Just honest advice from someone who checks every machine before it ships.</p>
    <div class="cta-box-buttons">
      <a href="https://wa.me/8618911415465?text=Hi%20Vivian%2C%20I%27d%20like%20to%20get%20a%20quote%20for%20a%20backhoe%20loader." class="cta-box-btn whatsapp">💬 WhatsApp +86 189 1141 5465</a>
      <a href="quote.html" class="cta-box-btn quote">📋 Get a detailed quote</a>
      <a href="mailto:vivian.aolite@gmail.com" class="cta-box-btn email">✉️ vivian.aolite@gmail.com</a>
    </div>
    <div class="cta-trust-row">
      <div class="cta-trust-item">
        <div class="trust-num">7</div>
        <div class="trust-label">Models available</div>
      </div>
      <div class="cta-trust-item">
        <div class="trust-num">12<span style="font-size:18px;">mo</span></div>
        <div class="trust-label">Warranty</div>
      </div>
      <div class="cta-trust-item">
        <div class="trust-num">95%</div>
        <div class="trust-label">Ports covered</div>
      </div>
      <div class="cta-trust-item">
        <div class="trust-num">1<span style="font-size:18px;">hr</span></div>
        <div class="trust-label">Avg response time</div>
      </div>
    </div>
  </div>
</section>

<!-- Footer -->"""

# Replace the entire Contact section + Footer marker
old_contact = """<!-- Contact -->
<section class="contact-section" id="contact">
  <div class="container">
    <div class="section-eyebrow">Get in touch</div>
    <h2 class="section-title">Text me. I usually reply within an hour.</h2>
    <p class="section-subtitle">I'm at the factory from 8am to 6pm (GMT+8). If I don't reply right away, I'm probably under a machine. WhatsApp is the fastest way to reach me.</p>
    <div class="contact-buttons">
      <a href="https://wa.me/8618911415465" class="contact-btn primary">💬 WhatsApp +86 189 1141 5465</a>
      <a href="quote.html" class="contact-btn secondary">📋 Get a detailed quote</a>
      <a href="mailto:vivian.aolite@gmail.com" class="contact-btn secondary">✉️ vivian.aolite@gmail.com</a>
    </div>
  </div>
</section>

<!-- Footer -->"""

html = html.replace(old_contact, SECTION_F_H, 1)

# ============================================================
# Write the modified file
# ============================================================
with open(INDEX_PATH, "w", encoding="utf-8") as f:
    f.write(html)

print("Done! All 5 sections added:")
print("  B. How I Work - 4-step process flow")
print("  C. Comparison Table - 7 models side by side")
print("  D. Where We Ship - 4 region cards")
print("  F. FAQ Preview - 4 key FAQs")
print("  H. CTA Box - Enhanced contact section with trust indicators")
