def payment_system():
    budget = float(input("Введите сумму бюджета: "))
    plategka = float(input("Введите сумму платежки: "))
    if plategka > budget:
        print("недостаточно средств")
    else:
        budget -= plategka
        print(f"Платеж оплачен. Остаток: {budget}")
    print("Конец операции")
payment_system()