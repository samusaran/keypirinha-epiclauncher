# Keypirinha launcher (keypirinha.com)

import keypirinha as kp
import keypirinha_util as kpu
import keypirinha_net as kpnet

import json
import os
import collections
import time

from glob import glob

GAME_LAUNCH_URL = "com.epicgames.launcher://apps/{}?action=launch&silent=true"
ALL_USERS_PATH = "C:\\ProgramData\\Epic\\EpicGamesLauncher\\Data\\Manifests"

InstalledApp = collections.namedtuple('InstalledApp',
                                      ['InstallLocation', 'AppName', 'AppID', 'AppVersion', 'Icon'])


class EpicLauncher(kp.Plugin):
    """
    Add installed Epic Games Launcher games to the Keypirinha Catalog.

    Version: 1.0
    """

    CATEGORY = kp.ItemCategory.USER_BASE + 1

    def __init__(self):
        super().__init__()

    def on_start(self):
        pass

    def on_catalog(self):
        applist = self.get_applist()

        start_time = time.time()

        target = GAME_LAUNCH_URL.split(":")[0]

        command, icon = kpu.shell_url_scheme_to_command(target)
        default_icon_handle = self.load_icon("@{}".format(icon))
        self.set_default_icon(default_icon_handle)

        items = [
            self.create_item(
                category=self.CATEGORY,
                label=app.AppName,
                target=app.AppID,
                short_desc="Launch game",
                args_hint=kp.ItemArgsHint.ACCEPTED,
                hit_hint=kp.ItemHitHint.KEEPALL)
            for app in applist]

        self.set_catalog(items)

        elapsed = time.time() - start_time
        stat_msg = "Cataloged {} games in {:0.1f} seconds"
        self.info(stat_msg.format(len(items), elapsed))

    def on_suggest(self, user_input, items_chain):
        pass

    def on_execute(self, item, action):
        appname = item.target()
        target = GAME_LAUNCH_URL.format(appname)
        kpu.shell_execute(target)

    def on_activated(self):
        pass

    def on_deactivated(self):
        pass

    def on_events(self, flags):
        pass

    def get_applist(self):
        results = []
        
        if not os.path.exists(ALL_USERS_PATH):
            self.warn("No launcher data found")
            return results

        for file_path in glob(ALL_USERS_PATH + '\\*.item'):
            item_file = open(file_path, 'r')
            installed = json.load(item_file)

            appname = installed["AppName"]
            if appname.startswith("UE_"):
                continue

            app = InstalledApp(installed["InstallLocation"], installed["DisplayName"], installed["AppName"], installed["AppVersionString"], None)
            results.append(app)

        return results
