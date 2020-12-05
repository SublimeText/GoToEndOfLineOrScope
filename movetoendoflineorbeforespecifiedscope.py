import sublime
import sublime_plugin
from itertools import takewhile
from .sublime_helper import get_previous_token_on_line_which_matches_selector, get_logical_eol_positions

class MoveToEndOfLineOrBeforeSpecifiedScopeCommand(sublime_plugin.TextCommand):
    def run(self, edit, **kwargs):
        if 'scope' not in kwargs:
            raise ValueError('scope not specified')
        extend = kwargs.get('extend', False)
        before_whitespace = kwargs.get('before_whitespace', False)
        scope = kwargs['scope']
        eol_first = kwargs.get('eol_first', 'auto')
        find_only_at_eol = kwargs.get('find_only_at_eol', True)
        
        new_cursors = calculate_eol_positions(self.view, self.view.sel(), extend, before_whitespace, scope, eol_first, find_only_at_eol)
        self.set_cursors(new_cursors)

    def set_cursors(self, new_cursors):
        self.view.sel().clear()
        self.view.sel().add_all(new_cursors)
        self.view.show(new_cursors[0]) # scroll to show the first cursor, if it is not already visible

def calculate_eol_positions(view, cursors, extend, before_whitespace, before_scope, eol_first, find_only_at_eol):
    new_cursors = []
    for cursor in cursors:
        line = view.line(cursor.b) # NOTE: deliberate use of `cursor.a` and `cursor.b` everywhere and not `cursor.begin()` and `cursor.end()`
        
        eol_positions = list(set([
            next(get_logical_eol_positions(view, (cursor.b, ))), # soft eol
            line.end(), # hard eol
        ]))
        
        relevant_token = get_previous_token_on_line_which_matches_selector(view, line.end() - (1 if line.size() > 0 else 0), before_scope, find_only_at_eol)
        
        if relevant_token:
            before_scope_pos = relevant_token[0].begin()
            if before_whitespace:
                line_text_before_scope = view.substr(sublime.Region(line.begin(), before_scope_pos))
                rtrimmed = line_text_before_scope.rstrip()
                # check the entire line before the scope isn't whitespace
                if rtrimmed.strip() != '':
                    before_scope_pos -= len(line_text_before_scope) - len(rtrimmed)

            eol_positions.append(before_scope_pos)

        if eol_first == 'auto':
            eol_first = len(eol_positions) < 3
        list_method = list if eol_first else sorted

        desired_end_pos = next((eol_pos for eol_pos in list_method(eol_positions) if eol_pos > cursor.b), None)
        if not desired_end_pos: # no eol position was found after the caret position
            if len(eol_positions) > 1:
                desired_end_pos = before_scope_pos # jump back to the previous eol pos, i.e. before a comment starts
            else:
                desired_end_pos = cursor.b # keep the caret in the same position
        if extend:
             start_pos = cursor.a
        else:
            start_pos = desired_end_pos
        
        new_cursors.append(sublime.Region(start_pos, desired_end_pos))
    
    return new_cursors
