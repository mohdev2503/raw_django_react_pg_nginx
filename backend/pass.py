import secrets

def generate_secret_key():
    return secrets.token_urlsafe(10)

secret_key = generate_secret_key()
print(f"POSTGRES_PASSWORD={secret_key}")

