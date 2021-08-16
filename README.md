# DnD Assistant

Pet project to write a bot capable of performing several useful functions for online D&D games run via Discord.

Available commands:

* `$roll` will allow you to roll one or multiple dice. It can be used with or without a preceding multiplier, such as `d6` or `2d6`. You can also add or subtract a multiplier from each roll, such as `2d6+4` or `2d6-1`. You can also do space-separated dice rolls, such as `2d6+4 3d4+2`.

* `$addxp <character> <xp>` will either insert a new record into the database to keep track of a character's XP, or update their current XP by the specified amount

* `$showxp <character>` will show the character's current XP total

* `$removexp <character>` will remove the character's XP from the database

* `$initstats <character>` initializes base stats for given character

* `$stats <character>` will show the base stats for a given character

* `$combat <character>` will show the combat stats for a given character

* `$updatestats <character> <attribute> <score>` will update that specific attribute score for the given chracter

* `$deletestats <character>` will delete all stats for the given character

* `$inspire` will send a random inspirational quote from the ZenQuotes API

* `$new_quote` will allow you to add an encouraging quote to the existing list

* `$list_quotes` will show all the current encouraging quotes that can be sent

* `$delete_quote #` will delete the specified index of an encouraging quote

* `$responding <True/False>` will enable or disable the bot to send encouraging messages when users send texts containing sad words
