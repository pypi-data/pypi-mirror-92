# -*- coding: utf-8 -*-
"""
    :copyright: 2020, ExonLabs. All rights reserved.
    :license: BSD, see LICENSE for more details.
"""
import json
from . import UiBaseMacro

__all__ = []


class UiFormsMacro(UiBaseMacro):
    root_path = 'webui/macros/forms'


class UiInputForm(UiFormsMacro):
    tpl_name = 'inputform.tpl'

    def __new__(cls, options, styles=''):
        fields = []
        for i, k in enumerate(options.get('fields', [])):
            fields.append({
                'type': k.get('type', 'text'),
                'label': k.get('label', 'Field %s' % (i + 1)),
                'name': k.get('name', 'field_%s' % i),
                'value': k.get('value', ''),
                'default': k.get('default', ''),
                'format': k.get('format', ''),
                'options': k.get('options', []),
                'multiple': k.get('multiple', False),
                'rows': k.get('rows', 4),
                'maxsize': k.get('maxsize', 0),
                'placeholder': k.get('placeholder', k.get('label', '')),
                'required': k.get('required', False),
                'confirm': k.get('confirm', False),
                'strength': k.get('strength', False),
                'help': k.get('help', ''),
                'helpguide': k.get('helpguide', ''),
                'prepend': k.get('prepend', []),
                'append': k.get('append', []),
            })
        return cls.tpl(**{
            'id': options.get('form_id', cls.randint()),
            'submit_url': options.get('submit_url', ''),
            'fields': fields,
            'styles': styles,
        })


class UiQBuilder(UiFormsMacro):
    tpl_name = 'qbuilder.tpl'

    def __new__(cls, options, styles=''):
        filters = []
        for k in options.get('filters', []):
            filters.append(json.dumps({
                'id': k['id'],
                'label': k['label'],
                'type': k.get('type', 'string'),
                'input': k.get('input', 'text'),
                'operators': k.get('operators', None),
                'values': k.get('values', None),
                'default_value': k.get('default', None),
                'size': k.get('maxsize', None),
                'rows': k.get('rows', 3),
                'multiple': k.get('multiple', False),
                'validation': k.get('validation', None),
            }))
        return cls.tpl(**{
            'id': options.get('form_id', cls.randint()),
            'filters': ','.join(filters),
            'rules': json.dumps(options.get('initial_rules', None)),
            'allow_groups': options.get('allow_groups', '1'),
            'allow_empty': options.get('allow_empty', 'true'),
            'default_condition': options.get('default_condition', 'AND'),
            'inputs_separator': options.get('inputs_separator', ','),
            'styles': styles,
        })


class UiLoginForm(UiFormsMacro):
    tpl_name = 'loginform.tpl'

    def __new__(cls, options, styles=''):
        return cls.tpl(**{
            'id': options.get('form_id', cls.randint()),
            'submit_url': options.get('submit_url', ''),
            'authkey': options.get('authkey', ''),
            'btn_style': options.get('btn_style', 'btn-primary'),
            'styles': styles,
        })
