import json
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import SMSCode


def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('home')
        else:
            messages.error(request, "Login yoki parol noto'g'ri!")
    else:
        form = AuthenticationForm()
    return render(request, 'auth_app/login.html', {'form': form})


def register_view(request):
    """Step 1: Phone number input"""
    if request.user.is_authenticated:
        return redirect('home')
    return render(request, 'auth_app/register.html')


def send_sms_code(request):
    """AJAX: Send SMS code to phone"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            phone = data.get('phone', '').strip()
        except Exception:
            phone = request.POST.get('phone', '').strip()

        if not phone:
            return JsonResponse({'success': False, 'error': 'Telefon raqami kiritilmadi'})

        # Check if user already exists
        if User.objects.filter(username=phone).exists():
            return JsonResponse({'success': False, 'error': 'Bu raqam allaqachon ro\'yxatdan o\'tgan'})

        # Invalidate old codes
        SMSCode.objects.filter(phone=phone, is_used=False).update(is_used=True)

        # Generate new code
        code = SMSCode.generate_code()
        SMSCode.objects.create(phone=phone, code=code)

        # TODO: Real SMS integration (Eskiz, Play Mobile, etc.)
        # sms_send(phone, f"MedStaff tasdiqlash kodi: {code}")

        # For development: print to console
        print(f"\n{'='*40}")
        print(f"📱 SMS → {phone}: Tasdiqlash kodi: {code}")
        print(f"{'='*40}\n")

        return JsonResponse({
            'success': True,
            'message': f'Kod {phone} raqamiga yuborildi',
            # Dev mode: expose code (REMOVE in production!)
            'dev_code': code
        })

    return JsonResponse({'success': False, 'error': 'Noto\'g\'ri so\'rov'})


def verify_sms_code(request):
    """AJAX: Verify code and create user"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            phone = data.get('phone', '').strip()
            code = data.get('code', '').strip()
            password = data.get('password', '').strip()
        except Exception:
            phone = request.POST.get('phone', '').strip()
            code = request.POST.get('code', '').strip()
            password = request.POST.get('password', '').strip()

        if not phone or not code or not password:
            return JsonResponse({'success': False, 'error': 'Barcha maydonlar to\'ldirilishi shart'})

        if len(password) < 6:
            return JsonResponse({'success': False, 'error': 'Parol kamida 6 ta belgidan iborat bo\'lishi kerak'})

        # Find latest valid code
        sms = SMSCode.objects.filter(phone=phone, is_used=False).order_by('-created_at').first()

        if not sms:
            return JsonResponse({'success': False, 'error': 'Kod topilmadi. Qayta yuborib ko\'ring'})

        if not sms.is_valid():
            return JsonResponse({'success': False, 'error': 'Kod muddati o\'tdi. Qayta yuborib ko\'ring'})

        if sms.code != code:
            return JsonResponse({'success': False, 'error': 'Kod noto\'g\'ri'})

        # Mark code as used
        sms.is_used = True
        sms.save()

        # Create user
        if User.objects.filter(username=phone).exists():
            return JsonResponse({'success': False, 'error': 'Bu raqam allaqachon ro\'yxatdan o\'tgan'})

        user = User.objects.create_user(username=phone, password=password)
        login(request, user)

        return JsonResponse({'success': True, 'redirect': '/'})

    return JsonResponse({'success': False, 'error': 'Noto\'g\'ri so\'rov'})


def logout_view(request):
    logout(request)
    messages.success(request, "Tizimdan chiqdingiz.")
    return redirect('login')


from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash

@login_required
def profile_view(request):
    if request.method == 'POST':
        action = request.POST.get('action')
        user = request.user

        if action == 'update_info':
            first_name = request.POST.get('first_name', '').strip()
            last_name = request.POST.get('last_name', '').strip()
            email = request.POST.get('email', '').strip()
            user.first_name = first_name
            user.last_name = last_name
            user.email = email
            user.save()
            messages.success(request, "Ma'lumotlar muvaffaqiyatli yangilandi!")
            return redirect('profile')

        elif action == 'change_password':
            old_password = request.POST.get('old_password', '')
            new_password = request.POST.get('new_password', '')
            confirm_password = request.POST.get('confirm_password', '')
            if not user.check_password(old_password):
                messages.error(request, "Joriy parol noto'g'ri!")
            elif len(new_password) < 6:
                messages.error(request, "Yangi parol kamida 6 ta belgidan iborat bo'lishi kerak!")
            elif new_password != confirm_password:
                messages.error(request, "Yangi parollar mos kelmadi!")
            else:
                user.set_password(new_password)
                user.save()
                update_session_auth_hash(request, user)
                messages.success(request, "Parol muvaffaqiyatli o'zgartirildi!")
            return redirect('profile')

    return render(request, 'auth_app/profile.html', {'user': request.user})
