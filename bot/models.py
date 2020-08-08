from django.db import models


class User(models.Model):
    name = models.TextField(verbose_name='Имя')

    def __str__(self):
        return f'№{self.pk} {self.name}'
    
    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class Message(models.Model):
    user = models.ForeignKey(
        to=User,
        verbose_name='Пользователь',
        on_delete=models.CASCADE
        )
    text = models.TextField(verbose_name='Сообщение')
    date_for_send = models.DateField(verbose_name='Время отправки')

    def __str__(self):
        return f'Сообщение {self.pk} от {self.user}'

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'
