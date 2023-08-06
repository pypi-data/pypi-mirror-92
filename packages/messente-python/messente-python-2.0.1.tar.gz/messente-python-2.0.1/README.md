# messente-python

Messente SMS API library for Python 3.6+.

Full documentation: <https://messente.com/documentation>

## Installation

The library can be installed/upgraded via pip:

```
pip install messente-python==2.0.1
```

or by using setuptools:

```
python setup.py build
python setup.py install
```

## Examples

You can find sample scripts in the 'examples' directory.

## Configuration parameters

Configuration parameters can passed via:
- keyword arguments in constructor
- configuration file (*.ini)

Authentication parameters can also be set in environment instead:
- **MESSENTE_API_USERNAME**
- **MESSENTE_API_PASSWORD**

### Configuration file

Configuration can be stored in a *.ini file (please see config.sample.ini).
The path to the file can be passed to a contructor as "ini_path" keyword argument:

```python
from messente.api.sms import Messente
api = messente.Messente(ini_path="some/path/filename.ini")
```

Configuration file is divided into following sections:
- default
- sms
- delivery
- credit
- pricing
- number-verification

All the module specific sections can override any of
the parameters in the "default" section.


### Logging configuration

The library uses logging module from standard python library, and
logging should be configured by the application that uses this library.
For more information, please visit:
https://docs.python.org/3/howto/logging.html

# LICENSE

Apache Licence, Version 2
