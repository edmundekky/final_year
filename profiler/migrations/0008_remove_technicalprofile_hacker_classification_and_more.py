# Generated by Django 5.0.1 on 2024-02-06 01:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiler', '0007_alter_cybercriminal_last_known_location_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='technicalprofile',
            name='hacker_classification',
        ),
        migrations.AddField(
            model_name='technicalprofile',
            name='hacker_classification',
            field=models.CharField(choices=[('WH', 'White Hat'), ('BH', 'Black Hat'), ('GH', 'Grey Hat'), ('SK', 'Script Kiddie'), ('HA', 'Hacktivist'), ('SS', 'State-Sponsored'), ('CT,Cyber-Terrorist', 'Cyber Terrorist'), ('MI', 'Malicious Insider')], default='BH', max_length=20),
        ),
    ]
