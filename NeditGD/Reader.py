from Editor import Editor

# This script simply reads and prints the current level
if __name__ == '__main__':
    editor = Editor.loadCurrentLevel()
    print(editor.readObjects())
