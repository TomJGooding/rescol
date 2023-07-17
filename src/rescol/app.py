from textual.app import App, ComposeResult
from textual.containers import Horizontal
from textual.widget import Widget
from textual.widgets import Static


class Band(Static):
    DEFAULT_CSS = """
    Band {
        height: 5;
        width: 3;
        background: black;
        margin: 0 2;
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

    Resistor #digit-bands {
        width: 24;
        margin: 0 2;
    }
    """

    def compose(self) -> ComposeResult:
        with Horizontal(id="digit-bands"):
            yield Band(id="digit-one")
            yield Band(id="digit-two")
            yield Band(id="multiplier")

        yield Band(id="tolerance")


class ResistorColorApp(App):
    CSS = """
    Screen {
        align: center middle;
    }
    """

    def compose(self) -> ComposeResult:
        yield Resistor()


if __name__ == "__main__":
    app = ResistorColorApp()
    app.run()
