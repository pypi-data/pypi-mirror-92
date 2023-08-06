# /usr/bin/python3
####### PACKAGES
from . import anutils as an

# a generic class for an object set
class Object_set(list):
    """ Object_set
        A class that contains a list of objects plus extra methods and properties
        
    """
    def __init__(self, *args, id=1,
                 config=None, name=None,  build=None, type=None, **kwargs):
        list.__init__(self)

        # Filling info
        self.name = name
        self.id = id
        self.type = type

        # Reading properties
        self.properties = an.get_prop_dicts(config, type=type, name=name)

        # We allow a custom constructor
        if build is not None:
            build(self, *args, **kwargs)
        else:
            self.build_objects(*args, **kwargs)

    # Stupid builder
    def build_objects(self, *args, **kwargs):
        self.append(Object(None))

    # Generic analyzer
    def analyze(self, obj, analyze={}, *args, **kwargs):
        analysis={}
        for name, func in analyze.items():
            analysis[name] = func(obj)

        return analysis

# A class to contain a single object :
class Object():
    """ Object
        Generic useless object
        """

    def __init__(self, *args,  id = 1, **kwargs):
        self.id = id
