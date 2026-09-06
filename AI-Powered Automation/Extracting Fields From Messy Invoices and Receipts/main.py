import os
from dotenv import load_dotenv
from google import genai
from pydantic import BaseModel, ValidationError
from typing import Optional


class InvoiceData(BaseModel):
    vendor: str
    invoice_number: Optional[str] = None
    date: str
    total: float

load_dotenv()
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

invoice_text = """Bill from: Golden Wheat Distributors
Ref No: GW-88213
03/18/2024
AMOUNT: 189.50 USD"""

prompt = f"""Extract the vendor, invoice number, date, and total from this invoice.
Respond with only JSON, no other text.

{invoice_text}"""

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=prompt
)

print(response.text)

good_json = '{"vendor": "Riverside Bakery Supplies", "invoice_number": "INV-2024-0512", "date": "2024-03-15", "total": 245.00}'

invoice = InvoiceData.model_validate_json(good_json)
print(invoice)
print(type(invoice.total))

bad_json = '{"vendor": "Golden Wheat Distributors", "date": "2024-03-18"}'

try:
    invoice = InvoiceData.model_validate_json(bad_json)
    print(invoice)
except ValidationError as e:
    print("Validation failed:")
    print(e)
    

messy_json = '{"vendor": "Sunrise Packaging Co.", "date": "2024-03-20", "total": "$412.75"}'

try:
    invoice = InvoiceData.model_validate_json(messy_json)
    print(invoice)
except ValidationError as e:
    print("Validation failed:")
    print(e)