from pypdf import PdfReader, PdfWriter

original = PdfReader("invoice_2024_03.pdf")
numbers = PdfReader("page_numbers_overlay.pdf")

writer = PdfWriter()

for i, page in enumerate(original.pages):
    page.merge_page(numbers.pages[i])
    writer.add_page(page)

writer.write("invoice_2024_03_numbered.pdf")
writer.close()