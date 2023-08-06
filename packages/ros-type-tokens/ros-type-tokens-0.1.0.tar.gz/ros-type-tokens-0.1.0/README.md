# ROS Type Tokens

This is a small Python library that provides *type tokens* (objects that represent a type) for [Robot Operating System](https://www.ros.org/) built-in types and message types.

This library was initially developed as a utility of the [HAROS framework](https://github.com/git-afsantos/haros/), and is now distributed on its own.

## What Is In The Box

This repository contains a Python package, and the respective source code, to create (manually or automatically) type tokens for the various ROS data types.
Type tokens contain attributes not only of the type itself but also of any related subtypes.
For example:

```python
from rostypes import HEADER

HEADER.type_name    # 'std_msgs/Header'
HEADER.is_builtin   # True
HEADER.is_primitive # False
HEADER.is_message   # True
HEADER.constants    # {}
HEADER.fields       # {'seq': UINT32, 'stamp': TIME, 'frame_id': STRING}

assert HEADER.fields['seq'].is_number
assert HEADER.fields['stamp'].is_time
assert HEADER.fields['frame_id'].is_string
```

## Installing

To install this package, make sure that you have Python 2.7 or greater.
Simply run the command:

```
pip install ros-type-tokens
```

## Bugs, Questions and Support

Please use the [issue tracker](https://github.com/git-afsantos/ros-type-tokens/issues).

## Contributing

See [CONTRIBUTING](./CONTRIBUTING.md).

## Acknowledgment

This work is financed by the ERDF – European Regional Development Fund through the Operational Programme for Competitiveness and Internationalisation - COMPETE 2020 Programme and by National Funds through the Portuguese funding agency, FCT - Fundação para a Ciência e a Tecnologia within project PTDC/CCI-INF/29583/2017 (POCI-01-0145-FEDER-029583).
