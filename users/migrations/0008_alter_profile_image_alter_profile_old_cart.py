# Generated by Django 4.2.18 on 2025-05-18 10:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_customuser_referral_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='image',
            field=models.ImageField(blank=True, default='default/pic.png', null=True, upload_to='uploads/profile_pic'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='old_cart',
            field=models.JSONField(blank=True, default=dict),
        ),
    ]
