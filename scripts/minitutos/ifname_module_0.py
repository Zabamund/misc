def whoami():
    print("I am module 0 and my __name__ is: {}".format(__name__))
    return None


def main():
    whoami()
    return None

if __name__ == '__main__':
    main()