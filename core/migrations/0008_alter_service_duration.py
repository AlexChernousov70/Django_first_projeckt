# Generated by Django 5.1.7 on 2025-05-02 18:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_remove_order_status_idx_remove_order_created_at_idx_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='service',
            name='duration',
            field=models.PositiveIntegerField(default=20, help_text='Время выполнения в минутах', verbose_name='Время выполнения услуги'),
        ),
    ]
