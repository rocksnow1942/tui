import prompt_toolkit as pt
from prompt_toolkit import print_formatted_text as pft
from prompt_toolkit import lexers
import prompt_toolkit.validation as ptv
import prompt_toolkit.completion as ptc
import prompt_toolkit.document as ptd
import prompt_toolkit.auto_suggest as pta
import prompt_toolkit.styles as pts
import prompt_toolkit.shortcuts as ptsct
import prompt_toolkit.buffer as ptb
from prompt_toolkit.layout import containers, layout, controls, menus
import prompt_toolkit.layout as pt_layout
import prompt_toolkit.key_binding as ptkb
import prompt_toolkit.formatted_text as ptf
from prompt_toolkit import widgets
import prompt_toolkit.key_binding.bindings.focus as kb_focus
import prompt_toolkit.filters as pt_filter
from prompt_toolkit import styles

STYLE = styles.Style.from_dict(
    {
        "window.border": "#888888",
        "shadow": "bg:#222222",
        "menu-bar": "bg:#aaaaaa #888888",
        "menu-bar.selected-item": "bg:#ffffff #000000",
        "menu": "bg:#888888 #ffffff",
        "menu.border": "#aaaaaa",
        "window.border shadow": "#444444",
        "focused  button": "bg:#880000 #ffffff noinherit",
        # Styling for Dialog widgets.
        "button-bar": "bg:#aaaaff",
    }
)


def main() -> None:
    command_text = [f"command - {i}" for i in range(100)]
    command_completer = ptc.WordCompleter(command_text)
    commands = [widgets.Checkbox(text=t) for t in command_text]
    search_input = widgets.TextArea(
        height=1,
        prompt="> ",
        multiline=False,
        completer=command_completer,
        focus_on_click=True,
    )

    input_area = containers.VSplit(
        [
            # widgets.Label(text=">", width=16),
            search_input,
        ],
    )
    command_area = containers.VSplit(
        [
            widgets.Frame(
                title="Commands",
                body=pt_layout.ScrollablePane(containers.HSplit(commands)),
                width=pt_layout.Dimension(weight=1),
            ),
            widgets.Frame(
                title="Command Doc",
                body=widgets.Label(
                    text="Tab to navigate to a command to show help doc."
                ),
                width=pt_layout.Dimension(weight=1),
            ),
        ],
    )

    def handle_search(buffer: ptb.Buffer) -> bool:
        """Handle search input."""
        query = buffer.text
        # For simplicity, we just filter commands that contain the query.
        return True

    search_input.accept_handler = handle_search

    button_area = widgets.Box(
        containers.VSplit(
            [
                widgets.Button(
                    text="Select All",
                    handler=lambda: None,
                    width=16,
                    left_symbol="[",
                    right_symbol="]",
                ),
                widgets.Button(
                    text="Run Selected",
                    handler=lambda: None,
                    width=16,
                    left_symbol="[",
                    right_symbol="]",
                ),
                widgets.Button(
                    text="Add Favorite",
                    handler=lambda: None,
                    width=16,
                    left_symbol="[",
                    right_symbol="]",
                ),
            ],
            align=pt_layout.HorizontalAlign.CENTER,
            padding=3,
        ),
        height=3,
        style="class:button-bar",
    )

    root_container = containers.FloatContainer(
        content=containers.HSplit(
            [
                widgets.Label(
                    # ASCII art of INCUR
                    text=r"""
          ((`\          |   Type to search for command.      
       ___ \\ '--._     |   Select the filtered command by click or space.
    .'`   `'    o  )    |   Click Run or press Shift + Enter to execute.
   /    \   '. __.'     |   Press Ctrl-C to exit.
  _|    /_  \ \_\_      |   Press tab or shift + tab to navigate.
 {_\______\-'\__\_\     |     
"""
                ),
                widgets.Frame(title="Search [keybinding: s]", body=input_area),
                command_area,
                button_area,
            ],
        ),
        floats=[
            containers.Float(
                content=menus.CompletionsMenu(max_height=36, scroll_offset=1),
                xcursor=True,
                ycursor=True,
            )
        ],
    )
    root_layout = layout.Layout(container=root_container, focused_element=input_area)

    # Global key bindings.
    bindings = ptkb.KeyBindings()
    bindings.add("tab")(kb_focus.focus_next)
    bindings.add("s-tab")(kb_focus.focus_previous)
    bindings.add("c-c")(lambda event: event.app.exit())

    @bindings.add("s", filter=~pt_filter.has_focus(input_area))
    def _(event: ptkb.KeyPressEvent) -> None:
        """Focus the search input."""
        event.app.layout.focus(input_area)

    # conditional_bindings = ptkb.ConditionalKeyBindings(
    #     ptkb.KeyBindings(), filter=filter_input_focused
    # )

    result: str = pt.Application(
        layout=root_layout,
        key_bindings=bindings,
        full_screen=True,
        mouse_support=True,
        style=STYLE,
    ).run()
    pft(pt.HTML(f"You entered: <ansigreen>{result}</ansigreen>"))


if __name__ == "__main__":
    main()
