# Metadata - Really Updated Decorators

We're able to use decorator factories to activate the function underneath. 

The decorator adds an attribute that we're able to interpret on our own accord.


```py
@function_decorator
def add_tag():
    """
    Example decorator to add a 'tag' attribute to a function. 
    :param tag: the 'tag' value to set on the decorated function (default 'hi!).
    """
    def _apply_decorator(f):
        """
        This is the method that will be called when `@add_tag` is used on a 
        function `f`. It should return a replacement for `f`.
        """
        setattr(f, 'is_callable', True)
        return f
    return _apply_decorator
```

The upside to this is that we're able to set tags that can change the run order inside of the exact code itself.

```py
class DankMemes(BaseModel, abc.ABC):
    def __new__(cls):
        self = super().__new__(cls)

        assets = []
        ports = {}
        has_tag = False
        name = self.__class__.__name__
        cls_name = underscore(name)
        for member in get_members(self):
            if skip_missing(member, ["__code__"]):
                continue
            SPOOKY = create_existing_name(member.__code__, cls_name)
            if SPOOKY in EXISTING_FUNCS:
                
                fn_curried(member, self, SPOOKY, assets)
                continue

            has_callable = hasattr(member, 'is_callable')
            if has_callable:
                if getattr(member, "is_callable"):
                    member = curry(member, self)
                    assets.append(member)
                    EXISTING_FUNCS.add(SPOOKY)
        return self
```