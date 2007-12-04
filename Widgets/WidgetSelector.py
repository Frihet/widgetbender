#! /bin/env python
# -*- coding: UTF-8 -*-
# vim: set fileencoding=UTF-8 :

# WidgetBender
# Copyright (C) 2007 FreeCode AS, Egil Moeller <redhog@redhog.org>

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA

import Webwidgets, os.path, StringIO, cgi

class WidgetSelector(Webwidgets.ActionInput, Webwidgets.List, Webwidgets.DirectoryServer):
    functions = {'select': "Select"}
    
    def draw(self, output_options):
        self.register_style_link(self.calculate_url(
            {'widget_class': 'WidgetBender.Widgets.WidgetSelector.WidgetSelector',
             'location': ['WidgetSelector.css']},
            {}))

        # FIXME: Handle another draw_wrapper already in output_options in some way (wrap it!)
        output_options = Webwidgets.Utils.subclass_dict(
            output_options,
            {'internal': Webwidgets.Utils.subclass_dict(output_options.get('internal', {}),
                                                        {'draw_wrapper': self.draw_wrapper})})
        self.register_styles(output_options)
        Webwidgets.ActionInput.draw(self, output_options)
        return Webwidgets.List.draw(self, output_options)

    def draw_wrapper(self, parent, path, child, visible, result, output_options, invisible_as_empty):
        info = {'html_class': self.html_class,
                'editor_id': Webwidgets.Utils.path_to_id(self.path),
                'child_id': Webwidgets.Utils.path_to_id(child.path),
                'result': result
                }

        buttons = ["""<button
                       class="%(function)s %(html_class)s"
                       type="submit"
                       name="%(editor_id)s"
                       value="%(function)s:%(child_id)s">%(title)s</button>""" %
                   Webwidgets.Utils.subclass_dict(info, {'function':name, 'title':title})
                   for name, title in self.functions.iteritems()]
        info['buttons'] = '\n'.join(buttons)

        return """<div class="%(html_class)s">
                   <div class="functions">%(buttons)s</div>
                   <div class="widget">%(result)s</div>
                  </div>""" % info

    def field_input(self, path, string_value):
        if string_value != '':
            function, widget = string_value.split(':')
            if function not in self.functions: return
            self.notify('widget_selected', function, Webwidgets.Utils.id_to_path(widget))
