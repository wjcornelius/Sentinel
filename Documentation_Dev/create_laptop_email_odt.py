"""
Convert the laptop request email TXT to ODT format
Requires: odfpy library (pip install odfpy)
"""

from odf.opendocument import OpenDocumentText
from odf.style import Style, TextProperties, ParagraphProperties
from odf.text import P, Span

# Read the text file
with open('Laptop_Request_Email_2_Intel_x64.txt', 'r', encoding='utf-8') as f:
    content = f.read()

# Create ODT document
doc = OpenDocumentText()

# Define styles
# Bold style for headings
bold_style = Style(name="Bold", family="text")
bold_style.addElement(TextProperties(fontweight="bold", fontsize="12pt"))
doc.styles.addElement(bold_style)

# Title style
title_style = Style(name="Title", family="paragraph")
title_style.addElement(TextProperties(fontweight="bold", fontsize="16pt"))
title_style.addElement(ParagraphProperties(textalign="center"))
doc.styles.addElement(title_style)

# Heading style
heading_style = Style(name="Heading", family="paragraph")
heading_style.addElement(TextProperties(fontweight="bold", fontsize="14pt"))
doc.styles.addElement(heading_style)

# Monospace style for boxes
mono_style = Style(name="Monospace", family="text")
mono_style.addElement(TextProperties(fontfamily="Courier New", fontsize="10pt"))
doc.styles.addElement(mono_style)

# Add content line by line
for line in content.split('\n'):
    p = P()

    # Check if it's a special line
    if line.startswith('Subject:'):
        p.stylename = title_style
        p.addText(line)
    elif line.startswith('┏') or line.startswith('╔') or line.startswith('┌'):
        # Box drawing - use monospace
        span = Span(stylename=mono_style)
        span.addText(line)
        p.addElement(span)
    elif line.strip().startswith('✨') or line.strip().startswith('🔧') or line.strip().startswith('⚠️') or line.strip().startswith('✅'):
        # Section headers with emoji
        p.stylename = heading_style
        p.addText(line)
    elif '✓' in line or '✗' in line or '→' in line:
        # Bullet points
        p.addText(line)
    else:
        # Normal text
        p.addText(line)

    doc.text.addElement(p)

# Save the document
doc.save('Laptop_Request_Email_2_Intel_x64.odt')
print("Created: Laptop_Request_Email_2_Intel_x64.odt")
print("You can now open this file in LibreOffice Writer")
