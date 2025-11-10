"""Having fun with prompt_toolkit!"""

from curses.panel import bottom_panel
import prompt_toolkit as pt
from prompt_toolkit import print_formatted_text as pft
import prompt_toolkit.lexers as ptl
import pygments.lexers.python as plp
import prompt_toolkit.validation as ptv
import prompt_toolkit.completion as ptc
import prompt_toolkit.document as ptd
import prompt_toolkit.auto_suggest as pta
import prompt_toolkit.styles as pts
import prompt_toolkit.shortcuts as ptsct
import prompt_toolkit.buffer as ptb
from prompt_toolkit.layout import containers, layout, controls
import prompt_toolkit.key_binding as ptkb
import prompt_toolkit.formatted_text as ptf


def word_complete() -> None:
    completer = ptc.WordCompleter(["apple", "banana", "grape", "orange", "pear"])
    text = pt.prompt("Enter a fruit: ", completer=completer)
    pft(pt.HTML(f"You selected: <ansigreen>{text}</ansigreen>"))
    pft(ptsct.progress_bar.formatters.SpinningWheel())


def nested_complete() -> None:
    completer = ptc.NestedCompleter.from_nested_dict(
        {
            "fruit": {"apple": None, "banana": None, "grape": None},
            "vegetable": {"carrot": None, "broccoli": None, "spinach": None},
        }
    )
    text = pt.prompt("Select a category and item: ", completer=completer)
    pft(pt.HTML(f"You selected: <ansigreen>{text}</ansigreen>"))


def custom_complete() -> None:
    class CustomCompleter(ptc.Completer):
        def get_completions(self, document, complete_event):
            word = document.get_word_before_cursor()
            yield ptc.Completion(
                "completion1",
                start_position=-len(word),
                style="bg:ansiyellow fg:ansiblack",
            )

            # Underline completion.
            yield ptc.Completion(
                "completion2", start_position=-len(word), style="underline"
            )

            # Specify class name, which will be looked up in the style sheet.
            yield ptc.Completion(
                "completion3",
                start_position=-len(word),
                display=pt.HTML(
                    "<ansired>completion</ansired> <b><ansigreen>3</ansigreen></b>"
                ),
            )

    class CustomValidator(ptv.Validator):
        def validate(self, document: ptd.Document) -> None:
            text = document.text
            if "completion" not in text:
                raise ptv.ValidationError(
                    message="Input must contain the word 'completion'",
                    cursor_position=len(text),
                )

    completer = CustomCompleter()
    text = pt.prompt(
        "Enter something: ",
        completer=ptc.FuzzyCompleter(completer),
        complete_while_typing=None,
        validator=CustomValidator(),
    )
    pft(pt.HTML(f"You entered: <ansigreen>{text}</ansigreen>"))


def prompt_session() -> None:
    session: pt.PromptSession = pt.PromptSession()
    style = pts.Style.from_dict(
        {
            "frame.border": "ansiblue",
        }
    )
    while True:
        text = session.prompt(
            "Session prompt: ",
            auto_suggest=pta.AutoSuggestFromHistory(),
            bottom_toolbar=lambda: pt.HTML(
                "Press <b><ansired>Ctrl-C</ansired></b> to exit."
            ),
            # vi_mode=True,
            show_frame=True,
            style=style,
        )
        pft(pt.HTML(f"You entered: <ansigreen>{text}</ansigreen>"))


def dialog_prompt() -> None:
    result = ptsct.choice(
        message="Select your favorite fruit:",
        options=[
            ("apple", "Apple"),
            ("banana", "Banana"),
            ("cherry", "Cherry"),
        ],
    )
    pft(pt.HTML(f"You selected: <ansigreen>{result}</ansigreen>"))

    ptsct.message_dialog(
        title="Selection Complete",
        text=f"You selected: {result}",
    ).run()

    text = ptsct.input_dialog(
        title="Enter your name", text="Please enter your name:"
    ).run()
    pft(pt.HTML(f"Hello, <ansigreen>{text}</ansigreen>!"))

    result = ptsct.radiolist_dialog(
        title="RadioList dialog",
        text="Which breakfast would you like ?",
        values=[
            ("breakfast1", "Eggs and beacon"),
            ("breakfast2", "French breakfast"),
            ("breakfast3", "Equestrian breakfast"),
        ],
    ).run()
    pft(pt.HTML(f"You selected: <ansigreen>{result}</ansigreen>"))

    results_array = ptsct.checkboxlist_dialog(
        title="CheckboxList dialog",
        text="What would you like in your breakfast ?",
        values=[
            ("eggs", "Eggs"),
            ("bacon", "Bacon"),
            ("croissants", "20 Croissants"),
            ("daily", "The breakfast of the day"),
        ],
    ).run()

    pft(pt.HTML(f"You selected: <ansigreen>{results_array}</ansigreen>"))


def app() -> None:
    kb = ptkb.KeyBindings()

    @kb.add("c-c")
    def _(event: ptkb.KeyPressEvent) -> None:
        """Exit the application."""
        event.app.exit()

    buf = ptb.Buffer()
    root_container = containers.VSplit(
        [
            containers.Window(content=controls.BufferControl(buffer=buf)),
            containers.Window(
                width=1,
                char="\u2502",
                style="class:line",
            ),
            containers.Window(
                content=controls.FormattedTextControl(text="Hello world!")
            ),
        ]
    )
    layout_ = layout.Layout(root_container)

    app: pt.Application = pt.Application(
        layout=layout_, full_screen=True, key_bindings=kb
    )
    app.run()


def main() -> None:
    """Main function to run prompt_toolkit demos."""
    word_complete()
    # nested_complete()
    # custom_complete()
    # prompt_session()
    # dialog_prompt()
    # app()


if __name__ == "__main__":
    main()
