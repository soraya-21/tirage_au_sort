# Generated by Django 4.2.11 on 2024-11-04 14:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Chapeau",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("numero_de_chapeau", models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name="NameModel",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("nom", models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name="Championnat",
            fields=[
                (
                    "namemodel_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="Tirage.namemodel",
                    ),
                ),
            ],
            bases=("Tirage.namemodel",),
        ),
        migrations.CreateModel(
            name="Pays",
            fields=[
                (
                    "namemodel_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="Tirage.namemodel",
                    ),
                ),
            ],
            bases=("Tirage.namemodel",),
        ),
        migrations.CreateModel(
            name="Equipe",
            fields=[
                (
                    "namemodel_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="Tirage.namemodel",
                    ),
                ),
                ("logo", models.ImageField(upload_to="")),
                (
                    "quel_championat",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="Tirage.championnat",
                    ),
                ),
                (
                    "quel_chapeau",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="Tirage.chapeau"
                    ),
                ),
                (
                    "quel_pays",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="Tirage.pays"
                    ),
                ),
            ],
            bases=("Tirage.namemodel",),
        ),
    ]