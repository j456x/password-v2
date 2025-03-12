import re
import random
import string

# Function to evaluate password strength
def evaluate_password(password):
    score = 0
    feedback = []
    
    # Check length
    if len(password) >= 12:
        score += 3
    elif len(password) >= 8:
        score += 2
    else:
        feedback.append("Password is too short (less than 8 characters).")
    
    # Check for uppercase letters
    if re.search(r"[A-Z]", password):
        score += 1
    else:
        feedback.append("Add uppercase letters for better strength.")
    
    # Check for lowercase letters
    if re.search(r"[a-z]", password):
        score += 1
    else:
        feedback.append("Add lowercase letters for better strength.")
    
    # Check for numbers
    if re.search(r"\d", password):
        score += 1
    else:
        feedback.append("Add numbers for better strength.")
    
    # Check for special characters
    if re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        score += 2
    else:
        feedback.append("Add special characters (e.g., !@#$%) for better strength.")
    
    # Common password check (simplified)
    common_passwords = ["password", "123456", "qwerty", "letmein"]
    if password.lower() in common_passwords:
        score -= 5
        feedback.append("This is a common password; avoid using it!")
    
    return score, feedback

# Function to generate a strong password
def generate_strong_password(length=16):
    characters = string.ascii_letters + string.digits + string.punctuation
    password = [
        random.choice(string.ascii_uppercase),  # Ensure at least one uppercase
        random.choice(string.ascii_lowercase),  # Ensure at least one lowercase
        random.choice(string.digits),           # Ensure at least one number
        random.choice(string.punctuation)       # Ensure at least one special char
    ]
    # Fill the rest of the password length with random characters
    password += random.choices(characters, k=length - 4)
    random.shuffle(password)  # Shuffle to avoid predictable patterns
    return ''.join(password)

# Main program
def password_scanner():
    print("Password Security Scanner")
    print("Enter your Gmail passwords one by one (or type 'done' to finish):")
    
    passwords = []
    while True:
        pwd = input("Enter a password: ")
        if pwd.lower() == "done":
            break
        passwords.append(pwd)
    
    if not passwords:
        print("No passwords provided.")
        return
    
    print("\nScanning passwords...\n")
    for i, password in enumerate(passwords, 1):
        score, feedback = evaluate_password(password)
        print(f"Password {i}: {'*' * len(password)} (hidden for privacy)")
        print(f"Strength Score: {score}/8")
        if feedback:
            print("Feedback:")
            for fb in feedback:
                print(f" - {fb}")
        
        if score < 6:
            new_password = generate_strong_password()
            print(f"Recommended New Password: {new_password}")
        else:
            print("This password is strong enough!")
        print()

# Run the program
if __name__ == "__main__":
    password_scanner()
