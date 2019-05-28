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
        # Get all method arguments
        method_arguments = locals()
        # We will not be passing self into ECM3
        del method_arguments['self']
        # A set of pythonic arguments and their ECM3 counterparts
        conversions = {
            'email': 'email',
            'title': 'title',
            'date_of_birth': 'dateOfBirth',
            'search_from': 'from',
            'search_to': 'to',
            'customer_reference': 'customerRef',
            'first_name': 'firstName',
            'surname': 'surname',
            'company_name': 'companyName',
            'post_code': 'postCode',
            'account_number': 'accountNumber',
            'sort_code': 'bankSortCode',
            'account_holder_name': 'accountHolderName',
            'home_phone': 'homePhoneNumber',
            'work_phone': 'workPhoneNumber',
            'mobile_phone': 'mobilePhoneNumber',
        }

        parameters = {}
        key = None
        if settings.warnings['customer_search'] and all(
                value == '' for value in method_arguments.values()):
            warn('Retrieving customers without using any search times '
                 'may take some time.')

        try:
            for key, value in method_arguments.items():
                if value != '':
                    parameters.update({conversions[key]: value})
        except KeyError:
            # Raise custom error if the passed parameter is not defined
            raise exceptions.InvalidParameterError(
                '%s is not an acceptable argument for this call, refer'
                'to the man page for all available arguments' % key
            )

        self.api.endpoint = 'customer'
        self.api.params = parameters
        response = self.api.get()

        if str(response) != '{"Customers":[]}':
            return response
        else:
            return 'No customers could be found using the search terms:' \
                   '%s' % parameters
