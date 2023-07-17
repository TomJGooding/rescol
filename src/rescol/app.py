from enum import Enum

from textual import on
from textual.app import App, ComposeResult
from textual.containers import Center, Vertical
from textual.reactive import reactive
from textual.widget import Widget
from textual.widgets import Label, Select, Static


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

    color_code = reactive(ColorCode.BLACK)

    def watch_color_code(self) -> None:
        self.styles.background = self.color_code.name.lower()


class ValueBands(Widget):
    DEFAULT_CSS = """
    ValueBands {
        height: 5;
        width: 24;
        layout: horizontal;
        margin: 0 2;
    }
    """

    def compose(self) -> ComposeResult:
        yield Band(id="digit-one-band")
        yield Band(id="digit-two-band")
        yield Band(id="multiplier-band")


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
    """

    def compose(self) -> ComposeResult:
        yield ValueBands()
        yield ToleranceBand()


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

    @on(Select.Changed)
    def on_band_select_changed(self, event: Select.Changed) -> None:
        color_code = event.value
        assert isinstance(color_code, ColorCode)

        if event.select.id == "digit-one-select":
            band = self.query_one("#digit-one-band", Band)
            band.color_code = color_code
        elif event.select.id == "digit-two-select":
            band = self.query_one("#digit-two-band", Band)
            band.color_code = color_code
        elif event.select.id == "multiplier-select":
            band = self.query_one("#multiplier-band", Band)
            band.color_code = color_code
        else:
            raise NotImplementedError()


if __name__ == "__main__":
    app = ResistorColorCodeApp()
    app.run()
