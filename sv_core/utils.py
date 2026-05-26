import random, string

def generate_password(length=12):
    chars = string.ascii_letters + string.digits + "!@#$%^&*"
    return ''.join(random.choice(chars) for _ in range(length))

def check_strength(p):
    score = 0
    if len(p)>=8: score+=1
    if any(c.isdigit() for c in p): score+=1
    if any(c.isupper() for c in p): score+=1
    if any(c in "!@#$%^&*" for c in p): score+=1

    return ["Weak","Medium","Strong"][min(score//2,2)]