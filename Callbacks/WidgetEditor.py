#! /bin/env python
# -*- coding: UTF-8 -*-
# vim: set fileencoding=UTF-8 :

# Webwidgets web developement framework
# Copyright (C) 2006 uAnywhere, Egil Moeller <redhog@redhog.org>
# Copyright (C) 2007 FreeCode AS, Egil Moeller <redhog@redhog.org>
# Copyright (C) 2007 FreeCode AS, Axel Liljencrantz <axel.liljencrantz@freecode.no>

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

import Webwidgets.Utils, Webwidgets.Constants
import Base, Formatting


class WidgetSelector(Base.ActionInput, Formatting.List):
    def draw(self, output_options):
        # FIXME: Handle another draw_wrapper already in output_options in some way (wrap it!)
        output_options = Webwidgets.Utils.subclass_dict(output_options,
                                                        {'draw_wrapper': self.draw_wrapper})
        Base.ActionInput.draw(self, output_options)
        return Formatting.List.draw(self, output_options)

    def draw_wrapper(self, parent, path, child, visible, result, output_options, invisible_as_empty):
        return """<div class="%(html_class)s">
                   <button class="%(html_class)s" type="submit" name="%(editor_id)s" value="%(child_id)s">Edit</button>
                   %(result)s
                  </div>""" % {
            'html_class': self.html_class,
            'editor_id': Webwidgets.Utils.path_to_id(self.path),
            'child_id': Webwidgets.Utils.path_to_id(child.path),
            'result': result
            }

    def field_input(self, path, string_value):
        if string_value != '':
            self.notify('widget_selected', Webwidgets.Utils.id_to_path(string_value))


    def widget_selected(self, path, widget):
        print widget
