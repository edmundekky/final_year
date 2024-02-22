from django.contrib import messages
from django.db.models import Count, Q
from django.http import FileResponse, HttpResponse
from django.shortcuts import redirect, render
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph, SimpleDocTemplate, Table, TableStyle

from accounts.decorators import investigator_required
from profiler.matcher import match_criminal, match_projected_techniques

from .forms import CyberCriminalForm
from .models import (
    Alias,
    AssociatedDevice,
    AssociatedIP,
    CyberCriminal,
    CyberCriminalMatch,
    Technique,
)


@investigator_required
def view_profile(request, criminal_id):
    cyber_criminal = CyberCriminal.objects.get(id=criminal_id)

    context = {
        "cyber_criminal": cyber_criminal,
    }
    template_name = "profiler/view_profile.html"
    return render(request, template_name, context)


@investigator_required
def add_profile(request):
    techniques = Technique.objects.all()

    if request.method != "POST":
        criminal_form = CyberCriminalForm()
    else:
        criminal_form = CyberCriminalForm(request.POST)
        aliases = request.POST.get("aliases", "")
        alias_list = [alias.strip() for alias in aliases.split(",")]
        associated_ips = request.POST.get("ips", "")
        ip_list = [ip.strip() for ip in associated_ips.split(",")]
        associated_devices = request.POST.get("devices", "")
        device_list = [device.strip() for device in associated_devices.split(",")]
        techniques_used = request.POST.getlist("techniques")

        if criminal_form.is_valid():
            cyber_criminal = criminal_form.save(commit=False)
            cyber_criminal.investigator = request.user
            cyber_criminal.save()

            for alias in alias_list:
                Alias.objects.create(cyber_criminal=cyber_criminal, name=alias)

            for ip in ip_list:
                AssociatedIP.objects.create(
                    cyber_criminal=cyber_criminal, ip_address=ip
                )

            for device in device_list:
                AssociatedDevice.objects.create(
                    cyber_criminal=cyber_criminal, device_name=device
                )

            tactics = set()

            for technique in set(techniques_used):
                new_technique = Technique.objects.get(id=technique)
                cyber_criminal.techniques.add(new_technique)
                tactics.add(new_technique.tactic)

            for tactic in tactics:
                cyber_criminal.tactics.add(tactic)

            messages.success(
                request,
                f"Criminal Profile for {cyber_criminal.name} created successfully.",
            )
            return redirect("profiler:criminal_profiles")

    context = {
        "criminal_form": criminal_form,
        "techniques": techniques,
    }
    template_name = "profiler/add_profile.html"
    return render(request, template_name, context)


@investigator_required
def criminal_profiles(request):
    cyber_criminals = CyberCriminal.objects.all()

    context = {"cyber_criminals": cyber_criminals}
    tempate_name = "profiler/cyber_criminals.html"
    return render(request, tempate_name, context)


@investigator_required
def match_profile(request):
    cyber_criminals = CyberCriminal.objects.all()
    techniques = Technique.objects.all()

    if request.method != "POST":
        criminal_form = CyberCriminalForm()
    else:
        criminal_form = CyberCriminalForm(request.POST)
        aliases = request.POST.get("aliases", "")
        alias_list = [alias.strip() for alias in aliases.split(",")]
        associated_ips = request.POST.get("ips", "")
        ip_list = [ip.strip() for ip in associated_ips.split(",")]
        associated_devices = request.POST.get("devices", "")
        device_list = [device.strip() for device in associated_devices.split(",")]
        techniques_used = request.POST.getlist("techniques")

        if criminal_form.is_valid():
            temp_criminal = criminal_form.save(commit=False)
            temp_criminal.investigator = request.user
            temp_criminal.save()

            for alias in alias_list:
                Alias.objects.create(cyber_criminal=temp_criminal, name=alias)

            # add ip only if ip is not empty
            if ip_list[0] != "":
                for ip in ip_list:
                    AssociatedIP.objects.create(
                        cyber_criminal=temp_criminal, ip_address=ip
                    )

            # add device only if device is not empty
            if device_list[0] != "":
                for device in device_list:
                    AssociatedDevice.objects.create(
                        cyber_criminal=temp_criminal, device_name=device
                    )

            tactics = set()
            temp_techniques = set()

            for technique in set(techniques_used):
                new_technique = Technique.objects.get(id=technique)
                temp_criminal.techniques.add(new_technique)
                temp_techniques.add(new_technique)
                tactics.add(new_technique.tactic)

            for tactic in tactics:
                temp_criminal.tactics.add(tactic)

            matched_criminals = match_criminal(temp_criminal)
            if matched_criminals is None:
                messages.info(
                    request,
                    f"No matching criminal profiles found for {temp_criminal.name}.",
                )
                return redirect("profiler:criminal_profiles")
            else:
                possible_techniques = match_projected_techniques(
                    temp_criminal, matched_criminals
                )

                temp_criminal.delete()

                cyber_criminal_match = CyberCriminalMatch.objects.create(
                    made_by=request.user,
                )

                matched_criminals_list = []
                for criminal, _ in matched_criminals:
                    matched_criminals_list.append(criminal.id)

                cyber_criminal_match.matched_criminals.set(matched_criminals_list)
                cyber_criminal_match.techniques.set(possible_techniques)
                cyber_criminal_match.save()

                messages.success(
                    request,
                    f"Matching criminal profiles found",
                )
                return redirect(
                    "profiler:match_results", match_id=cyber_criminal_match.id
                )

    context = {
        "cyber_criminals": cyber_criminals,
        "techniques": techniques,
        "criminal_form": criminal_form,
    }
    tempate_name = "profiler/match_profile.html"
    return render(request, tempate_name, context)


@investigator_required
def match_results(request, match_id):
    cyber_criminal_match = CyberCriminalMatch.objects.get(id=match_id)

    matched_criminals = cyber_criminal_match.matched_criminals.all()
    possible_techniques = cyber_criminal_match.techniques.all()

    context = {
        "match": cyber_criminal_match,
        "matched_criminals": matched_criminals,
        "possible_techniques": possible_techniques,
    }
    template_name = "profiler/match_results.html"
    return render(request, template_name, context)


@investigator_required
def search(request):
    query = request.GET.get("q")

    cyber_criminals = CyberCriminal.objects.filter(
        Q(name__icontains=query)
        | Q(techniques__name__icontains=query)
        | Q(tactics__name__icontains=query)
        | Q(aliases__name__icontains=query)
        | Q(associated_ips__ip_address__icontains=query)
        | Q(associated_devices__device_name__icontains=query)
    ).distinct()

    context = {
        "cyber_criminals": cyber_criminals,
    }
    template_name = "profiler/search.html"
    return render(request, template_name, context)


@investigator_required
def generate_results_pdf(request, match_id):
    match = CyberCriminalMatch.objects.get(id=match_id)

    # Create a FileResponse object with the appropriate PDF headers.
    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = (
        f"attachment; filename=Match by {match.made_by} on {match.matched_on.strftime('%Y-%m-%d %H:%M:%S')} Report.pdf"
    )

    # Create the PDF object, using the response object as its "file".
    p = SimpleDocTemplate(response, pagesize=letter)

    # Prepare data for the table
    data = [["Name", "Description"]]
    styles = getSampleStyleSheet()
    for technique in match.techniques.all():
        name = Paragraph(technique.name, styles["BodyText"])
        description = Paragraph(technique.description, styles["BodyText"])
        data.append([name, description])

    # Calculate the available width of the page
    available_width = letter[0] - 2 * 20  # assuming a margin of 20 on each side

    # Create a Table with the data and add it to the PDF
    table = Table(data, colWidths=[available_width / 2, available_width / 2])
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, 0), 14),
                ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
                ("BACKGROUND", (0, 1), (-1, -1), colors.beige),
                ("GRID", (0, 0), (-1, -1), 1, colors.black),
                ("LEFTPADDING", (0, 0), (-1, -1), 5),
                ("RIGHTPADDING", (0, 0), (-1, -1), 5),
                ("TOPPADDING", (0, 0), (-1, -1), 5),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
            ]
        )
    )
    styles["Title"].fontSize = 23

    # add a page title and its styling, it should be underlined
    title = Paragraph(
        f"<u>Report on Match by {match.made_by.get_full_name()} on {match.matched_on.strftime('%Y-%m-%d %H:%M:%S')}</u>",
        styles["Title"],
    )
    styles["BodyText"].fontSize = 14

    text1 = Paragraph(
        "<i>Based on the information provided, the following techniques are projected to be used by the cyber-criminal.</i>",
        styles["BodyText"],
    )

    # addtional styling for the text
    title.spaceAfter = 20
    text1.spaceAfter = 20

    elements = [title, text1, table]
    p.build(elements)

    return response
