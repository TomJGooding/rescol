from __future__ import annotations

from enum import Enum

from textual import on
from textual.app import App, ComposeResult
from textual.containers import Center, Horizontal, Vertical
from textual.message import Message
from textual.reactive import reactive
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


class BandSelects(Widget):
    DEFAULT_CSS = """
    BandSelects {
        width: auto;
        height: auto;
        layout: horizontal;
        margin: 1;
    }

    BandSelects Vertical {
        width: 22;
        height: auto;
    }

    BandSelects Label {
        text-style: bold;
        text-align: center;
        width: 100%;
    }

    BandSelects SelectOverlay {
        max-height: 12;
    }
    """

    def compose(self) -> ComposeResult:
        digit_options = [
            (f"{color_code.value} ({color_code.name.title()})", color_code)
            for color_code in ColorCode
        ]

        superscripts = ["⁰", "¹", "²", "³", "⁴", "⁵", "⁶", "⁷", "⁸", "⁹"]
        multiplier_options = [
            (
                f"x10{superscripts[color_code.value]} ({color_code.name.title()})",
                color_code,
            )
            for color_code in ColorCode
        ]

        with Vertical():
            yield Label("First Digit")
            yield Select(
                digit_options,
                id="digit-one-select",
                allow_blank=False,
            )
        with Vertical():
            yield Label("Second Digit")
            yield Select(
                digit_options,
                id="digit-two-select",
                allow_blank=False,
            )
        with Vertical():
            yield Label("Multiplier")
            yield Select(
                multiplier_options,
                id="multiplier-select",
                allow_blank=False,
            )


class Band(Static):
    DEFAULT_CSS = """
    Band {
        height: 5;
        width: 3;
        margin: 0 2;
    }
    """

    value = reactive(ColorCode.BLACK)

    class Changed(Message):
        def __init__(self, band: Band, value: ColorCode) -> None:
            super().__init__()
            self.value: ColorCode = value
            self.band: Band = band

        @property
        def control(self) -> Band:
            return self.band

    def watch_value(self, value: ColorCode) -> None:
        self.styles.background = self.value.name.lower()
        self.post_message(self.Changed(self, value))


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
        height: 5;
        width: 35;
        background: #e1bc7b;
        layout: horizontal;
    }

    Resistor #value-bands {
        width: 24;
        margin: 0 2;
    }
    """

    value = reactive(0)
    digit_one = reactive(0)
    digit_two = reactive(0)
    multiplier = reactive(pow(10, 0))

    class Changed(Message):
        def __init__(self, resistor: Resistor, value: int) -> None:
            super().__init__()
            self.value: int = value
            self.resistor: Resistor = resistor

        @property
        def control(self) -> Resistor:
            return self.resistor

    def compose(self) -> ComposeResult:
        with Horizontal(id="value-bands"):
            yield Band(id="digit-one-band")
            yield Band(id="digit-two-band")
            yield Band(id="multiplier-band")
        yield ToleranceBand()

    def compute_value(self) -> int:
        number = (self.digit_one * 10) + self.digit_two
        return number * self.multiplier

    def watch_value(self, value: int) -> None:
        self.post_message(self.Changed(self, value))

    @on(Band.Changed)
    def on_band_changed(self, event: Band.Changed) -> None:
        color_code = event.value
        assert isinstance(color_code, ColorCode)

        if event.band.id == "digit-one-band":
            self.digit_one = color_code.value
        elif event.band.id == "digit-two-band":
            self.digit_two = color_code.value
        elif event.band.id == "multiplier-band":
            self.multiplier = pow(10, int(color_code.value))
        else:
            raise NotImplementedError()


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

    value = reactive(0, init=False)

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

    @on(Select.Changed)
    def on_band_select_changed(self, event: Select.Changed) -> None:
        color_code = event.value
        assert isinstance(color_code, ColorCode)

        if event.select.id == "digit-one-select":
            band = self.query_one("#digit-one-band", Band)
            band.value = color_code
        elif event.select.id == "digit-two-select":
            band = self.query_one("#digit-two-band", Band)
            band.value = color_code
        elif event.select.id == "multiplier-select":
            band = self.query_one("#multiplier-band", Band)
            band.value = color_code
        else:
            raise NotImplementedError()

    @on(Resistor.Changed)
    def on_resistor_changed(self, event: Resistor.Changed) -> None:
        value_label = self.query_one(ResistorValueDisplay)
        value_label.value = event.value


def run() -> None:
    app = ResistorColorCodeApp()
    app.run()
