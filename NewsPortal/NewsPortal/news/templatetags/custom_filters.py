from django import template


register = template.Library()


@register.filter(name='censor')
def censor(value):
    list = ['екалэмэнэ',
            'дурак',
            'фиг']

    if isinstance(value, str):
        for i in list:
            for j in value:
                if j == i:
                    j = "***"
        return str(value)
    else:
        raise ValueError(f' {type(value)} не является строкой')
