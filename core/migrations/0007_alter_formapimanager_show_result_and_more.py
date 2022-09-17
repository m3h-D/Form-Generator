# Generated by Django 4.1.1 on 2022-09-17 06:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_formapimanager_show_result'),
    ]

    operations = [
        migrations.AlterField(
            model_name='formapimanager',
            name='show_result',
            field=models.BooleanField(default=False, verbose_name='Show Result'),
        ),
        migrations.AlterField(
            model_name='formdetail',
            name='form',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='detail', to='core.form', verbose_name='Form'),
        ),
    ]
