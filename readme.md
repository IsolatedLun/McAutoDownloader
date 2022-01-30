# McAutoDownloader
Download any mods from minecraft with just filling a txt file!

## How to use
* `Create **mc_mods.txt** and type in mod names`
* `Open the terminal => python downloader.py`
* Enjoy!

- Always go to a new line for the names.
**Ex.**
tinkers contruct
mekanism
...

### Keywords
M-N = Mod Name
D-F = Download Failed
DL = Download
INF = Information
WARN = Warning
ERR = Error

### Variables
strict = Only download mod when the version's are exactly the same 
    or are relative. (1.16, 1.16.2)
rate_limit = Cooldown for each request to avoid [429] errors.
err_threshold = max amount of acceptable errors, if 0 then break the script.

#### Warning
This project is pretty old so I suggest you to only use it for fun... feel free to tinker with it, when
I feel like fixing some things I'll definitely do it.