from django.db import models


class Menu(models.Model):
    name = models.CharField(
        max_length=100,
        verbose_name='name'
    )

    class Meta:
        verbose_name = 'Menu'
        verbose_name_plural = 'Menus'

    def __str__(self):
        return self.name


class MenuItem(models.Model):
    menu = models.ForeignKey(
        Menu,
        related_name='items',
        verbose_name='menu',
        on_delete=models.CASCADE
    )
    parent = models.ForeignKey(
        'self',
        verbose_name='parent',
        related_name='child',
        blank=True, null=True,
        on_delete=models.PROTECT

    )
    name = models.CharField(
        max_length=100,
        verbose_name='name'
    )
    url = models.URLField(
        verbose_name='url'
    )

    class Meta:
        verbose_name = 'Menu item'
        verbose_name_plural = 'Menu items'

    def __str__(self):
        return self.name
