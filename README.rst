License
=======

* GameQuery is licensed under MIT license.

Requirements
============

* Python 3.5 or better

Usage
=====

.. code-block:: python

    >>> import asyncio
    >>> from query import *
    >>>
    >>> async def fetch_data(class_, ip, port, timeout):
    >>>     async with class_(ip=ip, port=port, timeout=timeout) as s:
    >>>         info = await s.get_info()
    >>>         print('get_info', info)
    >>>
    >>>         players = await s.get_players()
    >>>         print('get_players', players)
    >>>
    >>>         rules = await s.get_rules()
    >>>         print('get_rules', rules)
    >>>
    >>>
    >>> servers = [
    >>>     # Class, IP, Port, Timeout
    >>>     (GoldSource, '127.0.0.1', 27027, 5),
    >>>     (Source, '127.0.0.1', 27050, 5),
    >>> ]
    >>>
    >>> list_tasks = list()
    >>> for args in servers:
    >>>     list_tasks.append(fetch_data(*args))
    >>>
    >>> asyncio.get_event_loop().run_until_complete(asyncio.wait(list_tasks))


TODO
====

* write Tests
* add install from pip
* adds more docs and samples

SUPPORTED GAMES
===============

+---------------------------------+----------+
| Game                            | Query    |
+---------------------------------+----------+
| 7 Days to Die                   | source   |
+---------------------------------+----------+
| ARMA 2                          | gamespy4 |
+---------------------------------+----------+
| ARMA 3                          | gamespy4 |
+---------------------------------+----------+
| Alien Swarm                     | source   |
+---------------------------------+----------+
| America's Army 3                | source   |
+---------------------------------+----------+
| America's Army: Proving Grounds | source   |
+---------------------------------+----------+
| Battlefield 1942                | gamespy1 |
+---------------------------------+----------+
| Battlefield 2                   | gamespy3 |
+---------------------------------+----------+
| Blade Symphony                  | source   |
+---------------------------------+----------+
| Call of Duty                    | quake3   |
+---------------------------------+----------+
| Call of Duty 2                  | quake3   |
+---------------------------------+----------+
| Call of Duty 4                  | quake3   |
+---------------------------------+----------+
| Call of Duty World at War       | quake3   |
+---------------------------------+----------+
| Call of Duty: Modern Warfare 3  | source   |
+---------------------------------+----------+
| Centration                      | source   |
+---------------------------------+----------+
| Counter-Strike 1.6              | source   |
+---------------------------------+----------+
| Counter-Strike Global Offensive | source   |
+---------------------------------+----------+
| Counter-Strike: Condition Zero  | source   |
+---------------------------------+----------+
| Counter-Strike: Source          | source   |
+---------------------------------+----------+
| DOTA 2                          | source   |
+---------------------------------+----------+
| Day of Defeat                   | source   |
+---------------------------------+----------+
| Day of Defeat: Source           | source   |
+---------------------------------+----------+
| DayZ                            | source   |
+---------------------------------+----------+
| F.E.A.R.                        | gamespy2 |
+---------------------------------+----------+
| Garry's Mod                     | source   |
+---------------------------------+----------+
| Half-Life 1                     | source   |
+---------------------------------+----------+
| Half-Life 2: Deathmatch         | source   |
+---------------------------------+----------+
| Halo                            | gamespy2 |
+---------------------------------+----------+
| Homefront                       | source   |
+---------------------------------+----------+
| Insurgency                      | source   |
+---------------------------------+----------+
| Insurgency Standalone           | source   |
+---------------------------------+----------+
| Just Cause 2: Multiplayer       | source   |
+---------------------------------+----------+
| Killing Floor                   | gamespy1 |
+---------------------------------+----------+
| Left 4 Dead                     | source   |
+---------------------------------+----------+
| Left 4 Dead 2                   | source   |
+---------------------------------+----------+
| Medal of Honor Allied Assault   | gamespy1 |
+---------------------------------+----------+
| Medal of Honor Spearhead        | gamespy1 |
+---------------------------------+----------+
| Minecraft                       | gamespy4 |
+---------------------------------+----------+
| Natural Selection 2             | source   |
+---------------------------------+----------+
| Quake 3                         | quake3   |
+---------------------------------+----------+
| Red Orchestra                   | gamespy1 |
+---------------------------------+----------+
| Red Orchestra 2                 | source   |
+---------------------------------+----------+
| Rust                            | source   |
+---------------------------------+----------+
| SWAT 4                          | gamespy2 |
+---------------------------------+----------+
| Sniper Elite V2                 | source   |
+---------------------------------+----------+
| Soldier of Fortune II           | quake3   |
+---------------------------------+----------+
| Star Wars Battlefront 2         | gamespy1 |
+---------------------------------+----------+
| Star Wars Jedi Knight           | quake3   |
+---------------------------------+----------+
| Starbound                       | source   |
+---------------------------------+----------+
| Team Fortress 2                 | source   |
+---------------------------------+----------+
| Team Fortress Classic           | source   |
+---------------------------------+----------+
| Unreal Tournament               | gamespy1 |
+---------------------------------+----------+
| Unreal Tournament 2004          | gamespy1 |
+---------------------------------+----------+
| Unreal Tournament 3             | gamespy4 |
+---------------------------------+----------+
| Urban Terror                    | quake3   |
+---------------------------------+----------+
| Wolfenstein Enemy Territory     | quake3   |
+---------------------------------+----------+
| Zombie Panic Source             | source   |
+---------------------------------+----------+