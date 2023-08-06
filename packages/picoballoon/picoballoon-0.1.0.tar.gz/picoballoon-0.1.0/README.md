# Picoballoon API


## Install script
To install the package run:<br>
`pip install -e git+https://gitlab.com/picoballoon/python-api.git#egg=picoballoon`


## Example
```python
from picoballoon import Picoballoon

picoballoon = Picoballoon(1)

measure = picoballoon.Measure().packet(1)

print(measure.getAltitude())
```