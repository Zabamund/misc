########################################################
#
# Acknowledgements:
#
# This code would not exist without
# Troy Hunt: twitter.com/troyhunt?ref_src=twsrc%5Egoogle%7Ctwcamp%5Eserp%7Ctwgr%5Eauthor
# the creator of haveibeenpwned.com
#
########################################################
#
# Usage:
#
# $ python pwnd_email_checker.py
#
# where `enviro.account_list` is a *.py file containing:
# account_list = ['email1@domain.com', 'email2@domain.com']
#
########################################################

import requests
import json
import urllib
from enviro import account_list, haveibeenpwnd_API_key
import time

def encode_account(account):
    """
    encode an email address for GET request
    args:
        email address like 'example@example.come'
    returns:
        encoded email string
    """
    return urllib.parse.quote(account)

def query_api(account):
    """
    post GET request to haveibeenpwned.com to check whether given email has been pwnd
    args:
        email address to check like 'example@example.com'

    prints out response to CLI

    returns:
        None
    """
    # set up and run query
    headers = {'User-Agent': 'Pwnage-Checker-For-Manjaro', 'hibp-api-key': haveibeenpwnd_API_key}
    url = 'https://haveibeenpwned.com/api/v3/breachedaccount/' + encode_account(account) + '?truncateResponse=false'
    r = requests.get(url, headers=headers)
    #print(f'request status code: {r.status_code}')

    # check result code and print output
    if r.status_code == 401:
        print('Bad credentials, check authorization\n')

    if r.status_code == 404:
        print(f'Response code: {r.status_code} email not found — <{account}> has not been pwned\n')
        return

    if r.status_code == 200:
        raw_results = r.text
        results = json.loads(raw_results)
        output = {}
        for res in results:
            output[res['Name']] = {'BreachDate': res['BreachDate'],
                                 'AddedDate': res['AddedDate'],
                                 'IsVerified': res['IsVerified'],
                                  }
        print(f'Response code: {r.status_code} email found — <{account}> has been pwned {len(results)} times:')
        print(output)
        print('\n')

    if r.status_code == 429:
        print('Exceeding rate limit')
    return

def check_accounts(account_list):
    """
    Calls `query_api()` on each account in a list of email accounts to see if any are pwnd
    args:
        list of accounts to check like:
        ['example1@example.com', 'example2@example.com', 'example3@example.com']
    returns:
        None
    """
    print('Accounts to check:\n')
    for account in account_list:
        print(account)
    print('\n=======\n')
    for account in account_list:
        query_api(account)
        time.sleep(2)

    return

if __name__ == "__main__":
    check_accounts(account_list)
    print(f'\nDone, all accounts have been checked')
