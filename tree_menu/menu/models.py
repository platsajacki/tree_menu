from django.db import models


class Menu(models.Model):
    """Модель для хранения информации о меню."""
    name = models.CharField(
        max_length=100,
        verbose_name='name'
    )

    class Meta:
        verbose_name = 'Menu'
        verbose_name_plural = 'Menus'

    def __str__(self) -> str:
        """Строковое представление наименования меню."""
        return self.name


class MenuItem(models.Model):
    """Модель для хранения информации о пунктах меню."""
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

    def __str__(self) -> str:
        """Строковое представление наименования пункта меню."""
        return self.name
