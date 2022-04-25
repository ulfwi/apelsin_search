# Setup

Add the following to ~/.bashrc to get access to the search command:

`source /path/to/apelsin`

This will create a config files (if it doesn't already exist) and bind apelsin search to Ctrl+e.

# Key bindings

## Ctrl+e

Open up the search interface. Use arrow keys to select search result. Press enter to execute command or right arrow key to just copy it to the command line.

## Ctrl+f

Add selected command to favorites.

## Delete

Remove command from favorites or ~/.bash_history.

# TODO

* Handle printing emojis: 📈
  * There's something strange with it so it makes us write past the end of the terminal
  * Handle special characters in a good way
* Add quick search (similar to ctrl+r) with favourites