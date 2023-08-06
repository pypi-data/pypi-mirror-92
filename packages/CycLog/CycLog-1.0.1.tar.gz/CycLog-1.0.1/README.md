# CycleLog

This library will let you log into a cyclic file easily. You

####  What is a cycle log?
- A cycle log is a log file which does not keep more than N lines, once the log reaches N lines the logger will delete older lines from the beginning,
so you can only have latest logs which you need to figure out the error, to reproduce last steps, and such.


### basic example:
```python
from CycLog import CycleLogger

logger = CycleLogger(
    file_name="your_project.log"
)
for i in range(10):
    logger.log(i)
```

which will be logged:

```
[27/01/2021 - 19:36] : 0
[27/01/2021 - 19:36] : 1
[27/01/2021 - 19:36] : 2
[27/01/2021 - 19:36] : 3
[27/01/2021 - 19:36] : 4
[27/01/2021 - 19:36] : 5
[27/01/2021 - 19:36] : 6
[27/01/2021 - 19:36] : 7
[27/01/2021 - 19:36] : 8
[27/01/2021 - 19:36] : 9

```

Since the default max lines is 500, we got the entire log. let's try to change it to 5:

```python
from CycLog import CycleLogger

logger = CycleLogger(
    file_name="your_project.log",
    max_lines=5
)
for i in range(10):
    logger.log(i)
```

And now we only get the last 5 lines.
```
[27/01/2021 - 19:38] : 5
[27/01/2021 - 19:38] : 6
[27/01/2021 - 19:38] : 7
[27/01/2021 - 19:38] : 8
[27/01/2021 - 19:38] : 9

```

In principle you can gives any object that has `__str__` method, `logger.log` 
converts implicitly any object to string.


### Few more settings:

> `include_date: bool`, default: `True`
>>determines whether to add time to log message or not.
> **it affects the format message only in case of the format message is the default.**
>>> for example, without date, a typical message will look:
>>>> `[19:38] : 9` 

> `include_time: bool`, default: `True`
>>determines whether to add date to log message or not.
> **it affects the format message only in case of the format message is the default.**
>>> for example, without time, a typical message will look:
>>>> `[27/01/2021] : 9`


>if both `include_time` and `include_date` will be False, a log will only show the message itself.

> `max_lines: int`, default: `500`.
>>Determines the maximum of lines in a file.

>`message_format: str`, default: `"[{date} - {time}] : {message}"`
>> you can set it to your own message and then you 
can add keyword arguments to `logger.log`, for example:
>>> `logger.log("hello")` will log `hello`, without date or time.
 ```python
from CycLog import CycleLogger

logger = CycleLogger(
    file_name="your_project.log",
    max_lines=5,
    message_format=CycleLogger.MESSAGE_FORMAT + " [from {name} - {n}]"
)
for i in range(10):
    logger.log(i, name="Jonatan", n=i)
```
will be 
```[27/01/2021 - 19:50] : 5 [from Jonatan - 5]
[27/01/2021 - 19:50] : 6 [from Jonatan - 6]
[27/01/2021 - 19:50] : 7 [from Jonatan - 7]
[27/01/2021 - 19:50] : 8 [from Jonatan - 8]
[27/01/2021 - 19:50] : 9 [from Jonatan - 9]
```
>`date_format: str`, default: `"%d/%m/%Y"`
>> Determines how the date will look. 

>`time_format: str`, default: `"%H:%M"`
>> Determines how the time will look.

>`file_mode: str`, default: `a+`
>> A mode to open the file in, the mode must be writable and readable.
> you can see a list of modes and explanation: https://docs.python.org/3/library/functions.html#open