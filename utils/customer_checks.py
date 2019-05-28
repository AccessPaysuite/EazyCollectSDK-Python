from exceptions import InvalidParameterError
from re import search as s


def check_postcode_is_valid_uk_format(post_code):
    """ A simple regex check to determine whether a postcode is a valid
    format. Overseas or BFPO codes are not accepted.
    """
    r = s(
        '^([A-Za-z][A-Ha-hJ-Yj-y]?[0-9][A-Za-z0-9]? ?[0-9][A-Za-z]{2}|[Gg][Ii]'
        '[Rr] ?0[Aa]{2})$', post_code
    )
    if not r:
        raise InvalidParameterError(
            '%s is not formatted as a UK post code. Please check the post code'
            ' and re-submit.' % post_code
        )
    else:
        pass


def check_email_address_format(email_address):
    """ A non-RFC complaint regex search to determine the validity of an
    email address. Covers 99.99% of use cases.
    """
    r = s(
        '(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)', email_address
    )
    if not r:
        raise InvalidParameterError(
            '%s is not a valid email address. Please check the email address'
            ' and re-submit.' % email_address
        )
    else:
        pass


def check_bank_details_format(account_number, sort_code, account_name):
    """ A simple bank account detail check. This does not verify
    whether a bank account exists or whether the sort code matches to
    the account number.
    """
    num_r = s(
        '^[0-9]{8}$', account_number
    )
    sort_r = s(
        '^[0-9]{6}$', sort_code
    )
    name_r = s(
        '^[A-Z0-9\-\/& ]{3,18}$', account_name.upper()
    )
    if not num_r:
        raise InvalidParameterError(
            '%s is not formatted as a UK bank account number. UK bank'
            ' account numbers are 8 digits long. Please check the bank'
            ' account number and re-submit.' % account_number
        )
    elif not sort_r:
        raise InvalidParameterError(
            '%s is not formatted as a UK sort code. UK sort codes are 6 digits'
            ' long. Make sure to not include any hyphens. Please check the'
            ' sort code and re-submit.' % sort_code
        )
    elif not name_r:
        raise InvalidParameterError(
            '%s is not formatted as an account holder name. Account holder'
            ' names must be between 3 and 18 characters, contain only capital'
            ' letters (A-7), ampersands (&), hyphens (-), forward'
            ' slashes (/), and spaces ( ).' % account_name
        )
    else:
        pass
