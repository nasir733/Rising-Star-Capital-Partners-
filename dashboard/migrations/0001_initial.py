# Generated by Django 3.2.7 on 2021-09-29 11:30

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='Product', max_length=500, null=True)),
                ('price', models.DecimalField(decimal_places=2, default=0, max_digits=100, validators=[django.core.validators.MinValueValidator(0)])),
                ('charge', models.DecimalField(decimal_places=2, default=0, max_digits=100, validators=[django.core.validators.MinValueValidator(0)])),
                ('recurring', models.IntegerField(choices=[(1, 'One time'), (2, 'Month'), (3, 'Year')], default=1, null=True)),
                ('product_id', models.CharField(blank=True, max_length=100, null=True)),
                ('price_id', models.CharField(blank=True, max_length=100, null=True)),
                ('price_lookup', models.CharField(blank=True, max_length=100, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('video', models.URLField(blank=True, null=True)),
                ('link', models.URLField(blank=True, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ProductPurchasedModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('payments_left', models.DecimalField(decimal_places=2, default=0, max_digits=100)),
                ('amount_left', models.DecimalField(decimal_places=2, default=0, max_digits=100)),
                ('username', models.CharField(blank=True, max_length=50, null=True)),
                ('password', models.CharField(blank=True, max_length=50, null=True)),
                ('link', models.URLField(blank=True, null=True)),
                ('logged_link', models.URLField(blank=True, null=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dashboard.product')),
            ],
        ),
    ]
