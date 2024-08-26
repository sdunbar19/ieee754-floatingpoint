MAX = 2000
powers_list = []
from tqdm import tqdm

curr = 1
for i in tqdm(range(MAX + 1)):
    powers_list.append(curr)
    curr *= 2
f = open("powers_of_two.txt", "w")
for power in powers_list:
    f.write(str(power) + "\n")
f.close()

