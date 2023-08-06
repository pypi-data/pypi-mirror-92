from django.utils.html import mark_safe

def url_to_html_img(url, height=50):
    return mark_safe(f'<img height="{height}px" src="{url}" />')