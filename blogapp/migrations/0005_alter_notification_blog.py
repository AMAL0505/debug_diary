# Generated by Django 4.2.19 on 2025-02-17 19:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blogapp', '0004_notification_blog_notification_notification_type_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='blog',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_notifications', to='blogapp.blog'),
        ),
    ]
