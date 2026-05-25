from django import forms
from .models import Hospital, Staff


class HospitalForm(forms.ModelForm):
    class Meta:
        model = Hospital
        fields = ['name', 'hospital_type', 'region', 'address', 'phone', 'email', 'website', 'bed_count']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Kasalxona nomi'}),
            'hospital_type': forms.Select(attrs={'class': 'form-select'}),
            'region': forms.Select(attrs={'class': 'form-select'}),
            'address': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'To\'liq manzil'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+998 XX XXX XX XX'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'website': forms.URLInput(attrs={'class': 'form-control'}),
            'bed_count': forms.NumberInput(attrs={'class': 'form-control'}),
        }


class StaffForm(forms.ModelForm):
    class Meta:
        model = Staff
        fields = ['first_name', 'last_name', 'middle_name', 'age', 'position',
                  'specialization', 'hospital', 'experience_years', 'shift',
                  'phone', 'email', 'photo', 'salary', 'hired_date', 'notes']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'middle_name': forms.TextInput(attrs={'class': 'form-control'}),
            'age': forms.NumberInput(attrs={'class': 'form-control', 'min': 18, 'max': 80}),
            'position': forms.Select(attrs={'class': 'form-select'}),
            'specialization': forms.TextInput(attrs={'class': 'form-control'}),
            'hospital': forms.Select(attrs={'class': 'form-select'}),
            'experience_years': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
            'shift': forms.Select(attrs={'class': 'form-select'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+998 XX XXX XX XX'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'salary': forms.NumberInput(attrs={'class': 'form-control'}),
            'hired_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
