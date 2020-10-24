from . import elements


def attach_dyn_propr(instance, prop_name, propr):
    """Attach property proper to instance with name prop_name.

    Reference: 
      * https://stackoverflow.com/a/1355444/509706
      * https://stackoverflow.com/questions/48448074
    """
    class_name = instance.__class__.__name__
    child_class = type(class_name, (instance.__class__,), {prop_name: propr})

    instance.__class__ = child_class
    

def make_getter(attr):
    def getfunc(self):
        return getattr(self, '_{}'.format(attr))
    return getfunc


def make_setter(attr):
    def setfunc(self, new):
        setattr(self, '_{}'.format(attr), new)
        self.parent_element.args[attr.replace('__', ':').replace('_', '-')] = new
    return setfunc
    

class PresentationAttributes:
        
    def __init__(self, attributes, parent_element):
        fixed = []
        for k in attributes:
            k = k.replace(':', '__')
            k = k.replace('-', '_')
            fixed.append(k)
        attributes = fixed
        self._attributes = attributes
        self.parent_element = parent_element
        
        for attr in attributes:
            setattr(self, '_{}'.format(attr), None)
        
        for attr in attributes:
            getfunc = make_getter(attr)
            setfunc = make_setter(attr)
            attach_dyn_propr(self, attr, property(getfunc, setfunc))


class CircleWithPresentationAttributes(elements.Circle):
    
        def __init__(self, cx, cy, r, **kwargs):
            super().__init__(cx=cx, cy=cy, r=r, **kwargs)
            # Just need a little manual effort to populate value Presentation Attributes from SVG specifications
            # https://developer.mozilla.org/en-US/docs/Web/SVG/Element/circle#Attributes
            circle_attributes = [
            'clip-path',
            'clip-rule',
            'color',
            'color-interpolation',
            'color-rendering',
            'cursor',
            'display',
            'fill',
            'fill-opacity',
            'fill-rule',
            'filter',
            'mask',
            'opacity',
            'pointer-events',
            'shape-rendering',
            'stroke',
            'stroke-dasharray',
            'stroke-dashoffset',
            'stroke-linecap',
            'stroke-linejoin',
            'stroke-miterlimit',
            'stroke-opacity',
            'stroke-width',
            'transform',
            'vector-effect',
            'visibility'
            ]
            self.presentation = PresentationAttributes(circle_attributes, self)
