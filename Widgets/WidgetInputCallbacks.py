import Webwidgets

class WidgetInput(Webwidgets.Fieldgroup, Webwidgets.ValueInput):
    value = None
    class Module(object):
        def value_changed(self, path, value):
            self.parent.value = None
            tree_widget = self.parent['Widget']['Field']['Child']
            tree_widget.root = value
            tree_widget.tree.root_node = tree_widget.tree.Node(tree_widget.tree)
    
    class Widget(object):
        class Field(object):
            class HideButton(object):
                class Title(object):
                    def __get__(self, instance, owner):
                        if instance.parent.parent.parent.value is None:
                           return 'No widget selected' 
                        return instance.parent.parent.parent.value.__name__
                title = Title()
        def selected(self, path, item):
            self.parent.value = item
            self['Field']['HideButton'].value = False

