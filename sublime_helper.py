import sublime

def get_previous_token_on_line_which_matches_selector(view, from_pos, selector, find_only_tokens_at_eol):
    line_begin = view.line(from_pos).begin()
    previous_token = None
    while from_pos >= line_begin:
        tokens = view.extract_tokens_with_scopes(sublime.Region(from_pos, from_pos))
        if not tokens:
            break
        for token in reversed(tokens):
            if sublime.score_selector(token[1], selector) == 0:
                if find_only_tokens_at_eol or previous_token:
                    return previous_token
                else:
                    continue
            previous_token = token
        from_pos = tokens[-1][0].begin() - 1
    return previous_token


def get_logical_eol_positions(view, positions):
    width, _ = view.layout_extent()
    for pos in positions:
        _, y = view.text_to_layout(pos)
        eol_pos = view.layout_to_text((width, y))
        yield eol_pos
