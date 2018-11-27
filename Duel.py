__author__ = 'Assassin'
__version__ = '1.0'
import clr

clr.AddReferenceByPartialName("Fougerite")
import Fougerite
import math
import System
from System import *
import re
import sys

path = Util.GetRootFolder()
sys.path.append(path + "\\Save\\Lib\\")

try:
    import random
except ImportError:
    pass

red = "[color #FF0000]"
green = "[color #009900]"
gr = "[color #96bad2]"
prp = "[color #a395c8]"
"""
    Class
"""

Pending = []


class Duel:

    sys = None
    Maxuses = None
    Cooldown = None
    TimeoutR = None
    TpDelay = None
    CheckIfPlayerIsNearStructure = None
    CheckIfPlayerIsOnDeployable = None
    CheckIfPlayerIsInShelter = None

    def On_PluginInit(self):
        DataStore.Flush("duelTimer")
        DataStore.Flush("duelpending")
        DataStore.Flush("duelpending2")
        DataStore.Flush("duelcooldown")
        config = self.DuelConfig()
        self.sys = config.GetSetting("Settings", "sysname")
        self.Maxuses = int(config.GetSetting("Settings", "Maxuses"))
        self.Cooldown = int(config.GetSetting("Settings", "cooldown"))
        self.TimeoutR = int(config.GetSetting("Settings", "timeoutr"))
        self.TpDelay = int(config.GetSetting("Settings", "tpdelay"))
        self.CheckIfPlayerIsNearStructure = int(config.GetSetting("Settings", "CheckIfPlayerIsNearStructure"))
        self.CheckIfPlayerIsOnDeployable = int(config.GetSetting("Settings", "CheckIfPlayerIsOnDeployable"))
        self.CheckIfPlayerIsInShelter = int(config.GetSetting("Settings", "CheckIfPlayerIsInShelter"))
        Util.ConsoleLog("Duel Plugin v" + __version__ + " by " + __author__ + " loaded.", True)
        Util.ConsoleLog("PLEASE REPORT EVERY BUG/ISSUE YOU SEE!!", True)

    def DuelConfig(self):
        if not Plugin.IniExists("DuelConfig"):
            loc = Plugin.CreateIni("DuelConfig")
            loc.Save()
        return Plugin.GetIni("DuelConfig")

    def DuelItems(self):
        if not Plugin.IniExists("DuelItems"):
            ini = Plugin.CreateIni("DuelItems")
            ini.AddSetting("DuelItems", "P250", "1")
            ini.AddSetting("DuelItems", "9mm Ammo", "30")
            ini.AddSetting("DuelItems", "Large Medkit", "2")
            ini.Save()
        return Plugin.GetIni("DuelItems")

    def WearClothes(self, Player):
        Player.Inventory.AddItemTo("Leather Helmet", 36, 1)
        Player.Inventory.AddItemTo("Leather Vest", 37, 1)
        Player.Inventory.AddItemTo("Leather Pants", 38, 1)
        Player.Inventory.AddItemTo("Leather Boots", 39, 1)
        Player.Inventory.AddItemTo("P250", 30, 1)
        Player.Inventory.AddItemTo("Large Medkit", 31, 5)

    def StartDuel(self, Player):
         Player.TeleportTo(-5331.7, 385.8, 4519.1)
         Player.MessageFrom(self.sys, "[color #b1a7ff]Düello için Arenaya Işınlandınız !")
         Player.RestrictCommand("home")
         Player.RestrictCommand("kit")
         Player.RestrictCommand("tpr")
         Player.RestrictCommand("tpa")
         Player.RestrictCommand("tpto")
         Player.MessageFrom(self.sys, "[color #b1a7ff]Düello Başladı !")
         ini2 = self.DuelItems()
         enum = ini2.EnumSection("DuelItems")
         for item in enum:
            c = int(ini2.GetSetting("DuelItems", item))
            Player.Inventory.AddItem(item, c)

    def Cloth(self, attacker):
        attacker.Inventory.Clear()
        attacker.Inventory.RemoveItem(36);
        attacker.Inventory.RemoveItem(37);
        attacker.Inventory.RemoveItem(38);
        attacker.Inventory.RemoveItem(39);

    def UnRestrication(self, victim):
        victim.UnRestrictCommand("home")
        victim.UnRestrictCommand("kit")
        victim.UnRestrictCommand("tpr")
        victim.UnRestrictCommand("tpa")
        victim.UnRestrictCommand("tpto")
        victim.UnRestrictCommand("tpaccept")

    def KillJob(self, Player):
        if Player in Pending:
            Pending.remove(Player)

    """
        CheckV method based on Spock's method.
        Upgraded by DreTaX
        Can Handle Single argument and Array args.
        V4.1
    """

    def GetPlayerName(self, namee):
        try:
            name = namee.lower()
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
            for pl in Server.Players:
                if nargs in pl.Name.lower():
                    p = pl
                    count += 1
                    continue
        if count == 0:
            Player.MessageFrom(self.sys, "Couldn't find [color#00FF00]" + str.join(" ", args) + "[/color]!")
            return None
        elif count == 1 and p is not None:
            return p
        else:
            Player.MessageFrom(self.sys, "Bu isimde [color#FF0000]" + str(count)
                               + "[/color] Oyuncu Bulundu. [color#FF0000] Lütfen Oyuncu ismini Tam Yazınız !")
            return None

    def getPlayer(self, d):
        pl = Server.FindPlayer(d)
        return pl

    def Replace(self, String):
        str = re.sub('[(\)]', '', String)
        return str.split(',')

    def isMod(self, id):
        if DataStore.ContainsKey("Moderators", id):
            return True
        return False

    """
        Timer Functions by DreTaX
    """

    def addJob(self, xtime, PlayerFrom, PlayerTo, callback, id=None, tid=None):
        List = Plugin.CreateDict()
        List["PlayerF"] = PlayerFrom
        List["PlayerT"] = PlayerTo
        # Let's make sure we have the steamid all the time.
        if id is None:
            List["PlayerFID"] = PlayerFrom.SteamID
            List["PlayerTID"] = PlayerTo.SteamID
        else:
            List["PlayerFID"] = id
            List["PlayerTID"] = tid
        List["Call"] = callback
        Plugin.CreateParallelTimer("DuelJobTimer", xtime * 1000, List).Start()

    def clearTimers(self):
        Plugin.KillParallelTimer("DuelJobTimer")

    def DuelJobTimerCallback(self, timer):
        timer.Kill()
        List = timer.Args
        PlayerFrom = List["PlayerF"]
        PlayerTo = List["PlayerT"]
        callback = List["Call"]
        id = List["PlayerFID"]
        tid = List["PlayerTID"]
        if not PlayerFrom.IsOnline or not PlayerTo.IsOnline:
            DataStore.Add("duelban", id, "none")
            self.KillJob(PlayerFrom)
            self.KillJob(PlayerTo)
            return
        if callback == 1:
            if self.CheckIfPlayerIsInShelter == 1:
                if PlayerTo.IsInShelter:
                    DataStore.Add("duelcooldown", id, 7)
                    PlayerFrom.MessageFrom(self.sys, ""+ gr +"[color red]Your player is in a shelter, can't teleport!")
                    PlayerTo.MessageFrom(self.sys, ""+ gr +"[color redYou are in a shelter, can't teleport!")
                    return
            if self.CheckIfPlayerIsOnDeployable == 1:
                if PlayerTo.IsOnDeployable:
                    DataStore.Add("duelcooldown", id, 7)
                    PlayerFrom.MessageFrom(self.sys, ""+ gr +"[color redYour player is in on a Deployable, can't teleport!")
                    PlayerTo.MessageFrom(self.sys, ""+ gr +"[color redYou are on a Deployable, can't teleport!")
                    return
            if self.CheckIfPlayerIsNearStructure == 1:
                if PlayerTo.IsNearStructure:
                    DataStore.Add("duelcooldown", id, 7)
                    PlayerFrom.MessageFrom(self.sys, ""+ gr +"[color redYour player is near a house, can't teleport!")
                    PlayerTo.MessageFrom(self.sys, ""+ gr +"[color redYou are near a house, can't teleport!")
                    return
        elif callback == 2:
            if PlayerFrom not in Pending or PlayerTo not in Pending:
                return
            self.KillJob(PlayerFrom)
            self.KillJob(PlayerTo)
            ispend = DataStore.Get("duelpending", id)
            ispend2 = DataStore.Get("duelpending2", tid)
            if ispend is not None and ispend2 is not None:
                DataStore.Remove("duelpending", id)
                DataStore.Remove("duelpending2", tid)
                DataStore.Add("duelcooldown", id, 7)
                if PlayerFrom is not None:
                    PlayerFrom.MessageFrom(self.sys, ""+ gr +"Düello isteği Zaman Aşıma Uğradı !")
                if PlayerTo is not None:
                    PlayerTo.MessageFrom(self.sys, ""+ gr +"Düello isteği Zaman Aşıma Uğradı !")
        elif callback == 3:
            self.Cloth(Player)
            self.Cloth(playerr)
            self.StartDuel(Player)
            self.StartDuel(playerr)
            DataStore.Add("induel", Player.SteamID, "1")
            DataStore.Add("induel", playerr.SteamID, "1")
       
# Start Of Functions for Duel Actions
    def On_PlayerSpawned(self, Player, SpawnEvent):
        if DataStore.ContainsKey("induel", Player.SteamID):
            DataStore.Remove("induel", Player.SteamID)
            Player.Kill()
            Player.MessageFrom(self.sys, "" + gr + "Düello Bağlantısı Kesildi !")

    def On_Command(self, Player, cmd, args):
        id = Player.SteamID
        if cmd == "dcleartpatimers":
            if Player.Admin or self.isMod(id):
                self.clearTimers()
                Player.MessageFrom(self.sys, "Zamanlayıcılar Temizlendi !")
        elif cmd == "duel":
            if len(args) == 0:
                Player.MessageFrom(self.sys, "/duel [PlayerName] - Start Duello")
                Player.MessageFrom(self.sys, "/djoin - to accept a requested duel")
                Player.MessageFrom(self.sys, "/dduel - to deny a duel")
                Player.MessageFrom(self.sys, "/dcount - to see how many requests you have remaining")
                Player.MessageFrom(self.sys, "/duelc - to cancel your own request")
                Player.MessageFrom(self.sys, "/dleave - to leave Duel Arena")
            else:
                if DataStore.ContainsKey("HGIG", Player.SteamID):
                    Player.MessageFrom(self.sys, ""+ gr + "You are in HungerGames!Leave HG and try again!")
                elif DataStore.ContainsKey("induel", Player.SteamID):
                    Player.MessageFrom(self.sys, ""+ gr + "Zaten Düello Yapıyorsun ! Aynı Anda 2 Tane Düello Yapamazsın !")
                else:
                    playertor = self.CheckV(Player, args)
                    if playertor is None:
                        return
                    if playertor == Player:
                        Player.MessageFrom(self.sys, ""+ gr +"Kendinle Düello Yapamazsın !")
                        return
                    if DataStore.ContainsKey("HGIG", playertor.SteamID) or DataStore.ContainsKey("induel", playertor.SteamID):
                        Player.MessageFrom(self.sys, ""+ gr +"Bu Oyuncu Şuanda Başka Bir Oyuncu ile Düello Yapıyor !")
                        return
                    name = Player.Name
                    id = Player.SteamID
                    idt = playertor.SteamID
                    namet = playertor.Name
                    time = DataStore.Get("duelcooldown", id)
                    usedtp = DataStore.Get("duelusedtp", id)
                    if time is None:
                        DataStore.Add("duelcooldown", id, 7)
                        time = 7
                    calc = System.Environment.TickCount - time
                    if calc < 0 or math.isnan(calc):
                        DataStore.Add("duelcooldown", id, 7)
                        time = 7
                    if calc >= self.Cooldown or time == 7:
                        if usedtp is None:
                            DataStore.Add("duelusedtp", id, 0)
                            usedtp = 0
                        if self.Maxuses > 0:
                            if self.Maxuses  <= int(usedtp):
                                Player.MessageFrom(self.sys, ""+ gr +"Maximum Sayıda Düello isteğine Ulaşıldı !")
                                return
                        if DataStore.Get("duelpending2", idt) is not None:
                            Player.MessageFrom(self.sys, ""+ gr +"Bu Oyuncu Bir istek Bekliyor ! Lütfen Biraz Bekle...")
                            return
                        if DataStore.Get("duelpending", id):
                            Player.MessageFrom(self.sys, ""+ gr +"Bir Düello isteği Bekliyorsunuz ! Biraz Bekleyin Ya da iptal Edin.")
                            return

                        DataStore.Add("duelcooldown", id, System.Environment.TickCount)
                        playertor.MessageFrom(self.sys, ""+ gr +"[color orange]" + name + " Adlı Oyuncudan Düello Talebi Geldi ! Kabul Etmek için /djoin")
                        Player.MessageFrom(self.sys, ""+ gr + namet + " Adlı Oyuncuya Düello isteği Gönderildi !")
                        DataStore.Add("duelpending", id, idt)
                        DataStore.Add("duelpending2", idt, id)
                        self.KillJob(Player)
                        self.KillJob(playertor)
                        Pending.append(Player)
                        Pending.append(playertor)
                        self.addJob(self.TimeoutR, Player, playertor, 2, id, idt)
                    else:
                        Player.MessageFrom(self.sys, ""+ gr +"Tekrar Talep Etmeden Biraz Beklemeniz Gerekiyor !")
                        done = round((calc / 1000) / 60, 2)
                        done2 = round((self.Cooldown / 1000) / 60, 2)
                        Player.MessageFrom(self.sys, ""+ gr +"Bekleme Süresi : " + str(done) + " / " + str(done2) + " mins")
# Don't Active this Part if you don't want to test some issues or bugs...
#        elif cmd == "test":
#            DataStore.Add("induel", Player.SteamID, "1")
#            Player.MessageFrom(self.sys, ""+ gr +"Now you have induel Data")
#        elif cmd == "untest":
#            Player.MessageFrom(self.sys, ""+ prp +" Now you don't have induel Data")
#            DataStore.Remove("induel", Player.SteamID)
        elif cmd == "djoin":
            pending = DataStore.Get("duelpending2", id)
            if pending is not None:
                playerfromm = self.getPlayer(pending)
                if playerfromm is not None:
                    self.KillJob(Player)
                    self.KillJob(playerfromm)
                    playerdueluse = int(DataStore.Get("duelusedtp", pending))

                    if self.Maxuses > 0:
                        playerdueluse = int(playerdueluse) + 1
                        DataStore.Add("duelusedtp", pending, playerdueluse)
                        playerfromm.MessageFrom(self.sys, ""+ gr +"Duel requests used "+ prp +"" + str(playerdueluse) + " / "
                                                + str(self.Maxuses))
                    else:
                        playerfromm.MessageFrom(self.sys, ""+ gr +"Sınırsız istek var !")

                    idt = playerfromm.SteamID
                    if self.TpDelay > 0:
                        playerfromm.MessageFrom(self.sys, ""+ prp +"Düello Arenasına Teleport Oluyorsunuz : [color yellow]" + str(self.TpDelay) + " [color clear]saniye !")
                        self.addJob(self.TpDelay, playerfromm, Player, 1, idt, id)

                    else:
                        if self.CheckIfPlayerIsInShelter == 1:
                            if Player.IsInShelter:
                                DataStore.Add("duelcooldown", id, 7)
                                playerfromm.MessageFrom(self.sys, ""+ gr +"[color red]Your player is in a shelter, can't start Duel!")
                                Player.MessageFrom(self.sys, ""+ gr +"[color red]You are in a shelter, can't start Duel!")
                                return
                        if self.CheckIfPlayerIsOnDeployable == 1:
                            if Player.IsOnDeployable:
                                DataStore.Add("duelcooldown", id, 7)
                                playerfromm.MessageFrom(self.sys, ""+ gr +"[color red]Your player is in on a Deployable, can't start Duel!")
                                Player.MessageFrom(self.sys, ""+ gr +"[color red]You are on a Deployable, can't start Duel!")
                                return
                        if self.CheckIfPlayerIsNearStructure == 1:
                            if Player.IsNearStructure:
                                DataStore.Add("duelcooldown", id, 7)
                                playerfromm.MessageFrom(self.sys, ""+ gr +"[color red]Your player is near a house, can't start Duel!")
                                Player.MessageFrom(self.sys, ""+ gr +"[color red]You are near a house, can't start Duel!")
                                return
                        self.Cloth(Player)
                        self.Cloth(playerfromm)
                        self.StartDuel(Player)
                        self.StartDuel(playerfromm)
                        DataStore.Add("induel", Player.SteamID, "1")
                        DataStore.Add("induel", playerfromm.SteamID, "1")

                    DataStore.Remove("duelpending", idt)
                    DataStore.Remove("duelpending2", id)
                    Player.MessageFrom(self.sys, ""+ gr +"Düello isteği Kabul Edildi !")

                else:
                    self.KillJob(Player)
                    Player.MessageFrom(self.sys, ""+ gr +"Player Online Değil !")
            else:
                Player.MessageFrom(self.sys, ""+ gr +"Düello isteğiniz Zaman Aşımına Uğradı !")
        elif cmd == "dduel":
            pending = DataStore.Get("duelpending2", id)
            if pending is not None:
                playerfromm = self.getPlayer(pending)
                if playerfromm is not None:
                    playerfromm.MessageFrom(self.sys, ""+ gr +"Düello isteğiniz Reddedildi !")
                    self.KillJob(playerfromm)
                self.KillJob(Player)
                DataStore.Remove("duelpending", pending)
                DataStore.Add("duelcooldown", pending, 7)
                DataStore.Remove("duelpending2", id)
                Player.MessageFrom(self.sys, ""+ gr +"Düello isteği Reddedildi !")
            else:
                Player.MessageFrom(self.sys, ""+ gr +"Herhangi Bir istek Bulunmuyor !")
        elif cmd == "duelc":
            pending = DataStore.Get("duelpending", id)
            if pending is not None:
                playerto = self.getPlayer(pending)
                if playerto is not None:
                    playerto.MessageFrom(self.sys, Player.Name + " [color red]Cancelled the request!")
                    self.KillJob(playerto)
                self.KillJob(Player)
                DataStore.Remove("duelpending", id)
                DataStore.Add("duelcooldown", id, 7)
                DataStore.Remove("duelpending2", pending)
                Player.MessageFrom(self.sys, ""+ gr +"Request [color red]Cancelled!")
            else:
                Player.MessageFrom(self.sys, ""+ gr +"There is nothing to cancel.")
        elif cmd == "dcount":
            if self.Maxuses > 0:
                uses = int(DataStore.Get("duelusedtp", id))
                if uses is None:
                    uses = 0
                Player.MessageFrom(self.sys, ""+ gr +"Duel requests used " + str(uses) + " / " + str(self.Maxuses))
            else:
                Player.MessageFrom(self.sys, ""+ gr +"You have unlimited requests remaining!")
        elif cmd == "duelresettime":
            if Player.Admin or self.isMod(id):
                DataStore.Add("duelcooldown", id, 7)
                Player.Message("Reset!")
        elif cmd == "dclearuses":
            id = Player.SteamID
            if Player.Admin or self.isMod(id):
                DataStore.Flush("duelusedtp")
                Player.MessageFrom(self.sys, "Flushed!")
        elif cmd == "dleave":
            if DataStore.Get("induel", Player.SteamID):
                Player.Kill()
                Player.MessageFrom(self.sys, "" + gr + "You are not in Duel anymore!")
                DataStore.Remove("induel", Player.SteamID)


    def On_PlayerKilled(self, DeathEvent):
        attacker = DeathEvent.Attacker
        victim = DeathEvent.Victim
        if DeathEvent.AttackerIsPlayer and DeathEvent.VictimIsPlayer and DeathEvent.Attacker is not None and DeathEvent.Victim is not None:
            if DataStore.Get("induel", attacker.SteamID) and DataStore.Get("induel", victim.SteamID):
                if victim == attacker:
                    Server.BroadcastFrom("[Düello]","[color #bf4d35]" + victim.Name + " did a nice Suicide while he/she was in Duel ;)")
                    victim.MessageFrom(self.sys, "[color #9ff3e9]There is no fear Bro =)Lets Try it Again")
                    self.Cloth(victim)
                    self.StartDuel(victim)
                else:
                    Server.BroadcastFrom("[Düello]"," [color green] " + attacker.Name + "[color white] Wins Duel Against[color red] " + victim.Name + "!")
                    DataStore.Remove("induel", attacker.SteamID)
                    DataStore.Remove("induel", victim.SteamID)
                    self.UnRestrication(victim)
                    self.UnRestrication(attacker)
                    attacker.Kill()
                    attacker.MessageFrom(self.sys, "[color #9ff3e9]You Won!")