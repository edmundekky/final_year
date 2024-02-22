from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager
from django.utils import timezone


class ContactType(models.TextChoices):
    INVESTIGATOR = "INV", "Investigator"
    GUEST = "GST", "Guest"


class AdminInvestigatorManager(UserManager):
    """Custom Admin Investigator Manager"""

    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .filter(investigator_type=Investigator.InvestigatorType.ADMIN)
        )


class InvestigatorManager(UserManager):
    """Custom Investigator Manager"""

    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .filter(investigator_type=Investigator.InvestigatorType.INVESTIGATOR)
        )


class Investigator(AbstractUser):
    """
    The model for a forensic investigator.
    """

    class InvestigatorType(models.TextChoices):
        INVESTIGATOR = "INV", "Investigator"
        ADMIN = "ADM", "Admin Investigator"

    # The investigator's phone number.
    phone = models.CharField(max_length=20, blank=False, unique=True)
    # The investigator's address.
    address = models.CharField(max_length=200, blank=False)
    investigator_type = models.CharField(
        max_length=3,
        choices=InvestigatorType.choices,
        default=InvestigatorType.INVESTIGATOR,
    )

    # The default manager.
    objects = UserManager()
    # The admin investigator users manager.
    admin_investigator_objects = AdminInvestigatorManager()
    # The investigator users manager.
    investigator_objects = InvestigatorManager()

    @property
    def is_investigator(self):
        return self.investigator_type == self.InvestigatorType.INVESTIGATOR

    @property
    def is_admin_investigator(self):
        return self.investigator_type == self.InvestigatorType.ADMIN

    @property
    def completion_percentage(self):
        # Define the fields to be checked for completion
        profile_fields = [
            self.first_name,
            self.last_name,
            self.email,
            self.phone,
            self.address,
        ]
        # Calculate the number of completed fields
        completed_fields = sum(1 for field in profile_fields if field)

        # Calculate the percentage of completion
        if len(profile_fields) > 0:
            completion_percentage = (completed_fields / len(profile_fields)) * 100
        else:
            completion_percentage = (
                100  # Profile is considered complete if there are no fields to complete
            )

        return int(completion_percentage)

    class Meta:
        verbose_name = "Investigator"
        verbose_name_plural = "Investigators"
        ordering = ["username"]


class Contact(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField(null=True, blank=True)
    subject = models.CharField(max_length=255)
    message = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    contact_type = models.CharField(
        max_length=3,
        choices=ContactType.choices,
        default=ContactType.GUEST,
    )

    def __str__(self):
        return f"{self.name} - {self.subject[:50]}..."

    class Meta:
        verbose_name = "Contact"
        verbose_name_plural = "Contacts"
        ordering = ["created_at"]
