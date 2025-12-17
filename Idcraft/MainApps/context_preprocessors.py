from Authentications.models import CompanyDetails, CompanyPaymentDetails, ServicePrice

def company_details(request):
    """
    Fetch the latest active company, its active payment details, 
    and active service prices.
    """
    try:
        company = CompanyDetails.objects.filter(is_active=True).latest('created_at')
    except CompanyDetails.DoesNotExist:
        company = None

    if company:
        payment_details = CompanyPaymentDetails.objects.filter(company=company, is_active=True)
       
    else:
        payment_details = None
   

    return {
        'company': company,
        'company_payment': payment_details,
       
    }
