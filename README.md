# CoolOutput

## Table of Contents

1. [About The Project](#about-the-project)
   - [Built With](#built-with)
2. [Examples](#examples)
   - [Progress Bar Class](#progress-bar-class)
   - [Advanced Status Window Class](#advanced-status-window-class)

## About The Project

Wanted a bit cooler output in my python projects. For the small projects I created these two classes to make the outputs easy and fancy.

### Built With

* [Python 3.9](www.python.org)

## Examples

Some examples on how I plan on using the code.

### Progress Bar Class

If you want a full width progress bar set the width to -1.

Example Code:
```python
bar = ProgressBar('Example', 50, 20)
for i in range(50):
  bar.update_bar(i)
bar.end_bar()
```
Output of Example:
```
Example Progress: [=========>          ] 50 %
```

### Advanced Status Window Class

With the ASW we can track multiple attributes at the same time. Each attribute can have a selected visualisation. We have these 5 visualisations:

 - ProgressBar
 - Percentage
 - Division
 - Counter
 - Status

I have made a short example to each of them. Lastly there is a example how to update multiple values at once

#### ProgressBar

The progress bar will always be the full width of the window.

Example Code:
```python
asw = AdvancedStatusWindow('My Status Window')
asw.add_attribute('Example', 'ProgressBar', False, 50)
for i in range(50):
  asw.update_attribute('Example', i)
asw.close_window()
```
Output of Example:
```
Example: [=========>          ] 50 %
```

#### Percentage

Example Code:
```python
asw = AdvancedStatusWindow('My Status Window')
asw.add_attribute('Example', 'Percentage', False, 50)
for i in range(50):
  asw.update_attribute('Example', i)
asw.close_window()
```
Output of Example:
```
Example: 50 %
```

#### Division

Example Code:
```python
asw = AdvancedStatusWindow('My Status Window')
asw.add_attribute('Example', 'Division', False, 50)
for i in range(50):
  asw.update_attribute('Example', i)
asw.close_window()
```
Output of Example:
```
Example: 25/50
```
#### Counter

Example Code:
```python
asw = AdvancedStatusWindow('My Status Window')
asw.add_attribute('Example', 'Counter')
for i in range(50):
  asw.update_attribute('Example', i)
asw.close_window()
```
Output of Example:
```
Example: 25
```

#### Status

Example Code:
```python
asw = AdvancedStatusWindow('My Status Window')
asw.add_attribute('Example', 'Status')
for i in range(50):
  if (i%2) == 0:
	  asw.update_attribute('Example', 'Even')
  else: 
	  asw.update_attribute('Example', 'Odd')
asw.close_window()
```
Output of Example:
```
Example: Even
```

#### Update Many

Example Code:
```python
asw = AdvancedStatusWindow('My Status Window')
asw.add_attribute('Percentage Example', 'Percentage', False, 50)
asw.add_attribute('Division Example', 'Division', False, 100)
for i in range(50):
  asw.update_many({'Percentage Example': i, 'Division Example': i*2})
asw.close_window()
```
Output of Example:
```
Percentage Example: 50 %
Division Example: 50/100
```

#### Logging
Attributes that you want can be logged into a file.

Example Code:
```python
asw = AdvancedStatusWindow('My Status Window', '/home/myUsername/Desktop/myCoolLog.log')
asw.add_attribute('Example', 'Percentage', True, 50)
for i in range(50):
  asw.update_attribute('Example', i)
asw.close_window()
```
Example Log File:
```
Example: 0
Example: 1
Example: 2
...
```


