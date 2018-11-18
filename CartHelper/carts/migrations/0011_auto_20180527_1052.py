# Generated by Django 2.0.1 on 2018-05-27 16:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('carts', '0010_auto_20180527_1049'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='fault',
            options={'ordering': ['hour']},
        ),
        migrations.AddField(
            model_name='fault',
            name='cart',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='carts.Cart'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='fault',
            name='code',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='datacollection',
            name='name',
            field=models.CharField(default='2018-05-27 10:50:45', max_length=30),
        ),
    ]
