Simple Metrics Manager facilitates managing metrics.

A "metric" as defined here consists of:

 * A string name (and an associated python constant)
 * A function that takes no arguments and returns some data
 * The data returned from the metric function

### StorageInterfaces

A `StorageInterface` is a class that supports storing metric data using some
persistent backend. The current default is the fairly generic '.npz' format
used to store numpy arrays and simple python objects `NpzStorageInterface`.

To prevent data corruption, it always saves data to a temp file and then
moves it into the real file (potentially replacing any older copies).

It has a simple save/load/exists API.

#### Pre-defined StorageInterface classes:

`JsonStorageInterface` uses `json.load` and `json.dump` and
automatically coerces numpy arrays to lists.

`NpyStorageInterface` just uses `np.save` and `np.load` directly.

`NpzStorageInterface` uses numpy's `np.load` and (hidden) `_savez` method.
It and does some simple checks to allow saving arrays as well as lists
of arrays and dictionaries of arrays.

This is very fast, efficient, reliable, and gives quite a bit of flexibility.

The option to `allow_pickle=False` means that saving object arrays will fail,
so change it to `True` if you need it, but pickle is considered volatile,
so changes to python or relevant package versions might mean your data
is unreadable. This is super convenient though, so it hasn't stopped big
packages like scikit-learn from relying on it.

You could also easily add a pure pickle-based storage interface yourself
with `pickle.load` and `pickle.dump`, but I don't include it here for
the reasons listed above :)



### Cache Managers

A `DatedCacheManager` uses a `StorageInterface` and supports the following:

 * Automatic caching to both memory and persistent storage,
 * Automatic cache utilization, falling back on memory cache and then
   persistent cache (override with `force=False`)
 * Dating of all metrics using "side-car" metrics (*_date)
 * Printing of all major actions (disable with `verbose=False`)


It has the following API:

 * `set_functions_dict`
   - Set the core data for the manager, a dictionary that actually defines the metrics.
     Keys are metric names and values are metric functions (no arguments).
     By calling this after `\__init__`, the manager itself can be used within metric functions.
     See "Usage" below.
 * `exists`
   - Boolean, whether the metric is in the memory cache.
 * `clear_cache`
   - Remove all metrics from the cache.
 * `compute`
   - Call a metric function.
     Caches and returns the data.
 * `save`
   - Compute a metric and save the result with the StorageInterface.
     Caches to memory and disk and returns the data.
 * `load`
   - Load a metric (assumed to exist)
     Tries the cache, then the StorageInterface, fails otherwise.
     Returns the data
 * `get`
   - Call save and then load.
     Caches to disk and the `StorageInterface`.
     Returns the cached data.
     Overloaded with `[]` (aka `__getitem__`).

In addition, `ParameterizedDatedCacheManager` adds a powerful decorator
called `collect` that collects metrics automatically.

#### Basic usage:

    CM = DataCacheManager(NpyStorageInterface(SOME_DIRECTORY))

    @CM.collect
    def metric_1():
        stuff = do_something()
        return stuff

    @CM.collect
    def metric_2():
        stuff = do_something_else(CM.metric_1())  # <- use of the cached version here
        other_stuff = convert(stuff)
        return other_stuff

Now calls to `CM.metric_1()` and `CM.metric_2()` seamlessly use the
cache (both in-memory and on disk).

This allows for complex dependencies to be handled automatically
and efficiently.

If you prefer, `metric_1(cache=True)` is equivalent to `CM.metric_1()`.
Both will invoke `CM['metric_1']` which in turn will invoke the
"undecorated" `metric_1()` as it appears above when it does not exist.

Passing `use_stored=False` on any of these will invalidate the
cache and overwrite it with the new value.

The original function (called without `cache=True`) will be unchanged.

Example: `metric_1()` will intentionally _skip_ the cache and just run
like normal.

#### Parameterized usage:
    CM = ParameterizedDataCacheManager(NpyStorageInterface(SOME_DIRECTORY))

    @CM.collect(params_list=[[1], [4]])
    def poly_X(a):
        return do_something_hard(a)

    @CM.collect(params_list=[1, 2], [1, 3], [4, 5])
    def poly_Y(a, b):
        return CM.poly_X(a) ** 2 + do_something_else(b)
    
`CM.poly_Y(1, 2)` will run `poly_Y(1, 2)` which will run `CM.poly_X(1)`
which will run `poly_X(1)`

Then another call to `CM.poly_Y(1, 2)` will load `CM['poly_Y_1_2']` and return it

A call to `poly_Y(1, 3)` will run `poly_Y(1, 3)` which will run `CM.poly_X(1)`
which will load `CM['poly_X_1]`

The point is that if `poly_X` or `poly_Y` take a long time, subsequent calls
will be fast.

Pre-running everything can be done like so:

    CM.poly_X.get_all()
    CM.poly_Y.get_all()

which is handy, for instance, if you need to run a large set of
computations overnight.

The above will fail if you pass undefinied parameters (which is good if
you want to ensure you have pre-cached everything you might invoke).

If you _really_ want to call the functions in the cache manager with any
parameters, just add this option to the code above:

    CM = ParameterizedDataCacheManager(NpyStorageInterface(SOME_DIRECTORY),
                                       dynamic_metric_creation=True)

With this change, things like `CM.poly_Y(12, 13)` will also work.

Finally, to reiterate, the original functions `poly_X` and `poly_Y` will
still work with any parameters regardless of this setting because they
are _unchanged_ unless you specify `cache=True`.

#### Manual usage of DatedCacheManager:

    METRIC_1 = 'metric_1'
    METRIC_2 = 'metric_2'

    CM = DataCacheManager(NpyStorageInterface(SOME_DIRECTORY))

    def metric_1_function():
        stuff = do_something()
        return stuff

    def metric_2_function():
        stuff = do_something_else(CM[METRIC_1])
        other_stuff = convert(stuff)
        return other_stuff

    FUNCTIONS_DICT = {
      METRIC_1: metric_1_function,
      METRIC_2: metric_2_function,
      ...
    }

    CM.set_functions_dict(FUNCTIONS_DICT)

Then in some other place invoke: `CM[METRIC_1]` or `CM[METRIC_2]`

This has the same effect as the "Basic usage" example above but with a
lot more boilerplate. You can still use this if you despise decorator
magic though ;)

