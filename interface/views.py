from django.shortcuts import render
import pandas as pd
from django.http import FileResponse,Http404
from .forms import FileUploadForm
from .validators import validate_data_integrity
from django.core.mail import send_mail
from .mail import send_mail
from DevTest.settings import BASE_DIR
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
import tempfile
import os

# Create your views here.
@login_required
@require_http_methods(["GET"])
def generate_report(request):

    file_name = request.GET.get('file')
    if not file_name:
        raise Http404("File not specified")
    
    if not os.path.exists(file_name):
        raise Http404("File not found")

    response = FileResponse(open(file_name, 'rb'), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'attachment; filename="Report.xlsx"'
    return response
@login_required
@require_http_methods(["GET","POST"])
def form_view(request):
    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['file']
            try:
                # Handle Excel or CSV file based on extension
                if file.name.endswith('.xlsx') or file.name.endswith('.xls'):
                    df = pd.read_excel(file, sheet_name=0)
                elif file.name.endswith('.csv'):
                    df = pd.read_csv(file)
                else:
                    form.add_error('file', 'Unsupported file format.')
                    return render(request, 'input_form.html', {'form': form})
                
                # Data validations
                validate_data_integrity(df)

                summary_report = df.groupby(['Cust State', 'Cust Pin']).agg({'DPD': 'sum'}).reset_index()
                summary_html = summary_report.to_html(
                    index=False,
                    border=0,
                    classes='table table-striped table-bordered',
                    render_links=True
                )
                summary_xlsx = tempfile.NamedTemporaryFile(suffix=".xlsx", delete=False)
                with pd.ExcelWriter(summary_xlsx.name, engine='xlsxwriter') as writer:
                    df.to_excel(writer, index=False, sheet_name='Summary Report')

                # Email content
                user_email = request.user.email
                print(user_email)
                email_subject = 'Python Assignment - Arju Mukherjee'
                email_body = f"""
                Hello,

                The summary report from the uploaded file is attached below

                Regards,
                Arju Mukherjee
                """
                response,msg = send_mail(
                    to = user_email,
                    body = email_body,
                    subject = email_subject,
                    attachments = summary_xlsx.name
                )
                print(response, msg)
                return render(request, 'input_form.html', {'summary': summary_html, 'report_xlsx': summary_xlsx.name})
            except Exception as e:
                form.add_error('file', f"Error processing file: {e}")
    else:
        form = FileUploadForm()

    return render(request, 'input_form.html', {'form': form})