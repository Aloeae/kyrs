import tkinter as tk
from tkinter import ttk, messagebox


class MortgageCalculatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Ипотечный калькулятор для юридических лиц")
        self.root.geometry("600x650")
        self.root.resizable(False, False)

        self.create_widgets()

    def create_widgets(self):
        # Заголовок
        tk.Label(self.root, text="Ипотечный калькулятор", font=("Arial", 16, "bold")).pack(pady=10)

        # Поля ввода
        self.fields = {}
        self.add_input_field("Стоимость жилья (₽):", "price")
        self.add_input_field("Первоначальный взнос (₽):", "down_payment")
        self.add_input_field("Срок (лет):", "term")
        self.add_input_field("Процентная ставка (%):", "rate")

        # Выбор способа оплаты
        tk.Label(self.root, text="Способ оплаты:", font=("Arial", 12)).pack(pady=5)
        self.payment_method = tk.StringVar(value="Аннуитетный")
        ttk.Combobox(
            self.root,
            textvariable=self.payment_method,
            values=["Аннуитетный", "Дифференцированный"],
            state="readonly",
        ).pack(pady=5)

        # Кнопка расчета
        tk.Button(self.root, text="Рассчитать", command=self.calculate).pack(pady=20)

        # Вывод результатов
        self.result_label = tk.Label(self.root, text="", font=("Arial", 12, "bold"), justify="left")
        self.result_label.pack(pady=10)

    def add_input_field(self, label_text, field_name):
        tk.Label(self.root, text=label_text, font=("Arial", 12)).pack(pady=5)
        entry = tk.Entry(self.root)
        entry.pack(pady=5)
        self.fields[field_name] = entry

    def calculate(self):
        try:
            # Получение данных
            price = self.get_positive_float(self.fields["price"].get(), "Стоимость жилья")
            down_payment = self.get_positive_float(self.fields["down_payment"].get(), "Первоначальный взнос")
            term = self.get_positive_int(self.fields["term"].get(), "Срок")
            rate = self.get_positive_float(self.fields["rate"].get(), "Процентная ставка")

            if down_payment >= price:
                raise ValueError("Первоначальный взнос не может быть больше или равен стоимости жилья.")

            loan_amount = price - down_payment
            monthly_rate = rate / 12 / 100
            months = term * 12

            # Расчет по выбранному способу оплаты
            if self.payment_method.get() == "Аннуитетный":
                monthly_payment = self.calculate_annuity_payment(loan_amount, monthly_rate, months)
                total_interest = monthly_payment * months - loan_amount
            else:  # Дифференцированный
                payments, total_interest = self.calculate_differentiated_payments(loan_amount, monthly_rate, months)
                monthly_payment = payments[0]  # Первый платёж в таблице

            total_payment = loan_amount + total_interest
            min_income = monthly_payment / 0.3

            # Вывод результатов
            self.result_label.config(
                text=(
                    f"Ежемесячный платёж: {monthly_payment:,.2f} ₽\n"
                    f"Сумма процентов: {total_interest:,.2f} ₽\n"
f"Общая сумма выплат: {total_payment:,.2f} ₽\n"
                    f"Необходимый доход: {min_income:,.2f} ₽"
                )
            )
        except ValueError as e:
            messagebox.showerror("Ошибка ввода", str(e))

    def calculate_annuity_payment(self, loan_amount, monthly_rate, months):
        """Расчет аннуитетного платежа."""
        return loan_amount * monthly_rate * (1 + monthly_rate) ** months / ((1 + monthly_rate) ** months - 1)

    def calculate_differentiated_payments(self, loan_amount, monthly_rate, months):
        """Расчет дифференцированных платежей."""
        payments = []
        total_interest = 0

        for i in range(1, months + 1):
            principal_payment = loan_amount / months
            interest_payment = (loan_amount - (i - 1) * principal_payment) * monthly_rate
            monthly_payment = principal_payment + interest_payment
            payments.append(monthly_payment)
            total_interest += interest_payment

        return payments, total_interest
