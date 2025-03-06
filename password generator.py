import random
import string

def generate_password(length):
    if length < 1:
        return "Password length must be at least 1."

    # Define the character sets to use for the password
    lowercase = string.ascii_lowercase
    uppercase = string.ascii_uppercase
    digits = string.digits
    special_characters = string.punctuation

    # Combine all character sets
    all_characters = lowercase + uppercase + digits + special_characters

    # Generate a random password
    password = ''.join(random.choice(all_characters) for _ in range(length))
    return password

# Prompt the user for the desired password length
try:
    length = int(input("Enter the desired length of the password: "))
    password = generate_password(length)
    print(f"Generated password: {password}")
except ValueError:
    print("Please enter a valid integer for the password length.")