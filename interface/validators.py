
from django.core.exceptions import ValidationError
import pandas as pd

MAX_FILE_SIZE = 20 * 1024 * 1024  # 20MB

def validate_data_integrity(df):
    if not pd.api.types.is_numeric_dtype(df['Cust Pin']):
        raise ValidationError("Cust Pin must be numeric.")
    if not pd.api.types.is_numeric_dtype(df['DPD']):
        raise ValidationError("DPD must be an integer.")
    try:
        pd.to_datetime(df['Date'])
    except ValueError:
        raise ValidationError("Date format is invalid.")


def validate_file_size(file):
    if file.size > MAX_FILE_SIZE:
        raise ValidationError("File size exceeds the 20MB limit")

def validate_file_content(file):
    try:
        df = pd.read_excel(file) if file.name.endswith('.xlsx') else pd.read_csv(file)
        required_columns = ['Date', 'ACCNO', 'Cust State', 'Cust Pin', 'DPD']
        if not all(col in df.columns for col in required_columns):
            raise ValidationError("File doesn't contain the required columns.")
    except Exception as e:
        raise ValidationError("Invalid file content or format.")

def validate_empty_file(file):
    if file.size == 0:
        raise ValidationError("Uploaded file is empty.")