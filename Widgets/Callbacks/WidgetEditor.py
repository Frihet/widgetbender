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
