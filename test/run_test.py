# Requirements:
#  * python 2.6 backport of test discovery ( https://pypi.python.org/pypi/discover )
#  * xmlrunner: https://pypi.python.org/pypi/xmlrunner/1.7.3
#  * coverage.py
import os
from unittest import TestSuite, TestLoader
import sys
#import mock
import traceback

def start_checking_no_prints():
    def write_custom(*args):
        sys.__stdout__.write("".join(traceback.format_stack()))
    sys.stdout = mock.Mock(write=write_custom)

def extract_test(testsuite, name):
    test = []
    if type(testsuite) == TestSuite:
        for t in testsuite._tests:
            test+=extract_test(t, name)
    else:
        if testsuite._testMethodName == name:
            return [testsuite]
    return test

def stop_checking_no_prints():
    sys.stdout = sys.__stdout__

if __name__ == '__main__':
    import xmlrunner
    import coverage
    import argparse

    parser = argparse.ArgumentParser(description='CoinplusWeb')
    parser.add_argument('--test-name', dest="testname", help='The specify a unique test name', default=None, )
    args = parser.parse_args(sys.argv[1:])
    
    
    loader = TestLoader()

    sys.path.append(os.path.join(os.path.dirname(__file__), "bitcoinlib", "test"))

    cov = coverage.coverage(source=["src"], omit=[])
    cov.start()

    tests = loader.discover(start_dir="test", pattern='test*.py', top_level_dir="test")

    if args.testname is not None:
        new_tests = extract_test(tests, args.testname)
        tests = TestSuite(new_tests)

#    start_checking_no_prints()
    runner = xmlrunner.XMLTestRunner(output='test-reports')
    runner.run(tests)
    cov.stop()
    stop_checking_no_prints()
    cov.html_report(ignore_errors=True, directory='python-coverage-html')

