from django import forms

from .models import MedicalRecord


# ==========================================
# MEDICAL RECORD FORM
# ==========================================

class MedicalRecordForm(forms.ModelForm):

    class Meta:

        model = MedicalRecord

        fields = [
            'symptoms',
            'diagnosis',
            'treatment',
            'notes',
        ]

        widgets = {

            'symptoms': forms.Textarea(
                attrs={
                    'rows': 4,
                    'placeholder':
                        'Enter patient symptoms'
                }
            ),

            'diagnosis': forms.Textarea(
                attrs={
                    'rows': 4,
                    'placeholder':
                        'Enter diagnosis'
                }
            ),

            'treatment': forms.Textarea(
                attrs={
                    'rows': 4,
                    'placeholder':
                        'Enter treatment details'
                }
            ),

            'notes': forms.Textarea(
                attrs={
                    'rows': 4,
                    'placeholder':
                        'Enter additional medical notes'
                }
            ),
        }