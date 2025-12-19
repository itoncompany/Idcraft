from Authentications.models import CompanyDetails, CompanyPaymentDetails
from MainApps.models import SchoolDetails

def company_details(request):
    try:
        company = CompanyDetails.objects.filter(is_active=True).latest('created_at')
    except CompanyDetails.DoesNotExist:
        company = None

    if company:
        payment_details = CompanyPaymentDetails.objects.filter(
            company=company,
            is_active=True
        )
    else:
        payment_details = None

    schools = SchoolDetails.objects.all()

    return {
        'company': company,
        'company_payment': payment_details,
        'schools': schools,
    }
