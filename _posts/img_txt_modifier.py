import os

def replace(folder, file, y, m, d):
    path = f'./{folder}'
    new_file = path + '/' + file
    with open(new_file, 'r', encoding='UTF8') as f:
        text = f.read()

    text = list(text)
    prefix = '![Untitled]'
    suffix = '.png)'
    cnt = 1
    new_string = f'![Untitled](https://gonnnnn.github.io/image/{folder}/{m:0>2}{d:0>2}({cnt}).png)'

    for i in range(len(text)):
        if text[i] == '!':
            if "".join(text[i:i+11]) == prefix:
                j = 0
                while("".join(text[i+j:i+j+len(suffix)]) != suffix):
                    j += 1
                string_len = j+len(suffix)

                for k in range(min(string_len, len(new_string))):
                    text[i + k] = new_string[k]

                if len(new_string) <= string_len:
                    for k in range(len(new_string), string_len):
                        text[i + k] = ' '
                else:
                    print("The new string that will replace the previous one is longer than the previous one")
                    print(f"{y}-{m}-{d}, {cnt}th(st/nd) photo")
                cnt += 1
                new_string = f'![Untitled](https://gonnnnn.github.io/image/{folder}/{m:0>2}{d:0>2}({cnt}).png)'


    with open(new_file, 'w', encoding='UTF8') as f:
        f.write("".join(text))

folder = input("Folder: ")
from_when = input("From when(MM DD): ")

src_path = f'./{folder}'
tm, td = map(int, from_when.split(" "))
file_list = os.listdir(src_path)
start = 0
for i in range(len(file_list)-1, -1, -1):
    y, m, d = map(int, file_list[i][:10].split('-'))
    if m < tm or (m == tm and d < td):
        break
    else:
        replace(folder, file_list[i], y, m, d)