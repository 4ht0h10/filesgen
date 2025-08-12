import streamlit_authenticator as stauth

# Lista de contraseñas en texto plano
PASSWORD = 'xxxxxxx'

# Hashearlas correctamente
hashed_passwords = stauth.Hasher().hash(PASSWORD)
# Resultado 1

# Resultado 1
print(f" - la contraseña {PASSWORD} haseada es: {hashed_passwords}")
