import sys, types


def _get_mod(module_path):
    try:
        aMod = sys.modules[module_path]
        if not isinstance(aMod, types.ModuleType):
            raise KeyError
    except KeyError:
        # The last [''] is very important!
        aMod = __import__(module_path, globals(), locals(), [''])
        sys.modules[module_path] = aMod
    return aMod


def _get_func(full_func_name):
    """Retrieve a function object from a full dotted-package name."""
    # Parse out the path, module, and function
    lastDot = full_func_name.rfind(u".")
    funcName = full_func_name[lastDot + 1:]
    modPath = full_func_name[:lastDot]
    aMod = _get_mod(modPath)
    aFunc = getattr(aMod, funcName)
    # Assert that the function is a *callable* attribute.
    assert callable(aFunc), u"%s is not callable." % full_func_name
    # Return a reference to the function itself,
    # not the results of the function.
    return aFunc


def _get_Class(full_class_name, parent_class=None):
    """Load a module and retrieve a class (NOT an instance).
  If the parentClass is supplied, className must be of parentClass
  or a subclass of parentClass (or None is returned).
  """
    aClass = _get_func(full_class_name)
    # Assert that the class is a subclass of parentClass.
    if parent_class is not None:
        if not issubclass(aClass, parent_class):
            raise TypeError(u"%s is not a subclass of %s" %
                            (full_class_name, parent_class))
    # Return a reference to the class itself, not an instantiated object.
    return aClass


# def applyFuc(obj,strFunc,arrArgs):
#   objFunc = getattr(obj, strFunc)
#   # return apply(objFunc,arrArgs)
#   return apply(objFunc,arrArgs)


def _get_object(full_class_name):
    clazz = _get_Class(full_class_name)
    return clazz()
