# pyppy
*pyppy* is a Python library that allows to initialize a global config object that can be used
throughout your code without passing a config object between all of your methods. Additionally, 
pyppy comes with a function decorator that allows for easy retrieval of config attributes in methods.


## Please Read the Docs
https://pyppy.readthedocs.io/en/latest/

## Installation
```bash
pip install pyppy
```

## Table of Contents
  * [Usecases](#usecases)
  * [Global Config Object](#global-config-object)
  * [Automatic Argument Filling from Config Object](#automatic-argument-filling-from-config-object)
    + [Automatic Detection of Arguments to be Filled](#automatic-detection-of-arguments-to-be-filled)
    + [Mixed Parameters](#mixed-parameters)
    + [Explicit Parameter Filling](#explicit-parameter-filling)
  * [Conditional Execution of Functions based on Global Config State](#conditional-execution-of-functions-based-on-global-config-state)
    + [Exact Value Matching](#exact-value-matching)
    + [Custom Conditions](#custom-conditions)
    + [Logical Conjunction and Disjunction of Conditions](#logical-conjunction-and-disjunction-of-conditions)
  * [Enhancements](#enhancements)
  * [Contribution](#contribution)

## Usecases
*pyppy* might help you if you want one of the following: 
* Easy global config access throughout your code 
* Execute methods conditionally based on the global configuration

## Global Config Object
More here: https://pyppy.readthedocs.io/en/latest/pyppy.config.html 

You can use the method ```initialize_config``` to initialize a global config and then use
the config with ```config()``` all throughout your project. In the following example we use 
it as a wrapper for arguments parsed with ```ArgumentParser``` but you can you any object
that has attributes to initialize a config.  
```python
from argparse import ArgumentParser
from pyppy.config import initialize_config, config

parser = ArgumentParser()
parser.add_argument(
    "--debug",
    action="store_true",
    default=False
)

cli_args = ["--debug"]
args = parser.parse_args(cli_args)

initialize_config(args)

def debug_log():
    if config().debug:
        return "debugging"

>>> debug_log()
debugging
```

## Automatic Argument Filling from Config Object
More here: https://pyppy.readthedocs.io/en/latest/pyppy.args.html
### Automatic Detection of Arguments to be Filled
It gets even better. You can use the ```@fill_args``` decorator to automatically fill
function arguments from the global config object. If a function argument has the same name 
as an attribute of your config it will automatically be filled with the corresponding value.
(We're assuming here you have initialized the same config as in the last example.)
```python
from pyppy.args import fill_args

initialize_config()
config().debug = True

@fill_args()
def debug_log(debug):
    if debug:
        return "debugging"

>>> debug_log()
debugging
```
### Mixed Parameters
If you have mixed parameters (parameters coming from the global config and parameters passed ad-hoc)
the decorator only fills the arguments which names exactly match with one of the attributes of 
the global config. **Please note** that the "normal" parameters
can then only be passed as keyword arguments when calling the function.   
```python
from pyppy.config import initialize_config, config

initialize_config()
config().debug = True

@fill_args()
def debug_log(debug, message):
    if debug:
        return f"debugging: {message}"

>>> debug_log(message="useful logs") 
debugging: useful logs
```
### Explicit Parameter Filling
In some cases it's necessary to tell the decorator exactly which arguments should be filled
from the global config (e.g. when a function argument has the same name as an attribute of the 
global config but should not be filled from the global config). Then you can pass the names of
the arguments to be filled to the decorator as strings. The decorator will then only fill the
parameters that are explicitly passed.
```python
initialize_config()
config().debug = True

@fill_args("debug")
def debug_log(debug, message):
    if debug:
        return f"debugging: {message}"

>>> debug_log(message="useful logs")
debugging: useful logs
```
## Conditional Execution of Functions based on Global Config State
More here: https://pyppy.readthedocs.io/en/latest/pyppy.conditions.html

### Exact Value Matching
*pyppy* allows you to execute functions based on conditions in your global config object.
In the example below, the ```@condition``` decorator will only execute the decorated function
when the specified condition evaluates to true in based on the global config. An expression
like ```exp(debug=True)``` means that the function will only be executed if the attribute ```debug```
has the value ```True```. 
```python
from pyppy.conditions import Exp, condition

initialize_config()
config().debug = False

@condition(Exp(debug=True))
def debug_log():
    return "hello"

>>> debug_log()
<no output>

>>> config().debug = True

>>> debug_log()
hello
```
### Custom Conditions
In cases you want to apply more complex conditions the decorator allows you to pass
a function with custom logic. The function should always return a boolean value (which
specifies if the decorated function should be executed or not). In the example below, we
use a lambda function but you can naturally use normal functions too. The only requirements
are that the function should exactly expect one argument (the global config) and should return
a boolean value.
```python

initialize_config()
config().log_level = "WARN_LEVEL_1"

@condition(Exp(lambda config: config.log_level.startswith("WARN")))
def log_warn():
    return "WARNING"

>>> log_warn()
WARNING

>>> config().log_level

>>> log_warn()
INFO_LEVEL_2

```
### Logical Conjunction and Disjunction of Conditions
If you have multiple conditions that have to be true at the same time or either one has
to be true you can use ```or_``` and ```and_``` to build the logic around them. ```or_``` and
```and``` can be nested if necessary. 

```python
from pyppy.conditions import condition, Exp, and_

initialize_config()
config().log_level = "WARN"
config().specific_log_level = "LEVEL_1"

@condition(
    and_(
        Exp(log_level="WARN"),
        Exp(specific_log_level="LEVEL_1")
    )
)
def log_warn_level_1():
    return "WARNING LEVEL 1"

>>> log_warn_level_1()
WARNING LEVEL 1

>>> config().log_level = "INFO"

>>> log_warn_level_1()
<no output>
```
## Enhancements
We're working on some enhancements so stay tuned :)

## Contribution
Feel free to create pull requests or contact me if you want to become a permanent 
contributor. 
