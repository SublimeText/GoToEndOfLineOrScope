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
        
        new_cursors = calculate_eol_positions(self.view, self.view.sel(), extend, before_whitespace, scope)
        self.set_cursors(new_cursors)

    def set_cursors(self, new_cursors):
        self.view.sel().clear()
        self.view.sel().add_all(new_cursors)
        self.view.show(new_cursors[0]) # scroll to show the first cursor, if it is not already visible

def calculate_eol_positions(view, cursors, extend, before_whitespace, before_scope):
    new_cursors = []
    for cursor in cursors:
        line = view.line(cursor.b) # NOTE: deliberate use of `cursor.a` and `cursor.b` everywhere and not `cursor.begin()` and `cursor.end()`
        
        eol_positions = set([
            line.end(), # hard eol
            next(get_logical_eol_positions(view, (cursor.b, ))) # soft eol
        ])
        
        relevant_token = get_previous_token_on_line_which_matches_selector(view, line.end(), before_scope)
        
        if relevant_token:
            before_scope_pos = relevant_token[0].begin()
            if before_whitespace:
                line_text_before_scope = view.substr(sublime.Region(line.begin(), before_scope_pos))
                rtrimmed = line_text_before_scope.rstrip()
                # check the entire line before the scope isn't whitespace
                if rtrimmed.strip() != '':
                    before_scope_pos -= len(line_text_before_scope) - len(rtrimmed)

            eol_positions.add(before_scope_pos)
        
        eol_positions = sorted(eol_positions)

        desired_end_pos = next((eol_pos for eol_pos in eol_positions if eol_pos > cursor.b), None)
        if not desired_end_pos: # no eol position was found after the caret position
            if len(eol_positions) > 1:
                desired_end_pos = eol_positions[-2] # jump back to the previous eol pos, i.e. before a comment starts
            else:
                desired_end_pos = cursor.b # keep the caret in the same position
        if extend:
             start_pos = cursor.a
        else:
            start_pos = desired_end_pos
        
        new_cursors.append(sublime.Region(start_pos, desired_end_pos))
    
    return new_cursors
