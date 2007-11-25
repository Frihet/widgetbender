import Webwidgets

class ModuleInput(Webwidgets.Html, Webwidgets.ValueInput):
    value = None
    class Tree(object):
        class HideButton(object):
            class Title(object):
                def __get__(self, instance, owner):
                    if instance.parent.parent.value is None:
                       return 'No module selected' 
                    return instance.parent.parent.value.__name__
            title = Title()
    def selected(self, path, item):
        self.value = item
        self['Tree']['HideButton'].value = False

