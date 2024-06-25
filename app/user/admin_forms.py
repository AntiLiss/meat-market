from django import forms
from .models import CustomerProfile, AdminProfile


class CustomerProfileAdminForm(forms.ModelForm):
    """Custom admin form with uneditable `user` field after creation"""

    class Meta:
        model = CustomerProfile
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.fields["user"].disabled = True


class AdminProfileAdminForm(forms.ModelForm):
    """Custom admin form with uneditable `user` field after creation"""

    class Meta:
        model = AdminProfile
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.fields["user"].disabled = True
