import Webwidgets, os.path, StringIO, cgi

file = open(os.path.join(os.path.dirname(__file__),
                         '../WidgetBender.css'))
widget_bender_style = file.read()
file.close()

class MainWindow(Webwidgets.ApplicationWindow):
    widget_style = {Webwidgets.Constants.FINAL_OUTPUT: widget_bender_style,
                   'Content-type': 'text/css',
                   'Cache-Control': 'public; max-age=3600',
                   }
    class Body(object):
        class LogIn(object):
            def authenticate(self, username, password):
                return True
