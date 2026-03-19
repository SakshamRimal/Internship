from pwdlib import PasswordHash

password_hash = PasswordHash.recommended()

# hash the password
# user.password

def hash_password(password :str):
    return password_hash.hash(password)

