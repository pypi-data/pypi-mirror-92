#-------------------------------------------------------------------------------------------
# Get the nested value of a dictionary based on the path defined in an array of ordered keys
#-------------------------------------------------------------------------------------------
def get_item_by_path(root, items, missingAsNULL = False):
    """Access a nested object in root by item sequence."""
    #obj = reduce(operator.getitem, items, root)
    #return obj
    try:
        obj = reduce(operator.getitem, items, root)
    except Exception as e:
        if missingAsNULL == False:
            raise
        else:
            obj = None
    return obj

def set_item_by_path(root, items, value):
    """Set a value in a nested object in root by item sequence."""
    get_item_by_path(root, items[:-1])[items[-1]] = value



    