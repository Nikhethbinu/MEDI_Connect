from django import forms

from .models import (
    Prescription,
    PrescriptionItem,
    Medicine
)


# ==========================================
# PRESCRIPTION FORM
# ==========================================

class PrescriptionForm(forms.ModelForm):

    class Meta:
        model = Prescription

        fields = [
            'diagnosis',
            'notes',
        ]

        widgets = {

            'diagnosis': forms.Textarea(
                attrs={
                    'rows': 4,
                    'placeholder': 'Enter diagnosis'
                }
            ),

            'notes': forms.Textarea(
                attrs={
                    'rows': 4,
                    'placeholder': 'Enter additional notes'
                }
            ),
        }


# ==========================================
# PRESCRIPTION ITEM FORM
# ==========================================

class PrescriptionItemForm(forms.ModelForm):

    class Meta:
        model = PrescriptionItem

        fields = [
            'medicine',
            'dosage',
            'frequency',
            'duration',
            'instructions',
        ]

        widgets = {

            'dosage': forms.TextInput(
                attrs={
                    'placeholder': 'Example: 500 mg'
                }
            ),

            'frequency': forms.TextInput(
                attrs={
                    'placeholder': 'Example: Twice daily'
                }
            ),

            'duration': forms.TextInput(
                attrs={
                    'placeholder': 'Example: 5 days'
                }
            ),

            'instructions': forms.Textarea(
                attrs={
                    'rows': 3,
                    'placeholder': 'Additional instructions'
                }
            ),
        }

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.fields['medicine'].queryset = Medicine.objects.filter(
            is_active=True
        ).order_by('name')