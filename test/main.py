import unittest

# from models import manage

# def db_init():
#     print('============Data Base Init Start============')
#     manage.delete_all()
#     manage.create_all()
#     print('============Data Base Init Complete============')


def run_all_test():
    # db_init()

    print('============Unit Test Start============')
    testSuite = unittest.TestSuite()
    module_strings = ['ocr'
                      ]
    [__import__(model_str) for model_str in module_strings]
    suites = [unittest.TestLoader().loadTestsFromName(model_str) for model_str in module_strings]
    [testSuite.addTest(suite) for suite in suites]

    result = unittest.TestResult()
    testSuite.run(result)
    print('============Unit Test Complete============')
    print()
    print('============Test Result Count============')
    print(result)
    print()

    def print_errors(elements):
        for element in elements:
            print(element[0])  # Error class.function_name
            print(element[1])  # Error Trace Back
            print()

    if len(result.errors) != 0:
        print('============Error List============')
        print_errors(result.errors)

    if len(result.failures) != 0:
        print('============Failure List============')
        print_errors(result.failures)

    print()

    # Ok, at this point I have a result
    # How do I display it as the normal unit test command line output?


if __name__ == "__main__":
    run_all_test()