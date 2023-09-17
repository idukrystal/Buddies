allowed_in_password = "_-+*$&"

min_password_len = 6

allowed_in_username = "_-."

def valid_password(password):
    if len(password) < min_password_len:
        return False
    for char in password:
        if not char.isalnum() and char not in alowed_in_password:
            return False
    return True

def valid_username(username):
    #impplement this
    return True
