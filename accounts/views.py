import os
import base64
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm
from .models import Activity, UserProfile

from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding, rsa
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

# --------------------------
# RSA KEY MANAGEMENT
# --------------------------
KEY_DIR = 'rsa_keys'
PRIVATE_KEY_PATH = os.path.join(KEY_DIR, 'private_key.pem')
PUBLIC_KEY_PATH = os.path.join(KEY_DIR, 'public_key.pem')

def ensure_keys():
    if not os.path.exists(KEY_DIR):
        os.makedirs(KEY_DIR)
    if not os.path.exists(PRIVATE_KEY_PATH) or not os.path.exists(PUBLIC_KEY_PATH):
        private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
        with open(PRIVATE_KEY_PATH, "wb") as f:
            f.write(private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.PKCS8,
                encryption_algorithm=serialization.NoEncryption()
            ))
        public_key = private_key.public_key()
        with open(PUBLIC_KEY_PATH, "wb") as f:
            f.write(public_key.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo
            ))

def load_private_key():
    with open(PRIVATE_KEY_PATH, "rb") as f:
        print("Loading private key from:", PRIVATE_KEY_PATH)
        pp = f.read()
        print("Private key content:", pp)
        return serialization.load_pem_private_key(pp, password=None)

# --------------------------
# AES DECRYPTION
# --------------------------
def aes_decrypt(cipher_text_b64, key_b64, iv_b64):
    cipher_text = base64.b64decode(cipher_text_b64)
    key = base64.b64decode(key_b64)
    iv = base64.b64decode(iv_b64)

    cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
    decryptor = cipher.decryptor()
    padded_data = decryptor.update(cipher_text) + decryptor.finalize()
    pad_len = padded_data[-1]
    return padded_data[:-pad_len].decode('utf-8')

# --------------------------
# HYBRID DECRYPTION
# --------------------------
def decrypt_payload(enc_key_b64, enc_username_b64, enc_password_b64):
    print("=== Starting decrypt_payload ===")
    print(f"enc_key_b64 received: {enc_key_b64[:50] if enc_key_b64 else 'None'}...")
    print(f"enc_username_b64 received: {enc_username_b64[:50] if enc_username_b64 else 'None'}...")
    print(f"enc_password_b64 received: {enc_password_b64[:50] if enc_password_b64 else 'None'}...")

    try:
        ensure_keys()
        private_key = load_private_key()
        print("Private key loaded successfully.", private_key)
        
        print("Encrypted Key:", enc_key_b64)

        # TODO: Remove this hardcoded key override - use the actual key from client
        # enc_key_b64 = "j4qYlIQPm97CmTSwi/T+9K9PN+HlqTzxySfWxM5o6E7PjLAsUm/8p0D/OHNm5XiCM+zSM2pxLON3M9ftHXc144N3Em+gvQw7se1AYwO8yoDDBAxWKR6MObTTbJUA4VxTg3iFGg3Kk5Koh6SUDdUvesKGTPCpdnkrKcQd54asHz+kbRkwDgWXY08A8zdLAxOVUpBqcSMeC+v/6FSM9U42/RnjrZ1+K+IwERBumnufwuWHXQso7fIp3VZr8pJmAWeOFqmp6ymOtjAaPRP56oJs1ocLp7syaTyx/IOD3yyeOosUkcevxAXcth5Bp42MHWz0WVhAuMoxdIHp9POccVMNTw=="
        print("Using encrypted key from client")

        decrypted_key_iv_b64 = private_key.decrypt(
            base64.b64decode(enc_key_b64),
            padding.PKCS1v15()
        )
        print("RSA decryption successful")
        
        combined_bytes = base64.b64decode(decrypted_key_iv_b64)
        aes_key = combined_bytes[:16]
        iv = combined_bytes[16:32]
        print(f"Extracted AES key length: {len(aes_key)}")
        print(f"Extracted IV length: {len(iv)}")

        aes_key_b64 = base64.b64encode(aes_key).decode()
        iv_b64 = base64.b64encode(iv).decode()

        print("About to decrypt username...")
        print(f"enc_username_b64 length: {len(enc_username_b64)}")
        print(f"enc_username_b64 content: {enc_username_b64}")
        
        username = aes_decrypt(enc_username_b64, aes_key_b64, iv_b64)
        print(f"Decrypted username: '{username}'")
        print(f"Username length: {len(username)}")
        print(f"Username repr: {repr(username)}")
        print(f"Username type: {type(username)}")
        
        print("About to decrypt password...")
        print(f"enc_password_b64 length: {len(enc_password_b64)}")
        print(f"enc_password_b64 content: {enc_password_b64}")
        
        password = aes_decrypt(enc_password_b64, aes_key_b64, iv_b64)
        print(f"Decrypted password length: {len(password)}")
        print("Password decryption successful")

        print("=== decrypt_payload completed successfully ===")
        
        # Check for empty username
        if not username or not username.strip():
            raise ValueError("Decrypted username is empty or contains only whitespace")
            
        return username.strip(), password
        
    except Exception as e:
        print(f"Error in decrypt_payload: {e}")
        import traceback
        traceback.print_exc()
        raise

# --------------------------
# REGISTER VIEW
# --------------------------
def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.save()
            login(request, user)

            Activity.objects.create(user=user, action='register', description='New account created.')
            messages.success(request, f"Welcome, {user.first_name}! Your account has been created.")
            return redirect('resumes:upload')
        else:
            messages.error(request, "Please fix the errors below.")
    else:
        form = CustomUserCreationForm()

    return render(request, 'accounts/register.html', {
        'form': form,
        'nav_mode': 'login_register'
    })

# --------------------------
# LOGIN VIEW (Hybrid Decryption)
# --------------------------
def login_view(request):
    print("=== LOGIN VIEW CALLED ===")
    if request.method == 'POST':
        print("=== POST REQUEST DETECTED ===")
        try:
            enc_username = request.POST.get("enc_username")
            enc_password = request.POST.get("enc_password")
            enc_key = request.POST.get("enc_key")

            print(f"Received enc_username: {enc_username is not None}")
            print(f"Received enc_password: {enc_password is not None}")
            print(f"Received enc_key: {enc_key is not None}")

            if not all([enc_username, enc_password, enc_key]):
                raise ValueError("Missing encrypted fields")

            print("About to call decrypt_payload...")
            username, password = decrypt_payload(enc_key, enc_username, enc_password)
            print("Decrypted Username:", username)
            
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                Activity.objects.create(user=user, action='login', description='User logged in successfully.')
                messages.success(request, f"Welcome back, {user.first_name}!")
                return redirect('resumes:upload')
            else:
                print("Authentication failed for username:", username)
                messages.error(request, "Invalid username or password.")
                
        except Exception as e:
            import traceback
            print("Decryption/Login error:", str(e))
            traceback.print_exc()
            messages.error(request, f"Login failed: {str(e)}")

    return render(request, 'accounts/login.html', {
        'nav_mode': 'login_register'
    })

# --------------------------
# LOGOUT VIEW
# --------------------------
def logout_view(request):
    if request.user.is_authenticated:
        Activity.objects.create(user=request.user, action='logout', description='User logged out.')
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect('accounts:login')

# --------------------------
# USER ACTIVITY HISTORY
# --------------------------
@login_required
def user_history(request):
    activities = Activity.objects.filter(user=request.user).order_by('-timestamp')
    return render(request, 'accounts/history.html', {
        'activities': activities,
        'nav_mode': 'default'
    })

# --------------------------
# EDIT PROFILE
# --------------------------
@login_required
def edit_profile(request):
    profile, created = UserProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        bio = request.POST.get('bio')
        profile_picture = request.FILES.get('profile_picture')

        profile.bio = bio
        if profile_picture:
            profile.profile_picture = profile_picture
        profile.save()

        messages.success(request, "Your profile has been updated.")
        return redirect('accounts:edit_profile')

    return render(request, 'accounts/edit_profile.html', {
        'profile': profile,
        'nav_mode': 'default'
    })