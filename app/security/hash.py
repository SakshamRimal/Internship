from pwdlib import PasswordHash

password_hash = PasswordHash.recommended()

# hash the password
# user.password
def hash_password(password :str):
    return password_hash.hash(password)

# this is used for verifying the password
def verify_password(plain_password : str , hashed_password : str):
    return password_hash.verify(plain_password, hashed_password)

