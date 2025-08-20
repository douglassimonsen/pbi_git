{% if visual.change_type != ChangeType.NO_CHANGE %}
### Visual: {{ visual.entity.pbi_core_name() }}

{{ visual.to_markdown() }}
{% endif %}
