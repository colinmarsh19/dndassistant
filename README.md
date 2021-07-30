# dndassistant

Pet project to write a bot capable of performing several useful utilities for online D&D games run via Discord.

Available commands:

* `$roll d#` will roll the specified dice number (#). Even if the die doesn't exist, as long as the number is greater than 0, it will choose a random number between 1 and that number

* `$inspire` will send a random inspirational quote from the ZenQuotes API

* `$new` will allow you to add an encouraging quote to the existing list

* `$list` will show all the current encouraging quotes that can be sent

* `$del #` will delete the specified index of an encouraging quote. Use `$list` to determine what quotes are at what index

* `$responding True` will enable the bot to send encouraging messages when users type in messages containing sad words

* `$responding False` will disable the bot from sending encouraging messages