# Generated by Django 2.2.4 on 2019-08-25 10:16

from django.db import migrations
import django.db.models.deletion
import isc_common.fields.related


class Migration(migrations.Migration):

    dependencies = [
        ('clndr', '0058_auto_20190825_1015'),
    ]

    operations = [
        migrations.AlterField(
            model_name='calendar_shifts_days',
            name='saturday',
            field=isc_common.fields.related.ForeignKeyCascade(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='saturday_rel', to='clndr.Shift_day'),
        ),
    ]
