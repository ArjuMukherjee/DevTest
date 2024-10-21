from django import forms
from django.core.validators import FileExtensionValidator
from .validators import validate_empty_file, validate_file_size, validate_file_content

# Define a form for file upload

class FileUploadForm(forms.Form):
    file = forms.FileField(
        widget=forms.ClearableFileInput(attrs={
            'class': 'form-control', 
            'id': 'formFile',
            'aria-describedby': 'fileHelpBlock'
        }),
        label='Upload here:',  # Custom label text
        required=True,
        validators=[FileExtensionValidator(allowed_extensions=['xls', 'xlsx', 'csv']), validate_file_size, validate_file_content, validate_empty_file]
    )
