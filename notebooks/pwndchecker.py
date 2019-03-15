import hashlib
import requests
import sys

def read_file(filename):
    """
    read in the file.
    args:
        filename, should be a relative path as a string pointing to
        a comma-separted list of passwords as strings
    returns:
        password list object
    """
    with open(filename, 'r') as f:
        pwd_list = f.readlines()
    pwd_list = pwd_list[0].split(',')
    pwd_list = [pwd.replace("'",'') for pwd in pwd_list]
    return pwd_list


def make_hash(pwd):
    """
    return hashed version of a single password
    args:
        a single password as a string
    returns:
        a single hashed version of the input password
    """
    encoded_pwd = bytes(pwd, 'utf-8')
    hashed_pwd = hashlib.sha1(encoded_pwd)
    decoded_hash = hashed_pwd.hexdigest()
    return decoded_hash

def query_api(decoded_hash):
    """
    query the API with the first 5 characters of the decoded hashed password (the prefix) using https
    args:
        a single hashed password as a string
    returns:
        - the status code that should always be 200, the API should not return a 404
        - a list of suffixes matching the prefix and the count of how many times each was found
    """
    prefix = decoded_hash[:5]
    url = 'https://api.pwnedpasswords.com/range/' + prefix
    r = requests.get(url)
    print(f'request status code: {r.status_code}')
    api_results = r.text.split()
    return api_results

def pwned_count(query_api_results, decoded_hash):
    """
    check whether a given hash is in the list of return matching hashes and returns count found
    args:
        - a hashed password to check
        - a list of matching suffixes for an input decoded_hash
    returns:
        prints out the results
        returns None
    """
    count = 0
    decoded_hash_section = decoded_hash[5:].lower()
    for result in query_api_results:
        clean_res = result.split(':')
        if decoded_hash_section == clean_res[0].lower():
            count = int(clean_res[1])
            print(f'WARNING: {clean_res[0]} was pwned {clean_res[1]} times.')
    if count == 0:
        print(f'CLEAR: {clean_res[0]} was not in the pwned database.')
    return

if __name__ == "__main__":
    pwd_list = read_file(sys.argv[1])
    hashed_pwds = [make_hash(pwd) for pwd in pwd_list]
    for hashed_pwd in hashed_pwds:
        test_results = query_api(hashed_pwd)
        pwned_count(test_results, hashed_pwd)
