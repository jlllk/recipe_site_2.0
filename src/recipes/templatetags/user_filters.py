from django import template

register = template.Library()


@register.filter
def addclass(field, css):
    return field.as_widget(attrs={"class": css})


@register.filter
def addcheckboxclass(field, tag):
    return field.as_widget(attrs={"class": css})
