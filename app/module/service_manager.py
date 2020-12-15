import random
import string

from flask import jsonify

from .models import Transaction, TransactionResponse
from .validation_manager import ValidationManager
from .const import HttpStatus


class ServiceManager:
    def __init__(self):
        self.success = False
        self.error = HttpStatus.OK
        self.error_msg = []
        self.message = ""

    def process_payment(self, requests):

        try:
            self.req_data = requests.get_json()
        except:
            self.error = HttpStatus.BAD_REQUEST
            self.error_msg = ['Input is not in proper format']
            construct = {
                'error': self.error_msg,
                'success': self.success
            }
            response = jsonify(construct)
            response.status_code = self.error
            return response

        if 'CreditCardNumber' in self.req_data and 'CardHolder' in self.req_data and 'ExpirationDate' in self.req_data and 'SecurityCode' in self.req_data and 'Amount' in self.req_data:
            transaction = Transaction(self.req_data['CreditCardNumber'], self.req_data['CardHolder'],
                                      self.req_data['ExpirationDate'], self.req_data['SecurityCode'],
                                      self.req_data['Amount'])
        else:
            self.error = HttpStatus.BAD_REQUEST
            self.error_msg = ['Please use Appropriate Input Fields']
            construct = {
                'error': self.error_msg,
                'success': self.success
            }
            response = jsonify(construct)
            response.status_code = self.error
            return response
        self.message = ''
        if ValidationManager().validate_request(transaction):
            res = self.make_payment(transaction)

            if res.Status == 1:
                self.success = True
                self.message = "Transaction Completed with id : {}".format(res.TransactionNumber)
                self.error = HttpStatus.OK
            else:
                self.success = False
                self.error_msg = ["Transaction Unsuccessful with reference no : {}".format(res.TransactionNumber)]
                self.error = HttpStatus.OK
        else:
            self.success = False
            self.error = HttpStatus.BAD_REQUEST
            self.error_msg = ['Check your Input Fields', 'Input Valid Values']

        construct = {
            'error': self.error_msg,
            'success': self.success,
            'message': self.message
        }
        response = jsonify(construct)
        response.status_code = self.error
        return response

    def _redirect_to_payment_type_by_amount(self, transaction):
        pass

    def make_payment(self, transaction):
        if transaction.Amount <= 20:
            return self.process_cheap_payment_gateway()
        elif transaction.Amount >= 21 and transaction.Amount <= 500:
            return self.process_expensive_payment_gateway()
        else:
            return self.process_expensive_payment_gateway()

    def process_cheap_payment_gateway(self):
        return self.process_transaction()

    def process_transaction(self):
        try_count = 0
        res = None
        while try_count < 3:

            if res is None:
                res = self.generate_random_transactionResponse()
            else:
                res = self.generate_random_transactionResponse(res)

            if res.Status == 1:
                break
            try_count += 1
        return res

    def process_expensive_payment_gateway(self):
        return self.process_transaction()

    def process_premium_payment_gateway(self):
        return self.process_transaction()

    def generate_random_transactionResponse(self, transactionReport=None):
        status = random.getrandbits(1)

        if transactionReport is None:
            transactionId = self.get_transaction_key()
            return TransactionResponse(transactionId, status)

        transactionReport.Status = status
        return transactionReport

    def get_transaction_key(self):
        return ''.join(
            random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(16))
