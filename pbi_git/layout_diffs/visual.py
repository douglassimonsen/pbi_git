from typing import TYPE_CHECKING

from pbi_core.git.change_classes import ChangeType, VisualChange

from .filters import filter_diff

if TYPE_CHECKING:
    from pbi_core.static_files.layout.visual_container import VisualContainer


def visual_diff(parent_visual: "VisualContainer", child_visual: "VisualContainer") -> VisualChange:
    field_changes = {}
    for k in ["x", "y", "z", "width", "height", "tabOrder"]:
        parent_val = getattr(parent_visual, k, None)
        child_val = getattr(child_visual, k, None)
        if parent_val != child_val and not (parent_val is None and child_val is None):
            field_changes[k] = (parent_val, child_val)

    filter_changes = filter_diff(parent_visual.filters, child_visual.filters)  # type: ignore reportArgumentType
    change_type = ChangeType.UPDATED if field_changes or filter_changes else ChangeType.NO_CHANGE

    return VisualChange(
        id=parent_visual.pbi_core_id(),
        entity=parent_visual,
        change_type=change_type,
        field_changes=field_changes,
        filters=filter_changes,
    )
