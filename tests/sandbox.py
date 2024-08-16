class Wallet:
    def __init__(self, currency, balance):
        if not isinstance(currency, str):
            raise TypeError("Неверный тип валюты")
        if len(currency) != 3:
            raise NameError("Неверная длина названия валюты")
        if not currency.isupper():
            raise ValueError("Название должно состоять только из заглавных букв")
        self.currency = currency
        self.balance = balance

    def __eq__(self, other):
        if self.currency != other.currency:
            raise TypeError(f"Нельзя сравнить разные валюты")
        if not isinstance(other, Wallet):
            raise TypeError(f"Wallet не поддерживает сравнение с {other}")
        else:
            return self.balance == other.balance

    def __add__(self, other):
        if not isinstance(other, Wallet) or self.currency != other.currency:
            raise TypeError("Данная операция запрещена")
        else:
            return Wallet(self.currency, (self.balance + other.balance))
    def __sub__(self, other):
        if not isinstance(other, Wallet) or self.currency != other.currency:
            raise TypeError("Данная операция запрещена")
        else:
            return Wallet(self.currency, (self.balance - other.balance))
