from django.db import models
from django_countries.fields import CountryField
from django.core.validators import MinValueValidator, MaxValueValidator
from accounts.models import Investigator
from django.utils.text import slugify
from django.utils import timezone

class HackerClassification(models.TextChoices):
    BLACK_HAT = "BH", "Black Hat"
    GREY_HAT = "GH", "Grey Hat"
    SCRIPT_KIDDIE = "SK", "Script Kiddie"
    HACKTIVIST = "HA", "Hacktivist"
    STATE_SPONSORED = "SS", "State-Sponsored"
    CYBER_TERRORIST = "CT," "Cyber-Terrorist"
    MALICIOUS_INSIDER = "MI", "Malicious Insider"


class CyberCriminal(models.Model):
    investigator = models.ForeignKey(
        "accounts.Investigator", on_delete=models.CASCADE, null=True, blank=True
    )
    name = models.CharField(
        max_length=255,
        help_text="Middle name/s should be entered in full and not be represented by an initial",
        null=True,
        blank=True,
    )
    d_o_b = models.DateField(null=True, blank=True)
    nationality = models.CharField(
        null=True,
        blank=True,
        max_length=200,
        choices=CountryField().choices + [("", "Select Country")],
    )

    last_known_location = models.CharField(
        max_length=200,
        null=True,
        blank=True,
        choices=CountryField().choices + [("", "Select Country")],
    )
    hacker_classification = models.CharField(
        max_length=20,
        choices=HackerClassification.choices,
        default=HackerClassification.BLACK_HAT,
    )
    tactics = models.ManyToManyField(
        "Tactic", related_name="criminal_profiles", blank=True
    )
    techniques = models.ManyToManyField(
        "Technique", related_name="criminal_profiles", blank=True
    )
    manifesto = models.TextField(null=True, blank=True)

    height = models.PositiveIntegerField(
        help_text="Height in centimeters", null=True, blank=True
    )
    weight = models.PositiveIntegerField(
        help_text="Weight in kilograms", null=True, blank=True
    )
    hair_color = models.CharField(max_length=255, null=True, blank=True)
    eye_color = models.CharField(max_length=255, null=True, blank=True)

    aggression_level = models.IntegerField(
        help_text="Aggression level on a scale of 1-10",
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        default=5,
    )
    risk_taking_level = models.IntegerField(
        help_text="Risk-taking level on a scale of 1-10",
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        default=5,
    )

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name_plural = "Cyber Criminals"
        ordering = ["investigator", "name"]


class Technique(models.Model):
    name = models.CharField(max_length=255)
    tactic = models.ForeignKey("Tactic", on_delete=models.CASCADE, null=True)
    description = models.TextField()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Techniques"
        unique_together = ["name", "tactic"]
        ordering = ["name"]


class Tactic(models.Model):
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(unique=True, null=True, blank=True)
    description = models.TextField()

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Tactic, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = "Tactics"


class AssociatedDevice(models.Model):
    cyber_criminal = models.ForeignKey(
        CyberCriminal,
        on_delete=models.CASCADE,
        related_name="associated_devices",
        null=True,
    )
    device_name = models.CharField(max_length=255)

    def __str__(self):
        return self.device_name

    class Meta:
        verbose_name_plural = "Associated Devices"


class AssociatedIP(models.Model):
    cyber_criminal = models.ForeignKey(
        CyberCriminal,
        on_delete=models.CASCADE,
        related_name="associated_ips",
        null=True,
    )
    ip_address = models.GenericIPAddressField()

    def __str__(self):
        return self.ip_address

    class Meta:
        verbose_name_plural = "Associated IPs"


class Alias(models.Model):
    cyber_criminal = models.ForeignKey(
        CyberCriminal,
        on_delete=models.CASCADE,
        related_name="aliases",
    )

    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Aliases"


class CyberCriminalMatch(models.Model):
    made_by = models.ForeignKey(
        "accounts.Investigator", on_delete=models.CASCADE, null=True
    )
    techniques = models.ManyToManyField("Technique", related_name="matches", blank=True)
    matched_criminals = models.ManyToManyField(
        "CyberCriminal", related_name="matches", blank=True
    )
    matched_on = models.DateTimeField(default=timezone.now)
    def __str__(self):
        return f"{self.made_by}'s Cyber Criminal Match"

    class Meta:
        verbose_name_plural = "Cyber Criminal Matches"
        ordering = ["made_by"]
