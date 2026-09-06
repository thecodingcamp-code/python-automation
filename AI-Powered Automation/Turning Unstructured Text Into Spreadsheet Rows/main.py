import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
from pydantic import BaseModel, ValidationError
from typing import Optional
import pandas as pd

load_dotenv()
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

class InvoiceData(BaseModel):
    vendor: str
    invoice_number: Optional[str] = None
    date: str
    total: float

invoice_texts = [
    open("invoice_riverside.txt").read(),
    open("invoice_goldenwheat.txt").read(),
    open("invoice_sunrise.txt").read(),
]

successes = []
failures = []

for i, text in enumerate(invoice_texts):
    try:
        response = client.models.generate_content(
            model="gemini-3.5-flash",
            contents=f"Extract the invoice details from this text:\n\n{text}",
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=InvoiceData
            )
        )
        successes.append(response.parsed)
    except (ValidationError, Exception) as e:
        failures.append({"index": i, "error": str(e)})

print(f"Succeeded: {len(successes)}, Failed: {len(failures)}")


class InvoiceData(BaseModel):
    vendor: str
    invoice_number: Optional[str] = None
    date: str
    total: float

simulated_responses = [
    '{"vendor": "Riverside Bakery Supplies", "invoice_number": "INV-2024-0512", "date": "2024-03-15", "total": 245.00}',
    '{"vendor": "Golden Wheat Distributors", "invoice_number": "GW-88213", "date": "2024-03-18", "total": 189.50}',
    'not even valid json at all {{{',
    '{"vendor": "Sunrise Packaging Co.", "invoice_number": "SPK-4471", "date": "2024-03-20", "total": 412.75}',
]

successes = []
failures = []

for i, raw in enumerate(simulated_responses):
    try:
        invoice = InvoiceData.model_validate_json(raw)
        successes.append(invoice)
    except (ValidationError, ValueError) as e:
        failures.append({"index": i, "error": str(e)[:80]})

print("Successes:", len(successes))
print("Failures:", len(failures))
for f in failures:
    print(" -", f)
    
rows = [invoice.model_dump() for invoice in successes]
df = pd.DataFrame(rows)
print(df)

df.to_excel("extracted_invoices.xlsx", sheet_name="Invoices", index=False)