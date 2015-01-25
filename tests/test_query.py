from unittest import TestCase
import query

from threading import Thread
import socket

server_data = {
    '7 Days to Die': (
        'valve',
        b'\xff\xff\xff\xffI\x11[ff8000]8.6 Hunting Zone\x00Navezgane\x007DTD\x00\x00\x00\x00\x08\x18\x00dw\x00\x00Alpha 8.6\x00\xb1\xa8a\x074w\xfb3\x11@\x01ZombiesRun:0;Port:25000;IsDedicated:True;Version:Alpha 8.6;PlayerDamageGiven:0;BuildCreate:False;GameType:7DTD;CurrentPlayers:0\x00\xb2\xd6\x03\x00\x00\x00\x00\x00',
        {'hostname': '[ff8000]8.6 Hunting Zone', 'map': 'Navezgane', 'is_password': False, 'maxplayers': 24, 'players': 8},
    ),
    'ARMA 2': (
        'gamespy4',
        b'\x00\x04\x05\x06\x07splitnum\x00\x80\x00gamever\x001.62.95251\x00hostname\x00Another Gameservers.com server is born\x00mapname\x00\x00gametype\x00\x00numplayers\x000\x00numteams\x000\x00maxplayers\x0035\x00gamemode\x00openwaiting\x00timelimit\x000\x00password\x000\x00param1\x0030\x00param2\x0020\x00currentVersion\x00162\x00requiredVersion\x00162\x00mod\x00Arma 2;Arma 2: Operation Arrowhead;Arma 2: British Armed Forces (Lite);Arma 2: Private Military Company (Lite)\x00equalModRequired\x000\x00gameState\x001\x00dedicated\x001\x00platform\x00win\x00language\x0065545\x00difficulty\x003\x00mission\x00\x00gamename\x00arma2oapc\x00sv_battleye\x001\x00verifySignatures\x001\x00signatures\x00bi;bi2\x00modhash\x00PMC v. 1.02;BAF v. 1.03;01a7de012d75ad0f4adb45c885cb9c8ab2636963;\x00hash\x00CC15E928BA1CA9CA2CC5658BE67FE4AA642AE47F\x00reqBuild\x000\x00reqSecureId\x000\x00\x00\x01player_\x00\x00\x00team_\x00\x00\x00score_\x00\x00\x00deaths_\x00\x00\x00\x00\x02\x00',
        {'hostname': 'Another Gameservers.com server is born', 'map': 'Unknown', 'is_password': False, 'maxplayers': 35, 'players': 0},
    ),
    'ARMA 3': (
        'gamespy4',
        b'\x00\x04\x05\x06\x07splitnum\x00\x80\x00gamever\x001.18.124200\x00hostname\x00Another GameServers.com Hosted Server\x00mapname\x00\x00gametype\x00\x00numplayers\x000\x00numteams\x000\x00maxplayers\x0010\x00gamemode\x00openwaiting\x00timelimit\x000\x00password\x000\x00param1\x000\x00param2\x000\x00ver\x00118\x00requiredVersion\x00118\x00mod\x00Arma 3;Arma 3 Zeus\x00equalModRequired\x000\x00gameState\x001\x00dedicated\x001\x00platform\x00win\x00language\x0065545\x00difficulty\x000\x00mission\x00\x00gamename\x00arma3pc\x00sv_battleye\x001\x00verifySignatures\x002\x00signatures\x00a3\x00modhash\x00640c1f3bc04df148baa15cc5ba7ae7d55f37eeaf;\x00hash\x00327FC17A771AAE5AEB6430F98E206F3CCC507F20\x00reqBuild\x000\x00reqSecureId\x002\x00lat\x004194303\x00lng\x004194303\x00ISO2\x00\x00\x00\x01player_\x00\x00\x00team_\x00\x00\x00score_\x00\x00\x00deaths_\x00\x00\x00\x00\x02\x00',
        {'hostname': 'Another GameServers.com Hosted Server', 'map': 'Unknown', 'is_password': False, 'maxplayers': 10, 'players': 0},
    ),
    'Alien Swarm': (
        'valve',
        b'\xff\xff\xff\xffI\x11"[U.S.S.[Sulaco] AvP server | www.usssulaco.ru"\x00Pyramid\x00avp3\x00Aliens vs Predator\x00\xb8)\x07\x0c\x00dw\x00\x011.0.0.0\x00\xb1\x96i\x08$gm%\x11@\x01_3_687472640_0_12_1_0_1735255732_1_____________________________14000000c8000000000000000000000000000000e1d19f440000000000000000\x00\xb8)\x00\x00\x00\x00\x00\x00',
        {'hostname': '"[U.S.S.[Sulaco] AvP server | www.usssulaco.ru"', 'map': 'Pyramid', 'is_password': False, 'maxplayers': 12, 'players': 7},
    ),
    "America's Army 3": (
        'valve',
        b'\xff\xff\xff\xffI\x11[Honor Server] -=312th=- Dallas I\x00Alley\x00aa3game\x00America\'s Army 3.3\x00T3\x1c\x1a\x00dw\x00\x001.0.0.0\x00\xb1I"\x00\x94\x8c\xe23\x11@\x01M=vip;W=cloudy;T=day;P=0;C=0;pb=1;voip=1;ver=AA3.3.1;\x00T3\x00\x00\x00\x00\x00\x00',
        {'hostname': '[Honor Server] -=312th=- Dallas I', 'map': 'Alley', 'is_password': False, 'maxplayers': 26, 'players': 28},
    ),
    "America's Army: Proving Grounds": (
        'valve',
        b'\xff\xff\xff\xffI\x11-=312th=- / Dallas I\x00FLO_ThreeKings_AC\x00aa4game\x00America\'s Army: Proving Grounds\x00\x00\x00\x0c\x18\x00dw\x00\x001.0.0.0\x00\xb1I"\x00\xb8\x02\xd65\x11@\x01M=;ver=124855;T=Waiting For Players;VM=0;P=0;C=1;pb=1;voip=1;sm=396;HONOR=1;\x00\x1a\x1a\x03\x00\x00\x00\x00\x00',
        {'hostname': '-=312th=- / Dallas I', 'map': 'FLO_ThreeKings_AC', 'is_password': False, 'maxplayers': 24, 'players': 12},
    ),
    'Battlefield 1942': (
        'gamespy1',
        b'\\averageFPS\\0\\content_check\\2\\dedicated\\2\\gameId\\bf1942\\gamemode\\openplaying\\gametype\\conquest\\hostname\\ --=[ aX ]=-- (CD and Origin)\\hostport\\14567\\mapId\\BF1942\\mapname\\iwo jima\\maxplayers\\64\\numplayers\\42\\password\\0\\reservedslots\\0\\roundTime\\2700\\roundTimeRemain\\2424\\status\\4\\sv_punkbuster\\0\\tickets1\\925\\tickets2\\886\\unpure_mods\\\\version\\v1.612\\final\\\\queryid\\347.1',
        {'hostname': ' --=[ aX ]=-- (CD and Origin)', 'map': 'iwo jima', 'is_password': False, 'maxplayers': 64, 'players': 42},
    ),
    'Battlefield 2': (
        'gamespy3',
        b'\x00\x04\x05\x06\x07splitnum\x00\x80\x00hostname\x00Another Gameservers.com Server is Born\x00gamename\x00battlefield2\x00gamever\x001.5.3153-802.0\x00mapname\x00Strike At Karkand\x00gametype\x00gpm_cq\x00gamevariant\x00bf2\x00numplayers\x000\x00maxplayers\x0032\x00gamemode\x00openplaying\x00password\x000\x00timelimit\x000\x00roundtime\x003\x00hostport\x0016567\x00bf2_dedicated\x001\x00bf2_ranked\x001\x00bf2_anticheat\x001\x00bf2_os\x00win32\x00bf2_autorec\x000\x00bf2_d_idx\x00http://\x00bf2_d_dl\x00http://\x00bf2_voip\x001\x00bf2_autobalanced\x000\x00bf2_friendlyfire\x001\x00bf2_tkmode\x00Punish\x00bf2_startdelay\x0015\x00bf2_spawntime\x0015.000000\x00bf2_sponsortext\x00\x00bf2_sponsorlogo_url\x00\x00bf2_communitylogo_url\x00\x00bf2_scorelimit\x000\x00bf2_ticketratio\x00100\x00bf2_teamratio\x00100.000000\x00bf2_team1\x00MEC\x00bf2_team2\x00US\x00bf2_bots\x000\x00bf2_pure\x001\x00bf2_mapsize\x0032\x00bf2_globalunlocks\x001\x00bf2_fps\x00\x00bf2_plasma\x000\x00bf2_reservedslots\x000\x00bf2_coopbotratio\x00\x00bf2_coopbotcount\x00\x00bf2_coopbotdiff\x00\x00bf2_novehicles\x000\x00\x00\x01player_\x00\x00\x00score_\x00\x00\x00ping_\x00\x00\x00team_\x00\x00\x00deaths_\x00\x00\x00pid_\x00\x00\x00skill_\x00\x00\x00AIBot_\x00\x00\x00\x00\x02team_t\x00\x00MEC\x00US\x00\x00score_t\x00\x000\x000\x00\x00\x00',
        {'hostname': 'Another Gameservers.com Server is Born', 'map': 'Strike At Karkand', 'is_password': False, 'maxplayers': 32, 'players': 0},
    ),
    'Call of Duty': (
        'quake3',
        b'\xff\xff\xff\xffstatusResponse\n\\^2Location\\^1New York\\^2Owner\\^2<^7endless^2> ^0clan\\^2Website\\endless^2-^7clan^2.com\\g_gametype\\tdm\\gamename\\Call of Duty\\mapname\\mp_carentan\\protocol\\1\\psv_powerserver\\1\\shortversion\\1.1\\sv_allowAnonymous\\0\\sv_floodProtect\\1\\sv_hostname\\ ^2<^7endless^2> ^7TDM\\sv_maxclients\\46\\sv_maxPing\\500\\sv_maxRate\\25000\\sv_minPing\\0\\sv_privateClients\\2\\sv_pure\\0\\pswrd\\0\n9 118 "DaN"\n0 999 "eze gran amigo de tablonn"\n5 287 "^^54Striker ^^01Eureka ^^66Evo"\n13 241 "F-Brasil                     77"\n1 167 "BAYRON"\n14 221 "Mr Clutch 971"\n13 203 "MARIE_12"\n15 168 "^^44G^^11o^^33o^^44g^^22l^^11e"\n9 325 "Pvt. Drake"\n13 115 "^4Me :)"\n0 151 "SEBAX1999"\n0 277 "A.R.G//leg@lice (c.a.r.p)      "\n28 151 "dR-mR"\n1 100 "Altair"\n20 224 "^^33el taxy"\n7 227 "^-I n V i C t u $*"\n0 121 "Endlosleben"\n3 178 "alferez mario"\n9 29 "WAKKO55555555555555555555555555"\n10 145 "Chuy Rolando"\n0 128 "Lord              9999999999999"\n6 153 "^6***bad-girl***"\n0 198 "Whattevahhh"\n11 175 "www_pl"\n10 124 "General Erwin Rommel"\n20 153 "Psyke"\n4 338 "yo XD"\n2 235 "alfer97                        "\n41 98 "^2MASTR p "\n9 308 "Possum21"\n',
        {'hostname': ' ^2<^7endless^2> ^7TDM', 'map': 'mp_carentan', 'is_password': False, 'maxplayers': 46, 'players': 30},
    ),
    'Call of Duty 2': (
        'quake3',
        b'\xff\xff\xff\xffstatusResponse\n\\_Admin_1\\^3IAF ^5Sexy ^8Dirty ^3Sniper\\_Admin_2\\^3IAF ^1Lost^3Com\\_Admin_3\\^3IAF ^1KILLI^7NGMA^4CHINE^7\\_Clan\\^5IAF\\_Location\\International\\_Maps\\^3Custom\\_Mod\\^5IAF ^3Custom ^3e^1X^3treme^2+\\_ModUpdate\\October 2013\\_ModVer\\^2v2.9+ custom\\_TeamSpeak3_IP\\216.52.148.11:9810\\_Website\\^3www.IAOFF.com\\fs_game\\IAF_SDS29v7\\g_antilag\\0\\g_gametype\\tdm\\gamename\\Call of Duty 2\\mapname\\mp_subharbor\\protocol\\118\\shortversion\\1.3\\sv_allowAnonymous\\0\\sv_floodProtect\\1\\sv_hostname\\^5IAF ^3Custom^7#1 ^3e^1X^3treme^2+ ^7v2.9+   ^3[www.IAOFF.com]\\sv_maxclients\\50\\sv_maxPing\\400\\sv_maxRate\\25000\\sv_minPing\\0\\sv_privateClients\\0\\sv_punkbuster\\0\\sv_pure\\1\\sv_voice\\0\\pswrd\\0\\mod\\1\n75 125 "RealLittleMack"\n0 999 "^4\xbbMichelle\xab"\n0 999 "Leopard88"\n0 66 "Amex"\n0 165 "Eierfeile"\n50 112 "^2Sparty"\n0 999 "JungleJohn"\n20 18 "^9[^1OUT^9LAW^1]^9HELL^1Razor"\n0 101 "Nukin\'"\n0 999 "powerpeter"\n0 999 "WERTEX33"\n10 67 "^9[^1OUT^9LAW^1]^9xray^1girl^7"\n0 70 "benito"\n0 999 "^2Replicant^3X"\n0 126 "^4I^3A^4F OLDMAN"\n10 136 "JimmyJohnson"\n0 244 "^4I^3A^4F R^3o^4adR^3u^4nner"\n0 999 "Dino"\n0 999 "Hegal"\n0 73 "^3 I Can\'t See You ^1-____-"\n0 999 "^4Killer350"\n0 999 "LtGenJackONeill"\n0 83 "Private Lazlo"\n25 50 "Bambino"\n40 46 "ToTheMoon^9Alice"\n0 999 "^^1MD^^1Scidadle"\n0 34 "Dogface"\n20 53 "HanoiMcCoy66"\n0 999 "POLYnation"\n0 999 "zaghiman"\n10 55 "^3IAOFF.com ^7\xbb ^9IAF Guest1"\n0 43 "Broken Heart"\n0 162 "^1IAF ^7shake[J^1P^7N]"\n0 63 " ^2IAF MATRIX"\n0 999 "kasakasakasa"\n',
        {'hostname': '^5IAF ^3Custom^7#1 ^3e^1X^3treme^2+ ^7v2.9+   ^3[www.IAOFF.com]', 'map': 'mp_subharbor', 'is_password': False, 'maxplayers': 50, 'players': 35},
    ),
    'Call of Duty 4': (
        'quake3',
        b'\xff\xff\xff\xffstatusResponse\n\\sv_punkbuster\\0\\sv_maxclients\\50\\shortversion\\1.7\\protocol\\6\\sv_privateClients\\0\\sv_hostname\\^5[AR51] ^3CRK #1 HardCore Full2 AntiDDOS ^5By WWW.AR51.EU\\sv_minPing\\0\\sv_maxPing\\0\\sv_disableClientConsole\\0\\sv_voice\\1\\g_gametype\\war\\mapname\\mp_creek\\sv_maxRate\\20000\\sv_floodprotect\\4\\sv_pure\\1\\_Admin\\Kevin & Cybersonic\\_Email\\cybersonic@team-area51.net\\_Website\\www.team-area51.net\\_Comment\\Serveur offre Kimsufi.com\\scr_ar51_hud\\1\\scr_ar51_hudpos\\BOTTOMLEFT\\gamename\\Call of Duty 4\\g_compassShowEnemies\\0\\Patch_by\\www.ar51.eu\\Patch_by_2014\\www.ar51.eu\\AR51NoNameStealing\\1\\AR51GuidCheck\\1\\AR51AntiAimbot\\1\\AR51AntiNadeSwitching\\1\n20 82 "PAPA"\n72 63 "DJA"\n50 49 "daske82 (CRO)"\n20 125 "[Cel\' Razgrom]"\n50 17 "digit"\n80 45 "MadMax"\n20 72 "Juba"\n0 -1 "Gurolock"\n20 72 "Ammy"\n30 122 "Nero"\n32 52 "Art"\n0 37 "Martinez"\n60 52 "Herowz"\n26 61 "samir   "\n20 55 "loUkAS"\n0 158 "jose"\n20 123 "Spongebob"\n50 177 "fyxqjy"\n0 35 "Przemek"\n30 46 "Damage"\n50 55 "Uri"\n62 116 "<Z/E/U/S>FEKA23"\n40 68 "2nd 2nd 2nd NoDev"\n10 101 "Broseidon"\n80 203 "Franco"\n52 66 "Maximus"\n0 58 "cazamia"\n50 31 "Valar"\n10 38 "3l_PuToGnOmO"\n40 53 "DevilTEO"\n10 154 "wawd"\n10 40 "DID"\n',
        {'hostname': '^5[AR51] ^3CRK #1 HardCore Full2 AntiDDOS ^5By WWW.AR51.EU', 'map': 'mp_creek', 'is_password': False, 'maxplayers': 50, 'players': 32},
    ),
    'Call of Duty World at War': (
        'quake3',
        b'\xff\xff\xff\xffstatusResponse\n\\fxfrustumCutoff\\1000\\g_compassShowEnemies\\0\\g_gametype\\tdm\\gamename\\Call of Duty: World at War\\mapname\\mp_stalingrad\\penetrationCount\\5\\protocol\\101\\r_watersim_enabled\\1\\shortversion\\1\\sv_allowAnonymous\\0\\sv_disableClientConsole\\0\\sv_floodprotect\\4\\sv_hostname\\^1=[^3JFF^1]= ^3Cracked ^1Server ^3#1\\sv_maxclients\\40\\sv_maxPing\\500\\sv_maxRate\\25000\\sv_minPing\\0\\sv_privateClients\\4\\sv_punkbuster\\0\\sv_pure\\1\\sv_voice\\0\\ui_maxclients\\64\\pswrd\\0\\mod\\0\n30 144 "Expediential"\n28 247 "bebop"\n195 63 "RomanTheSnowman"\n31 286 "MOTHER FUCK JONES"\n108 162 "MajorCojones"\n22 226 "Samuelsniper"\n58 240 "Hassan Camp"\n80 213 "Traitor_Joe"\n20 92 "[nost]Adison"\n0 177 "[HERO]004michael"\n36 87 "Drini"\n73 40 "ppc1on"\n125 296 "Prof. UKELELE"\n0 234 "Airenal14"\n112 76 "Bossferatu"\n20 51 "Haarlekin69"\n',
        {'hostname': '^1=[^3JFF^1]= ^3Cracked ^1Server ^3#1', 'map': 'mp_stalingrad', 'is_password': False, 'maxplayers': 40, 'players': 16},
    ),
    'Call of Duty: Modern Warfare 3': (
        'valve',
        b'\xff\xff\xff\xffI\x11!   !   !   !^3WWW.^2MB2.^3CZ\x00Mission\x00modernwarfare3\x00MW3 Game Description\x00\xc2\xa6\x00\x12\x00dw\x00\x011.0.0.1\x00\xb1\x82u\x02\xd0\xd9@ \x11@\x01gn\\IW5\\gt\\war\\hc\\0\\pu\\0\\m\\mp_bravo\\px\\\\pn\\\\mr\\\\pc\\0\\ff\\0\\fg\\\\md\\\\kc\\1\\ac\\1\\d\\2\\qp\\30081\\vo\\1\\\x00\xc2\xa6\x00\x00\x00\x00\x00\x00',
        {'hostname': '!   !   !   !^3WWW.^2MB2.^3CZ', 'map': 'Mission', 'is_password': False, 'maxplayers': 18, 'players': 0},
    ),
    'Centration': (
        'valve',
        b'\xff\xff\xff\xffI\x11Official Contagion - NY Server CE_BarloweSquare #1\x00ce_barlowesquare\x00contagion\x00Contagion\x00\x00\x00\x08\x08\x00dw\x00\x012.0.9.4\x00\xb1\x87i\x04\x84O?0\x11@\x01secure\x00^\xa3\x03\x00\x00\x00\x00\x00',
        {'hostname': 'Official Contagion - NY Server CE_BarloweSquare #1', 'map': 'ce_barlowesquare', 'is_password': False, 'maxplayers': 8, 'players': 8},
    ),
    'Counter-Strike 1.6': (
        'valve',
        b'\xff\xff\xff\xffm127.0.0.1:27015\x00ZmOldSchool.CsBlackDevil.Com [Zombie Plauge]\x00zm_2day\x00cstrike\x00Counter-Strike\x00  /dl\x00\x01\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x01\x00\x01\x00',
        {'hostname': 'ZmOldSchool.CsBlackDevil.Com [Zombie Plauge]', 'map': 'zm_2day', 'is_password': False, 'maxplayers': 32, 'players': 32},
    ),
    'Counter-Strike Global Offensive': (
        'valve',
        b'\xff\xff\xff\xffI\x11OG:\\\\ NewbSurf #3 [Tier 1-2] OpiumGaming.com\x00surf_mesa\x00csgo\x00Counter-Strike: Global Offensive\x00\xda\x02((\x00dl\x00\x011.33.4.0\x00\xa1\x87iOpiumGaming.com,bhop,chicago,fastdl,og,rank,record,respawn,skill,surf,timer,secure\x00\xda\x02\x00\x00\x00\x00\x00\x00',
        {'hostname': 'OG:\\\\ NewbSurf #3 [Tier 1-2] OpiumGaming.com', 'map': 'surf_mesa', 'is_password': False, 'maxplayers': 40, 'players': 40},
    ),
    'Counter-Strike: Condition Zero': (
        'valve',
        b'\xff\xff\xff\xffm127.0.0.1:27018\x00UGC | Dust2 #1 24/7 | UGC-Gaming.net\x00de_dust2_cz\x00czero\x00<------------------------------\x00\x19 /dl\x00\x01\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x01\x00\x01\x00',
        {'hostname': 'UGC | Dust2 #1 24/7 | UGC-Gaming.net', 'map': 'de_dust2_cz', 'is_password': False, 'maxplayers': 32, 'players': 25},
    ),
    'Counter-Strike: Source': (
        'valve',
        b'\xff\xff\xff\xffI\x11[GFLClan.com]24/7 ZOMBIE ESCAPE |Rank|NoBlock|FastDL|Chicago\x00ze_death_star_escape_v4_3\x00cstrike\x00Counter-Strike: Source\x00\xf0\x00?@\x00dl\x00\x012230303\x00\xb1\x89i\x05(\xc142\x11@\x01alltalk,awesome,bunnyhopping,escape,games,gfl,gl,gravity,increased_maxplayers,life,startmoney,ze,zm,zombie,zombie escape\x00\xf0\x00\x00\x00\x00\x00\x00\x00',
        {'hostname': '[GFLClan.com]24/7 ZOMBIE ESCAPE |Rank|NoBlock|FastDL|Chicago', 'map': 'ze_death_star_escape_v4_3', 'is_password': False, 'maxplayers': 64, 'players': 63},
    ),
    'DOTA 2': (
        'valve',
        b'\xff\xff\xff\xffI\x11Valve Dota 2 Singapore Server (srcds144.153.29)\x00dota\x00dota\x00Dota 2\x00:\x02\t\x1f\x00dl\x00\x0140\x00\xf1\xa3i\x07$^\xe53\x11@\x01\x90m\x00empty\x00:\x02\x00\x00\x00\x00\x00\x00',
        {'hostname': 'Valve Dota 2 Singapore Server (srcds144.153.29)', 'map': 'dota', 'is_password': False, 'maxplayers': 31, 'players': 9},
    ),
    'Day of Defeat': (
        'valve',
        b'\xff\xff\xff\xffm127.0.0.1:27011\x00\xe3\x80\x90\xe8\x93\x9d\xe6\xb5\xb7\xe6\x88\x98\xe9\x98\x9f01\xe3\x80\x91\xe6\xb7\xb7\xe6\x88\x98-\xe5\xa4\x9a\xe5\xbc\xb9\xe5\xa4\xb93\xe6\x89\x8b\xe9\x9b\xb7\x00dod_assault2\x00dod\x00www.dod168.com\xe5\xae\x98\xe7\xbd\x91\x00\x1d /dw\x00\x01\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x01\x00\x01\x00',
        {'hostname': '【蓝海战队01】混战-多弹夹3手雷', 'map': 'dod_assault2', 'is_password': False, 'maxplayers': 32, 'players': 29},
    ),
    'Day of Defeat: Source': (
        'valve',
        b'\xff\xff\xff\xffI\x11     24/7 =(eGO)= AVALANCHE NO BOTS! | GameME\x00dod_avalanche\x00dod\x00Day of Defeat: Source\x00,\x01\x1e \x00dw\x00\x012230303\x00\xb1\x87i\x02\xb8\x03\xde.\x11@\x01fadetoblack,gameME\x00,\x01\x00\x00\x00\x00\x00\x00',
        {'hostname': '     24/7 =(eGO)= AVALANCHE NO BOTS! | GameME', 'map': 'dod_avalanche', 'is_password': False, 'maxplayers': 32, 'players': 30},
    ),
    'DayZ': (
        'valve',
        b"\xff\xff\xff\xffI\x11Drunken Bastards - 24/7 Day - 2hr restart - Everybody Welcome\x00DayZ_Auto\x00dayz\x00DayZ\x00\x00\x00'(\x00dw\x00\x010.45.124426\x00\xb1\xfe\x08\x02xD\x144\x11@\x01battleye,15:24\x00\xac_\x03\x00\x00\x00\x00\x00",
        {'hostname': 'Drunken Bastards - 24/7 Day - 2hr restart - Everybody Welcome', 'map': 'DayZ_Auto', 'is_password': False, 'maxplayers': 40, 'players': 39},
    ),
    'F.E.A.R.': (
        'gamespy2',
        b'\x00CORYhostname\x00=MXT=CTF Server\x00gamever\x00FEAR v1.08\x00mapname\x00[SEC2] - MXTTrollHouse\x00gametype\x00CTF\x00gamevariant\x00-archcfg Retail\x00numplayers\x0017\x00numteams\x000\x00maxplayers\x0018\x00gamemode\x00SEC2 v2.0.1 (Mar  1 2014 - 11:00:56)\x00fraglimit\x005\x00timelimit\x0015\x00password\x000\x00gsgamename\x00fear\x00mappath\x00\x00options\x00(0)(1.4);(3)(0);(6)(0.0);(7)(1.0);(8)(5);(9)(15);(10)(2);(12)(1);(20)(18);(23)(2);(25)(0);(26)(0);(27)(1);(32)(10);(46)(5);(48)(1000);(49)(20);(51)(700);(52)(35);(54)(100);(55)(15);(57)(25);(59)(15);(61)(95);(63)(8);(64)(20);(66)(15);(67)(1.0);(84)(QuarterRound);(85)(MapChange);(86)(2.0);(87)(5);(88)(10)\x00hasoverrides\x000\x00downloadablefiles\x00\x00overridesdata\x00\x00dedicated\x001\x00linux\x001\x00punkbuster\x000\x00\x00',
        {'hostname': '=MXT=CTF Server', 'map': '[SEC2] - MXTTrollHouse', 'is_password': False, 'maxplayers': 18, 'players': 17},
    ),
    "Garry's Mod": (
        'valve',
        b'\xff\xff\xff\xffI\x11DarkRP Reloaded | [M9K|Custom|Cars|Jobs|Casino|Drugs]  UPDATED\x00rp_downtown_v4c_v2_drp_ext\x00garrysmod\x00DarkRP\x00\xa0\x0fCa\x00dw\x00\x0114.04.19\x00\xb1\x87i\t\xb0\xd8\x983\x11@\x01 gm:darkrp\x00\xa0\x0f\x00\x00\x00\x00\x00\x00',
        {'hostname': 'DarkRP Reloaded | [M9K|Custom|Cars|Jobs|Casino|Drugs]  UPDATED', 'map': 'rp_downtown_v4c_v2_drp_ext', 'is_password': False, 'maxplayers': 97, 'players': 67},
    ),
    'Half-Life 1': (
        'valve',
        b'\xff\xff\xff\xffm127.0.0.1:27015\x00! !--Good_Half-Life_Server--! !\x00crossfire\x00valve\x00Half-Life\x00\x0b /dw\x00\x01\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x01\x00\x01\x01',
        {'hostname': '! !--Good_Half-Life_Server--! !', 'map': 'crossfire', 'is_password': False, 'maxplayers': 32, 'players': 11},
    ),
    'Half-Life 2: Deathmatch': (
        'valve',
        b'\xff\xff\xff\xffI\x11-=24/7 BATTLEGROUND *HARDCORE*=-\x00aoc_battleground\x00ageofchivalry\x00Age of Chivalry\x00fD\x12 \x00dl\x00\x011.0.0.6\x00\xb1\x87i\x00|\xe3\x04(\x11@\x01HLstatsX:CE,increased_maxplayers\x00fD\x00\x00\x00\x00\x00\x00',
        {'hostname': '-=24/7 BATTLEGROUND *HARDCORE*=-', 'map': 'aoc_battleground', 'is_password': False, 'maxplayers': 32, 'players': 18},
    ),
    'Halo': (
        'gamespy2',
        b'\x00CORYhostname\x00~  BLOODY GULCH - www.bloodygulch.info\x00gamever\x0001.00.04.0607\x00hostport\x00\x00maxplayers\x0016\x00password\x000\x00mapname\x00bloodgulch\x00dedicated\x001\x00gamemode\x00openplaying\x00game_classic\x000\x00numplayers\x0016\x00gametype\x00CTF\x00teamplay\x001\x00gamevariant\x00wow\x00fraglimit\x005\x00player_flags\x001629863940,1094\x00game_flags\x0097\x00\x00',
        {'hostname': '~  BLOODY GULCH - www.bloodygulch.info', 'map': 'bloodgulch', 'is_password': False, 'maxplayers': 16, 'players': 16},
    ),
    'Homefront': (
        'valve',
        b'\xff\xff\xff\xffI\x07!Crywars.de TDM\x00FL-LOWLANDS\x00homefront.1.5.500001\x00Homefront\x00<\xd7\x00 \x00dw\x00\x011.5.500001\x00\xb1\x88i\x05\x88uJ0\x11@\x01 s1 306 s2 1 s3 2 s4 1 s5 0 s10 3 s11 0 s12 0\x00<\xd7\x00\x00\x00\x00\x00\x00',
        {'hostname': '!Crywars.de TDM', 'map': 'FL-LOWLANDS', 'is_password': False, 'maxplayers': 32, 'players': 0},
    ),
    'Insurgency': (
        'valve',
        b'\xff\xff\xff\xffI\x11http://xFLOWservers.COM PVP [GAMEME][LOSANGELES] 1\x00district\x00insurgency\x00Insurgency\x00\x00\x00\x1b \x00dl\x00\x011.2.1.9\x00\xb1\x87i\x08\xf0\r 1\x11@\x01firefight,mm:pvp,theater:default,mcl2445,nwibanlist,nospawnprotection,\x00\xa0f\x03\x00\x00\x00\x00\x00',
        {'hostname': 'http://xFLOWservers.COM PVP [GAMEME][LOSANGELES] 1', 'map': 'district', 'is_password': False, 'maxplayers': 32, 'players': 27},
    ),
    'Insurgency Standalone': (
        'valve',
        b'\xff\xff\xff\xffI\x11-SD- Adversarial Fun House!\x00buhriz\x00insurgency\x00Insurgency\x00\x00\x00\x00 \x00dl\x00\x011.2.1.9\x00\xb1\x87i\x03x\xb0\x1c\x12\x11@\x01push,mm:pvp,theater:default,mcl2445,nwibanlist,empty,\x00\xa0f\x03\x00\x00\x00\x00\x00',
        {'hostname': '-SD- Adversarial Fun House!', 'map': 'buhriz', 'is_password': False, 'maxplayers': 32, 'players': 0},
    ),
    'Just Cause 2: Multiplayer': (
        'valve',
        b'\xff\xff\xff\xffI\x11Hasbo\'s FREEROAM|FREE STORE|WARP|TP\x00Players: 11/5000\x00jc2mp\x00Just Cause 2: Multiplayer Mod\x00\x00\x00\x00\x01\x00dl\x00\x001.0.0.0\x00\x91a\x1e\x03x\x9f\xc9"\x11@\x01\x08\xf4\x03\x00\x00\x00\x00\x00',
        {'hostname': "Hasbo's FREEROAM|FREE STORE|WARP|TP", 'map': 'Unknown', 'is_password': False, 'maxplayers': 5000, 'players': 11},
    ),
    'Killing Floor': (
        'gamespy1',
        b'\\hostname\\ZOMBIEMANIYA#2|V.1058|TOTALLINE|0-255lvl\\hostport\\7707\\maptitle\\Untitled\\mapname\\KF-LOTD-TheaterZM\\gametype\\UZGameType\\numplayers\\12\\maxplayers\\50\\gamemode\\openplaying\\gamever\\3339\\minnetver\\3180\\queryid\\39.1\\final\\',
        {'hostname': 'ZOMBIEMANIYA#2|V.1058|TOTALLINE|0-255lvl', 'map': 'KF-LOTD-TheaterZM', 'is_password': False, 'maxplayers': 50, 'players': 12},
    ),
    'Left 4 Dead': (
        'valve',
        b'\xff\xff\xff\xffI\x07COOP`16 Paradis [l4dZone.ru]\x00l4d_airport01_greenhouse\x00left4dead\x00L4D - Co-op - Normal\x00\xf4\x01\x00\x10\x00dl\x00\x001.0.2.9\x00\xa0bjempty,no-steam\x00',
        {'hostname': 'COOP`16 Paradis [l4dZone.ru]', 'map': 'l4d_airport01_greenhouse', 'is_password': False, 'maxplayers': 16, 'players': 0},
    ),
    'Left 4 Dead 2': (
        'valve',
        b'\xff\xff\xff\xffI\x11ZambiLand 13vs13 [2.1.2.5]\x00c5m1_waterfront\x00left4dead2\x00Left 4 Dead 2\x00&\x02\x14\x1b\x00dl\x00\x012.1.2.5\x00\xb1\x87i\x07H\x1b\x053\x11@\x01versus,increased_maxplayers,loot,no-steam,rank,secure\x00&\x02\x00\x00\x00\x00\x00\x00',
        {'hostname': 'ZambiLand 13vs13 [2.1.2.5]', 'map': 'c5m1_waterfront', 'is_password': False, 'maxplayers': 27, 'players': 20},
    ),
    'Medal of Honor Allied Assault': (
        'gamespy1',
        b'\\gamemode\\openplaying\\maxplayers\\50\\numplayers\\33\\gametype\\Capture-The-Flag\\mapname\\obj/obj_team2\\hostport\\12203\\hostname\\{AB} v2 Sniper/Rifle Only\\final\\\\queryid\\792.1',
        {'hostname': '{AB} v2 Sniper/Rifle Only', 'map': 'obj/obj_team2', 'is_password': False, 'maxplayers': 50, 'players': 33},
    ),
    'Medal of Honor Spearhead': (
        'gamespy1',
        b'\\pure\\0\\realism\\1\\sprinton\\1\\dedicated\\1\\gametype_i\\2\\gamemode\\openplaying\\maxplayers\\26\\numplayers\\19\\gametype\\Countdown X 2.1\\mapname\\mohdm3\\hostport\\12203\\hostname\\[=CDX=] COUNTDOWN X\\final\\\\queryid\\459070.1',
        {'hostname': '[=CDX=] COUNTDOWN X', 'map': 'mohdm3', 'is_password': False, 'maxplayers': 26, 'players': 19},
    ),
    'Minecraft': (
        'gamespy4',
        b'\x00\x04\x05\x06\x07splitnum\x00\x80\x00hostname\x00\xa7f\xa7k.:\xa7b\xa7lGC\xa79\xa7l2\xa7f\xa7k:. \xa79\xa7l:\xa7f\xa7lSKYBLOCK\xa7b\xa7l :\xa79\xa7l:\xa7b\xa7l: \xa7f\xa7lFRAKCJE\xa79\xa7l:\xa7l           \xa7c\xa7lPobierz MC 1.7.4 tutaj: \xa7a\xa7lwww.gc2.pl                        \xa7f\xa7l[\xa7a\xa7l1\xa7f.\xa7a\xa7l7\xa7f.\xa7a\xa7lX\xa7f\xa7l]\x00gametype\x00SMP\x00game_id\x00MINECRAFT\x00version\x001.7.9\x00plugins\x00\x00map\x00BungeeCord_Proxy\x00numplayers\x0023\x00maxplayers\x002000\x00hostport\x0025565\x00hostip\x0094.23.93.10\x00\x00\x01player_\x00\x00Paco0403\x00destruyenex\x00jovan\x00Kirssika\x00trutru9\x00walterhabib18\x00gadi\x00BanG\x00arcoirisnp9\x00nestino\x00adameczek11\x00seba\x00barush\x00leka98\x00fionn_bennis\x00lodzikaaa\x00kubson\x00basti2014\x00McPatoo\x00nico2014\x00PelaoCTM\x00Jones2008\x00BoobsMen\x00\x00',
        {'hostname': '§f§k.:§b§lGC§9§l2§f§k:. §9§l:§f§lSKYBLOCK§b§l :§9§l:§b§l: §f§lFRAKCJE§9§l:§l           §c§lPobierz MC 1.7.4 tutaj: §a§lwww.gc2.pl                        §f§l[§a§l1§f.§a§l7§f.§a§lX§f§l]', 'map': 'BungeeCord_Proxy', 'is_password': False, 'maxplayers': 2000, 'players': 23},
    ),
    'Natural Selection 2': (
        'valve',
        b'\xff\xff\xff\xffI\x11Combat MOD+ IBISGaming.com (LagFREE)\x00ns2_co_pulse\x00naturalselection2\x00Natural Selection 2\x008\x13\x15\x17\x00lw\x00\x011.0.0.0\x00\xb1\x87i\x00tM\xa13\x11@\x01266|combat|M|143|rookie|R_S1|shine|P_S0\x008\x13\x00\x00\x00\x00\x00\x00',
        {'hostname': 'Combat MOD+ IBISGaming.com (LagFREE)', 'map': 'ns2_co_pulse', 'is_password': False, 'maxplayers': 23, 'players': 21},
    ),
    'Quake 3': (
        'quake3',
        b'\xff\xff\xff\xffstatusResponse\n\\sv_maxclients\\32\\server_freezetag\\1\\sv_hostname\\{CROM} FREEZE\\sv_maxRate\\25000\\sv_minPing\\0\\sv_maxPing\\0\\sv_floodProtect\\1\\dmflags\\0\\fraglimit\\20\\timelimit\\20\\capturelimit\\8\\version\\Q3 1.32c linux-i386 May  8 2006\\sv_punkbuster\\0\\protocol\\68\\g_gametype\\3\\mapname\\q3dm9\\sv_privateClients\\0\\sv_allowDownload\\0\\bot_minplayers\\2\\.Administrator\\Kal\\.E-mail\\admin@cromctf.com\\.IRC\\#crom @ irc.enterthegame.com\\.Location\\Chicago, IL\\.Website\\www.cromctf.com\\g_needpass\\0\\gamename\\freeze\\gameversion\\OSP v1.03a\\Score_Blue\\3 \\Score_Red\\3 \\Players_Blue\\0 2 4 6 8 \\Players_Red\\1 3 5 7 9 \\Score_Time\\10:51\\server_ospauth\\0\\server_promode\\0\n0 16 "Cloud9"\n21 21 "^1l^7*^1l^7fugs.^1spot"\n0 38 "Doc"\n32 32 "^0tr^7!^0umph"\n0 11 "loser"\n0 12 "killMEnow"\n0 8 "Best.Freezer!"\n-1 22 "UnnamedPlayer"\n19 21 "^8UnnamedPlayer"\n0 21 "^2Justy"\n0 34 "^1Killer-Face"\n0 57 "S1812JM"\n0 27 "weeman"\n0 46 "ping?"\n0 23 "Harpoon"\n3 21 "^1l^7*^1l^7S^1g^7t^1.^7Gum^1b^7y"\n0 66 "crunk"\n0 53 "^5Icey"\n0 20 "^1BOB^3M4R^2L3Y"\n0 40 "6201"\n7 67 "^2Sha^0row"\n20 43 "^al^o*^al^oJorge^a.Colombi^o@"\n0 31 "Snippet"\n0 17 "hoedown"\n16 28 "^5War_spinal"\n19 10 "^b^B^7EnDU^N^1R^b^B^7AnCE"\n1 20 "^2*VIP*^1^F^4CHIVITO"\n',
        {'hostname': '{CROM} FREEZE', 'map': 'q3dm9', 'is_password': False, 'maxplayers': 32, 'players': 27},
    ),
    'Red Orchestra': (
        'gamespy1',
        b'\\hostname\\\xa0\xa0\xa0\xa0[REDORCHESTRA.RU]\xa0Russian\xa0Community\xa0Server\xa0by\xa0[GMNET.RU]\\hostport\\7757\\maptitle\\Roadblock\\mapname\\RO-Roadblock_X5\\gametype\\ROKDTeamGame\\numplayers\\20\\maxplayers\\50\\gamemode\\openplaying\\gamever\\3339\\minnetver\\3180\\queryid\\30.1\\final\\',
        {'hostname': '    [REDORCHESTRA.RU] Russian Community Server by [GMNET.RU]', 'map': 'RO-Roadblock_X5', 'is_password': False, 'maxplayers': 50, 'players': 20},
    ),
    'Red Orchestra 2': (
        'valve',
        b'\xff\xff\xff\xffI\x11[2.FJg] HOS - Tactical Realism\x00TE-Bridges_of_Druzhina_MCP\x00ro2\x00Red Orchestra 2\x00z\x8aF@\x00lw\x00\x012.0.0.15\x00\xb1a\x1e\x03\xe0:")\x11@\x01a:64,s:2,b:1,e:1,m:0,h:1,c:0,d:0,n:0,o:0,i:1,g:0,k:100,j:0,t:100,r:0,u:0,f:0,l:,p:0,q:,\x00z\x8a\x00\x00\x00\x00\x00\x00',
        {'hostname': '[2.FJg] HOS - Tactical Realism', 'map': 'TE-Bridges_of_Druzhina_MCP', 'is_password': False, 'maxplayers': 64, 'players': 70},
    ),
    'Rust': (
        'valve',
        b'\xff\xff\xff\xffI\x116-21 | BATTLEFIELD | NOLAG | KEVLAR/M4 | TP\x00rust_island_2013\x00rust\x00Rust Server\x00\x00\x00Sd\x00lw\x00\x011069\x00\xb1\x84m\x07T\xef\xc63\x11@\x01rust,modded,oxide,cp83,mp100,v1069\x00J\xda\x03\x00\x00\x00\x00\x00',
        {'hostname': '6-21 | BATTLEFIELD | NOLAG | KEVLAR/M4 | TP', 'map': 'rust_island_2013', 'is_password': False, 'maxplayers': 100, 'players': 83},
    ),
    'SWAT 4': (
        'gamespy2',
        b'\x00CORYhostname\x00[C=FFFF00]HOUSE OF P\x00numplayers\x009\x00maxplayers\x0010\x00gametype\x00Barricaded Suspects\x00gamevariant\x00SWAT 4\x00mapname\x00A-Bomb Nightclub\x00hostport\x0010480\x00password\x00False\x00gamever\x001.0\x00\x00\x00',
        {'hostname': '[C=FFFF00]HOUSE OF P', 'map': 'A-Bomb Nightclub', 'is_password': False, 'maxplayers': 10, 'players': 9},
    ),
    'Sniper Elite V2': (
        'valve',
        b'\xff\xff\xff\xffI\x11X-Seven\x00ARMS RACE\x00sniperelitev2\x00SEV2 dedicated server\x00\x94\xf7\x0b\x0c\x00dw\x00\x011.1.1.1\x00\xb1\xa8i\x03|\xd842\x11@\x01_1357_6_0_0_-1936053789_1______________________________________140003050000000003000000a30d0000a30d0000a30d0000a30d00005f420145\x00\x94\xf7\x00\x00\x00\x00\x00\x00',
        {'hostname': 'X-Seven', 'map': 'ARMS RACE', 'is_password': False, 'maxplayers': 12, 'players': 11},
    ),
    'Soldier of Fortune II': (
        'quake3',
        b'\xff\xff\xff\xffstatusResponse\n\\game_version\\sof2mp-1.02\\sv_keywords\\SOF2FULL \\sv_pure\\0\\scorelimit\\10\\timelimit\\20\\sv_minrate\\2500\\bot_minplayers\\6\\sv_allowDownload\\1\\sv_allowAnonymous\\0\\sv_privateClients\\0\\g_needpass\\0\\g_gametype\\CTF\\fraglimit\\100\\g_friendlyFire\\1\\g_maxGameClients\\0\\sv_floodProtect\\1\\sv_maxPing\\450\\sv_minPing\\0\\sv_maxRate\\8000\\sv_punkbuster\\0\\sv_maxclients\\32\\sv_hostname\\^kHouse ^7of ^bBoom ^7Next: Shop69\\dmflags\\8\\version\\SOF2MP GOLD V1.03 win-x86 Nov  5 2002\\protocol\\2004\\mapname\\mp_kam4\\g_motd\\^kHouse ^7of ^bBoom ^7Next:Shop69\\Administrator\\ \\Location\\USA\\sv_modClient\\1\\gamename\\sof2mp\\gameversion\\ROC2.1c, AI-1.5.9\\g_available\\22222222012222002212\\redscore\\0\\bluescore\\0\n3 170 2 "Gollum!!!!"\n0 298 3 "ToxXxic"\n3 83 1 "^g:|4:20|:|^14thHorseman^g|:"\n0 158 1 "MadKiller"\n0 100 3 "[Made]OUCH"\n1 79 1 "|S-M-C|Hinter"\n2 150 2 "dexter"\n0 151 3 "MiLLet The BarBar"\n0 999 2 "^2W^kare^2V^kon^2W^kolf"\n6 300 2 "^&mu^&ddy boots"\n7 155 2 "Psycho@PT[Killer]"\n0 74 2 "jANK"\n1 106 1 "kdog"\n3 305 1 "^.**^.POLACO**"\n0 112 2 "T3"\n0 115 1 "sToNeY"\n',
        {'hostname': '^kHouse ^7of ^bBoom ^7Next: Shop69', 'map': 'mp_kam4', 'is_password': False, 'maxplayers': 32, 'players': 16},
    ),
    'Star Wars Battlefront 2': (
        'gamespy1',
        b'\\hostname\\(TSoF)_Funwar\\gamever\\1.0\\hostport\\3659\\mapname\\tat2g_ctf\\gametype\\duel\\numplayers\\0\\numteams\\2\\maxplayers\\10\\password\\1\\gamemode\\openplaying\\teamplay\\1\\fraglimit\\20\\timelimit\\5000\\session\\-1405720051\\prevsession\\0\\swbregion\\3\\teamdamage\\1\\autoaim\\1\\heroes\\0\\herounlock\\2\\herounlockval\\1\\heroteam\\0\\heroplayer\\7\\herorespawn\\0\\herorespawnval\\90\\autoteam\\0\\numai\\0\\team1reinforcements\\2147483647\\team2reinforcements\\2147483647\\servertype\\2\\minplayers\\6\\aidifficulty\\1\\showplayernames\\1\\invincibilitytime\\2\\team_t0\\Imperium\\team_t1\\Rebellen\\score_t0\\2147483647\\score_t1\\2147483647\\final\\\\queryid\\1.1',
        {'hostname': '(TSoF)_Funwar', 'map': 'tat2g_ctf', 'is_password': True, 'maxplayers': 10, 'players': 0},
    ),
    'Star Wars Jedi Knight': (
        'quake3',
        b'\xff\xff\xff\xffstatusResponse\n\\g_HideHUDFromSpecs\\0\\g_TKPointsMinorFriendly\\1\\g_TKPointsForgiveAfterRounds\\2\\g_TKPointsRemovedPerRound\\50\\g_TKPointsKickCount\\750\\g_TKPointsSpecCount\\500\\g_maxGameClients\\0\\g_noSpecMove\\0\\g_FullSpecTalkToPlayers\\1\\g_EUAllowed\\1\\g_TimePeriod\\0\\g_allowedVillainClasses\\0\\g_allowedHeroClasses\\0\\g_Authenticity\\0\\g_MinMBPoints\\80\\roundlimit\\50\\sv_maxConnections\\2\\sv_floodProtect\\1\\sv_maxPing\\0\\sv_minPing\\0\\sv_maxRate\\25000\\sv_maxclients\\32\\sv_hostname\\       ^1AOD ^0Pandemonium\\g_needpass\\0\\g_gametype\\7\\timelimit\\0\\fraglimit\\100\\version\\JAmp: v1.0.1.1 linux-i386 Nov 10 2003\\dmflags\\0\\capturelimit\\0\\g_maxHolocronCarry\\3\\g_privateDuel\\1\\g_saberLocking\\1\\g_maxForceRank\\6\\duel_fraglimit\\10\\g_forceBasedTeams\\0\\g_duelWeaponDisable\\1\\protocol\\26\\mapname\\mb2_dotf\\sv_allowDownload\\0\\gamename\\Movie Battles II V0.1.9\\g_gravity\\800\\g_SiegeClassQueue\\aaaaaaaaaaaa\\bg_fighterAltControl\\0\n51 59 "AOD_^4BlueStar^7[JK]"\n0 98 "^3.(@).^1=^7^^3F^7ord"\n0 270 "Agelus "\n0 55 "^6Q^5ueen"\n0 51 "^1T^7hraygo"\n0 150 "Nuke"\n0 135 "^3WorstMB2PlayerInTheWorld"\n0 50 "^7=^3^^0Ma^1g^7ma^7="\n0 55 "NoChelburging"\n0 58 "Sound of the Beef"\n0 77 "Your whole family[T]"\n0 51 "^7=^1Gov^7ern^1or X^7erx^1es^7="\n',
        {'hostname': '       ^1AOD ^0Pandemonium', 'map': 'mb2_dotf', 'is_password': False, 'maxplayers': 32, 'players': 12},
    ),
    'Starbound': (
        'valve',
        b'\xff\xff\xff\xffI\x07Roleplay Server Antares\x00Alpha Malkut 8527 I,Alpha Lyncis Minoris IV a,Beta Oswin 5395 VI a,     Yggdrasil Root     ,Gamma Marsin Minoris II,Gamma Arrakis Majoris III\x00starbound\x00Starbound\x00\xfe\xff\x1cF\x00DL\x00\x00Beta v. Enraged Koala - Update 8\x00\x80\x00\x00',
        {'hostname': 'Roleplay Server Antares', 'map': 'Alpha Malkut 8527 I,Alpha Lyncis Minoris IV a,Beta Oswin 5395 VI a,     Yggdrasil Root     ,Gamma Marsin Minoris II,Gamma Arrakis Majoris III', 'is_password': False, 'maxplayers': 70, 'players': 28},
    ),
    'Team Fortress 2': (
        'valve',
        b"\xff\xff\xff\xffI\x11LazyPurple's Silly Server #1\x00delfinoplaza_final\x00tf\x00Team Fortress\x00\xb8\x01\x1e\x1e\x00dw\x00\x012292213\x00\xb1\x87i\x08\x88\xf3\xc80\x11@\x01alltalk,increased_maxplayers,lazypurple,nocrits,replays,respawntimes\x00\xb8\x01\x00\x00\x00\x00\x00\x00",
        {'hostname': "LazyPurple's Silly Server #1", 'map': 'delfinoplaza_final', 'is_password': False, 'maxplayers': 30, 'players': 30},
    ),
    'Team Fortress Classic': (
        'valve',
        b'\xff\xff\xff\xffm127.0.0.1:27015\x00-[EVIL]- Battlezone-X |back to the basics|\x00casbah\x00tfc\x00NeoTF\x00\x16 /dw\x00\x01\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x01\x00\x01\x01',
        {'hostname': '-[EVIL]- Battlezone-X |back to the basics|', 'map': 'casbah', 'is_password': False, 'maxplayers': 32, 'players': 22},
    ),
    'Unreal Tournament': (
        'gamespy1',
        b'\\hostname\\zp|    [=======]    [PURE]    [INSTAGIB]    [US]    [=======] by www.unrealkillers.com\\hostport\\7777\\maptitle\\CTF-Abreez-SE\\mapname\\CTF-Abreez-SE\\gametype\\CTFGame\\numplayers\\12\\maxplayers\\13\\gamemode\\openplaying\\gamever\\451\\minnetver\\432\\worldlog\\false\\wantworldlog\\false\\queryid\\41.1\\final\\',
        {'hostname': 'zp|    [=======]    [PURE]    [INSTAGIB]    [US]    [=======] by www.unrealkillers.com', 'map': 'CTF-Abreez-SE', 'is_password': False, 'maxplayers': 13, 'players': 12},
    ),
    'Unreal Tournament 2004': (
        'gamespy1',
        b'\\hostname\\[MiA]\xa0WARFARE\\hostport\\7777\\maptitle\\Torlan\\mapname\\ONS-TORLAN\\gametype\\ONSOnslaughtGame\\numplayers\\16\\maxplayers\\26\\gamemode\\openplaying\\gamever\\3334\\minnetver\\3180\\queryid\\31.1\\final\\',
        {'hostname': '[MiA] WARFARE', 'map': 'ONS-TORLAN', 'is_password': False, 'maxplayers': 26, 'players': 16},
    ),
    'Unreal Tournament 3': (
        'gamespy4',
        b'\x00\x04\x05\x06\x07splitnum\x00\x00\x00hostname\x00UT3 Server PRO Best Maps (T.L.G.S.E.)\x00hostport\x007777\x00numplayers\x0018\x00maxplayers\x0064\x00gamemode\x00openplaying\x00mapname\x00OwningPlayerId=393646163,NumPublicConnections=64,bUsesStats=True,bIsDedicated=True,OwningPlayerName=UT3 Server PRO Best Maps (T.L.G.S.E.),EngineVersion=3815,MinNetVersion=3467,s32779=3,s1=0,s6=1,s7=0,s9=0,s11=0,s12=0,s13=0,s14=1,p1073741825=VCTF-Basically-FSE,p1073741826=UTGameContent.UTVehicleCTFGame_Content,p268435703=3,p1073741827=,p268435717=4096,p268435706=12,p268435968=                                                               0,p268435969=0,AverageSkillRating=2693.239990,s0=2,s8=0,s10=0,p268435704=7,p268435705=25,p1073741828=Server Advertisements\x1cDodgeJump\x1cUT3X v173 - 20/03/2014\x00OwningPlayerId\x00393646163\x00NumPublicConnections\x0064\x00bUsesStats\x00True\x00bIsDedicated\x00True\x00OwningPlayerName\x00UT3 Server PRO Best Maps (T.L.G.S.E.)\x00AverageSkillRating\x002693.239990\x00EngineVersion\x003815\x00MinNetVersion\x003467\x00s32779\x003\x00s0\x002\x00s1\x000\x00s6\x001\x00s7\x000\x00s8\x000\x00s9\x000\x00s10\x000\x00s11\x000\x00s12\x000\x00s13\x000\x00s14\x001\x00p1073741825\x00VCTF-Basically-FSE\x00p1073741826\x00UTGameContent.UTVehicleCTFGame_Content\x00p268435704\x007\x00p268435705\x0025\x00p268435703\x003\x00p1073741827\x00\x00p268435717\x004096\x00p1073741828\x00Server Advertisements\x1cDodgeJump\x1cUT3X v173 - 20/03/2014\x1cT.L.G.S.E.\x00p1073741829\x00\x1cServerAdverts\x1cMutDodgeJump\x1cUT3X\x1cUTTLGSE\x1c\x00p268435706\x0012\x00p268435968\x00p268435969\x000\x00\x00',
        {'hostname': 'UT3 Server PRO Best Maps (T.L.G.S.E.)', 'map': 'VCTF-Basically-FSE', 'is_password': False, 'maxplayers': 64, 'players': 18},
    ),
    'Urban Terror': (
        'quake3',
        b'\xff\xff\xff\xffstatusResponse\n\\sv_allowdownload\\0\\g_gametype\\7\\sv_maxclients\\32\\sv_floodprotect\\1\\capturelimit\\4\\sv_hostname\\^2WWW.FALLIN-ANGELS.ORG\\g_followstrict\\1\\fraglimit\\0\\timelimit\\20\\g_roundtime\\0\\g_hotpotato\\1\\g_waverespawns\\0\\g_respawndelay\\5\\g_suddendeath\\0\\g_friendlyfire\\1\\g_allowvote\\0\\g_armbands\\0\\sv_dlURL\\fallin-angels.org\\sv_maxrate\\0\\g_skins\\1\\g_funstuff\\1\\g_deadchat\\2\\g_teamnamered\\Devils\\g_teamnameblue\\Angels\\g_walljumps\\3\\ Clan\\www.fallin.angels.org\\ Location\\USA\\sv_privateclients\\4\\version\\ioQ3 1.35 urt 4.2.019 linux-i386 Jun 16 2014\\protocol\\68\\mapname\\ut4_harbortown\\gamename\\q3urt42\\g_needpass\\0\\g_enableDust\\0\\g_enableBreath\\0\\g_survivor\\0\\g_enablePrecip\\0\\auth\\1\\auth_status\\public\\g_modversion\\4.2.018\n2 51 "CROSSEDEYEDOG "\n0 85 "Buttermilk_Bisquit"\n0 79 "|FA|nutjob"\n1 90 "Benito Carlos"\n2 200 "KiMu"\n2 51 "|FA|Tir0L0c0"\n2 203 "Juanchi"\n0 48 "RespawnNoobtection"\n5 111 "|FA|BigTex"\n6 146 "nacho"\n4 287 "Fire"\n2 95 "pooploops"\n11 87 "|G|rizzleBunnyLlama"\n14 88 "Ourmanbones"\n2 73 "nous"\n0 128 "|FA|AlguienoAlgo"\n9 210 "|FA|sujoi78"\n4 150 "B4D"\n9 148 "spriggan"\n9 135 "|FA|RadarLove"\n3 74 "BlackOps"\n3 153 "Arris"\n11 148 "LILANDRA"\n8 62 "Dapper"\n11 50 "Viral"\n5 148 "Alptraumk"\n',
        {'hostname': '^2WWW.FALLIN-ANGELS.ORG', 'map': 'ut4_harbortown', 'is_password': False, 'maxplayers': 32, 'players': 26},
    ),
    'Wolfenstein Enemy Territory': (
        'quake3',
        b'\xff\xff\xff\xffstatusResponse\n\\omnibot_playing\\10\\P\\231111221322121211113122-30--2-2----------2\\voteFlags\\507903\\g_balancedteams\\1\\g_bluelimbotime\\8000\\g_redlimbotime\\12000\\gamename\\jaymod\\mod_version\\2.2.0\\mod_url\\http://jaymod.clanfu.org\\mod_binary\\linux-release\\sv_uptime\\23d08h46m\\sv_cpu\\Intel(R) Xeon(R) CPU           \\omnibot_enable\\1\\g_heavyWeaponRestriction\\100\\.URL\\fearless-assassins.com\\.NAME\\=F|A= Clan\\g_gametype\\2\\g_antilag\\1\\g_voteFlags\\0\\g_alliedmaxlives\\0\\g_axismaxlives\\0\\g_minGameClients\\8\\g_needpass\\0\\g_maxlives\\0\\g_friendlyFire\\0\\sv_allowAnonymous\\0\\sv_floodProtect\\1\\sv_maxPing\\0\\sv_minPing\\0\\sv_maxRate\\50000\\sv_hostname\\^1F^7|^1A ^7RECRUITING ^1XP SAVE\\sv_privateClients\\0\\mapname\\trmfght_beta2\\timelimit\\25\\sv_maxclients\\51\\version\\ET 3.00 - TB 0.7.0 linux-i386\\protocol\\84\n0 53 "^9gaussian"\n0 50 "Piper Maru"\n0 194 "NiCoH2"\n0 0 "Malin"\n0 0 "Milius"\n0 234 "^1red^7_^3pe^7a^3rl"\n0 0 "Hitnrun"\n0 0 "PillowPants"\n0 168 "EU"\n0 50 "^0|bc|^8E^3c^2l^1i^4p^*s^.e"\n0 198 "xxx"\n116675 70 "^1Gar^7yt^1he^1r^7et^1arD"\n0 189 "dj degg"\n0 0 "Oysterhead"\n0 0 "George"\n0 0 "Wens"\n0 50 "^0ratf^7!^0nk"\n0 0 "Merki"\n0 241 "^0|^qSUPERMAN^0|"\n0 151 "Takamanohara"\n0 54 "WWWWW"\n275 130 "Fred France"\n0 0 "Tarnok"\n0 0 "Mungri"\n0 148 "^1saCroSanto"\n61 999 "^0MASSARANDUBA"\n447603 198 "Custom_Marshall"\n0 48 "sgtatarms"\n0 75 "Grandpa Death"\n',
        {'hostname': '^1F^7|^1A ^7RECRUITING ^1XP SAVE', 'map': 'trmfght_beta2', 'is_password': False, 'maxplayers': 51, 'players': 29},
    ),
    'Zombie Panic Source': (
        'valve',
        b'\xff\xff\xff\xffI\x11LoS-Gaming :: 24/7 Cabin :: LoS-Clan.net \x00zpo_cabin_outbreak_b6\x00zps\x00ZPS 2.4.1i+\x00\\D\x10\x18\x00dw\x00\x012.4.1.0\x00\xb1\x87i\x08\x1c\xec\xcd3\x11@\x01gameME,increased_maxplayers\x00\\D\x00\x00\x00\x00\x00\x00',
        {'hostname': 'LoS-Gaming :: 24/7 Cabin :: LoS-Clan.net ', 'map': 'zpo_cabin_outbreak_b6', 'is_password': False, 'players': 16, 'maxplayers': 24},
    ),

    #this game are not in gametracker.com
    'Blade Symphony': (
        'valve',
        b'\xff\xff\xff\xffI\x11Server name\x00duel_district\x00berimbau\x00Blade Symphony\x00\x00\x00\x00\n\x00dl\x00\x010.01.02777\x00\xb1\x90i\t`\x9f\x0fl\x11@\x01mode:Blade Symphony,empty,gamemode:Duel,ranked:yes,sv_search_key_1000,\x00@q\x03\x00\x00\x00\x00\x00',
        {'hostname': 'Server name', 'map': 'duel_district', 'is_password': False, 'players': 0, 'maxplayers': 10},
    ),
}

# x = Query()
# x.debug = True
# print(x.query('80.72.40.110', 27024, 'valve'))


class ServerQuery(Thread):
    def __init__(self, port):
        super().__init__()
        self.port = port

    def run(self):
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP) as s:
            s.bind(('127.0.0.1', self.port))

            game_name = ''
            for data, addr in iter(lambda: s.recvfrom(1024), b''):
                # from test
                if data == b'stop':
                    break

                key = data.decode(errors="ignore")
                # from test
                if key in server_data:
                    game_name = key

                # from query
                elif game_name:
                    # gamespy4 challange
                    if data[:3] == b'\xFE\xFD\x09':
                        data2 = b'\x09' + data[3:7] + b'229496729\x00'
                        s.sendto(data2, addr)
                        data, addr = s.recvfrom(1024)

                    _, response_bytes, _ = server_data[game_name]
                    s.sendto(response_bytes, addr)


class TestQuery(TestCase):
    def setUp(self):
        self.port = 27601
        self.timeout = 1

        self.q = query.Query()

        #init server fork
        self.thread = ServerQuery(self.port)
        self.thread.start()

    def tearDown(self):
        pass

    def test_query(self):
        def send_to_socket(data):
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
                s.settimeout(self.timeout)
                s.connect(('127.0.0.1', self.port))
                s.send(data.encode())

        try:
            for key, values in server_data.items():
                typ, _, response_data = values
                send_to_socket(key)

                response_socket = self.q.query('127.0.0.1', self.port, typ)
                # with self.subTest(game=key):
                self.assertEqual(response_data, response_socket)
        finally:
            send_to_socket('stop')