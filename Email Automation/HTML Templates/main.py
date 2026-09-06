from email.message import EmailMessage
import email

risky_html = """
<style>
  .card { display: flex; flex-direction: column; background: white;
          border-radius: 6px; padding: 32px; width: 480px; margin: 0 auto; }
  .title { font-size: 20px; font-weight: bold; }
  .button { background: #2563eb; color: white; padding: 12px 24px;
            border-radius: 4px; text-decoration: none; }
</style>
<div class="card">
  <div class="title">Invoice from The Coding Camp</div>
  <p>Hi there,<br><br>Your invoice total is <strong>$2,482.92</strong>. Thanks for your business.</p>
  <a class="button" href="https://example.com/invoice/2024-03">View Invoice</a>
</div>
"""

safe_html = """
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="background-color:#f4f4f4; padding:24px 0;">
  <tr>
    <td align="center">
      <table role="presentation" width="480" cellpadding="0" cellspacing="0"
             style="background-color:#ffffff; border-radius:6px; padding:32px; font-family:Arial, sans-serif;">
        <tr>
          <td style="font-size:20px; font-weight:bold; color:#111111; padding-bottom:16px;">
            Invoice from The Coding Camp
          </td>
        </tr>
        <tr>
          <td style="font-size:14px; color:#333333; line-height:1.5; padding-bottom:20px;">
            Hi there,<br><br>
            Your invoice total is <strong>$2,482.92</strong>. Thanks for your business.
          </td>
        </tr>
        <tr>
          <td align="center">
            <table role="presentation" cellpadding="0" cellspacing="0">
              <tr>
                <td style="background-color:#2563eb; border-radius:4px;">
                  <a href="https://example.com/invoice/2024-03"
                     style="display:inline-block; padding:12px 24px; font-size:14px; color:#ffffff; text-decoration:none; font-family:Arial, sans-serif;">
                    View Invoice
                  </a>
                </td>
              </tr>
            </table>
          </td>
        </tr>
      </table>
    </td>
  </tr>
</table>
"""



msg = EmailMessage()
msg["Subject"] = "Your Invoice from The Coding Camp"
msg["From"] = "thecodingcamp.contact@gmail.com"
msg["To"] = "student@example.com"

plain_text = "Hi there,\n\nYour invoice total is $2,482.92. Thanks for your business.\n\n- Ahmed"
msg.set_content(plain_text)
msg.add_alternative(safe_html, subtype="html")


parsed = email.message_from_bytes(msg.as_bytes())
for part in parsed.walk():
    print(part.get_content_type())