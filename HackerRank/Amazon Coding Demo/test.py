def mod_list(l:list) -> list:
    sorted(l)
    l.append(2)
    return []

l = [2,3,1]
mod_list(l)
print(l)
l.sort()