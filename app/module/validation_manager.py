import datetime
import re
from calendar import monthrange

from bson.int64 import long


class ValidationManager:
    def _validate_card_number(self, card_number):

        if len(card_number) == 0:
            return False

        try:
            str(long(card_number))
        except:
            return False
        # reverse the credit card number
        cc_num = card_number[::-1]
        # convert to integer list
        cc_num = [int(x) for x in cc_num]
        # double every second digit
        doubled_second_digit_list = list()
        digits = list(enumerate(cc_num, start=1))
        for index, digit in digits:
            if index % 2 == 0:
                doubled_second_digit_list.append(digit * 2)
            else:
                doubled_second_digit_list.append(digit)

        # add the digits if any number is more than 9
        doubled_second_digit_list = [self._sum_digits(x) for x in doubled_second_digit_list]
        # sum all digits
        sum_of_digits = sum(doubled_second_digit_list)
        # return True or False
        return sum_of_digits % 10 == 0

    def _sum_digits(self, digit):
        if digit < 10:
            return digit
        else:
            sum = (digit % 10) + (digit // 10)
            return sum

    def _validate_card_holder_name(self, card_holder):
        return bool(re.fullmatch('[A-Za-z]{2,25}( [A-Za-z]{2,25})?', card_holder))

    def _validate_expiration_date(self, expiration_date):

        try:
            date_time_obj = datetime.datetime.strptime(expiration_date, "%m/%Y")
            print(date_time_obj)
            currentTime = datetime.datetime.now()
            date_time_obj = date_time_obj.replace(day=monthrange(date_time_obj.year,date_time_obj.month)[1])
            if currentTime > date_time_obj:
                return False

        except Exception as ex:
            print(ex)
            return False


        return True

    def _validate_security_code(self, security_code):
        if len(security_code) != 3 and len(security_code)!=0:
            return re.fullmatch("^[0-9]{3}$",security_code)
        return True

    def _validate_amount(self, amount):
        try:
            amount_float = float(amount)
            if amount_float < 0:
                return False
            else:
                return True
        except:
            return False

    def validate_request(self, transaction):

        if not self._validate_card_number(transaction.CreditCardNumber):
            return False

        elif not self._validate_amount(transaction.Amount):
            return False

        elif not self._validate_card_holder_name(transaction.CardHolder):
            return False

        elif not self._validate_security_code(transaction.SecurityCode):
            return False

        elif not self._validate_expiration_date(transaction.ExpirationDate):
            return False

        else:
            return True
