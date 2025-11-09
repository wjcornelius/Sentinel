#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Create ODT file with formatted email for OpenOffice
"""

from odf.opendocument import OpenDocumentText
from odf.style import Style, TextProperties, ParagraphProperties
from odf.text import P, Span, H

# Create document
doc = OpenDocumentText()

# Define styles
# Title style
title_style = Style(name="Title", family="paragraph")
title_props = ParagraphProperties(textalign="center")
title_style.addElement(title_props)
title_text = TextProperties(fontsize="16pt", fontweight="bold")
title_style.addElement(title_text)
doc.styles.addElement(title_style)

# Heading style
heading_style = Style(name="Heading", family="paragraph")
heading_text = TextProperties(fontsize="14pt", fontweight="bold", color="#2E86AB")
heading_style.addElement(heading_text)
doc.styles.addElement(heading_style)

# Box style (for highlighted sections)
box_style = Style(name="Box", family="paragraph")
box_props = ParagraphProperties(padding="0.1in", border="0.02in solid #2E86AB", backgroundcolor="#E8F4F8")
box_style.addElement(box_props)
box_text = TextProperties(fontsize="11pt")
box_style.addElement(box_text)
doc.styles.addElement(box_style)

# Bullet style
bullet_style = Style(name="Bullet", family="paragraph")
bullet_props = ParagraphProperties(marginleft="0.3in")
bullet_style.addElement(bullet_props)
doc.styles.addElement(bullet_style)

# Bold text style
bold_style = Style(name="Bold", family="text")
bold_text = TextProperties(fontweight="bold")
bold_style.addElement(bold_text)
doc.styles.addElement(bold_style)

# Divider style
divider_style = Style(name="Divider", family="paragraph")
divider_props = ParagraphProperties(textalign="center", borderbottom="0.02in solid #999999")
divider_style.addElement(divider_props)
doc.styles.addElement(divider_style)

# Normal text
normal_style = Style(name="Normal", family="paragraph")
normal_text = TextProperties(fontsize="11pt")
normal_style.addElement(normal_text)
doc.styles.addElement(normal_style)

# Add content
# Subject
p = P(stylename=title_style, text="Subject: Christmas Gift Request - New Laptop")
doc.text.addElement(p)

# Blank line
doc.text.addElement(P())

# Opening
p = P(stylename=normal_style, text="Hi Sis and Marc,")
doc.text.addElement(p)

doc.text.addElement(P())

p = P(stylename=normal_style)
p.addText("I hope you're both doing well! I wanted to reach out about Christmas this year. Instead of regular gifts, I'd really appreciate help with something practical that I need — a new laptop for the development work I've been doing.")
doc.text.addElement(p)

doc.text.addElement(P())

p = P(stylename=normal_style)
p.addText("My current setup is struggling with the programming projects I'm working on, and I could really use an upgrade. I've done some research and found a laptop that would be perfect:")
doc.text.addElement(p)

doc.text.addElement(P())

# Laptop box
p = P(stylename=box_style)
p.addText("📱  Lenovo Yoga 7 14\" 2-in-1")
doc.text.addElement(p)
p = P(stylename=box_style)
p.addText("     AMD Ryzen AI 7 350 Processor")
doc.text.addElement(p)
p = P(stylename=box_style)
p.addText("     Best Buy: $950-$1000")
doc.text.addElement(p)
p = P(stylename=box_style)
p.addText("     (Sometimes on sale!)")
doc.text.addElement(p)

doc.text.addElement(P())

# Why this model
p = P(stylename=heading_style, text="✨ WHY THIS SPECIFIC MODEL WOULD BE PERFECT:")
doc.text.addElement(p)

doc.text.addElement(P())

reasons = [
    ("2-in-1 convertible with touchscreen", "Flexible for different uses, can fold into tablet mode"),
    ("Fingerprint reader for security", "Important for the financial API work I'm doing"),
    ("HDMI port (critical!)", "I need this to connect to my 60\" TV for larger display when coding"),
    ("Multiple USB ports for peripherals", "Keyboard, mouse, external drives, etc."),
    ("1TB internal storage", "Plenty of room for my projects and data"),
    ("AMD processor with AI capabilities built in (50 TOPS NPU)", "Helps with the development work I'm doing, can run local AI models")
]

for title, desc in reasons:
    p = P(stylename=bullet_style)
    p.addText(f"✓  {title}")
    doc.text.addElement(p)
    p = P(stylename=bullet_style)
    p.addText(f"     → {desc}")
    doc.text.addElement(p)
    doc.text.addElement(P())

# Closing of first section
p = P(stylename=normal_style)
p.addText("I know it's more than a typical gift, but it would make a huge difference for the work I'm doing. I'm on SSI so big purchases like this aren't easy for me to swing on my own.")
doc.text.addElement(p)

doc.text.addElement(P())

p = P(stylename=normal_style)
p.addText("If this works for you both, I can send you the Best Buy link. No pressure at all — I completely understand if it's outside the budget. Just thought I'd ask!")
doc.text.addElement(p)

doc.text.addElement(P())
doc.text.addElement(P())

p = P(stylename=normal_style, text="Love you both,")
doc.text.addElement(p)
p = P(stylename=normal_style, text="WJ")
doc.text.addElement(p)

doc.text.addElement(P())
doc.text.addElement(P())

# Divider
p = P(stylename=divider_style)
p.addText("━" * 80)
doc.text.addElement(p)

doc.text.addElement(P())
doc.text.addElement(P())

# Technical section
p = P(stylename=heading_style, text="🔧 FOR MARC: TECHNICAL DETAILS")
doc.text.addElement(p)

doc.text.addElement(P())

p = P(stylename=normal_style)
p.addText("Hey Marc - since you're a computer scientist, I figured you'd want the technical justification for this specific model. Here's what I'm working on and why this laptop fits:")
doc.text.addElement(p)

doc.text.addElement(P())

# Project Overview
p = P(stylename=heading_style, text="📊  PROJECT OVERVIEW: \"Sentinel Corporation\"")
doc.text.addElement(p)

doc.text.addElement(P())

p = P(stylename=normal_style)
p.addText("I've built an automated stock trading system that uses multiple AI models (GPT-4o, GPT-4o-mini, GPT-5, Perplexity) to analyze markets and generate trading decisions.")
doc.text.addElement(p)

doc.text.addElement(P())

p = P(stylename=normal_style)
p.addText("Architecture: Simulated corporate structure with departments (Research, Risk, Compliance, Trading, etc.) that communicate via message passing.")
doc.text.addElement(p)

doc.text.addElement(P())

# System Requirements
p = P(stylename=heading_style, text="⚙️  CURRENT SYSTEM REQUIREMENTS")
doc.text.addElement(p)

doc.text.addElement(P())

reqs = [
    "Real-time market data processing (Alpaca API integration)",
    "Multiple concurrent AI API calls (OpenAI, Perplexity)",
    "SQLite database operations",
    "Complex portfolio optimization algorithms",
    "File I/O for caching and message passing between \"departments\"",
    "Git version control for 50+ Python files"
]

for req in reqs:
    p = P(stylename=bullet_style)
    p.addText(f"  • {req}")
    doc.text.addElement(p)

doc.text.addElement(P())

# Why this laptop
p = P(stylename=heading_style, text="💻  WHY THIS SPECIFIC LAPTOP")
doc.text.addElement(p)

doc.text.addElement(P())

sections = [
    ("1️⃣  AMD Ryzen AI 7 350 Processor (50 TOPS NPU)", [
        "Built-in Neural Processing Unit for local AI inference",
        "Run smaller language models locally vs. cloud APIs only",
        "Reduces monthly costs (currently $10-20/month on OpenAI)",
        "Enables offline development and testing with local LLMs"
    ]),
    ("2️⃣  1TB Storage", [
        "Current codebase: ~2GB with cache/logs",
        "Market data cache grows 10-50MB per trading day",
        "Room for backtest data and historical analysis",
        "Space for local model weights (7B-13B param models = 4-8GB each)"
    ]),
    ("3️⃣  HDMI Output (Essential!)", [
        "Connect to 60\" TV as extended display",
        "Multiple windows: code editor, terminal, logs, market data, DB viewer",
        "Current workflow needs 2-3 monitors worth of real estate"
    ]),
    ("4️⃣  2-in-1 Touchscreen", [
        "Tablet mode for reviewing logs and trading reports away from desk",
        "Touchscreen for quick navigation through large log files"
    ]),
    ("5️⃣  Build Quality & Portability", [
        "Lenovo Yoga line is solid for development work",
        "14\" hits sweet spot: portability vs. screen space",
        "AMD battery life > Intel for unplugged coding sessions"
    ])
]

for title, points in sections:
    p = P(stylename=normal_style)
    bold = Span(stylename=bold_style, text=title)
    p.addElement(bold)
    doc.text.addElement(p)

    for point in points:
        p = P(stylename=bullet_style)
        p.addText(f"    ✦ {point}")
        doc.text.addElement(p)

    doc.text.addElement(P())

# Probation section
p = P(stylename=heading_style, text="🔒  PROBATION REQUIREMENTS")
doc.text.addElement(p)

doc.text.addElement(P())

p = P(stylename=normal_style)
p.addText("Important context - I'm on probation and required to document my location/activities.")
doc.text.addElement(p)

doc.text.addElement(P())

p = P(stylename=normal_style, text="This laptop would:")
doc.text.addElement(p)

prob_points = [
    "Let me work from different locations (library, coffee shop) while compliant",
    "Built-in fingerprint reader = security for financial API credentials",
    "Portable enough to take to probation meetings to show my work"
]

for point in prob_points:
    p = P(stylename=bullet_style)
    p.addText(f"  ✓  {point}")
    doc.text.addElement(p)

doc.text.addElement(P())

# Cost optimization
p = P(stylename=heading_style, text="💰  CURRENT COST OPTIMIZATION")
doc.text.addElement(p)

doc.text.addElement(P())

p = P(stylename=normal_style)
p.addText("Recently optimized because GPT-5 was costing $30-50 per run (unsustainable on SSI).")
doc.text.addElement(p)

doc.text.addElement(P())

p = P(stylename=normal_style, text="Current setup:")
doc.text.addElement(p)

cost_points = [
    "Switched default to GPT-4o-mini → $0.50 per run",
    "Monthly AI costs: $10-20 (affordable on SSI)",
    "NPU would offload analysis to local models → further reduce cloud API costs"
]

for point in cost_points:
    p = P(stylename=bullet_style)
    p.addText(f"  • {point}")
    doc.text.addElement(p)

doc.text.addElement(P())

# Development workflow
p = P(stylename=heading_style, text="🛠️  DEVELOPMENT WORKFLOW")
doc.text.addElement(p)

doc.text.addElement(P())

workflow = [
    "Python 3.11+ with virtual environment",
    "Git version control (GitHub repo)",
    "VS Code / PyCharm for IDE",
    "SQLite for persistence",
    "Multiple concurrent processes (department simulation)",
    "Real-time API integrations (Alpaca trading, market data)"
]

for item in workflow:
    p = P(stylename=bullet_style)
    p.addText(f"  {item}")
    doc.text.addElement(p)

doc.text.addElement(P())
doc.text.addElement(P())

# Final note
p = P(stylename=normal_style)
p.addText("This isn't just \"nice to have\" - my current machine is genuinely struggling with the concurrent API calls and data processing. The system has grown way beyond what I initially planned, and I need hardware that can keep up.")
doc.text.addElement(p)

doc.text.addElement(P())

p = P(stylename=normal_style)
p.addText("Let me know if you want to see the codebase or have any technical questions about the architecture!")
doc.text.addElement(p)

doc.text.addElement(P())

p = P(stylename=normal_style, text="- WJ")
doc.text.addElement(p)

# Save the document
output_path = "C:\\Users\\wjcor\\OneDrive\\Desktop\\Sentinel\\Documentation_Dev\\Laptop_Request_Email.odt"
doc.save(output_path)
print(f"Created ODT file: {output_path}")
