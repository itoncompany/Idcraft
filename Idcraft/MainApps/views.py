from django.shortcuts import render, redirect, get_object_or_404 # pyright: ignore[reportMissingModuleSource]
from django.contrib import messages
from django.db.models import Q, Count # pyright: ignore[reportMissingModuleSource]
from django.http import HttpResponse # pyright: ignore[reportMissingModuleSource]
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.core.files.base import ContentFile
from datetime import datetime
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import landscape, A4
from reportlab.lib.units import mm
from reportlab.lib.utils import ImageReader
from reportlab.lib import colors
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from django.conf import settings
import pandas as pd
from datetime import datetime
from PIL import Image
from io import BytesIO
import os
from Authentications.models import Profile,TeamMember
from MainApps.models import SchoolDetails, Student, IDCardTemplate
from RatingAndReviews.models import Feedback
from Authentications.models import ServicePrice, CompanyPaymentDetails

# Register fonts
arial_path = os.path.join(settings.BASE_DIR, 'fonts', 'arial.ttf')
verdana_path = os.path.join(settings.BASE_DIR, 'fonts', 'verdana.ttf')
pdfmetrics.registerFont(TTFont('Arial', arial_path))
pdfmetrics.registerFont(TTFont('Verdana', verdana_path))



def school(request):
    user = request.user
    if not user.is_authenticated:
        messages.warning(request, "You need to log in to view the grade list.")
        return redirect('home')

    school = SchoolDetails.objects.filter(user=user).first()
    if not school:
        messages.warning(request, "No school details found for the logged-in user.")
        return redirect('home')

    students = school.students.all()

    # Total students
    total_students = students.count()

    # Status totals
    status_totals = {}
    for status_code, _status_name in Student.ID_STATUS_CHOICES:
        status_totals[status_code] = students.filter(status=status_code).count()

    # Grade-wise counts
    grade_counts_qs = students.values('grade').annotate(count=Count('id'))
    grade_counts = {item['grade']: item['count'] for item in grade_counts_qs}
    for code, _name in Student.GRADE_CHOICES:
        if code not in grade_counts:
            grade_counts[code] = 0

    # Gender counts
    gender_counts = students.aggregate(
        male=Count('id', filter=Q(gender='MALE')),
        female=Count('id', filter=Q(gender='FEMALE')),
        other=Count('id', filter=Q(gender='OTHER'))
    )

    context = {
        "school": school,
        "students": students,
        "total_students": total_students,
        "status_totals": status_totals,
        "grade_counts": grade_counts,
        "male_count": gender_counts.get('male', 0),
        "female_count": gender_counts.get('female', 0),
        "other_count": gender_counts.get('other', 0),
        "grades": Student.GRADE_CHOICES,
        "gender_choices": Student.GENDER_CHOICES,
        "section_choices": Student.SECTION_CHOICES,
    }

    return render(request, 'MainApps/school.html', context)


def home(request):
    ratings = Feedback.objects.filter(is_public=True).order_by('-created_at')[:5]
    team=TeamMember.objects.filter(is_active=True).order_by('-created_at')[:5]
    return render(request, 'MainApps/home.html', {'ratings': ratings,'tam_members':team})


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
    if not user.is_authenticated:
        messages.warning(request, "You need to log in to view the school dashboard.")
        return redirect('home')  # or any URL name for your homepage

    school = SchoolDetails.objects.filter(user=user).first()
    if not school:
        messages.warning(request, "No school details found for the logged-in user.")
        return redirect('home')

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
    if not user.is_authenticated:
        messages.warning(request, "You need to log in to view the grade list.")
        return redirect('home')

    school = SchoolDetails.objects.filter(user=user).first()
    if not school:
        messages.warning(request, "No school details found for the logged-in user.")
        return redirect('home')

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

    # 🔹 Roll filter (supports: 1 or 1,2,3)
    roll_input = request.GET.get('roll')
    if roll_input:
        roll_list = [r.strip() for r in roll_input.split(',') if r.strip()]
        students_list = students_list.filter(roll__in=roll_list)

    # 🔹 Status filter
    status = request.GET.get('status')
    if status:
        students_list = students_list.filter(status=status)

    # 🔹 Section filter
    section = request.GET.get('section')
    if section:
        students_list = students_list.filter(section=section)

    # 🔹 Sorting
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






def import_students_from_excel(file, request, school):
    df = pd.read_excel(file)
    count = 0

    for _, row in df.iterrows():
        Student.objects.create(
            user=request.user,
            school=school,

            full_name=str(row.get('full_name', '')).strip(),
            roll=str(row.get('roll')).strip() if pd.notna(row.get('roll')) else None,
            grade=row.get('grade'),
            section=str(row.get('section')).strip() if pd.notna(row.get('section')) else None,
            gender=row.get('gender') if pd.notna(row.get('gender')) else 'OTHER',

            dob=row.get('dob') if pd.notna(row.get('dob')) else None,
            valid_until=row.get('valid_until') if pd.notna(row.get('valid_until')) else None,

            parent_name=str(row.get('parent_name')).strip() if pd.notna(row.get('parent_name')) else None,
            parent_phone=str(row.get('parent_phone')).strip() if pd.notna(row.get('parent_phone')) else None,
            address=str(row.get('address')).strip() if pd.notna(row.get('address')) else None,

            status=row.get('status') if pd.notna(row.get('status')) else 'NEW',
        )
        count += 1

    return count



def upload_excel(request):
    if request.method == 'POST':
        excel_file = request.FILES.get('excel_file')

        if not excel_file:
            messages.error(request, "Please upload an Excel file.")
            return redirect(request.META.get('HTTP_REFERER'))

        school = SchoolDetails.objects.filter(user=request.user).first()

        if not school:
            messages.error(request, "School not found for this user.")
            return redirect(request.META.get('HTTP_REFERER'))

        try:
            count = import_students_from_excel(excel_file, request, school)
            messages.success(request, f"{count} students imported successfully.")

        except Exception as e:
            messages.error(request, f"Import failed: {e}")

        return redirect(request.META.get('HTTP_REFERER'))

    # Handle GET request
    return redirect('/')




def export_excel(request):
    school = SchoolDetails.objects.filter(user=request.user).first()
    students = Student.objects.filter(school=school)

    if not students.exists():
        messages.warning(request, "No students to export!")
        return redirect(request.META.get('HTTP_REFERER'))  # Back to the same page

    # Create DataFrame
    df = pd.DataFrame(list(students.values(
        'full_name', 'roll', 'grade', 'section', 'gender',
        'dob', 'valid_until', 'parent_name', 'parent_phone', 'address', 'status'
    )))

    # Prepare Excel file in memory
    from io import BytesIO
    output = BytesIO()
    df.to_excel(output, index=False)
    output.seek(0)

    # Show success message
    messages.success(request, "Students Excel exported successfully!")

    # Return file
    response = HttpResponse(
        output,
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename=students.xlsx'
    return response



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

        # Resize and compress photo if uploaded
        if request.FILES.get('photo'):
            image = request.FILES['photo']
            img = Image.open(image)
            img_format = img.format or 'JPEG'

            # Resize image if larger than 800x800 while maintaining aspect ratio
            max_size = (800, 800)
            img.thumbnail(max_size, Image.Resampling.LANCZOS)

            # Compress to target size (~400 KB)
            buffer = BytesIO()
            quality = 85
            img.save(buffer, format=img_format, optimize=True, quality=quality)

            while buffer.tell() > 400 * 1024 and quality > 20:
                buffer.seek(0)
                buffer.truncate()
                quality -= 5
                img.save(buffer, format=img_format, optimize=True, quality=quality)

            # Save compressed image to student.photo
            student.photo.save(image.name, ContentFile(buffer.getvalue()), save=False)

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
    response['Content-Disposition'] = f'inline; filename="id_cards_{class_id or "all"}.pdf"'

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
    pil_img = Image.open(template_path)
    img_width_px, img_height_px = pil_img.size
    dpi_x, dpi_y = pil_img.info.get('dpi', (300, 300))
    card_width = img_width_px * 72 / dpi_x
    card_height = img_height_px * 72 / dpi_y

    margin_x = 10
    margin_y = 10
    cards_per_row = 5
    total_card_width = cards_per_row * card_width
    x_spacing = (page_width - 2 * margin_x - total_card_width) / (cards_per_row - 1)
    y_spacing = 10
    cards_per_column = int((page_height - 2 * margin_y + y_spacing) // (card_height + y_spacing))
    cards_per_page = cards_per_row * cards_per_column

    # Query students
    students = Student.objects.filter(school=school)
    if class_id:
        students = students.filter(grade__icontains=class_id)
    section_filter = request.GET.get('section')
    if section_filter:
        students = students.filter(section=section_filter)
    status_filter = request.GET.get('status')
    if status_filter:
        students = students.filter(status=status_filter)
    roll_filter = request.GET.get('roll')
    if roll_filter:
        roll_list = [r.strip() for r in roll_filter.split(',') if r.strip()]
        students = students.filter(roll__in=roll_list)
    students = students.order_by('grade', 'section', 'roll')

    # Helper to draw text with color and alignment
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

    FIELD_NAMES = [
        'roll', 'full_name', 'dob', 'gender', 'email', 'student_phone',
        'parent_name', 'parent_phone', 'address', 'school_name', 'grade', 'section', 'valid_until'
    ]

    for idx, student in enumerate(students):
        pos_on_page = idx % cards_per_page
        row = pos_on_page // cards_per_row
        col = pos_on_page % cards_per_row

        if idx > 0 and idx % cards_per_page == 0:
            c.showPage()

        x = margin_x + col * (card_width + x_spacing)
        y = page_height - margin_y - (row + 1) * card_height - row * y_spacing

        # Draw template background
        c.drawImage(template_img, x, y, width=card_width, height=card_height, preserveAspectRatio=False, mask='auto')

        # Draw student photo
        if template.photo_value_active and getattr(student, 'photo', None):
            photo_path = os.path.join(settings.MEDIA_ROOT, student.photo.name)
            if os.path.exists(photo_path):
                photo_w = getattr(template, 'photo_width', 40)
                photo_h = getattr(template, 'photo_height', 50)
                photo_x = x + getattr(template, 'photo_x', 10)
                photo_y = y + getattr(template, 'photo_y', card_height - photo_h - 10)
                c.drawImage(photo_path, photo_x, photo_y, width=photo_w, height=photo_h, preserveAspectRatio=True, mask='auto')

        # Draw all fields
        for field in FIELD_NAMES:
            value_active = getattr(template, f"{field}_value_active", True)
            tag_active = getattr(template, f"{field}_tag_active", True)
            if not value_active and not tag_active:
                continue

            # Get field value
            if field == 'roll':
                roll = getattr(student, 'roll', '')
                section = getattr(student, 'section', '')
                value = f"{roll} - ({section})"
            elif field == 'valid_until':
                val = getattr(student, field, None)
                value = val.strftime("%d-%m-%Y") if val else ''
            else:
                value = getattr(student, field, '')

            # Position and styling
            x_pos = getattr(template, f"{field}_x", 10) + x
            y_pos = getattr(template, f"{field}_y", 10) + y
            font_size = getattr(template, f"{field}_font_size", 10)
            font_family = getattr(template, f"{field}_font_family", "Helvetica")
            alignment = getattr(template, f"{field}_alignment", "left")

            tag_text = getattr(template, f"{field}_tag", field.capitalize())
            tag_color = getattr(template, f"{field}_tag_color", "#000000")
            value_color = getattr(template, f"{field}_value_color", "#000000")

            if tag_active:
                draw_text(f"{tag_text}:", x_pos, y_pos, font_size, tag_color, font_family, alignment)

            if value_active:
                label_width = c.stringWidth(f"{tag_text}:", font_family, font_size) if tag_active else 0
                draw_text(value, x_pos + label_width + 2, y_pos, font_size, value_color, font_family, alignment)

    c.save()
    return response


@login_required
def update_school(request):
    user = request.user
    school, _ = SchoolDetails.objects.get_or_create(user=user)

    if request.method == "POST":
        school.school_name = request.POST.get("school_name", school.school_name)
        if request.FILES.get("school_logo"):
            school.school_logo = request.FILES["school_logo"]
        if request.FILES.get("school_image"):
            school.school_image = request.FILES["school_image"]
        school.address = request.POST.get("address", school.address)
        school.contact_email = request.POST.get("contact_email", school.contact_email)
        school.contact_phone = request.POST.get("contact_phone", school.contact_phone)
        school.website = request.POST.get("website", school.website)
        school.save()
        return redirect("home")  # or reload page

    return render(request, "update_school_modal.html", {"school": school})


@login_required
def update_profile(request):
    user = request.user
    profile, _ = Profile.objects.get_or_create(user=user)

    if request.method == "POST":
        profile.full_name = request.POST.get("full_name", profile.full_name)
        profile.ph_num = request.POST.get("ph_num", profile.ph_num)
        if request.FILES.get("pr_pic"):
            profile.pr_pic = request.FILES["pr_pic"]
        profile.bio = request.POST.get("bio", profile.bio)
        profile.address = request.POST.get("profile_address", profile.address)
        profile.city = request.POST.get("city", profile.city)
        profile.dob = request.POST.get("dob", profile.dob)
        profile.gender = request.POST.get("gender", profile.gender)
        profile.website = request.POST.get("profile_website", profile.website)
        profile.save()
        return redirect("home")  # or reload page

    return render(request, "update_profile_modal.html", {"profile": profile})
