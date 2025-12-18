from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from MainApps.models import SchoolDetails, Student,IDCardTemplate
from RatingAndReviews.models import Feedback
from Authentications.models import ServicePrice,CompanyPaymentDetails
# Create your views here.
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def home(request):
    ratings=Feedback.objects.filter(is_public=True).order_by('-created_at')[:5]
    return render(request, 'MainApps/home.html', {'ratings': ratings})


def service_pricing(request):
    company_payment_details = CompanyPaymentDetails.objects.filter(is_active=True, payment_method='esewa').first()
    service_prices = ServicePrice.objects.filter( is_active=True)
    return render(request, 'MainApps/service_pricing.html', {'service_prices': service_prices, 'company_payment_details': company_payment_details})


def school_dashboard(request):
    user = request.user

    # Get the school associated with this user
    school = SchoolDetails.objects.filter(user=user).first()
    if not school:
        return render(request, "MainApps/error.html", {
            "message": "No school details found for the logged-in user."
        })

    # Get all students of this school
    students = school.students.all().order_by('grade', 'section', 'roll')

    context = {
        "school": school,
        "students": students,
        "grade_choices": Student.GRADE_CHOICES,
        "gender_choices": Student.GENDER_CHOICES,
        "section_choices": Student.SECTION_CHOICES,
    }

    return render(request, "MainApps/school_dashboard.html", context)


def grade_list(request):
    user = request.user
    school = SchoolDetails.objects.filter(user=user).first()
    if not school:
        return render(request, "MainApps/error.html", {
            "message": "No school details found for the logged-in user."
        })

    # Get all students of this school
    students = school.students.all().order_by('grade', 'section', 'roll')

    context = {
        "school": school,
        "students": students,
        "grades": Student.GRADE_CHOICES,
        "gender_choices": Student.GENDER_CHOICES,
        "section_choices": Student.SECTION_CHOICES,
    }

    return render(request, 'MainApps/grade_list.html', context)


    
def card_form(request, class_id=None):
    user = request.user
    school = SchoolDetails.objects.filter(user=user).first()

    students_list = school.students.filter(grade=class_id)

    # Search by roll
    roll = request.GET.get('roll')
    if roll:
        students_list = students_list.filter(roll__icontains=roll)

    # Filter status
    status = request.GET.get('status')
    if status:
        students_list = students_list.filter(status=status)

    # Filter section
    section = request.GET.get('section')
    if section:
        students_list = students_list.filter(section=section)

    # Sorting
    sort = request.GET.get('sort')
    if sort == 'az':
        students_list = students_list.order_by('full_name')
    elif sort == 'za':
        students_list = students_list.order_by('-full_name')
    elif sort == 'roll':
        students_list = students_list.order_by('roll')
    else:
        students_list = students_list.order_by('grade', 'section', 'roll')

    # Pagination
    paginator = Paginator(students_list, 10)
    page = request.GET.get('page')
    students = paginator.get_page(page)

    context = {
        "students": students,
        "section_choices": Student.SECTION_CHOICES,
        "gender_choices": Student.GENDER_CHOICES,
        "school": school,
        "class_id":class_id,
    }
    return render(request, "MainApps/card_form.html", context)






@login_required
def edit_student(request, pk):
    student = get_object_or_404(Student, pk=pk)

    if request.method == 'POST':
        # Basic fields
        student.full_name = request.POST.get('full_name', student.full_name)
        student.roll = request.POST.get('roll', student.roll)
        student.grade = request.POST.get('grade', student.grade)
        student.section = request.POST.get('section', student.section)
        student.gender = request.POST.get('gender', student.gender)
        student.email = request.POST.get('email', student.email)
        student.student_phone = request.POST.get('student_phone', student.student_phone)
        student.parent_name = request.POST.get('parent_name', student.parent_name)
        student.parent_phone = request.POST.get('parent_phone', student.parent_phone)
        student.address = request.POST.get('address', student.address)
        student.status = request.POST.get('status', student.status)

        # Date fields (safe parsing)
        dob = request.POST.get('dob')
        if dob:
            student.dob = dob

        valid_until = request.POST.get('valid_until')
        if valid_until:
            student.valid_until = valid_until

        # Photo upload
        if request.FILES.get('photo'):
            student.photo = request.FILES['photo']

        student.save()
        messages.success(request, f"{student.full_name} updated successfully!")

    # Always return to previous page (modal UX)
    return redirect(request.META.get('HTTP_REFERER', 'home'))

@login_required
def add_student(request):
    if request.method == 'POST':
        # Get grade safely, fallback to 'OTHER' if missing or empty
        grade = request.POST.get('grade')
        if not grade:  # handles None or empty string
            grade = 'OTHER'
        school = SchoolDetails.objects.filter(user=request.user).first()

        student = Student(
            user=request.user,
            school=school,
            full_name=request.POST.get('full_name', '').strip(),
            roll=request.POST.get('roll', '').strip() or None,
            grade=grade,
            section=request.POST.get('section', '').strip() or None,
            gender=request.POST.get('gender') or 'OTHER',
            parent_name=request.POST.get('parent_name', '').strip() or None,
            parent_phone=request.POST.get('parent_phone', '').strip() or None,
            address=request.POST.get('address', '').strip() or None,
            status=request.POST.get('status', 'NEW'),
        )

        if request.FILES.get('photo'):
            student.photo = request.FILES['photo']

        student.save()
        messages.success(request, f"{student.full_name} added successfully!")

    return redirect(request.META.get('HTTP_REFERER', 'students_list'))

@login_required
def edit_student(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == 'POST':
        student.full_name = request.POST.get('full_name')
        student.roll = request.POST.get('roll')
        student.section = request.POST.get('section')
        student.gender = request.POST.get('gender')
        student.status = request.POST.get('status')
        student.parent_name = request.POST.get('parent_name')
        student.parent_phone = request.POST.get('parent_phone')
        student.address = request.POST.get('address')

        if request.FILES.get('photo'):
            student.photo = request.FILES['photo']

        student.save()
        messages.success(request, f"{student.full_name} updated successfully!")
        return redirect(request.META.get('HTTP_REFERER', 'students_list'))

    return redirect('students_list')


def delete_student(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == 'POST':
        student_name = student.full_name
        student.delete()
        messages.success(request, f"{student_name} deleted successfully!")
        # Redirect back to the same page (referer) or default page
        return redirect(request.META.get('HTTP_REFERER', '/'))
    
    # If GET request, just redirect back
    return redirect(request.META.get('HTTP_REFERER', '/'))






def student_list(request):
    students = Student.objects.all()

    # Get query parameters
    grade = request.GET.get('class')  # You have it disabled in form
    section = request.GET.get('section')
    search = request.GET.get('search')
    ids = request.GET.get('ids')

    # Filter by class/grade if provided
    if grade:
        students = students.filter(grade=grade)

    # Filter by section if provided
    if section:
        students = students.filter(section=section)

    # Filter by name or roll/id
    if search:
        students = students.filter(
            Q(full_name__icontains=search) | Q(roll__icontains=search)
        )

    # Filter by comma-separated IDs
    if ids:
        id_list = [i.strip() for i in ids.split(',') if i.strip().isdigit()]
        students = students.filter(id__in=id_list)

    context = {
        'students': students,
        'class_id': grade,
        'section_choices': Student.SECTION_CHOICES,
    }
    return render(request, 'students/student_list.html', context)
