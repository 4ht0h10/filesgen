import streamlit_authenticator as stauth

# Lista de contraseñas en texto plano
PASSWORD = 'xxxxx'

# Hashearlas correctamente
hashed_passwords = stauth.Hasher().hash(PASSWORD)
# Resultado 1

# Resultado 1
print(f" - la contraseña haseada es: {hashed_passwords}")

