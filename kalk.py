def format_number(number):
    """Функция для форматирования числа с пробелами для удобства чтения."""
    return '{:,.0f}'.format(number).replace(',', ' ')


def calculate_profit(initial_amount, monthly_salary, months, annual_rate=17):
    """Функция для расчета прибыли с учетом сложных процентов и ежемесячного пополнения."""
    monthly_rate = annual_rate / 12 / 100  # процентная ставка в месяц
    total_amount = initial_amount

    for month in range(months):
        total_amount += total_amount * monthly_rate  # начисление процентов
        total_amount += monthly_salary  # добавление зарплаты

    return total_amount


def main():
    # Ввод данных
    initial_amount = float(input("Введите начальную сумму: "))
    monthly_salary = float(input("Введите сумму ежемесячной зарплаты: "))
    months = int(input("Введите количество месяцев: "))

    # Расчет итоговой суммы
    final_amount = calculate_profit(initial_amount, monthly_salary, months)

    # Расчет, сколько процентов будет начислено на текущую сумму
    monthly_rate = 20 / 12 / 100  # процентная ставка в месяц
    monthly_profit = final_amount * monthly_rate

    # Вывод результата
    print(f"\nИтоговая сумма после {months} месяцев: {format_number(final_amount)}")
    print(f"В следующем месяце с этой суммы будет начислено: {format_number(monthly_profit)}")


if __name__ == "__main__":
    main()