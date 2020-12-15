class Transaction:
    def __init__(self, CreditCardNumber, CardHolder, ExpirationDate, SecurityCode, Amount):
        self.CreditCardNumber = CreditCardNumber
        self.CardHolder = CardHolder
        self.ExpirationDate = ExpirationDate
        self.SecurityCode = SecurityCode
        self.Amount = Amount


class TransactionResponse:
    def __init__(self, TransactionNumber, Status):
        self.TransactionNumber = TransactionNumber
        self.Status = Status
