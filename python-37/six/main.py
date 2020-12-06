# part 1
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

# part 2
current_group = {}
count = 0
group_size = 0
cnt = 0
for l in input:
    cnt+=1
    if not l:
        print(current_group, group_size)
        count += len([k for k, v in current_group.items() if v == group_size])
        current_group = {}
        group_size = 0
        continue
    group_size += 1
    print(sorted(l))
    for c in l:
        if c not in 'abcdefghijklmnopqrstuvwxyz':
            continue
        current_group[c] = current_group.get(c, 0) + 1
    if cnt == 22:
        break

count += len([k for k, v in current_group.items() if v == group_size])
current_group = {}
group_size = 0
print(count)
