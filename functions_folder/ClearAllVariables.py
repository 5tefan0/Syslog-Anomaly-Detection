#------------------------------------------------------------------------------#
# Clears the variables space from the workspace
#------------------------------------------------------------------------------#
def clear_all():
    """Clears all the variables from the workspace of the spyder application."""
    gl = globals().copy()
    for var in gl:
        if var[0] == '_': continue
        if 'func' in str(globals()[var]): continue
        if 'module' in str(globals()[var]): continue

        del globals()[var]
    print("ClearAllVariables() was called")
#------------------------------------------------------------------------------#
