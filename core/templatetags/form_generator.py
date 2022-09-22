from django import template
from django.urls import reverse
from django.utils.safestring import mark_safe

from core.models import Form, Form


register = template.Library()


@register.inclusion_tag('core/tags/form_tag.html')
def render_form(form_id: int):
    return {'url': reverse('form_generator:form_detail', args=(form_id,))}


@register.simple_tag(takes_context=True)
def render_pre_api(context, form_id, api_id=None):
    try:
        form = Form.objects.filter_valid().get(id=form_id)
    except Form.DoesNotExist:
        return 'Form id is not valid'
    else:
        responses = form.render_pre_apis({'request': context['request']})
        if api_id:
            responses = mark_safe(next((result for api_id_, result in responses if api_id_ == api_id)))
        else:
            responses = mark_safe('<br>'.join([result for _, result in responses]))
        return responses


@register.simple_tag(takes_context=True)
def render_post_api(context, form_id, api_id=None):
    try:
        form = Form.objects.filter_valid().get(id=form_id)
    except Form.DoesNotExist:
        return 'Form id is not valid'
    else:
        responses = form.render_post_apis({'request': context['request']})
        if api_id:
            responses = mark_safe(next((result for api_id_, result in responses if api_id_ == api_id)))
        else:
            responses = mark_safe('<br>'.join([result for _, result in responses]))
        return responses