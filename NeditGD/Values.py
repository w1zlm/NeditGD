class Map(dict):
    """
    Example:
    m = Map({'first_name': 'Eduardo'}, last_name='Pool', age=24, sports=['Soccer'])
    """
    def __init__(self, *args, **kwargs):
        super(Map, self).__init__(*args, **kwargs)
        for arg in args:
            if isinstance(arg, dict):
                for k, v in arg.items():
                    self[k] = v

        if kwargs:
            for k, v in kwargs.items():
                self[k] = v

    def __getattr__(self, attr):
        return self.get(attr)

    def __setattr__(self, key, value):
        self.__setitem__(key, value)

    def __setitem__(self, key, value):
        super(Map, self).__setitem__(key, value)
        self.__dict__.update({key: value})

    def __delattr__(self, item):
        self.__delitem__(item)

    def __delitem__(self, key):
        super(Map, self).__delitem__(key)
        del self.__dict__[key]
# thanks for the "Map" class to epool
Triggers=Map(
    sp=31,
    spawnpos=31,
    clr=899,
    color=899,
    m=901,
    move=901,
    st=1616,
    stop=1616,
    pls=1006,
    pulse=1006,
    a=1007,
    alpha=1007,
    tg=1049,
    toggle=1049,
    s=1268,
    spawn=1268,
    r=1346,
    rotate=1346,
    sc=2067,
    scale=2067,
    fl=1347,
    follow=1347,
    shk=1520,
    shake=1520
)
