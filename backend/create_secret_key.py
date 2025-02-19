import secrets

def generate_secret_key():
    return secrets.token_urlsafe(50)

secret_key = generate_secret_key()
print(f"DJANGO_SECRET_KEY={secret_key}")

