# <font color="red"> WARNING </font>
NEdit+ is currently is still in the development, expect any bugs to occure at any time. Please report these bug to [me](https://github.com/w1zlm).

# NEdit+

 Lightweight Geometry Dash level scripting tool

## Installation

 While NEdit is in early stages of development, you will need to download the code and import the modules manually. The main ones are Editor and Object. For more advanced save file interaction, import SaveLoad.

## Loading the level editor

 For now, NEdit can only read the level at the top of the created levels list ('current level'). If you want to edit a level, push it to the top of your levels list in Geometry Dash first.
 The Editor class handles loading and saving the data automatically. You only need to call the level loader, add your objects, and save the changes:

```python
# Load the most recent level using Editor.loadCurrentLevel()
editor = Editor.loadCurrentLevel()

# Make all the necessary changes (add/delete objects)
editor.add(
    Object(id=1, x=75, y=-15, groups=[12, 42], scale=5))

# Make all the necessary changes (add/delete objects)
editor.save()
```

## Special group 9999

 With NEdit you can add tens of thousands of objects to your level at a time. If your development process is iterative, they might need to be removed every time you re-run the script. To avoid doing that manually, NEdit uses group 9999 to mark objects as scripted. Upon a NEdit save, every previously existing object with group 9999 will be deleted and replaced with the new ones. Make sure you don't use this group to prevent your manual changes being deleted.
 If you prefer to disable that behaviour for any reason, you can do so by passing False as the second argument whenever loading the editor and adding new objects:

```python

 ...
editor = Editor.loadCurrentLevel(remove_scripted=False)
editor.add(your_object_list, mark_as_scripted=False)
```

## Level Version Control

 Due to the way GD saves are structured, NEdit has to load all of the existing levels in a compressed format before extracting/writing data. Therefore a large amount of levels leads to multiple second load times.
 VersionControl.py is a script that allows you to extract data from a GD file and save it in plaintext format for long-term storage. Useful in case you need to test a change - you don't have to create duplicate levels, so the total weight of your GD save becomes significantly lower.
 Finally, you can use this script to store finished projects or ones you aren't planning to work on for a while longer. That further reduces loadtimes, both of NEdit and GD cloud backup itself.

## Credits

* Original NEdit written and hosted by [Nemo2510](https://github.com/Boris-Filin)
* NEdit+ is made by w1zlm as a better version of NEdit

### Property decoding and testing

Huge thanks to people who helped me dig for property ids and debug NEdit:

* [Incidius](https://github.com/Incidius)
* Toastium
