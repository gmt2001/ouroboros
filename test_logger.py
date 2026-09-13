import logging
from pyouroboros.logger import BlacklistFilter

logger = logging.getLogger('test')
handler = logging.StreamHandler()
logger.addHandler(handler)

# Test 1: short string
short_filter = BlacklistFilter(['pass'])
record1 = logging.LogRecord('test', logging.INFO, '', 0, 'Password is pass.', (), None)
short_filter.filter(record1)
print(f"Test 1 MSG: {record1.msg}")
assert record1.msg == 'Password is ********.', f"Failed: {record1.msg}"

# Test 2: long string
long_filter = BlacklistFilter(['password123'])
record2 = logging.LogRecord('test', logging.INFO, '', 0, 'My password is password123!', (), None)
long_filter.filter(record2)
print(f"Test 2 MSG: {record2.msg}")
assert record2.msg == 'My password is ********rd123!', f"Failed: {record2.msg}"

# Test 3: arguments short string
record3 = logging.LogRecord('test', logging.INFO, '', 0, 'Arg pass: %s', ('pass',), None)
short_filter.filter(record3)
print(f"Test 3 ARGS: {record3.args}")
assert record3.args[0] == '********', f"Failed: {record3.args}"

# Test 4: arguments long string
record4 = logging.LogRecord('test', logging.INFO, '', 0, 'Arg password: %s', ('password123',), None)
long_filter.filter(record4)
print(f"Test 4 ARGS: {record4.args}")
assert record4.args[0] == '********rd123', f"Failed: {record4.args}"

print("All tests passed.")
