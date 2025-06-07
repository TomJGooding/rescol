from __future__ import annotations

from enum import Enum

from textual import on
from textual.app import App, ComposeResult
from textual.containers import Center, Horizontal, VerticalGroup
from textual.reactive import var
from textual.widget import Widget
from textual.widgets import Input, Label, Select, Static


class ColorCode(Enum):
    BLACK = 0
    BROWN = 1
    RED = 2
    ORANGE = 3
    YELLOW = 4
    GREEN = 5
    BLUE = 6
    VIOLET = 7
    GREY = 8
    WHITE = 9


class BandSelect(Select):
    def __init__(
        self,
        *,
        name: str | None = None,
        id: str | None = None,
        classes: str | None = None,
        disabled: bool = False,
    ):
        options = [
            (f"{color_code.value} ({color_code.name.title()})", color_code)
            for color_code in ColorCode
        ]
        super().__init__(
            options,
            allow_blank=False,
            name=name,
            id=id,
            classes=classes,
            disabled=disabled,
        )


class BandSelects(Widget):
    DEFAULT_CSS = """
    BandSelects {
        width: auto;
        height: auto;
        layout: horizontal;
        margin: 1;

        & > VerticalGroup {
            width: 20;

            & > Label {
            text-style: bold;
            text-align: center;
            width: 100%;
            }
        }
    }
    """

    def compose(self) -> ComposeResult:
        for digit in ["First", "Second"]:
            with VerticalGroup():
                yield Label(f"{digit} digit")
                yield BandSelect()

        with VerticalGroup():
            yield Label("Number of zeros")
            yield BandSelect(classes="multiplier")


class Band(Static):
    DEFAULT_CSS = """
    Band {
        height: 5;
        width: 3;
        margin: 0 2;
    }
    """

    value = var(ColorCode.BLACK)

    def watch_value(self) -> None:
        self.styles.background = self.value.name.lower()


class ToleranceBand(Static):
    DEFAULT_CSS = """
    ToleranceBand {
        height: 5;
        width: 3;
        margin: 0 2;
        background: gold;
    }
    """


class Resistor(Widget):
    DEFAULT_CSS = """
    Resistor {
        layout: horizontal;
        height: 5;
        width: 35;
        background: #e1bc7b;
    }

    Resistor #value-bands {
        width: 24;
        margin: 0 2;
    }
    """

    def compose(self) -> ComposeResult:
        with Horizontal(id="value-bands"):
            yield Band(id="digit-one-band")
            yield Band(id="digit-two-band")
            yield Band(id="multiplier-band")
        yield ToleranceBand()


class ResistorValueDisplay(Widget):
    DEFAULT_CSS = """
    ResistorValueDisplay {
        height: auto;
        width: auto;
        margin: 1;
        layout: horizontal;
    }

    ResistorValueDisplay Input {
        width: 20;
    }

    ResistorValueDisplay Label {
        width: auto;
        height: 3;
        content-align: center middle;
        text-style: bold;
    }
    """

    value = var(0, init=False)

    def compose(self) -> ComposeResult:
        yield Input(str(self.value), disabled=True)
        yield Label("ohms")

    def watch_value(self) -> None:
        input = self.query_one(Input)
        input.value = str(self.value)


class ResistorColorCodeApp(App):
    CSS = """
    Screen {
        align: center middle;
    }
    """

    def compose(self) -> ComposeResult:
        with Center():
            yield BandSelects()
        with Center():
            yield Resistor()
        with Center():
            yield ResistorValueDisplay()

    @on(BandSelect.Changed)
    def on_band_select_changed(self) -> None:
        band_selects = self.query(BandSelect)
        bands = self.query(Band)

        value = 0
        multiplier = 0
        for band_select, band in zip(band_selects, bands):
            color_code = band_select.value
            assert isinstance(color_code, ColorCode)

            band.value = color_code

            if band_select.has_class("multiplier"):
                multiplier = 10**color_code.value
            else:
                value = value * 10 + color_code.value

        value *= multiplier

        resistance_input = self.query_one(ResistorValueDisplay)
        resistance_input.value = value


def run() -> None:
    app = ResistorColorCodeApp()
    app.run()
