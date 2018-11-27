__title__ = 'AdminPlus'
__author__ = 'Jakkee'
__version__ = '1.8.6'

import clr
clr.AddReferenceByPartialName("Fougerite")
import Fougerite
PluginSettings = {}


class AdminPlus:
    def On_PluginInit(self):
        Util.ConsoleLog(__title__ + " by " + __author__ + " Version: " + __version__ + " loaded.", False)
        if not Plugin.IniExists("Settings"):
            Plugin.CreateIni("Settings")
            ini = Plugin.GetIni("Settings")
            ini.AddSetting("Config", "AdminDestroyEnabled", "true")
            ini.AddSetting("Config", "AdminDestroyWeapon", "Uber Hatchet")
            ini.AddSetting("Config", "AdminTPDistance", "30")
            ini.AddSetting("Config", "ModeratorsCanUse", "true")
            ini.AddSetting("Commands", "Player must run duty first?", "true")
            ini.AddSetting("AdminDoors", "76561198135558142", "Jakkee //These are the players who can open any door in the server! (/admin doors) to add/remove yourself")
            ini.Save()
        PluginSettings.clear()
        ini = Plugin.GetIni("Settings")
        PluginSettings["DestroyEnabled"] = ini.GetBoolSetting("Config", "AdminDestroyEnabled")
        PluginSettings["Distance"] = float(ini.GetSetting("Config", "AdminTPDistance"))
        PluginSettings["DestroyWeapon"] = ini.GetSetting("Config", "AdminDestroyWeapon")
        PluginSettings["ModeratorsCanUse"] = ini.GetBoolSetting("Config", "ModeratorsCanUse")
        PluginSettings["DutyFirst"] = ini.GetBoolSetting("Commands", "Player must run duty first?")

    def On_DoorUse(self, Player, DoorUseEvent):
        if self.toggled(Player):
            DoorUseEvent.Open = True

    def isMod(self, Player):
        if DataStore.ContainsKey("Moderators", Player.SteamID) or Player.Moderator:
            if PluginSettings["ModeratorsCanUse"]:
                return True
            else:
                return False
        else:
            return False

    def On_Command(self, Player, cmd, args):
        if cmd == "admin":
            if Player.Admin or self.isMod(Player):
                if len(args) == 0:
                    Player.MessageFrom("[Admin-Plus]", "[color aqua]/duty [on / off] [color yellow]- [color clear]Tüm izinler Aktif Ediniz")
                    Player.MessageFrom("[Admin-Plus]", "[color aqua]/admin [on / off] [color yellow]- [color clear]Admin Invisible Suit")
                    Player.MessageFrom("[Admin-Plus]", "[color aqua]/admin metal [color yellow]- [color clear]Metal Yapı Eşyaları")
                    Player.MessageFrom("[Admin-Plus]", "[color aqua]/admin wood [color yellow]- [color clear]Odun Yapı Eşyaları")
                    Player.MessageFrom("[Admin-Plus]", "[color aqua]/admin uber [color yellow]- [color clear]Admin Uber items")
                    Player.MessageFrom("[Admin-Plus]", "[color aqua]/admin kevlar [color yellow]- [color clear]Only Admin Kevlar Set")
                    Player.MessageFrom("[Admin-Plus]", "[color aqua]/admin clear [color yellow]- [color clear]Envanter Temizleme")
                    Player.MessageFrom("[Admin-Plus]", "[color aqua]/admin doors [color yellow]- [color clear]Admin Doors")
                    Player.MessageFrom("[Admin-Plus]", "[color aqua]/admin weapons [color yellow]- [color clear]Silah & Mermi")
                elif len(args) == 1:
                    if args[0] == "on":
                        if self.dutyfirst(Player):
                            Player.Inventory.RemoveItem(36)
                            Player.Inventory.RemoveItem(37)
                            Player.Inventory.RemoveItem(38)
                            Player.Inventory.RemoveItem(39)
                            Player.Inventory.AddItemTo("Invisible Helmet", 36, 1)
                            Player.Inventory.AddItemTo("Invisible Vest", 37, 1)
                            Player.Inventory.AddItemTo("Invisible Pants", 38, 1)
                            Player.Inventory.AddItemTo("Invisible Boots", 39, 1)
                            Player.Notice("☣", "Admin Invisible !")
                        else:
                            Player.Notice("☣", "Komut izinleri için Duty Aktif Ediniz !")
                    elif args[0] == "off":
                        if self.dutyfirst(Player):
                            Player.Inventory.RemoveItem(36)
                            Player.Inventory.RemoveItem(37)
                            Player.Inventory.RemoveItem(38)
                            Player.Inventory.RemoveItem(39)
                            Player.Notice("☣", "Player Visible !")
                        else:
                            Player.Notice("☣", "Komut izinleri için Duty Aktif Ediniz !")
                    elif args[0] == "wood":
                        if self.dutyfirst(Player):
                            Player.Inventory.AddItem("Wood Pillar", 250)
                            Player.Inventory.AddItem("Wood Foundation", 250)
                            Player.Inventory.AddItem("Wood Wall", 250)
                            Player.Inventory.AddItem("Wood Doorway", 250)
                            Player.Inventory.AddItem("Wood Window", 250)
                            Player.Inventory.AddItem("Wood Stairs", 250)
                            Player.Inventory.AddItem("Wood Ramp", 250)
                            Player.Inventory.AddItem("Wood Ceiling", 250)
                            Player.Inventory.AddItem("Metal Door", 15)
                            Player.Inventory.AddItem("Metal Window Bars", 15)
                            Player.Notice("☣", "Wood Building Parts Envanterine Eklendi !")
                        else:
                            Player.Notice("☣", "Komut izinleri için Duty Aktif Ediniz !")
                    elif args[0] == "weapons":
                        if self.dutyfirst(Player):
                            Player.Inventory.AddItem("Bolt Action Rifle", 1)
                            Player.Inventory.AddItem("M4", 1)
                            Player.Inventory.AddItem("MP5A4", 1)
                            Player.Inventory.AddItem("9mm Pistol", 1)
                            Player.Inventory.AddItem("P250", 1)
                            Player.Inventory.AddItem("Shotgun", 1)
                            Player.Inventory.AddItem("556 Ammo", 250)
                            Player.Inventory.AddItem("9mm Ammo", 250)
                            Player.Inventory.AddItem("Shotgun Shells", 250)
                            Player.Notice("☣", "Silahlar & Mermiler Envanterine Eklendi !")
                        else:
                            Player.Notice("☣", "Komut izinleri için Duty Aktif Ediniz !")
                    elif args[0] == "metal":
                        if self.dutyfirst(Player):
                            Player.Inventory.AddItem("Metal Pillar", 250)
                            Player.Inventory.AddItem("Metal Foundation", 250)
                            Player.Inventory.AddItem("Metal Wall", 250)
                            Player.Inventory.AddItem("Metal Doorway", 250)
                            Player.Inventory.AddItem("Metal Window", 250)
                            Player.Inventory.AddItem("Metal Stairs", 250)
                            Player.Inventory.AddItem("Metal Ramp", 250)
                            Player.Inventory.AddItem("Metal Ceiling", 250)
                            Player.Inventory.AddItem("Metal Door", 15)
                            Player.Inventory.AddItem("Metal Window Bars", 15)
                            Player.Notice("☣", "Metal Building Parts Envanterine Eklendi !")
                        else:
                            Player.Notice("☣", "Komut izinleri için Duty Aktif Ediniz !")
                    elif args[0] == "uber":
                        if self.dutyfirst(Player):
                            Player.Inventory.AddItem("Uber Hatchet", 1)
                            Player.Inventory.AddItem("Uber Hunting Bow", 1)
                            Player.Inventory.AddItem("Arrow", 40)
                            Player.Notice("☣", "Uber İtems Envanterine Eklendi !")
                        else:
                            Player.Notice("☣", "Komut izinleri için Duty Aktif Ediniz !")
                    elif args[0] == "kevlar":
                        if self.dutyfirst(Player):
                            Player.Inventory.RemoveItem(36)
                            Player.Inventory.RemoveItem(37)
                            Player.Inventory.RemoveItem(38)
                            Player.Inventory.RemoveItem(39)
                            Player.Inventory.AddItemTo("Kevlar Helmet", 36, 1)
                            Player.Inventory.AddItemTo("Kevlar Vest", 37, 1)
                            Player.Inventory.AddItemTo("Kevlar Pants", 38, 1)
                            Player.Inventory.AddItemTo("Kevlar Boots", 39, 1)
                            Player.Notice("☣", "Kevlar Set Giyildi - Oyuncular Üstünde Denemeyiniz !")
                        else:
                            Player.Notice("☣", "Komut izinleri için Duty Aktif Ediniz !")
                    elif args[0] == "clear":
                        if self.dutyfirst(Player):
                            Player.Inventory.ClearAll()
                            Player.Notice("☣", "Envanter Temizlendi !")
                        else:
                            Player.Notice("☣", "Komut izinleri için Duty Aktif Ediniz !")
                    elif args[0] == "doors":
                        if self.dutyfirst(Player):
                            self.toggle(Player)
                        else:
                            Player.Notice("☣", "Komut izinleri için Duty Aktif Ediniz !")
                    else:
                        Player.Notice("☣", "Bilinmeyen Bir Komut Girdiniz...")
                else:
                    Player.Notice("☣", "Tüm Komutlar için - /admin")
            else:
                Player.MessageFrom("[Admin-Plus]", "[color red]Bu Komut için Yeterli Yetkin Yok !")
        elif cmd == "duty":
            if Player.Admin or self.isMod(Player):
                if len(args) == 0:
                    Player.Notice("☣", "Tüm Komut izinleri için - /duty [on / off]")
                elif len(args) == 1:
                    if args[0] == "on":
                        DataStore.Add("OnDuty", Player.SteamID, "on")
                        Server.Broadcast(Player.Name + " [color lime]is now on duty ![color clear] Let him/her know if you need anything !")
                    elif args[0] == "off":
                        DataStore.Remove("OnDuty", Player.SteamID)
                        Server.Broadcast(Player.Name + " [color red]is now off duty ![color clear] Please direct questions to another admin !")
                    else:
                        Player.Notice("☣", "Bilinmeyen Komut Girdiniz...")
                else:
                    Player.Notice("☣", "Tüm Komut izinleri için - /duty [on / off]")
            else:
                Player.MessageFrom("[Admin-Plus]", "[color red]Bu Komut için Yeterli Yetkin Yok !")
        elif cmd == "sadasd":
            if Player.Admin or self.isMod(Player):
                if self.dutyfirst(Player):
                    if len(args) == 0:
                        Player.MessageFrom("AdminPlus", "Usage: /tpadmin [Player Name]")
                    else:
                        target = self.CheckV(Player, args)
                        if target is not None:
                            DataStore.Add("SavedLocation", Player.SteamID, Player.Location)
                            distance = PluginSettings["Distance"]
                            if distance is None:
                                distance = float(30)
                            vector3 = Util.Infront(target, distance)
                            Player.SafeTeleportTo(vector3)
                            Player.MessageFrom("AdminPlus", "Teleported: " + str(distance) + "m infront of " + target.Name)
                            Player.MessageFrom("AdminPlus", "Use /tpback to go back to your last location")
                        else:
                            return
                else:
                    Player.MessageFrom("AdminPlus", "Komut izinleri için Duty Aktif Ediniz !")
            else:
                Player.MessageFrom("AdminPlus", "You're not allowed to use that command!")
        elif cmd == "asdwq":
            if Player.Admin or self.isMod(Player):
                if self.dutyfirst(Player):
                    if len(args) == 0:
                        if DataStore.Get("SavedLocation", Player.SteamID):
                            BLocation = DataStore.Get("SavedLocation", Player.SteamID)
                            Player.TeleportTo(BLocation)
                            DataStore.Remove("SavedLocation", Player.SteamID)
                            Player.MessageFrom("AdminPlus", "Teleported back!")
                        else:
                            Player.MessageFrom("AdminPlus", "You have no last known locations")
                    elif len(args) > 0:
                        Player.MessageFrom("AdminPlus", "Usage: /tpback")
                else:
                    Player.MessageFrom("AdminPlus", "Komut izinleri için Duty Aktif Ediniz !")
            else:
                Player.MessageFrom("AdminPlus", "You're not allowed to use that command!")

    def On_PlayerDisconnected(self, Player):
        try:
            if DataStore.Get("SavedLocation", Player.SteamID) is not None:
                DataStore.Remove("SavedLocation", Player.SteamID)
            if DataStore.Get("OnDuty", Player.SteamID) is not None:
                DataStore.Remove("OnDuty", Player.SteamID)
                Server.Broadcast(Player.Name + " [color red]is now off duty ![color clear] Please direct questions to another admin !")
        except:
            pass

    def On_EntityHurt(self, HurtEvent):
        try:
            if HurtEvent.Attacker.Admin:
                if PluginSettings["DestroyEnabled"]:
                    if HurtEvent.WeaponName == PluginSettings["DestroyWeapon"]:
                        if HurtEvent.Entity.Name is not None:
                            HurtEvent.Entity.Destroy()
        except:
            pass

    def dutyfirst(self, Player):
        try:
            if PluginSettings["DutyFirst"]:
                if DataStore.Get("OnDuty", Player.SteamID) == "on":
                    return True
                else:
                    return False
            else:
                return True
        except:
            return False

    def toggle(self, Player):
        ini = Plugin.GetIni("Settings")
        if ini.GetSetting("AdminDoors", Player.SteamID) is None:
            ini.AddSetting("AdminDoors", Player.SteamID, Player.Name)
            ini.Save()
            Player.MessageFrom("☣", "Admin Doors Aktif !")
        else:
            ini.DeleteSetting("AdminDoors", Player.SteamID)
            ini.Save()
            Player.MessageFrom("☣", "Admin Doors De-Aktif !")

    def toggled(self, Player):
        ini = Plugin.GetIni("Settings")
        if ini.GetSetting("AdminDoors", Player.SteamID) is not None:
            return True
        else:
            return False

    def argsToText(self, args):
        text = str.join(" ", args)
        return text

    def GetPlayerName(self, name):
        try:
            name = name.lower()
            for pl in Server.Players:
                if pl.Name.lower() == name:
                    return pl
            return None
        except:
            return None

    def CheckV(self, Player, args):
        count = 0
        if hasattr(args, '__len__') and (not isinstance(args, str)):
            p = self.GetPlayerName(str.join(" ", args))
            if p is not None:
                return p
            for pl in Server.Players:
                for namePart in args:
                    if namePart.lower() in pl.Name.lower():
                        p = pl
                        count += 1
                        continue
        else:
            nargs = str(args).lower()
            p = self.GetPlayerName(nargs)
            if p is not None:
                return p
            for pl in Server.ActivePlayers:
                if nargs in pl.Name.lower():
                    p = pl
                    count += 1
                    continue
        if count == 0:
            Player.Message("Couldn't find " + str.join(" ", args) + "!")
            return None
        elif count == 1 and p is not None:
            return p
        else:
            Player.Message("Found " + str(count) + " players with similar a name. Use a more correct name!")
            return None
