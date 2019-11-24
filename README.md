# GoToEndOfLineOrScope
Sublime Text plugin to move the cursor(s) to the end of the line, or to before the specified scope at the end of the line.

## Features

This plugin allows you to create key bindings that will:

- Go to the end of the line, or
- Go to the start of the specified scope that is at the end of the line

To explain:

You have a line like: `foo bar # I am a comment`
You want to bind the <kbd>End</kbd> key, so that when you press it, the cursor will either go to the end of the line or to just before the start of the comment marker, depending where the cursor is and your preferences.
i.e. `foo bar |# I am a comment`, `foo bar| # I am a comment` or `foo bar # I am a comment|` where `|` represents the cursor.

It works with multiple cursors, and each key binding can use a different scope, and a different order.  For example, you might want the cursor to go to the start of the comment after any whitespace, then to the end of the line. Or you might want the cursor to go to the end of the line, then to the start of the comment before any whitespace. At the same time, you might want a different key binding to jump the cursor to just before the semi-colon at the end of the line.

## Binding

The command is called `move_to_end_of_line_or_before_specified_scope`, and it accepts the following arguments:
- `scope` - the scope to move the cursor before, if it is at the end of the line
- `extend` - whether or not to extend the selection
- `eol_first` - whether or not the cursor should go to the end of the line first or the beginning of the specified scope. Note that with word wrapped lines, as this plugin emulates the default <kbd>End</kbd> key behavior of going to hard EOL when at a soft EOL, setting this argument to `true` with word wrap enabled will make the command act like the default `move_to { "to": "eol" }` command. Suggestions for how to improve this behavior is welcome. For now, you can use `auto` which is equivalent to `true` if `word_wrap` is off or the line is unwrapped, and `false` if `word_wrap` is enabled. This is perhaps not ideal because the cursor location isn't consistent, hence the request for suggestions. Going to EOL first is the preferred default because it is easier for muscle memory to press it twice to get to the start of a comment than to press it once, expecting to be at EOL and finding oneself at a comment. It may be useful to get into the habit of pressing <kbd>Ctrl+Enter</kbd> instead of <kbd>End</kbd> followed by <kbd>Enter</kbd> to get a new line below the current one, then perhaps a more sane default would be `false`...
- `before_whitespace` - whether or not the cursor should go to the beginning of any whitespace that occurs immediately before the specified scope
