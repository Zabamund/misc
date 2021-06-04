import ifname_module_0

def whoami():
    print("I am module 1 and my __name__ is: {}".format(__name__))
    return None


def main():
    print('whoami from module 1:')
    whoami()
    print('whoami from module 0:')
    ifname_module_0.whoami()
    return None

if __name__ == '__main__':
    main()