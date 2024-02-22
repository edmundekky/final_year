# Generated by Django 5.0.1 on 2024-01-30 06:54

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='KnownPhrases',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phrase', models.CharField(max_length=255, unique=True)),
                ('slug', models.SlugField(max_length=255, unique=True)),
            ],
            options={
                'verbose_name_plural': 'Known Phrases',
            },
        ),
        migrations.CreateModel(
            name='Procedure',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
                ('slug', models.SlugField(max_length=255, unique=True)),
                ('description', models.TextField()),
            ],
            options={
                'verbose_name_plural': 'Procedures',
            },
        ),
        migrations.CreateModel(
            name='Tactics',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
                ('slug', models.SlugField(max_length=255, unique=True)),
                ('description', models.TextField()),
            ],
            options={
                'verbose_name_plural': 'Tactics',
            },
        ),
        migrations.CreateModel(
            name='Technique',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
                ('slug', models.SlugField(max_length=255, unique=True)),
                ('description', models.TextField()),
            ],
            options={
                'verbose_name_plural': 'Techniques',
            },
        ),
        migrations.CreateModel(
            name='CriminalProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('d_o_b', models.DateField()),
                ('height', models.CharField(max_length=255)),
                ('manifesto', models.TextField()),
                ('known_phrases', models.ManyToManyField(to='profiler.knownphrases')),
                ('procedures', models.ManyToManyField(to='profiler.procedure')),
                ('tactics', models.ManyToManyField(to='profiler.tactics')),
                ('techniques', models.ManyToManyField(to='profiler.technique')),
            ],
            options={
                'verbose_name_plural': 'Criminal Profiles',
            },
        ),
    ]
