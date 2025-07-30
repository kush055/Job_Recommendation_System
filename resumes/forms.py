from django import forms
from django.core.exceptions import ValidationError
import os

class ResumeUploadForm(forms.Form):
    file = forms.FileField(label='Upload your resume')

    def clean_file(self):
        uploaded_file = self.cleaned_data['file']
        valid_extensions = ['.pdf', '.jpg', '.jpeg', '.png']
        ext = os.path.splitext(uploaded_file.name)[1].lower()

        if ext not in valid_extensions:
            raise ValidationError("Only PDF and image files (JPG, PNG) are allowed.")

        # Optional: Check file size (limit to 5MB)
        if uploaded_file.size > 5 * 1024 * 1024:
            raise ValidationError("File size must be under 5MB.")

        return uploaded_file
