import account_management

while True:
    data = []
    for i in range(0, 4):
        data.append(input("Input" + str(i + 1) + ":"))
    account_management.create_user(data[0], data[1], data[2], int(data[3]))