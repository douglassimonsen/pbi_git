from typing import TYPE_CHECKING, Literal
from xml.etree import ElementTree as ET  # noqa: S405

import svgwrite
import svgwrite.shapes

if TYPE_CHECKING:
    from pbi_core.static_files.layout.section import Section
from pathlib import Path

SVGS: dict[str, str] = {f.stem: f.read_text() for f in (Path(__file__).parents[1] / "svgs").glob("*.svg")}
VISUAL_MAPPER = {
    "textbox": "text_box",
    "card": "card",
    "map": "map",
    "clusteredColumnChart": "bar",
    "pieChart": "pie",
    "scatterChart": "scatter",
}


class Raw:
    elementname: str = "rect"  # needed to pass validation

    def __init__(self, text: str, width: float, height: float) -> None:
        self.text = text
        self.width = width
        self.height = height

    def get_xml(self) -> ET.Element:
        ret = ET.fromstring(self.text)  # noqa: S314
        ret.set("width", str(self.width))
        ret.set("height", str(self.height))
        ret.set("preserveAspectRatio", "none")
        return ret


def conv_name(x: str) -> str:
    return x.lower().replace(" ", "_")


def gen_svgs(section: "Section", changed_ids: set[str], suffix: Literal["old", "new"]) -> str:
    assert section._layout is not None

    update_layer = "_deleted" if suffix == "old" else "_added"

    svg_path = (Path(__file__).parent / "test.svg").absolute()
    drawing = svgwrite.Drawing(
        svg_path.absolute().as_posix().replace("\\", "/"),
        profile="tiny",
        viewBox=f"0 0 {section.width} {section.height}",
    )

    for visual in section.visualContainers:
        if visual.config.singleVisual is not None:
            viz_type = visual.config.singleVisual.visualType
            if viz_type in VISUAL_MAPPER:
                g = drawing.g()
                g.translate(visual.x, visual.y)
                g.add(Raw(SVGS[VISUAL_MAPPER[viz_type]], visual.width, visual.height))
                if visual.name() in changed_ids:
                    g.add(Raw(SVGS[update_layer], visual.width, visual.height))
                drawing.add(g)
                continue

        drawing.add(
            svgwrite.shapes.Rect(
                insert=(visual.x, visual.y),
                size=(visual.width, visual.height),
                fill="red",
                stroke="black",
                stroke_width=1,
            ),
        )

    drawing.save()

    data = svg_path.read_text(encoding="utf-8")
    svg_path.unlink()
    return data
