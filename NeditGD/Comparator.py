from Editor import Editor
import Properties

# This script simply reads and prints the current level
if __name__ == '__main__':
    editor = Editor.loadCurrentLevel()
    objects = editor.objects
    objects.sort(key=lambda obj: obj.x)
    default = objects[0]
    differences = []
    for obj in objects:
        diff = {}
        differences.append(diff)
        for k, v in obj.data.items():
            k_name = Properties.get_property_name(k)
            if k in [2, 3, 155]: continue
            if default.data.get(k) != v:
                diff[k_name] = v
            for k2 in default.data.keys():
                if not k2 in obj.data.keys():
                    k2_name = Properties.get_property_name(k2)
                    diff[k2_name] = 'missing'
    print(*[f'\n{i+1}: {d}'
            for (i, d) in enumerate(differences)])


    # print(editor.read_objects())
