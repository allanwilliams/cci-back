# Generated by Django 3.2 on 2023-04-24 19:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cadastros', '0003_auto_20230424_1637'),
    ]

    operations = [
        migrations.RenameField(
            model_name='contatocliente',
            old_name='rg',
            new_name='contato',
        ),
    ]
