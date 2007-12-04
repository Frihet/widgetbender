import Webwidgets, sys, os, os.path

class WidgetEditor(object):
    excluded_attributes = ('win_id', 'name', '__module__', '_input_level',
                           'ww_class_order_nr', 'ww_class_path', 'html_class',
                           'root', 'id', 'classid')
    
    def widget_selected(self, path, function, widget_path):
        fields = self.get_widgets_by_attribute('field_name')

        widget = self.window + widget_path
        cls = type(widget)
        widget_cls = cls.__bases__[-1]

        parent_widget = self.window + widget_path[:-1]
        parent_cls = type(parent_widget)
        parent_widget_cls = parent_cls.__bases__[-1]

        widget_name = str(widget_path[-1])
        
        if function == 'remove':
            del parent_widget[widget_name]
            delattr(parent_cls, widget_name)
        elif function in ('insert-before', 'insert-within', 'insert-after'):

            new_widget_name = widget_name + "_before"
            
            class New(fields['new_widget'].value):
                pass
            New.__module__ = parent_cls.__module__
            New.ww_class_path = parent_cls.__name__
            if hasattr(parent_cls, 'ww_class_path'):
                New.ww_class_path = parent_cls.ww_class_path + '.' + parent_cls.__name__
            New.__name__ = new_widget_name
            
            setattr(parent_cls, new_widget_name, New)
            parent_widget[new_widget_name] = New(parent_widget.session, parent_widget.win_id)
            
        elif function == 'details':
            fields['editor_panels'].page = ['EditAttributes']
            
            fields['widget'].html = widget_cls.__module__
            if getattr(widget_cls, 'ww_widget_path', None) is not None:
                fields['widget'].html += '.' + widget_cls.ww_widget_path
            fields['widget'].html += '.' + widget_cls.__name__
            fields['widget'].html = fields['widget'].html.replace('.', ' . ')
            fields['location'].html = ' - '.join(widget.path)
            fields['primary_name'].value = widget.name

            fields['attributes'].rows[:] = []
            for name, value in cls.__dict__.iteritems():
                if name in self.excluded_attributes: continue
                input_widget = None
                if isinstance(value, bool):
                    input_widget = Webwidgets.Checkbox
                elif isinstance(value, int):
                    input_widget = Webwidgets.IntegerInput
                elif isinstance(value, (str, unicode)):
                    input_widget = Webwidgets.StringInput
                if input_widget is not None:
                    fields['attributes'].rows.append({
                        'name':name,
                        'value': input_widget(
                            self.session, self.win_id,
                            value=value)})

            fields['inherited_attributes'].rows[:] = []
            for name in dir(widget_cls):
                if name in self.excluded_attributes or name in cls.__dict__: continue
                value = getattr(widget_cls, name)
                if isinstance(value, (bool, int, str, unicode)):
                    fields['inherited_attributes'].rows.append({
                        'name':name,
                        'value': value})
