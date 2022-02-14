# Python Test Structure

This is a typical structure for a python test file.

## File

AAA structure.  
We can imagine our test is split into 3 sections:

* Arrange: this is were we prepare our context
* Act: here we run the behaviour we want to test
* Assert: here we check for conditions

```python
import unittest


class TestFunctionality(unittest.TestCase):
    def setUp(self):
        # Here we assign to this class all common variables we need
        # for the tests
        self.common_required_var = 2
        self.sample_resource = open(filename, 'r')

    def tearDown(self):
        # Here we cleanup what was required to run the tests
        close(self.sample_resource)
    
    def test_behaviour_1(self):
        # Arrange
        x = 1
    
        # Act
        result = f(x)

        # Assert
        self.assertTrue(result)

    def test_behaviour_2(self):
        # Arrange
        x = 1
        y = foo(self.common_required_var)
    
        # Act
        result = bar(x, y)

        # Assert
        self.assertTrue(result)
```

