# Generated by Django 5.0.6 on 2024-05-15 17:24

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_userrole'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='userrole',
            unique_together=set(),
        ),
        migrations.AlterField(
            model_name='userrole',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='userrole', to=settings.AUTH_USER_MODEL),
        ),
    ]
