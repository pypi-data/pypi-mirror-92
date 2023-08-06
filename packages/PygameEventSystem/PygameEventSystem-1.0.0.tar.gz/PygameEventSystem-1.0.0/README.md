## Super Simple and efficient EventSystem for python

##### Example:
```python
def printHello():
  print("hello")

e = Event()     # Create event system
e += printHello # Add printHello to the event
e()             # Output "hello"
e -= printHello # Remove it again
e()             # Does nothing because there are no subscribed functions
```
