License
=======

* GameQuery is licensed under `Creative Commons Attribution-NonCommercial 3.0 <http://creativecommons.org/licenses/by-nc/3.0/>`__ license.

Requirements
============

* Python 3.4 or better (or maybe python 3.3 [not tested])

Usage
=====

.. code-block:: python

    >>> import query
    >>> 
    >>> info = query.Query()
    >>> info.query('127.0.0.1', 27015, 'gamespy1')
    {'hostname': ' --=[ aX ]=-- (CD and Origin)', 'map': 'iwo jima', 'is_password': False, 'maxplayers': 64, 'players': 42}


TODO
====

* add asyncio module
* add players list
* add rules list
* add install from pip
* adds more docs and samples

SUPPORTED GAMES
===============

+---------------------------------+----------+
| Game                            | Query    |
+---------------------------------+----------+
| 7 Days to Die                   | valve    |
+---------------------------------+----------+
| ARMA 2                          | gamespy4 |
+---------------------------------+----------+
| ARMA 3                          | gamespy4 |
+---------------------------------+----------+
| Alien Swarm                     | valve    |
+---------------------------------+----------+
| America's Army 3                | valve    |
+---------------------------------+----------+
| America's Army: Proving Grounds | valve    |
+---------------------------------+----------+
| Battlefield 1942                | gamespy1 |
+---------------------------------+----------+
| Battlefield 2                   | gamespy3 |
+---------------------------------+----------+
| Blade Symphony                  | valve    |
+---------------------------------+----------+
| Call of Duty                    | quake3   |
+---------------------------------+----------+
| Call of Duty 2                  | quake3   |
+---------------------------------+----------+
| Call of Duty 4                  | quake3   |
+---------------------------------+----------+
| Call of Duty World at War       | quake3   |
+---------------------------------+----------+
| Call of Duty: Modern Warfare 3  | valve    |
+---------------------------------+----------+
| Centration                      | valve    |
+---------------------------------+----------+
| Counter-Strike 1.6              | valve    |
+---------------------------------+----------+
| Counter-Strike Global Offensive | valve    |
+---------------------------------+----------+
| Counter-Strike: Condition Zero  | valve    |
+---------------------------------+----------+
| Counter-Strike: Source          | valve    |
+---------------------------------+----------+
| DOTA 2                          | valve    |
+---------------------------------+----------+
| Day of Defeat                   | valve    |
+---------------------------------+----------+
| Day of Defeat: Source           | valve    |
+---------------------------------+----------+
| DayZ                            | valve    |
+---------------------------------+----------+
| F.E.A.R.                        | gamespy2 |
+---------------------------------+----------+
| Garry's Mod                     | valve    |
+---------------------------------+----------+
| Half-Life 1                     | valve    |
+---------------------------------+----------+
| Half-Life 2: Deathmatch         | valve    |
+---------------------------------+----------+
| Halo                            | gamespy2 |
+---------------------------------+----------+
| Homefront                       | valve    |
+---------------------------------+----------+
| Insurgency                      | valve    |
+---------------------------------+----------+
| Insurgency Standalone           | valve    |
+---------------------------------+----------+
| Just Cause 2: Multiplayer       | valve    |
+---------------------------------+----------+
| Killing Floor                   | gamespy1 |
+---------------------------------+----------+
| Left 4 Dead                     | valve    |
+---------------------------------+----------+
| Left 4 Dead 2                   | valve    |
+---------------------------------+----------+
| Medal of Honor Allied Assault   | gamespy1 |
+---------------------------------+----------+
| Medal of Honor Spearhead        | gamespy1 |
+---------------------------------+----------+
| Minecraft                       | gamespy4 |
+---------------------------------+----------+
| Natural Selection 2             | valve    |
+---------------------------------+----------+
| Quake 3                         | quake3   |
+---------------------------------+----------+
| Red Orchestra                   | gamespy1 |
+---------------------------------+----------+
| Red Orchestra 2                 | valve    |
+---------------------------------+----------+
| Rust                            | valve    |
+---------------------------------+----------+
| SWAT 4                          | gamespy2 |
+---------------------------------+----------+
| Sniper Elite V2                 | valve    |
+---------------------------------+----------+
| Soldier of Fortune II           | quake3   |
+---------------------------------+----------+
| Star Wars Battlefront 2         | gamespy1 |
+---------------------------------+----------+
| Star Wars Jedi Knight           | quake3   |
+---------------------------------+----------+
| Starbound                       | valve    |
+---------------------------------+----------+
| Team Fortress 2                 | valve    |
+---------------------------------+----------+
| Team Fortress Classic           | valve    |
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
| Zombie Panic Source             | valve    |
+---------------------------------+----------+