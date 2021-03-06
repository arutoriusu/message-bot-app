# Generated by Django 3.0.4 on 2020-08-07 05:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField(verbose_name='Имя')),
            ],
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(verbose_name='Сообщение')),
                ('date_for_send', models.DateField(verbose_name='Время отправки')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bot.User', verbose_name='Пользователь')),
            ],
        ),
    ]
