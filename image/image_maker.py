import os

# print(os.getcwd())
src_path = './TIL/folder/'
save_path = './TIL'
file_list = os.listdir(src_path)
first_one = list(file_list.pop())

date = input("what's the date? ")

for i in range(len(file_list)):
    if len(file_list[i]) == 14:
        file_list[i] = [int(file_list[i][9]),file_list[i]]
    else:
        file_list[i] = [int(file_list[i][9:11]), file_list[i]]
file_list.sort()
file_list.insert(0, [0, "".join(first_one)])

for idx, old_file in enumerate(file_list):
    old_name = os.path.join(src_path, old_file[1])
    new_name = os.path.join(save_path, date + f'({str(idx+1)}).png')
    os.rename(old_name, new_name)
    print(f'"{old_name}" to "{new_name}"')

print("done")