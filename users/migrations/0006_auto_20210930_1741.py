# Generated by Django 3.2.7 on 2021-09-30 12:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_customuser_bank_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='cash_line_of_credit',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=100, null=True),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='credit_line',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=100, null=True),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='total_line_of_credit',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=100, null=True),
        ),
    ]
