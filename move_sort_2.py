count_moves = int(input())
list_m = list()
for i in range(count_moves):
    move = input(str())
    list_m.append(move)
d1 = sorted(list_m)
print(count_moves)
if count_moves != 0:
    print(d1[0], end='')
    for i in range(1, len(d1)):
        if d1[i][:2] == d1[i-1][:2]:
            print('', d1[i], end='')
        else:
            print('\n', end='')
            print(d1[i], end='')