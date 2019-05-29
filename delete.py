import session
import settings
from warnings import warn
import exceptions
import json

class Delete:
    def __init__(self):
        """
        A collection of DELETE requests made to the ECM3 API
        """
        self.api = session.Session()

    @exceptions.common_exceptions_decorator
    def callback_url(self,):
        """
        Delete the current callback URL from ECM3

        :Example:
        callback_url()

        :Returns:
        'Callback URL deleted.'
        """
        self.api.endpoint = 'BACS/callback'
        response = self.api.delete()
        # NULL will be returned if a callback URL does not exist
        if str(response) == '{"Message":null}':
            return 'An unknown error has occurred.'
        else:
            # Use requests.json to get the part of the response we need.
            return 'Callback URL deleted.'

    @exceptions.common_exceptions_decorator
    def payment(self, contract, payment, comment):
        """
        Delete a payment from ECM3, as long as it hasn't already been
        submitted to BACS.

        :Args:
        - contract - The unique GUID of the contract.
        - payment - The unique GUID of the payment.
        - comment - A comment that can be returned when querying the
                    payment

        :Example:
        customers('ab09362d-f88e-4ee8-be85-e27e1a6ce06a',
                  ')

        :Returns:
        customer json object(s)
        """
