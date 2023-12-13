import io

import PyPDF2
from django.contrib import messages
from django.shortcuts import redirect, render
from docx import Document
from pyresparser import ResumeParser
from users.models import User

from .form import UpdateResumeForm
from .models import Resume


def extract_pdf_data(uploaded_file):
    # Convert the InMemoryUploadedFile to bytes
    file_content = uploaded_file.read()

    # Create a BytesIO object from the file content
    file_stream = io.BytesIO(file_content)

    # Create a PDF reader object
    pdf_reader = PyPDF2.PdfReader(file_stream)

    # Get the number of pages in the PDF
    num_pages = len(pdf_reader.pages)

    # Extract text from each page
    extracted_text = ""
    for page_num in range(num_pages):
        page = pdf_reader.pages[page_num]
        extracted_text += page.extract_text()

    doc = Document()
    doc.add_paragraph(extracted_text)
    doc.save("text.docx")
    resume_infos = ResumeParser("text.docx").get_extracted_data()

    return resume_infos


# Create your views here.
def update_resume(request):
    if request.user.is_applicant:
        resume = Resume.objects.get(user=request.user)
        if request.method == "POST":
            form = UpdateResumeForm(request.POST, request.FILES, instance=resume)
            if form.is_valid():
                if "upload_resume" in request.FILES:
                    file = request.FILES["upload_resume"]
                    extracted_data = extract_pdf_data(file)
                    # resume
                    fname = extracted_data["name"].split(" ")[0]
                    sname = extracted_data["name"].split(" ")[1]
                    phone_number = extracted_data["mobile_number"]
                    loc = extracted_data["designation"]
                    skills_list = " ".join(word for word in extracted_data["skills"])
                    print(fname, sname, loc, skills_list)
                    # resume = UpdateResumeForm(instance=resume)
                    context = {
                        "form": form,
                        "fname": fname,
                        "sname": sname,
                        "loc": loc,
                        "phone_number": phone_number,
                        "skills_list": skills_list,
                        "filename": file,
                    }

                if "submit" in request.POST:
                    var = form.save(commit=False)
                    user = User.objects.get(pk=request.user.id)
                    user.has_resume = True
                    user.save()
                    var.save()
                    messages.info(request, "Resume has been updated")
                    return redirect("dashboard")
                else:
                    return render(
                        request,
                        "resume/update_resume.html",
                        context,
                    )
            else:
                messages.warning(request, "Something went wrong")
        else:
            form = UpdateResumeForm(instance=resume)
            context = {"form": form}
            return render(
                request,
                "resume/update_resume.html",
                context,
            )
    else:
        messages.warning(request, "Permission denied.")
        return redirect("dashboard")


#
def resume_details(request, pk):
    resume = Resume.objects.get(pk=pk)
    context = {"resume": resume}
    return render(
        request,
        "resume/resume_details.html",
        context,
    )
