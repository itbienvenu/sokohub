from django import forms
from .models import Order

class CheckoutForm(forms.Form):
    delivery_address = forms.CharField(
        widget=forms.Textarea(attrs={
            'rows': 3,
            'placeholder': 'Enter your complete delivery address including street, city, and postal code',
            'class': 'form-control'
        }),
        help_text="Please provide your complete delivery address",
        label="Delivery Address"
    )
    phone = forms.CharField(
        max_length=15,
        widget=forms.TextInput(attrs={
            'placeholder': 'e.g., +255712345678',
            'class': 'form-control'
        }),
        help_text="Phone number for delivery updates",
        label="Phone Number"
    )
    quantity = forms.IntegerField(
        min_value=1,
        initial=1,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'min': '1'
        }),
        label="Quantity"
    )

    def clean_delivery_address(self):
        address = self.cleaned_data.get('delivery_address')
        if len(address.strip()) < 10:
            raise forms.ValidationError("Please provide a complete delivery address (at least 10 characters).")
        return address.strip()

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        # Basic phone validation - you can enhance this based on your needs
        if not phone.replace('+', '').replace(' ', '').isdigit():
            raise forms.ValidationError("Please enter a valid phone number.")
        return phone

    def clean_quantity(self):
        quantity = self.cleaned_data.get('quantity')
        if quantity < 1:
            raise forms.ValidationError("Quantity must be at least 1.")
        return quantity