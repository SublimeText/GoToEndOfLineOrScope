def get_scopes(view, start_at_position, stop_at_position):
    """Return the unique scopes in the view between start_at_position and stop_at_position, in the order in which they occur."""
    current_scope = None
    step = 1
    if stop_at_position < start_at_position:
        step = -1
    for pos in range(start_at_position, stop_at_position, step):
        scope = view.scope_name(pos)
        if current_scope is None:
            current_scope = (scope, pos, pos)
        elif current_scope[0] == scope: # if the current scope is exactly the same, extend it
            current_scope = (current_scope[0], current_scope[1], pos) # NOTE: if step is -1, as opposed to 1, then current_scope[1] will be > current_scope[2]
        else: # the previous scope is complete, register new one
            yield current_scope
            current_scope = (scope, pos, pos)
    if current_scope is not None:
        yield current_scope
