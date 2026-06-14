# game-jam-june-2026

This game was inspired by Groundhog Day, when the groundhog emerges from its hibernation to determine whether or not spring will be late, this game uses
that mechanism to determine whether or not spring will start based on how well the groundhog can wake up the bears to kick off spring in the first spring feast.

## Building

Run the following command:

```
pyinstaller.exe --name "great_bearwakening" --onedir -w --add-data font:font --add-data img:img --add-data map:map --contents-directory . "main.py"
```

And then distribute the file `dist/great_bearwakening.exe`.