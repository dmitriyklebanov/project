import multiprocessing

from django.contrib import admin
from django_registration.backends.activation.views import RegistrationView

from accounts.models import Profile

from financial_manager import settings


def spawn_process(email_sender, user):
    email_sender.send_activation_email(user)


def send_activation_email(_, request, queryset):
    email_sender = RegistrationView()
    email_sender.email_body_template = settings.ACTIVATION_EMAIL_BODY
    email_sender.email_subject_template = settings.ACTIVATION_EMAIL_SUBJECT
    email_sender.request = request

    processes = []
    for profile in queryset:
        process = multiprocessing.Process(target=spawn_process, args=(email_sender, profile.user))
        processes.append(process)
        process.start()

    for process in processes:
        process.join()


send_activation_email.short_description = 'Send activation email'


class ProfileAdmin(admin.ModelAdmin):
    actions = [send_activation_email, ]


admin.site.register(Profile, ProfileAdmin)
