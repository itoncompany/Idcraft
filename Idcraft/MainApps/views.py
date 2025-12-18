from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from datetime import datetime
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import landscape, A4
from reportlab.lib.units import mm
from reportlab.lib.utils import ImageReader
from reportlab.lib import colors
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from django.conf import settings
from PIL import Image
import os

from MainApps.models import SchoolDetails, Student, IDCardTemplate
from RatingAndReviews.models import Feedback
from Authentications.models import ServicePrice, CompanyPaymentDetails

# Register fonts
arial_path = os.path.join(settings.BASE_DIR, 'fonts', 'arial.ttf')
verdana_path = os.path.join(settings.BASE_DIR, 'fonts', 'verdana.ttf')
pdfmetrics.registerFont(TTFont('Arial', arial_path))
pdfmetrics.registerFont(TTFont('Verdana', verdana_path))


def home(request):
    ratings = Feedback.objects.filter(is_public=True).order_by('-created_at')[:5]
    return render(request, 'MainApps/home.html', {'ratings': ratings})


def service_pricing(request):
    company_payment_details = CompanyPaymentDetails.objects.filter(
        is_active=True, payment_method='esewa'
    ).first()
    service_prices = ServicePrice.objects.filter(is_active=True)
    return render(request, 'MainApps/service_pricing.html', {
        'service_prices': service_prices,
        'company_payment_details': company_payment_details
    })


def school_dashboard(request):
    user = request.user
    school = SchoolDetails.objects.filter(user=user).first()
    if not school:
        return render(request, "MainApps/error.html", {"message": "No school details found for the logged-in user."})

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
        return render(request, "MainApps/error.html", {"message": "No school details found for the logged-in user."})

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

    roll = request.GET.get('roll')
    if roll:
        students_list = students_list.filter(roll__icontains=roll)

    status = request.GET.get('status')
    if status:
        students_list = students_list.filter(status=status)

    section = request.GET.get('section')
    if section:
        students_list = students_list.filter(section=section)

    sort = request.GET.get('sort')
    if sort == 'az':
        students_list = students_list.order_by('full_name')
    elif sort == 'za':
        students_list = students_list.order_by('-full_name')
    elif sort == 'roll':
        students_list = students_list.order_by('roll')
    else:
        students_list = students_list.order_by('grade', 'section', 'roll')

    paginator = Paginator(students_list, 10)
    page = request.GET.get('page')
    students = paginator.get_page(page)

    context = {
        "students": students,
        "section_choices": Student.SECTION_CHOICES,
        "gender_choices": Student.GENDER_CHOICES,
        "school": school,
        "grade_choices": Student.GRADE_CHOICES,
        "class_id": class_id,
    }
    return render(request, "MainApps/card_form.html", context)


@login_required
def add_student(request):
    if request.method == 'POST':
        grade = request.POST.get('grade') or 'OTHER'
        school = SchoolDetails.objects.filter(user=request.user).first()

        dob_str = request.POST.get('dob', '').strip()
        valid_until_str = request.POST.get('valid_until', '').strip()
        dob = datetime.strptime(dob_str, '%Y-%m-%d').date() if dob_str else None
        valid_until = datetime.strptime(valid_until_str, '%Y-%m-%d').date() if valid_until_str else None

        student = Student(
            user=request.user,
            school=school,
            full_name=request.POST.get('full_name', '').strip(),
            roll=request.POST.get('roll', '').strip() or None,
            grade=grade,
            section=request.POST.get('section', '').strip() or None,
            gender=request.POST.get('gender') or 'OTHER',
            dob=dob,
            valid_until=valid_until,
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
        student.full_name = request.POST.get('full_name', student.full_name).strip()
        student.roll = request.POST.get('roll', student.roll).strip() or None
        student.grade = request.POST.get('grade', student.grade) or 'OTHER'
        student.section = request.POST.get('section', student.section).strip() or None
        student.gender = request.POST.get('gender', student.gender) or 'OTHER'
        student.status = request.POST.get('status', student.status)
        student.parent_name = request.POST.get('parent_name', student.parent_name).strip() or None
        student.parent_phone = request.POST.get('parent_phone', student.parent_phone).strip() or None
        student.address = request.POST.get('address', student.address).strip() or None

        dob_str = request.POST.get('dob', '').strip()
        valid_until_str = request.POST.get('valid_until', '').strip()
        if dob_str:
            student.dob = datetime.strptime(dob_str, '%Y-%m-%d').date()
        if valid_until_str:
            student.valid_until = datetime.strptime(valid_until_str, '%Y-%m-%d').date()

        if request.FILES.get('photo'):
            student.photo = request.FILES['photo']

        student.save()
        messages.success(request, f"{student.full_name} updated successfully!")

    return redirect(request.META.get('HTTP_REFERER', 'students_list'))


def delete_student(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == 'POST':
        student_name = student.full_name
        student.delete()
        messages.success(request, f"{student_name} deleted successfully!")
        return redirect(request.META.get('HTTP_REFERER', '/'))
    return redirect(request.META.get('HTTP_REFERER', '/'))


@login_required
def student_list(request):
    user = request.user
    school = SchoolDetails.objects.filter(user=user).first()
    if not school:
        return render(request, "MainApps/error.html", {"message": "No school details found for this user."})

    students = school.students.all()
    grade = request.GET.get('class')
    section = request.GET.get('section')
    status = request.GET.get('status')
    roll = request.GET.get('roll')
    sort = request.GET.get('sort')
    ids = request.GET.get('ids')

    if grade:
        students = students.filter(grade=grade)
    if section:
        students = students.filter(section=section)
    if status:
        students = students.filter(status=status)
    if roll:
        students = students.filter(roll__icontains=roll)
    if ids:
        id_list = [i.strip() for i in ids.split(',') if i.strip().isdigit()]
        students = students.filter(id__in=id_list)

    # Sorting
    if sort == 'az':
        students = students.order_by('full_name')
    elif sort == 'za':
        students = students.order_by('-full_name')
    elif sort == 'roll':
        students = students.order_by('roll')
    else:
        students = students.order_by('grade', 'section', 'roll')

    paginator = Paginator(students, 10)
    page = request.GET.get('page')
    students_page = paginator.get_page(page)

    context = {
        'students': students_page,
        'section_choices': Student.SECTION_CHOICES,
        'gender_choices': Student.GENDER_CHOICES,
        'class_id': grade,
    }
    return render(request, 'students/student_list.html', context)


@login_required
def export_id_cards(request, class_id=None):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename="id_cards_{class_id}.pdf"'

    page_width, page_height = landscape(A4)
    c = canvas.Canvas(response, pagesize=(page_width, page_height))

    user = request.user
    school = SchoolDetails.objects.filter(user=user).first()
    if not school:
        return HttpResponse("No school details found", status=404)

    template = IDCardTemplate.objects.filter(school=school).first()
    if not template or not template.template_image:
        return HttpResponse("No ID Card Template found", status=404)

    template_path = os.path.join(settings.MEDIA_ROOT, template.template_image.name)
    if not os.path.exists(template_path):
        return HttpResponse("Template image not found", status=404)

    template_img = ImageReader(template_path)

    students = Student.objects.filter(school=school)
    if class_id:
        students = students.filter(grade__icontains=class_id)

    section_filter = request.GET.get('section')
    if section_filter:
        students = students.filter(section=section_filter)

    roll_filter = request.GET.get('roll')
    if roll_filter:
        students = students.filter(roll__icontains=roll_filter)

    students = students.order_by('grade', 'section', 'roll')

    # Compute card size from template image
    pil_img = Image.open(template_path)
    img_width_px, img_height_px = pil_img.size
    dpi_x, dpi_y = pil_img.info.get('dpi', (300, 300))
    card_width = img_width_px * 72 / dpi_x
    card_height = img_height_px * 72 / dpi_y

    # Margins and spacing
    margin_x = 10 * mm
    margin_y = 10 * mm

    # Fix 5 cards per row and compute dynamic spacing
    desired_cards_per_row = 5
    total_card_width = desired_cards_per_row * card_width
    x_spacing = (page_width - 2 * margin_x - total_card_width) / (desired_cards_per_row - 1)
    cards_per_row = desired_cards_per_row

    # Cards per column
    y_spacing = 10 * mm
    cards_per_column = int((page_height - 2 * margin_y + y_spacing) // (card_height + y_spacing))
    cards_per_page = cards_per_row * cards_per_column

    # Function to draw text
    def draw_text(value, x_pos, y_pos, font_size=10, font_color="#000000", font_family="Helvetica", align='left'):
        try:
            c.setFont(font_family, font_size)
        except:
            c.setFont("Helvetica", font_size)
        c.setFillColor(colors.HexColor(font_color))
        if align == 'center':
            c.drawCentredString(x_pos, y_pos, str(value))
        elif align == 'right':
            c.drawRightString(x_pos, y_pos, str(value))
        else:
            c.drawString(x_pos, y_pos, str(value))

    # Map template fields to student model attributes
    FIELD_MAP = {
        'roll': 'roll',
        'full_name': 'full_name',
        'grade': 'grade',
        'address': 'address',
        'parent_name': 'parent_name',
        'parent_phone': 'parent_phone',
        'valid_until': 'valid_until',
    }

    # Labels for each field
    FIELD_LABELS = {
        'roll': 'Roll No:',
        'full_name': 'Name:',
        'grade': 'Class:',
        'address': 'Address:',
        'parent_name': 'Parent:',
        'parent_phone': 'Parent:',
        'valid_until': 'Valid Till:',
    }

    for index, student in enumerate(students):
        pos_on_page = index % cards_per_page
        row = pos_on_page // cards_per_row
        col = pos_on_page % cards_per_row

        if index > 0 and index % cards_per_page == 0:
            c.showPage()  # New page

        x = margin_x + col * (card_width + x_spacing)
        y = page_height - margin_y - (row + 1) * card_height - row * y_spacing

        # Draw template background
        c.drawImage(template_img, x, y, width=card_width, height=card_height, preserveAspectRatio=False, mask='auto')

        # Draw student photo
        if student.photo:
            photo_path = os.path.join(settings.MEDIA_ROOT, student.photo.name)
            if os.path.exists(photo_path):
                photo_w = getattr(template, 'photo_width', 40*mm)
                photo_h = getattr(template, 'photo_height', 50*mm)
                photo_x = x + getattr(template, 'photo_x', 10*mm)
                photo_y = y + getattr(template, 'photo_y', card_height - photo_h - 10*mm)
                c.drawImage(photo_path, photo_x, photo_y, width=photo_w, height=photo_h, preserveAspectRatio=True, mask='auto')

        # Draw fields dynamically with labels
        for field_name, student_attr in FIELD_MAP.items():
            # Special handling for Roll No + Section
            if field_name == 'roll':
                roll = getattr(student, 'roll', '')
                section = getattr(student, 'section', '')
                value = f"{roll} - ( {section} )"  # Display as Roll No: 2 -(A)
            else:
                value = getattr(student, student_attr, '')
                if field_name == 'valid_until' and value:
                    value = value.strftime('%d-%m-%Y')

            # Get font & position from template
            x_pos = getattr(template, f"{field_name}_x", 10)
            y_pos = getattr(template, f"{field_name}_y", 10)
            font_size = getattr(template, f"{field_name}_font_size", 10)
            font_color = getattr(template, f"{field_name}_font_color", "#000000")
            font_family = getattr(template, f"{field_name}_font_family", "Helvetica")
            alignment = getattr(template, f"{field_name}_alignment", "left")

            label = FIELD_LABELS.get(field_name, '')

            # Draw label
            draw_text(label, x + x_pos, y + y_pos, font_size, font_color, font_family, alignment)
            # Draw value next to label
            label_width = c.stringWidth(label, font_family, font_size)
            draw_text(value, x + x_pos + label_width + 2, y + y_pos, font_size, font_color, font_family, alignment)

    c.save()
    return response