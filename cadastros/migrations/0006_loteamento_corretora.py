# Generated by Django 3.2 on 2023-04-25 09:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cadastros', '0005_venda_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='loteamento',
            name='corretora',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='cadastros.corretora'),
        ),
    ]
