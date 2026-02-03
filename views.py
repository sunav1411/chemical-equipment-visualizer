import pandas as pd

from django.http import HttpResponse
from reportlab.pdfgen import canvas
from django.contrib.auth.decorators import login_required


from django.core.files.storage import default_storage
from django.http import JsonResponse

from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Dataset


# =========================
# CSV UPLOAD + ANALYTICS API
# =========================
@api_view(['POST'])
def upload_csv(request):

    """
    Upload CSV file, perform analytics using Pandas,
    store summary in database, keep only last 5 uploads.
    """
    file = request.FILES.get('file')
    if not file:
        return Response({"error": "No file uploaded"}, status=400)

    # Save file temporarily
    path = default_storage.save(file.name, file)

    # Read CSV using Pandas
    df = pd.read_csv(path)

    # Perform analytics
    summary = {
        "total_equipment": int(len(df)),
        "average_flowrate": float(df["Flowrate"].mean()),
        "average_pressure": float(df["Pressure"].mean()),
        "average_temperature": float(df["Temperature"].mean()),
        "type_distribution": df["Type"].value_counts().to_dict()
    }

    # Save to database
    Dataset.objects.create(
        filename=file.name,
        summary=summary
    )

    # Keep only last 5 datasets
    if Dataset.objects.count() > 5:
        Dataset.objects.order_by('uploaded_at').first().delete()

    return Response(summary)


# =========================
# HISTORY API (LAST 5 UPLOADS)
# =========================
@login_required
def history(request):

    """
    Return last 5 uploaded datasets and their summaries.
    Plain Django view to avoid DRF request conflicts.
    """
    datasets = Dataset.objects.order_by('-uploaded_at')[:5]

    data = []
    for d in datasets:
        data.append({
            "filename": d.filename,
            "uploaded_at": d.uploaded_at,
            "summary": d.summary
        })

    return JsonResponse(data, safe=False)


@login_required
def generate_pdf(request):
    dataset = Dataset.objects.order_by('-uploaded_at').first()

    if not dataset:
        return HttpResponse("No data available")

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="equipment_report.pdf"'

    c = canvas.Canvas(response)
    c.setFont("Helvetica", 12)

    c.drawString(100, 800, "Chemical Equipment Analytics Report")
    y = 760

    for key, value in dataset.summary.items():
        c.drawString(100, y, f"{key}: {value}")
        y -= 20

    c.save()
    return response

