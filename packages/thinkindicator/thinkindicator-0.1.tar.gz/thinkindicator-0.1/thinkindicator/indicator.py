import os

import gi

gi.require_version("Gtk", "3.0")
gi.require_version("AppIndicator3", "0.1")

from gi.repository import Gtk, Gdk, AppIndicator3, GLib

from .fan import get_level, LEVELS, set_level

APPINDICATOR_ID = "thinkindicator"
SCROLL_SPEED = 5


class ThinkIndicator:
    script_dir = os.path.dirname(os.path.realpath(__file__))

    def _get_icon(self):
        icon = self.current_level
        if icon == "auto":
            icon = "A"
        elif icon == "full-speed":
            icon = "F"
        elif icon == "disengaged":
            icon = "D"

        return f"{self.script_dir}/icons/{icon}.png"

    def _update_level(self):
        self.current_level = get_level()
        self.indicator.set_icon_full(self._get_icon(), self.current_level)

    def _update_level_timeout(self):
        self._update_level()
        GLib.timeout_add_seconds(1, self._update_level)

    def _set_level_action(self, _menu: Gtk.MenuItem, level: str):
        set_level(level)
        self._update_level()

    def _get_menu(self):
        menu = Gtk.Menu()
        group = None

        for level in LEVELS:
            item_level = Gtk.RadioMenuItem(
                group=group, label=level.replace("-", " ")
            )

            group = item_level
            item_level.show()
            item_level.connect("activate", self._set_level_action, level)

            if level == self.current_level:
                item_level.set_active(True)

            menu.append(item_level)

        item_quit = Gtk.MenuItem("Quit")
        item_quit.show()
        item_quit.connect("activate", Gtk.main_quit)
        menu.append(item_quit)

        return menu

    def scroll(
        self,
        _ind: AppIndicator3.Indicator,
        steps: int,
        direction: Gdk.ScrollDirection,
    ):
        # Check if we are in manual mode
        try:
            current_level_int = int(self.current_level)
        except ValueError:
            return

        if direction == Gdk.ScrollDirection.DOWN:
            self.scroll_progress -= steps
        elif direction == Gdk.ScrollDirection.UP:
            self.scroll_progress += steps

        if self.scroll_progress >= SCROLL_SPEED:
            if current_level_int != 7:
                set_level(str(current_level_int + 1))
                self._update_level()
            self.scroll_progress = 0
        elif self.scroll_progress <= -SCROLL_SPEED:
            # Not below one so we don't turn off fan completely by accident
            # and fry someone's computer
            if current_level_int != 1:
                set_level(str(current_level_int - 1))
                self._update_level()
            self.scroll_progress = 0

    def __init__(self):
        self.current_level = None
        self.scroll_progress = 0
        self.indicator = AppIndicator3.Indicator.new(
            APPINDICATOR_ID, "", AppIndicator3.IndicatorCategory.HARDWARE
        )

    def run(self):
        self.indicator.set_status(AppIndicator3.IndicatorStatus.ACTIVE)
        self._update_level_timeout()
        self.indicator.set_menu(self._get_menu())
        self.indicator.connect("scroll-event", self.scroll)
        Gtk.main()
