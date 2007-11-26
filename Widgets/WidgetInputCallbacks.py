import Webwidgets, Webwidgets.Utils, WidgetBender.Widgets.WidgetTree

class WidgetInput(Webwidgets.Fieldgroup, Webwidgets.ValueInput):
    value = None
    class Module(object):
        class Field(object):
            value = Webwidgets
            def value_changed(self, path, value):
                if path != self.path: return
                self.parent.parent.value = None
                tree_widget = self.parent.parent['Widget']['Field']['Child']
                tree_widget.tree.root = value
                tree_widget.tree.root_node = tree_widget.tree.Node(tree_widget.tree)

    class Widget(object):
        class Field(object):
            class HideButton(object):
                class Title(object):
                    def __get__(self, instance, owner):
                        widget_input = instance.parent.parent.parent
                        if widget_input.value is None:
                            return 'No widget selected' 
                        return Webwidgets.Utils.class_full_name(widget_input.value)
                title = Title()
            class Child(object):
                class TreeModel(WidgetBender.Widgets.WidgetTree.WidgetTree.TreeModel):
                    root = Webwidgets
        def selected(self, path, item):
            self.parent.value = item
            self['Field']['HideButton'].value = False

