import sublime
import sublime_plugin
from itertools import takewhile
from .sublime_helper import get_scopes

class MoveToEndOfLineOrBeforeSpecifiedScopeCommand(sublime_plugin.TextCommand):
    def run(self, edit, **kwargs):
        if 'scope' not in kwargs:
            raise ValueError('scope not specified')
        extend = kwargs.get('extend', False)
        before_whitespace = kwargs.get('before_whitespace', False)
        
        new_cursors = []
        for cursor in self.view.sel():
            line = self.view.line(cursor.b) # NOTE: deliberate use of `cursor.a` and `cursor.b` everywhere and not `cursor.begin()` and `cursor.end()`
            
            check_scope = line.end() == cursor.b and (extend or cursor.empty()) # if the cursor is at the end of the line, check the scope at the end of the line
            if not check_scope: # if the cursor is not at the end of the line
                check_scope = not kwargs.get('eol_first', True) # check the scope at the end of the line if the preference is to go to the scope first, then the eol
            
            desired_end_pos = line.end() # defaultly use default end of line behavior
            if check_scope:
                if self.view.match_selector(line.end() - 1, kwargs['scope']): # if the last character on the line contains the desired scope
                    relevant_scope_matches = list(takewhile(lambda scope: kwargs['scope'] in scope[0], get_scopes(self.view, line.end() - 1, line.begin()))) # work backwards from the end of the line while the scope matches
                    scope_begin = sublime.Region(relevant_scope_matches[-1][1], relevant_scope_matches[-1][2]).begin()
                    
                    if before_whitespace:
                        line_text_before_scope = self.view.substr(sublime.Region(line.begin(), scope_begin))
                        rtrimmed = line_text_before_scope.rstrip()
                        # check the entire line before the scope isn't whitespace
                        if rtrimmed.strip() != '':
                            scope_begin -= len(line_text_before_scope) - len(rtrimmed)
                    
                    if scope_begin != cursor.b: # if the cursor is not already at the character that represents the start of the desired scope
                        desired_end_pos = scope_begin # move the cursor to the start of the desired scope
            
            start_pos = desired_end_pos
            if extend:
                start_pos = cursor.a
            
            new_cursors.append(sublime.Region(start_pos, desired_end_pos))
        
        self.set_cursors(new_cursors)
    
    def set_cursors(self, new_cursors):
        self.view.sel().clear()
        self.view.sel().add_all(new_cursors)
        self.view.show(new_cursors[0]) # scroll to show the first cursor, if it is not already visible
