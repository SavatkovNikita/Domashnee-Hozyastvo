def box():
    # Объем шкафа
    fridge_volume = float(input("Введите объем шкафа: "))
    used_volume = 0 #использованный объм
    while True:
        print("\n Добавление бытовой химии")
        name = input("Введите название бытовой химии: ")
        k = int(input("Введите количество бытовой химии: "))
        volume = float(input("Введите объем одного продукта: "))# Вычисляем общий объем для этого продукта
        product_total_volume = k * volume# Проверяем, достаточно ли места
        if used_volume + product_total_volume <= fridge_volume:
            used_volume += product_total_volume
            print(f"Бытовая химия '{name}' добавлена")
            print(f"Занято места: {used_volume}/{fridge_volume}")
        else:
            print("Недостаточно места")
            break

        another = input("Добавить еще бытовой химии? (да/нет): ").lower()
        if another != 'да':
            print("Пака")
            break
box()