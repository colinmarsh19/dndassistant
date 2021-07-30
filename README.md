# DnD Assistant

Pet project to write a bot capable of performing several useful functions for online D&D games run via Discord.

Available commands:

* `$roll` will allow you to roll one or multiple dice. It can be used with or without a preceding multiplier, such as `d6` or `2d6`. You can also add or subtract a multiplier from each roll, such as `2d6+4` or `2d6-1`. You can also do space-separated dice rolls, such as `2d6+4 3d4+2`.

* `$inspire` will send a random inspirational quote from the ZenQuotes API

* `$new` will allow you to add an encouraging quote to the existing list

* `$list` will show all the current encouraging quotes that can be sent

* `$del #` will delete the specified index of an encouraging quote

* `$responding True` will enable the bot to send encouraging messages when users send texts containing sad words

* `$responding False` will disable the bot from sending encouraging messages
