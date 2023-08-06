# pyppy
## Please Read the Docs
https://pyppy.readthedocs.io/en/latest/
## Table of Contents
* [What Is It?](#what-is-it)
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

## What Is It?
*pyppy* is a Python library that allows to initialize a global config object that can be used
throughout your code without passing a config object between all of your methods. Additionally, 
pyppy comes with a function decorator that allows for easy retrieval of config attributes in methods.

In the following sections you can find some examples of what you can do with *pyppy*.

## When to Use It?
When you have a global application configuration that you want to access throughout
all your code without having to pass it around from function to function or from class to 
class.

## Installation
```bash
pip install pyppy
```

## Global Config Object
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
        print("debugging")
```
## Automatic Argument Filling from Config Object
### Automatic Detection of Arguments to be Filled
It gets even better. You can use the ```@fill_arguments``` decorator to automatically fill
function arguments from the global config object. If a function argument has the same name 
as an attribute of your config it will automatically be filled with the corresponding value.
(We're assuming here you have initialized the same config as in the last example.)
```python
@fill_arguments
def debug_log(debug):
    if debug is True:
        print("debugging")

>>> debug_log()
debugging
```
### Mixed Parameters
If you have mixed parameters (parameters coming from the global config and parameters passed ad-hoc)
the decorator only fills the arguments which names exactly match with one of the attributes of 
the global config. **Please note** that the "normal" parameters
can then only be passed as keyword arguments when calling the function.   
```python
@fill_arguments()
def debug_log(debug, message):
    if debug is True:
        print(message)

>>> debug_log(message="hello")
hello
```
### Explicit Parameter Filling
In some cases it's necessary to tell the decorator exactly which arguments should be filled
from the global config (e.g. when a function argument has the same name as an attribute of the 
global config but should not be filled from the global config). Then you can pass the names of
the arguments to be filled to the decorator as strings. The decorator will then only fill the
parameters that are explicitly passed.
```python
@fill_arguments("debug")
def debug_log(debug, message):
    if debug is True:
        print(message)

>>> debug_log(message="hello")
hello 
```
## Conditional Execution of Functions based on Global Config State
### Exact Value Matching
*pyppy* allows you to execute functions based on conditions in your global config object.
In the example below, the ```@condition``` decorator will only execute the decorated function
when the specified condition evaluates to true in based on the global config. An expression
like ```exp(debug=True)``` means that the function will only be executed if the attribute ```debug```
has the value ```True```. 
```python
from pyppy.conditions import Exp, condition
from pyppy.config import initialize_config
import types

args = types.SimpleNamespace()
args.debug = False
initialize_config(args)

@condition(exp(debug=True))
def debug_log():
    print("hello")

>>> debug_log()
<no console output>
```
### Custom Conditions
In cases you want to apply more complex conditions the decorator allows you to pass
a function with custom logic. The function should always return a boolean value (which
specifies if the decorated function should be executed or not). In the example below, we
use a lambda function but you can naturally use normal functions too. The only requirements
are that the function should exactly expect one argument (the global config) and should return
a boolean value.
```python
from pyppy.conditions import Exp, condition
from pyppy.config import initialize_config
import types

args = types.SimpleNamespace()
args.log_level = "WARN_LEVEL_1"

initialize_config(args)

@condition(exp(lambda config: config.log_level.startswith("WARN")))
def log_warn():
    print("WARNING")

>>> log_warn()
WARNING
```
### Logical Conjunction and Disjunction of Conditions
If you have multiple conditions that have to be true at the same time or either one has
to be true you can use ```or_``` and ```and_``` to build the logic around them. ```or_``` and
```and``` can be nested if necessary. 

```python
from pyppy.conditions import condition, Exp, and_
import types

args = types.SimpleNamespace()
args.log_level = "WARN"
args.specific_log_level = "LEVEL_1"

initialize_config(args)

@condition(
    and_(
        exp(log_level="WARN"),
        exp(specific_log_level="LEVEL_1")
    )
)
def log_warn_level_1():
    print("WARNING LEVEL 1")

log_warn_level_1()
```
## Enhancements
We're working on some enhancements so stay tuned :)

## Contribution
Feel free to create pull requests or contact me if you want to become a permanent 
contributor. 
