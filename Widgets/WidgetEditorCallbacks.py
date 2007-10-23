import Webwidgets

class WidgetEditor(object):
    def widget_selected(self, path, widget_path):
        fields = self.get_widgets_by_attribute('field_name')

        widget = self.window + widget_path
        cls = type(widget)
        widget_csl = cls.__bases__[-1]
        
        fields['widget'].html = widget_csl.__module__
        if getattr(widget_csl, 'ww_widget_path', None) is not None:
            fields['widget'].html += '.' + widget_csl.ww_widget_path
        fields['widget'].html += '.' + widget_csl.__name__
        fields['location'].html = Webwidgets.Utils.path_to_id(widget.parent.path)
        fields['primary_name'].value = widget.name

        fields['attributes'].rows[:] = []
        for name, value in cls.__dict__.iteritems():
            if name in ('win_id', 'name'): continue
            if isinstance(value, bool):
                fields['attributes'].rows.append({
                    'name':name,
                    'value': Webwidgets.Checkbox(
                        self.session, self.win_id,
                        value=value)})
            elif isinstance(value, int):
                fields['attributes'].rows.append({
                    'name':name,
                    'value': Webwidgets.StringInput(
                        self.session, self.win_id,
                        value=unicode(value))})
            elif isinstance(value, (str, unicode)):
                fields['attributes'].rows.append({
                    'name':name,
                    'value': Webwidgets.StringInput(
                        self.session, self.win_id,
                        value=value)})

        fields['inherited_attributes'].rows[:] = []
        for name in dir(widget_cls):
            value = getattr(widget_cls, name)
            if isinstance(value, (bool, int, str, unicode)):
                fields['inherited_attributes'].rows.append({
                    'name':name,
                    'value': value})
