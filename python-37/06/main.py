current_group = set()
count = 0
for l in input:
    if not l:
        count += len(current_group)
        current_group = set()
    for c in l:
        current_group.add(c)
count += len(current_group)
print(count)
