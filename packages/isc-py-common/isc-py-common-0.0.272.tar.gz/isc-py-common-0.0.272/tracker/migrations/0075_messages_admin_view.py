# Generated by Django 2.2.6 on 2019-10-19 19:08

from django.db import migrations, models
import django.utils.timezone
import isc_common.fields.description_field


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0074_messagesthemeusersaccess_props'),
    ]

    operations = [
        migrations.CreateModel(
            name='Messages_admin_view',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False, verbose_name='Идентификатор')),
                ('deleted_at', models.DateTimeField(blank=True, db_index=True, null=True, verbose_name='Дата мягкого удаления')),
                ('editing', models.BooleanField(default=True, verbose_name='Возможность редактирования')),
                ('deliting', models.BooleanField(default=True, verbose_name='Возможность удаления')),
                ('lastmodified', models.DateTimeField(db_index=True, default=django.utils.timezone.now, editable=False, verbose_name='Последнее обновление')),
                ('guid', models.UUIDField(blank=True, null=True)),
                ('date_create', models.DateTimeField(db_index=True, default=django.utils.timezone.now, verbose_name='Дата записи')),
                ('isFolder', models.BooleanField(default=False)),
                ('message', isc_common.fields.description_field.DescriptionField(verbose_name='Тело задач')),
            ],
            options={
                'verbose_name': 'Сообщения',
                'db_table': 'tracker_messages_admin_view',
                'managed': False,
            },
        ),
    ]
