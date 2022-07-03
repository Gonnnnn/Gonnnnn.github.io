import os

# print(os.getcwd())
src_path = './TIL/folder/'
save_path = './TIL'
file_list = os.listdir(src_path)
file_list.insert(0, file_list[-1])
file_list.pop()

date = input("what's the date? ")

for idx, old_file in enumerate(file_list):
    old_name = os.path.join(src_path, old_file)
    new_name = os.path.join(save_path, date + f'({str(idx+1)}).png')
    os.rename(old_name, new_name)
    print(f'"{old_name}" to "{new_name}"')

print("done")