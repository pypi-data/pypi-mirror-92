# Generated by Django 2.2.12 on 2020-10-06 06:23

import uuid

import django.db.models.deletion
from django.db import (
    migrations,
    models,
)


class Migration(migrations.Migration):
    dependencies = [
        ('billing', '0017_new_djmoney'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='delinquent',
            field=models.BooleanField(db_index=True, default=False),
        ),
        migrations.CreateModel(
            name='EventLog',
            fields=[
                ('id', models.UUIDField(
                    default=uuid.uuid4,
                    editable=False,
                    primary_key=True,
                    serialize=False
                )),
                ('created', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('type', models.CharField(
                    choices=[
                        ('NEW_DELINQUENT', 'New delinquent'),
                        ('NEW_COMPLIANT', 'New compliant')
                    ],
                    max_length=20
                )),
                ('text', models.CharField(blank=True, max_length=255)),
                ('account', models.ForeignKey(
                    on_delete=django.db.models.deletion.PROTECT,
                    related_name='event_logs',
                    to='billing.Account'
                )),
            ],
            options={
                'verbose_name': 'event log',
                'verbose_name_plural': 'event logs',
            },
        ),
    ]
