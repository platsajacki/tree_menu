from typing import Any

from django.db.models import QuerySet
from django.shortcuts import get_object_or_404
from django.template import Library
from django.utils.safestring import mark_safe, SafeText

from ..models import Menu, MenuItem

register: Library = Library()


def is_item_in_branch(menu_item: MenuItem, branch_root: MenuItem) -> bool:
    """
    Проверяет, существует ли пункт меню внутри ветки,
    начиная с определенного пункта или начала ветки.
    """
    if menu_item == branch_root:
        return True
    if menu_item.parent is None:
        return False
    return is_item_in_branch(menu_item.parent, branch_root)


def get_html_code_menu(
        items_menu: QuerySet, active_item: MenuItem,
        parent_item: None | MenuItem = None
) -> str:
    """Рекурсивно генерирует HTML-код меню."""
    main_branch: MenuItem | None = None
    menu_html: str = '<menu>'
    for item in items_menu.filter(parent=parent_item):
        is_active: bool = item == active_item
        class_active: str = ' class="active"' if is_active else ''
        menu_html += (
            f'<li{class_active}><a href="{item.url}">{item.name}</a></li>'
        )
        if not parent_item and is_item_in_branch(active_item, item):
            main_branch = item
        if is_active:
            menu_html += '<menu>'
            for child in item.child.all():
                menu_html += (
                    f'<li><a href="{child.url}">{child.name}</a></li>'
                )
            menu_html += '</menu>'
            continue
        if is_item_in_branch(active_item, item):
            menu_html += get_html_code_menu(
                items_menu, active_item, parent_item=item
            )
        if (
            not is_item_in_branch(active_item, item)
            and is_item_in_branch(item, main_branch)
        ):
            menu_html += f'<li><a href="{item.url}">{item.name}</a></li>'
    menu_html += '</menu>'
    return menu_html


@register.simple_tag(takes_context=True)
def draw_menu(context: dict[str, Any], name_menu: str) -> SafeText:
    """Данная функция генерирует HTML-представление меню."""
    absolute_url: str = context['request'].build_absolute_uri()
    items_menu: list[MenuItem] = get_object_or_404(
        Menu,
        name=name_menu
    ).items.all()
    active_item = items_menu.filter(url=absolute_url).first()
    return mark_safe(get_html_code_menu(items_menu, active_item))
