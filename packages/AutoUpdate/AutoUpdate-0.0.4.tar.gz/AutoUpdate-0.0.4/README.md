Check for updates in the easiest way possible.

Release notes (0.0.4)
===
* Removed useless code

Documentation
===

First, create a github repository. Then in the repository, create a file. Name this whatever you want, as long as it's a .txt file. Put the latest version in there. Update this file with the corresponding latest version constantly when there's a new update. Then, open the raw file using the raw button, and copy that URL.

Then with the URL copied to your clipboard, add the following code:

```py
import AutoUpdate

AutoUpdate.set_url("<FILE URL HERE>")
```

And replace the string's content with the file URL.

Then after that, set the current version of the software. You can do this by doing the following:

```py
import AutoUpdate

AutoUpdate.set_url("<FILE URL HERE>")
AutoUpdate.set_current_version("0.0.1")
```

Change the current version with anything you want. It doesn't have to be in that format, it can be 0.0.1, 0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.1, 2021.69.420, anything you like, even UGLYPOOPHEAD.

Then to check if the version is up to date, you simply run this code:

```py
import AutoUpdate

AutoUpdate.set_url("<FILE URL HERE>")
AutoUpdate.set_current_version("0.0.1")
print(AutoUpdate.is_up_to_date())
```

This will print `True` if it's up to date, `False` if it's not.

What you can also do is upload the file it needs to download in the same repository, always update that file too, and download it if the version is not up to date by using the following code:

```py
import AutoUpdate

AutoUpdate.set_url("<FILE URL HERE>")
AutoUpdate.set_download_link("<DOWNLOAD LINK HERE>")
AutoUpdate.set_current_version("0.0.1")

if not AutoUpdate.is_up_to_date():
    AutoUpdate.download("<PATH TO FILE HERE>")
```

If you need any help, email me (mr.bruh.dev@gmail.com) or join the Discord server (https://discord.gg/DQTRTWQ7yd)