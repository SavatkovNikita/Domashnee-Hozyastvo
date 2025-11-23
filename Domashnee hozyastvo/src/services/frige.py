def refrigerator():
    # Объем холодильника
    fridge_volume = float(input("Введите объем холодильника: "))
    used_volume = 0 #использованный объм
    while True:
        print("\n Добавление продукта")
        name = input("Введите название продукта: ")
        k = int(input("Введите количество продукта: "))
        volume = float(input("Введите объем одного продукта: "))# Вычисляем общий объем для этого продукта
        product_total_volume = k * volume# Проверяем, достаточно ли места
        if used_volume + product_total_volume <= fridge_volume:
            used_volume += product_total_volume
            print(f"Продукт '{name}' успешно добавлен!")
            print(f"Занято места: {used_volume}/{fridge_volume}")
        else:
            print("Недостаточно места")
            break

        another = input("Добавить еще продукт? (да/нет): ").lower()
        if another != 'да':
            print("Пака")
            break
refrigerator()