from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.db.models import Q, Count
from .models import Hospital, Staff, POSITION_CHOICES, REGION_CHOICES, HOSPITAL_TYPE_CHOICES
from .forms import HospitalForm, StaffForm


def is_admin(user):
    return user.is_staff or user.is_superuser


@login_required
def home(request):
    total_hospitals = Hospital.objects.filter(is_active=True).count()
    total_staff = Staff.objects.filter(is_active=True).count()
    recent_staff = Staff.objects.filter(is_active=True).select_related('hospital').order_by('-created_at')[:6]
    top_hospitals = Hospital.objects.filter(is_active=True).annotate(
        sc=Count('staff')).order_by('-sc')[:5]
    position_stats = []
    for code, name in POSITION_CHOICES[:6]:
        count = Staff.objects.filter(position=code, is_active=True).count()
        if count:
            position_stats.append({'name': name, 'count': count})

    return render(request, 'frontend/home.html', {
        'total_hospitals': total_hospitals,
        'total_staff': total_staff,
        'recent_staff': recent_staff,
        'top_hospitals': top_hospitals,
        'position_stats': position_stats,
    })


@login_required
def staff_list(request):
    staff = Staff.objects.filter(is_active=True).select_related('hospital')
    search = request.GET.get('search', '')
    position = request.GET.get('position', '')
    region = request.GET.get('region', '')
    hospital_id = request.GET.get('hospital', '')
    exp_min = request.GET.get('exp_min', '')
    exp_max = request.GET.get('exp_max', '')
    age_min = request.GET.get('age_min', '')
    age_max = request.GET.get('age_max', '')

    if search:
        staff = staff.filter(
            Q(first_name__icontains=search) |
            Q(last_name__icontains=search) |
            Q(middle_name__icontains=search) |
            Q(specialization__icontains=search) |
            Q(hospital__name__icontains=search)
        )
    if position:
        staff = staff.filter(position=position)
    if region:
        staff = staff.filter(hospital__region=region)
    if hospital_id:
        staff = staff.filter(hospital_id=hospital_id)
    if exp_min:
        staff = staff.filter(experience_years__gte=exp_min)
    if exp_max:
        staff = staff.filter(experience_years__lte=exp_max)
    if age_min:
        staff = staff.filter(age__gte=age_min)
    if age_max:
        staff = staff.filter(age__lte=age_max)

    hospitals = Hospital.objects.filter(is_active=True)
    return render(request, 'frontend/staff_list.html', {
        'staff': staff,
        'positions': POSITION_CHOICES,
        'regions': REGION_CHOICES,
        'hospitals': hospitals,
        'filters': request.GET,
        'total': staff.count(),
    })


@login_required
def staff_detail(request, pk):
    person = get_object_or_404(Staff, pk=pk)
    return render(request, 'frontend/staff_detail.html', {'person': person})


@login_required
def staff_add(request):
    if request.method == 'POST':
        form = StaffForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Xodim muvaffaqiyatli qo\'shildi!')
            return redirect('staff_list')
    else:
        form = StaffForm()
    return render(request, 'frontend/staff_form.html', {'form': form, 'title': 'Xodim qo\'shish'})


@login_required
def staff_edit(request, pk):
    person = get_object_or_404(Staff, pk=pk)
    if request.method == 'POST':
        form = StaffForm(request.POST, request.FILES, instance=person)
        if form.is_valid():
            form.save()
            messages.success(request, 'Xodim ma\'lumotlari yangilandi!')
            return redirect('staff_detail', pk=pk)
    else:
        form = StaffForm(instance=person)
    return render(request, 'frontend/staff_form.html', {'form': form, 'title': 'Xodimni tahrirlash', 'person': person})


@login_required
def staff_delete(request, pk):
    person = get_object_or_404(Staff, pk=pk)
    if request.method == 'POST':
        person.is_active = False
        person.save()
        messages.success(request, f'{person.full_name} o\'chirildi.')
        return redirect('staff_list')
    return render(request, 'frontend/staff_confirm_delete.html', {'person': person})


@login_required
def hospital_list(request):
    hospitals = Hospital.objects.filter(is_active=True).annotate(sc=Count('staff'))
    search = request.GET.get('search', '')
    region = request.GET.get('region', '')
    htype = request.GET.get('type', '')
    if search:
        hospitals = hospitals.filter(
            Q(name__icontains=search) | Q(address__icontains=search))
    if region:
        hospitals = hospitals.filter(region=region)
    if htype:
        hospitals = hospitals.filter(hospital_type=htype)
    return render(request, 'frontend/hospital_list.html', {
        'hospitals': hospitals,
        'regions': REGION_CHOICES,
        'types': HOSPITAL_TYPE_CHOICES,
        'filters': request.GET,
    })


@login_required
def hospital_detail(request, pk):
    hospital = get_object_or_404(Hospital, pk=pk)
    staff = hospital.staff.filter(is_active=True)
    return render(request, 'frontend/hospital_detail.html', {
        'hospital': hospital, 'staff': staff})


@login_required
@user_passes_test(is_admin, login_url='hospital_list')
def hospital_add(request):
    if request.method == 'POST':
        form = HospitalForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Kasalxona qo\'shildi!')
            return redirect('hospital_list')
    else:
        form = HospitalForm()
    return render(request, 'frontend/hospital_form.html', {'form': form, 'title': 'Kasalxona qo\'shish'})


@login_required
@user_passes_test(is_admin, login_url='hospital_list')
def hospital_edit(request, pk):
    hospital = get_object_or_404(Hospital, pk=pk)
    if request.method == 'POST':
        form = HospitalForm(request.POST, instance=hospital)
        if form.is_valid():
            form.save()
            messages.success(request, 'Kasalxona yangilandi!')
            return redirect('hospital_detail', pk=pk)
    else:
        form = HospitalForm(instance=hospital)
    return render(request, 'frontend/hospital_form.html', {'form': form, 'title': 'Kasalxonani tahrirlash'})
