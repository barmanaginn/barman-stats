# barman-stats - plugin for barman
# Copyright © 2020 Yoann Pietri <me@nanoy.fr>
#
# barman-stats is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# barman-stats is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with barman-stats.  If not, see <https://www.gnu.org/licenses/>.

from django.urls import reverse_lazy
from django.utils.translation import ugettext_lazy as _

from barman.plugin import BarmanPlugin


class PluginApp(BarmanPlugin):
    name = "barman_stats"

    class BarmanPluginMeta:
        name = "Statistics"
        author = "Yoann Pietri"
        description = _("Add some stats to BarMan")
        version = 0.1
        url = "https://github.com/barmanaginn/barman-stats"
        email = "me@nanoy.fr"

        nav_urls = (
            {
                "text": _("Stats"),
                "icon": "fas fa-chart-bar",
                "link": reverse_lazy("plugins:barman_stats:stats"),
                "permission": None,
                "login_required": True,
                "admin_required": True,
                "superuser_required": False,
            },
        )

        settings = ()

        user_profile = ()

    def ready(self):
        from . import signals

        return super().ready()


default_app_config = "barman_stats.PluginApp"
