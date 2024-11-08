# Made by Nemo2510
# Upgraded by w1zlm

from __future__ import annotations
from SaveLoad import *
from Object import Object
from Dictionaries.PropertyHSV import HSV
from Values import Triggers


WATERMARK_TEXT = [
    Object(id=914, x=-164, y=-15, scale=0.75,
           text="Made with Nedit", hsv_enabled=1, hsv=HSV(180, 1, 1, True)),
    Object(id=914, x=-213, y=-33, scale=0.5,
           text="by Nemo2510", hsv_enabled=1, hsv=HSV(-180, 0.5, 1, True)),
    Object(id=914, x=-218, y=-45, scale=0.3,
           text="Upgraded by w1zlm", hsv_enabled=1, hsv=HSV(-180, 0.2, 1, True)),
    Object(id=914, x=-147, y=-54, scale=0.2,
           text="(You can remove this watermark, "
           "but we'd appreciate it if you didn't)")
]


# The class that stores all loaded objects and handles
# interactions with the SaveLoad system for the user
class Editor():
    __root = None
    __level_node = None
    __level_string = None
    head = None
    objects = None

    # Create an editor object that automatically loads
    # the contents of the current level
    @classmethod
    def loadCurrentLevel(cls, remove_scripted: bool=True) -> Editor:
        editor = Editor()
        editor.loadLevel()
        if remove_scripted:
            editor.removeScriptedObjects()
        return editor
    

    # Load the editor, reading objects from a provided string
    # instead of the game savefile
    @classmethod
    def loadLevelString(cls, LevelString: str) -> Editor:
        editor = Editor()
        editor.loadLevel(LevelString)
        return editor
    
    
    # Load the editor data
    def loadLevel(self, data: str = None) -> None:
        self.__root = read_gamesave_xml()
        self.__level_node = get_working_level_node(self.__root)
        if not self.__level_node.text:
            self.loadDefaultLevel()
            return
        level_data = get_working_level(self.__level_node)
        if data is not None:
            self.__level_string = data
        else:
            self.__level_string = get_working_level_string(level_data)
        self.head = read_level_head(self.__level_string)
        self.objects = read_level_objects(self.__level_string)
    
    # New levels aren't initialised until the player saves them for
    # the first time. This method loads the default data for a level
    # and initialises it ahead of GD.
    def loadDefaultLevel(self) -> None:
        try:
            dir_path = os.path.dirname(os.path.realpath(__file__))
            file_path = os.path.join(dir_path,"DefaultLevel")
            # fr
            fr = open(file_path, "r")
            data = fr.read()
            fr.close()
        except:
            raise FileNotFoundError('Default level data missing!\n'
                                    'Reinstall the library or just'
                                    'save and exit the level in GD.')
        self.head = read_level_head(data)
        self.objects = []
        print('[Nedit]: Level initialised successfully!')

    # Remove the previously scripted objects;
    # It is assumed that they are marked with group 9999
    def removeScriptedObjects(self) -> None:
        res = []
        for obj in self.objects:
            groups = obj.groups
            if groups is None or not 9999 in groups:
                res.append(obj)
        self.objects = res

    # Add an object to the editor object list;
    # Mark it with group 9999
    def add(self, obj: dict, mark_as_scripted: bool=True):
        if mark_as_scripted:
            Editor.addGroup(obj, 9999)

        self.objects.append(obj)

    @staticmethod
    def addGroupToAll(objects: list[Object], group: int) -> None:
        for obj in objects: Editor.addGroup(obj, group)

    @staticmethod
    def addGroup(obj: Object, group: int) -> None:
        if (groups := obj.groups) is None:
            obj.groups = [9999]
        else:
            groups.append(9999)

    # Add multiple ojects to the editor
    def addMultiple(self, objects: list, mark_as_scripted: bool=True):
        for obj in objects:
            self.add(obj, mark_as_scripted)
        print(f'[Nedit]: Added {len(objects)} objects to editor.')

    # Get a string representing all objects in readable format
    def readObjects(self):
        res = ''
        for obj in self.objects:
            res += str(obj) + '\n'
        return res

    # Write the editor object list to the current level file
    def save(self):
        self.add(WATERMARK_TEXT)

        save_string = self.getLevelString()
        encrypted = encrypt_level_string(save_string.encode())
        set_level_data(self.__level_node, encrypted)

        xml_str = ET.tostring(self.__root)
        encryptGamesave(xml_str)
        print('[Nedit]: Changes saved!')


    # Get the string representation of the current level
    # with RobTop's encoding
    def getLevelString(self) -> str:
        return get_level_save_string(self.objects, self.head)


    # Get the highest group from the given list of objects
    @staticmethod
    def getMaxGroup(objects: list[Object]=None) -> int:
        object_groups = set()
        for obj in objects:
            if obj.groups is None: continue
            object_groups.update(set(obj.groups))
        object_groups.discard(9999)
        if not object_groups: return 0
        return max(object_groups)
    

    # Get the groups used in the level;
    # Only counts groups with assigned objects. Triggers with unused
    # targets are ignored.
    @staticmethod
    def getUsedGroups(objects: list[Object]) -> list[int]:
        used_groups = set() 
        for obj in objects:
            if obj.groups is None: continue
            for group in obj.groups: used_groups.add(group)
        return list(used_groups)
        
    
    # Convert a list of values (groups, IDs, etc) to intervals.
    # Slightly inefficient but works.
    @staticmethod
    def getIntervals(vals: list[int]) -> list[tuple[int]]:
        if not vals: return None

        intervals = []
        interval_start = None
            
        for i in range(min(vals), max(vals) + 1):
            used = i in vals
            if interval_start is None:
                if used:
                    interval_start = i
            else:
                if not used:
                    intervals.append((interval_start, i - 1))
                    interval_start = None
        return intervals


        
