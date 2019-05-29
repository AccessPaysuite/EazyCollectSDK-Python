from datetime import datetime
from utils.contract_checks import check_working_days_in_future
from settings import direct_debit_processing_days
from settings import payments as s_payments
from warnings import warn
from exceptions import InvalidParameterError


def check_collection_date(collection_date):
    date_format = '%Y-%m-%d'
    desired_date = datetime.strptime(collection_date, date_format).date()
    ongoing_days = direct_debit_processing_days['ongoing']
    first_date = check_working_days_in_future(ongoing_days)

    if desired_date < first_date:
        if s_payments['auto_fix_payment_date']:
            warn(
                '%s is not a valid start date. The earliest start date '
                'available is %s. This date has automatically been'
                ' selected.'
                % (desired_date, first_date)
            )
            return str(first_date)
        raise InvalidParameterError(
            '%s is not a valid start date. The earliest start date available'
            ' is %s. Please change this and re-submit.'
            % (desired_date, first_date)
        )
    else:
        pass


def is_credit_allowed_check():
    if s_payments['is_credit_allowed']:
        pass
    else:
        warn(
            'This client cannot use the is_credit function. It has been'
            ' automatically disabled.'
        )
        return False


def check_collection_amount(collection_amount):
    try:
        if float(collection_amount) >= 0.01:
            pass
        else:
            raise InvalidParameterError(
                'The collection amount must be positive. Zero or'
                ' non-negative amounts are not allowed.'
            )
    except:
        raise InvalidParameterError(
            'collection_amount must be a number.'
        )