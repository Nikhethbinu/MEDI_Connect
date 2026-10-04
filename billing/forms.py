from django import forms

from .models import Payment


# ==========================================
# PAYMENT FORM
# ==========================================

class PaymentForm(forms.ModelForm):

    class Meta:

        model = Payment

        fields = [
            'consultation_fee',
            'additional_charges',
            'payment_method',
            'status',
            'transaction_id',
        ]

        widgets = {

            'consultation_fee': forms.NumberInput(
                attrs={
                    'step': '0.01',
                    'min': '0'
                }
            ),

            'additional_charges': forms.NumberInput(
                attrs={
                    'step': '0.01',
                    'min': '0'
                }
            ),

            'transaction_id': forms.TextInput(
                attrs={
                    'placeholder':
                        'Enter transaction ID'
                }
            ),
        }

    def clean(self):

        cleaned_data = super().clean()

        consultation_fee = (
            cleaned_data.get(
                'consultation_fee'
            ) or 0
        )

        additional_charges = (
            cleaned_data.get(
                'additional_charges'
            ) or 0
        )

        cleaned_data['total_amount'] = (
            consultation_fee
            + additional_charges
        )

        return cleaned_data