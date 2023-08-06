# Using example inspired on the github below: Thanks!
# https://github.com/nathanbigaignon/django-uikit-admin/blob/master/uikit_admin/templatetags/uikit_admin.py

from django import template
from django.forms.boundfield import BoundField
from django.utils.html import format_html

from django.forms.widgets import Select
from django.contrib.admin.widgets import RelatedFieldWidgetWrapper, AdminTextareaWidget

register = template.Library()


@register.simple_tag
def uka_form_row_stacked(element, errors='', extra_classes=''):
    label = BoundField.label_tag(element, "", {'class': 'uk-form-label'}, label_suffix='')
    
    if errors:
        extra_classes = f'{extra_classes} uk-form-danger uk-clearfix'
    
    help_text = f'<div class="uk-text-muted"><span uk-icon="icon: comment"></span> {element.help_text}</div>' \
        if element.help_text else ''
    
    # Trying to infer if I'm dealing with a select
    override_class = ''
    if issubclass(element.field.widget.__class__, Select):
        override_class = ' uk-select'
    
    if issubclass(element.field.widget.__class__, RelatedFieldWidgetWrapper):
        override_class = ' uk-select'
        
    if issubclass(element.field.widget.__class__, AdminTextareaWidget):
        override_class = ' uk-textarea'
    
    original_classes = element.field.widget.attrs.get('class', '')
    
    if element.field.__class__.__name__ in ['SplitDateTimeField', 'ReadOnlyPasswordHashField', 'ModelMultipleChoiceField']:
        element = element.as_widget()
    else:
        element = element.as_widget(attrs={'class': f'{original_classes} uk-input uk-margin-small-top uk-margin-small-bottom {extra_classes}{override_class}'})
    
    html_error = format_html(f'<div class="uk-text-danger uk-margin-top">{errors}</div>')
    
    html = format_html(f'<div class="uk-form-row"><div>{label} {html_error}</div>'
                       f'<div class="uk-form-controls">{element}{help_text}</div></div>')
    return html

@register.simple_tag
def uk_element (element, css_class_override=None):
    
    if css_class_override is not None:
        element = element.as_widget(attrs={'class': css_class_override })
    else:
        element = element.as_widget()
        
    return format_html(element)
    

@register.simple_tag
def uka_form_row_stacked_button(text, classes=None):  # @todo Fix this
    if classes is None:
        classes = ''
    html = format_html(f'<div class="uk-form-row"><div class="uk-form-controls"><button class="uk-button {classes}">{text}</button></div></div>')
    return html


@register.simple_tag
def uka_button(text, classes=None, type_name=None, name=None):
    if classes is None:
        classes = ''
    if type_name is None:
        type_name = ''
    if name is None:
        name = ''
    html = format_html(
        '<button class="uk-button {}" type="{}" name="{}">{}</button>',
        classes, type, name, text)
    return html


@register.filter(name='addcss')
def addcss(field, css):
    return field.as_widget(attrs={"class": css})