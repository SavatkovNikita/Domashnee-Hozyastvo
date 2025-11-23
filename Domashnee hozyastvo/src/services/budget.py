def payment_system():
    zarplata = float(input("Введите зарплату: "))
    plategka = float(input("Введите сумму платежки: "))
    while True:
        plata = float(input("Введите сумму которую хотите залатить "))
        zarplata = zarplata - plata
        plategka = plategka - plata
        print(f"Платеж оплачен. Долг: {plategka} Остаток зарплаты {zarplata}")
        print("Конец операции")
        if plategka == 0:
            break
        another = input("Заплатить ещё? (да/нет): ").lower()
        if another != 'да':
            break
payment_system()