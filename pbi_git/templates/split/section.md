{% if section.change_type != ChangeType.NO_CHANGE %}
## Section: {{ section.entity.displayName }}

{{ section.to_markdown() }}

{% endif  %}
