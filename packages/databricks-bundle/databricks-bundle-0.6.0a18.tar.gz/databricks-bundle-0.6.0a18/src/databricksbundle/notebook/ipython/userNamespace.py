def getValue(key):
    import IPython  # pylint: disable = import-error, import-outside-toplevel
    return IPython.get_ipython().user_ns[key]

def setValue(key, val):
    import IPython  # pylint: disable = import-error, import-outside-toplevel
    IPython.get_ipython().user_ns[key] = val
