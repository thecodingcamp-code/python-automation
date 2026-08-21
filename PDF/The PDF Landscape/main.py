from reportlab.pdfgen import canvas

c = canvas.Canvas("generated_summary.pdf")

c.setFont("Helvetica-Bold", 16)
c.drawString(72, 750, "Monthly Summary Report")

c.setFont("Helvetica", 12)
c.drawString(72, 715, "Total Revenue: $2,482.92")
c.drawString(72, 695, "Invoice Reference: 2024-03")

c.save()