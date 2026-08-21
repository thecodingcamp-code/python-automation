from pypdf import PdfReader, PdfWriter

reader = PdfReader("client_intake_form.pdf")
writer = PdfWriter()
writer.append(reader)

writer.update_page_form_field_values(
    writer.pages[0],
    {
        "full_name": "Sara Lee",
        "email": "sara.lee@example.com",
        "signup_date": "2024-01-15",
        "subscribe": "/Yes",
    },
)

with open("client_intake_form_filled.pdf", "wb") as f:
    writer.write(f)