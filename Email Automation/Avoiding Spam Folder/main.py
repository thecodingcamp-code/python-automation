from email.message import EmailMessage

SPAM_TRIGGER_PHRASES = [
    "free money", "act now", "limited time", "click here", "guarantee",
    "risk free", "buy now", "no cost", "winner", "cash prize",
]

def spam_risk_check(subject, body):
    warnings = []
    lowered = (subject + " " + body).lower()

    for phrase in SPAM_TRIGGER_PHRASES:
        if phrase in lowered:
            warnings.append(f'Contains spam-trigger phrase: "{phrase}"')

    if subject.isupper() and len(subject) > 3:
        warnings.append("Subject line is entirely uppercase")

    exclamations = subject.count("!")
    if exclamations >= 2:
        warnings.append(f"Subject has {exclamations} exclamation marks")

    return warnings


subject1 = "FREE MONEY!!! ACT NOW!!!"
body1 = "Click here to claim your cash prize, guaranteed, no cost to you!"
print(spam_risk_check(subject1, body1))

subject2 = "Your Invoice from The Coding Camp"
body2 = "Hi there, please find your invoice attached. Thanks for your business."
print(spam_risk_check(subject2, body2))


msg = EmailMessage()
msg["Subject"] = "Your Invoice from The Coding Camp"
msg["From"] = "thecodingcamp.contact@gmail.com"
msg["To"] = "student@example.com"
msg["Reply-To"] = "thecodingcamp.contact@gmail.com"
msg.set_content("Hi there,\n\nPlease find your invoice attached.\n\nThanks,\nAhmed")
msg.add_alternative("<p>Hi there,<br><br>Please find your invoice attached.</p>", subtype="html")