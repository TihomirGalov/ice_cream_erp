# Generated by Django 4.2.3 on 2023-07-18 19:38

from decimal import Decimal
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('ice_cream_types', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Store',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cones', models.IntegerField()),
                ('cups', models.IntegerField()),
                ('worker', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='IceCream',
            fields=[
                ('type', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='ice_cream', serialize=False, to='ice_cream_types.icecreamtype')),
                ('quantity', models.DecimalField(decimal_places=2, max_digits=10, validators=[django.core.validators.MinValueValidator(Decimal('0.01'))])),
                ('stores', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ice_creams', to='stores.store')),
            ],
        ),
    ]
