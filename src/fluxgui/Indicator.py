import appindicator
import gtk

class Indicator:

    def __init__(self, xflux_controller):
        self.xflux_controller=xflux_controller
        self.setup_indicator()

    def setup_indicator(self):
        self.indicator = appindicator.Indicator(
          "fluxgui-indicator",
          "fluxgui",
          appindicator.CATEGORY_APPLICATION_STATUS)
        self.indicator.set_status(appindicator.STATUS_ACTIVE)

        # Check for special Ubuntu themes. copied from lookit

        try:
            theme = gtk.gdk.screen_get_default().get_setting('gtk-icon-theme-name')
        except:
            self.indicator.set_icon('fluxgui')
        else:
          if theme == 'ubuntu-mono-dark':
              self.indicator.set_icon('fluxgui-dark')
          elif theme == 'ubuntu-mono-light':
              self.indicator.set_icon('fluxgui-light')
          else:
              self.indicator.set_icon('fluxgui')

        #self.indicator.set_menu(self.setup_menu())
        self.indicator.set_menu(self.create_menu())

    def create_menu(self):
        menu=gtk.Menu()

        self.add_menu_item("_Pause f.lux", self._toggle_pause, \
                menu, MenuItem=gtk.CheckMenuItem)
        self.add_menu_item("_Preferences", self._open_preferences, menu)
        self.add_menu_separator(menu)
        self.add_menu_item("Quit",self._quit,menu)

        return menu

    def add_menu_item(self,label, handler, menu, \
            event="activate", MenuItem=gtk.MenuItem, show=True):
        item=MenuItem(label)
        item.connect(event,handler)
        menu.append(item)
        if show:
            item.show()
        return item

    def add_menu_separator(self, menu, show=True):
        item = gtk.SeparatorMenuItem()
        menu.append(item)
        if show:
            item.show()

    def _toggle_pause(self, item):
        self.xflux_controller.toggle_pause()

    def _open_preferences(self, item):
        pass

    def _quit(self, item):
        pass

    #def main(self):
    #   gtk.main()
    #def destroy(self):
    #   gtk.main_quit()
