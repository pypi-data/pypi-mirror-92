## nojazz

A collection of one-off functions I use for various tasks as a Data Scientist-- if it ain't broke, don't fix it.

Name inspired by my favorite Pearls Before Swine comic

![img](docs/comic.jpg)

Disclaimer: I also like jazz

## Installation

`nojazz` [is hosted on PyPI](https://pypi.org/project/nojazz/) and can be installed with a simple

`pip install nojazz`

## Features

As mentioned above, I finally sat down to make this package after noticing that I was copying a lot of the same helper methods from project to project. To that end, `nojazz` is hardly comprehensive (nor necessarily related, submodule to submodule) but has a few, small "figured it out once and packaged it for reuse" utilities for:

### sqlite3

My first and biggest re-use culprit. `nojazz` provides a simple context manager to allow that handles all of the connection/commit/closing of sqlite database functions.

``` python
with connect_to_db('test.db') as cursor:
    cursor.execute('some sql')
```

Note, this will generate a `nojazz_conf.py` at the root of your project when calling. The library uses this to read the *directory* location for all of these database connections (i.e. on another drive, perhaps)

### pandas

There are all kinds of tricks to this library. For now, `nojazz` provides the following helper methods

#### `fill_time_series_nulls`

For a given dataset with rows: agents and columns: observations, there are applications where want to consider `NULL` values as `0`, *but only after the user has shown up for the first time*. This function does this, at the row-level and returns a copy of the original DataFrame. For example

```
   0    1     2     3     4
0  1   NaN   NaN    1    NaN
1 NaN  NaN   1     NaN    1

```
transforms to

```
   0    1     2     3     4
0  1    0     0     1    NaN
1 NaN  NaN    1     0     1

```

#### `realign_nonnull_data`

Similar to `fill_time_series_nulls`, this function is used when you want to line all of your records up to the same starting period. Like so

```
    0     1     2    3
0  NaN   NaN   NaN   1
1  NaN   NaN    1    1
2  NaN    1     1    1
```

transforms to

```
    0     1     2    3
0   1    NaN   NaN   NaN
1   1     1    NaN   NaN
2   1     1     1    NaN
```

Note, this likely means needing to rename the columns to something more appropriate. Furthermore, we maintained the shape of the original DataFrame by padding all extra fields with `NaN`