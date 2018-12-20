# -*- encoding:utf8 -*-
from django import forms
from mdeditor.fields import MDTextFormField


# mdedtior富文本编辑器的前端form表单
class MDEditorForm(forms.Form):
    content = MDTextFormField(config_name='form_config')



