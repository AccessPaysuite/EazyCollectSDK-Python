import session
import exceptions
from exceptions import InvalidParameterError
from exceptions import ResourceNotFoundError
from utils import customer_checks
from utils import contract_checks


class Patch:
    def __init__(self):
        """
        A collection of PATCH requests made to the ECM3 API
        """
        self.api = session.Session()

    @exceptions.common_exceptions_decorator
    def customer(
            self, customer, email='', title='', date_of_birth='',
            first_name='', surname='', company_name='', line1='', post_code='',
            account_number='', sort_code='', account_holder_name='',
            home_phone='', mobile_phone='', work_phone='', line2='',
            line3='', line4='', initials=''
                 ):
        """
        Modify a customer in ECM3

        :Required args:
        - customer - The GUID of the customer to be modified within ECM3.

        :Optional args:
        - email - The email address of the customer. This must be unique
        - title - The title of the customer
        - first_name - The first name of the customer
        - surname - The surname of the customer
        - line1 - The first line of the customers address
        - post_code - The post code of the customer
        - account_number - The bank account number of the customer
        - sort_code - The sort code of the customer
        - account_holder_name - The customers full name as it appears
            on their bank account
        - line2 - The second line of the customers address
        - line3 - The third line of the customers address
        - line4 - The fourth line of the customers address
        - company_name - The name of the company the customer represents
        - date_of_birth - The date of birth of the customer,
            formatted to ISO standards (YYYY-MM-DD)
        - initials - The initials of the customer
        - home_phone - The home phone number of the customer
        - work_phone - The work phone number of the customer
        - mobile_phone - The mobile phone number of the customer

        :Example:
        customer(email='test@email.com')

        :Returns:
        'customer {guid} updated successfully'
        """
        # Get all method arguments
        method_arguments = locals()
        # We will not be passing self into ECM3
        del method_arguments['self']
        # A set of pythonic arguments and their ECM3 counterparts
        conversions = {
            'email': 'email',
            'title': 'title',
            'customer_reference': 'customerRef',
            'first_name': 'firstName',
            'surname': 'surname',
            'line1': 'line1',
            'post_code': 'postCode',
            'account_number': 'accountNumber',
            'sort_code': 'bankSortCode',
            'account_holder_name': 'accountHolderName',
            'line2': 'line2',
            'line3': 'line3',
            'line4': 'line4',
            'company_name': 'companyName',
            'date_of_birth': 'dateOfBirth',
            'initials': 'initials',
            'home_phone': 'homePhone',
            'work_phone': 'workPhone',
            'mobile_phone': 'mobilePhone',
        }
        parameters = {}

        key = None
        try:
            for key, value in method_arguments.items():
                if key == 'customer':
                    pass
                else:
                    parameters.update({conversions[key]: value})
        except KeyError:
            raise exceptions.ParameterNotAllowedError(
                '%s is not an acceptable argument for this call, refer'
                'to the man page for all available arguments' % key
            )

        # A collection of tests against required params
        if post_code != '':
            customer_checks.check_postcode_is_valid_uk_format(post_code)
        elif email != '':
            customer_checks.check_email_address_format(email)
        elif account_number != '':
            customer_checks.check_bank_details_format(
                account_number, '123456', 'Dummy data'
            )
        elif sort_code != '':
            customer_checks.check_bank_details_format(
                '12345678', sort_code, 'Dummy data'
            )
        elif account_holder_name != '':
            customer_checks.check_bank_details_format(
                '12345678', '123456', account_holder_name
            )

        self.api.endpoint = 'customer/' + customer
        self.api.params = parameters
        response = self.api.patch()

        if 'Customer updated' in response:
            return 'customer ' + customer + ' updated successfully'

        return response

    @exceptions.common_exceptions_decorator
    def contract_amount(self, contract, amount, comment):
        # Get all method arguments
        method_arguments = locals()
        # We will not be passing self into ECM3
        del method_arguments['self']
        # A set of pythonic arguments and their ECM3 counterparts
        parameters = {
            'amount': amount,
            'comment': comment,
        }
        for key, value in method_arguments.items():
            if value == '':
                raise InvalidParameterError(
                    key + ' cannot be empty.'
                )
        try:
            am = float(amount)
        except:
            raise InvalidParameterError('amount must be a number.')

        self.api.endpoint = 'contract/' + contract + '/amount'
        self.api.params = parameters
        response = self.api.patch()

        if 'Contract updated' in response:
            return 'Contract ' + contract + ' amount updated to ' + str(amount)
        elif 'Contract not found' in response:
            raise ResourceNotFoundError(
                contract + ' is not a contract belonging to this client.'
            )
        return response

    @exceptions.common_exceptions_decorator
    def contract_day_weekly(self,):
        return 'this function currently does not work as intended.'

    @exceptions.common_exceptions_decorator
    def contract_date_monthly(self, contract, new_day, comment,
                              amend_next_payment, next_payment_amount=''):
        # Get all method arguments
        method_arguments = locals()
        # We will not be passing self into ECM3
        del method_arguments['self']
        # A set of pythonic arguments and their ECM3 counterparts
        parameters = {
            'monthDay': new_day,
            'comment': comment,
            'patchNextPayment': amend_next_payment,
            'nextPaymentPatchAmount': next_payment_amount,
        }

        for key, value in method_arguments.items():
            if value == '' and key != 'next_payment_amount':
                raise InvalidParameterError(
                    key + ' cannot be empty.'
                )
        if amend_next_payment and next_payment_amount == '':
            raise InvalidParameterError(
                'next_payment_amount cannot be empty if amend_next_payment is'
                ' set to true.'
            )

        contract_checks.check_payment_day_in_month(new_day)
        self.api.endpoint = 'contract/' + contract + '/monthly'
        self.api.params = parameters
        response = self.api.patch()

        if 'Contract updated' in response:
            return 'Contract ' + contract + ' day updated to ' + str(new_day)
        elif 'Contract not found' in response:
            raise ResourceNotFoundError(
                contract + ' is not a contract belonging to this client.'
            )
        return response

    @exceptions.common_exceptions_decorator
    def contract_date_annually(self, contract, new_day, new_month, comment,
                               amend_next_payment, next_payment_amount=''):
        # Get all method arguments
        method_arguments = locals()
        # We will not be passing self into ECM3
        del method_arguments['self']
        # A set of pythonic arguments and their ECM3 counterparts
        parameters = {
            'monthDay': new_day,
            'month': new_month,
            'comment': comment,
            'patchNextPayment': amend_next_payment,
            'nextPaymentPatchAmount': next_payment_amount,
        }

        for key, value in method_arguments.items():
            if value == '' and key != 'next_payment_amount':
                raise InvalidParameterError(
                    key + ' cannot be empty.'
                )
        if amend_next_payment and next_payment_amount == '':
            raise InvalidParameterError(
                'next_payment_amount cannot be empty if amend_next_payment is'
                ' set to true.'
            )
        contract_checks.check_payment_day_in_month(new_day)
        self.api.endpoint = 'contract/' + contract + '/annual'
        self.api.params = parameters
        response = self.api.patch()

        if 'Contract updated' in response:
            return 'Contract ' + contract + ' day updated to ' + \
                   str(new_day) + ' and month updated to ' + str(new_month)
        elif 'Contract not found' in response:
            raise ResourceNotFoundError(
                contract + ' is not a contract belonging to this client.'
            )
        return response
