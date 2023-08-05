# Generated by Django 2.0.1 on 2018-02-02 17:29

from django.db import migrations, models
import django_fsm


class Migration(migrations.Migration):

    dependencies = [
        ('billing', '0012_index_deleted_field'),
    ]

    operations = [
        migrations.AddField(
            model_name='invoice',
            name='due_date',
            field=models.DateField(default='2000-01-01'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='invoice',
            name='status',
            field=django_fsm.FSMField(choices=[('PENDING', 'Pending'), ('PAID', 'Paid'), ('CANCELLED', 'Cancelled')], db_index=True, default='PENDING', max_length=20),
        ),
    ]
