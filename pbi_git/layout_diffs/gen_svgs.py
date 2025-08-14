from typing import TYPE_CHECKING
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
    elementname: str = "svg"

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


def embed_image(drawing: svgwrite.Drawing, svg_content: str) -> None:
    drawing.add()


def gen_svgs(section: "Section") -> None:
    assert section._layout is not None

    name = conv_name(section.name)
    name_index = [conv_name(s.name) for s in section._layout.sections].index(name)
    f_name = f"{name}.svg" if name_index == 0 else f"{name}_{name_index + 1}.svg"

    drawing = svgwrite.Drawing(f_name, profile="tiny", viewBox=f"0 0 {section.width} {section.height}")

    for visual in section.visualContainers:
        if visual.config.singleVisual is not None:
            viz_type = visual.config.singleVisual.visualType
            if viz_type in VISUAL_MAPPER:
                g = drawing.g()
                g.translate(visual.x, visual.y)
                e = Raw(SVGS[VISUAL_MAPPER[viz_type]], visual.width, visual.height)
                g.add(e)
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
    print("hi")
    exit()
