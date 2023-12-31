# Generated by Django 4.2.2 on 2023-06-28 10:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="post_info",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("name", models.CharField(blank=True, max_length=100, null=True)),
                ("title", models.CharField(blank=True, max_length=30, null=True)),
                (
                    "discription",
                    models.CharField(blank=True, max_length=100, null=True),
                ),
                ("content", models.CharField(blank=True, max_length=100, null=True)),
                ("creation_date", models.DateTimeField(auto_now=True)),
            ],
            options={
                "db_table": "post_info",
            },
        ),
        migrations.CreateModel(
            name="user_info",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("name", models.CharField(blank=True, max_length=100, null=True)),
                ("email", models.EmailField(blank=True, max_length=254, null=True)),
                ("password", models.TextField(blank=True, null=True)),
                ("created_at", models.DateTimeField(auto_now=True)),
            ],
            options={
                "db_table": "user_info",
            },
        ),
        migrations.CreateModel(
            name="Liked_Saved",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("is_liked", models.BooleanField(default=True)),
                ("created_at", models.DateTimeField(auto_now=True)),
                (
                    "post",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="app.post_info",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="app.user_info",
                    ),
                ),
            ],
            options={
                "db_table": "liked_saved_user",
            },
        ),
    ]
