import functools
import time

from django.db import connection, reset_queries


def query_debugger(func):

    @functools.wraps(func)
    def inner_func(*args, **kwargs):

        # to clear any previously executed queries:
        reset_queries()
        # the number of queries executed so far:
        start_queries = len(connection.queries)

        start = time.perf_counter()
        result = func(*args, **kwargs)
        end = time.perf_counter()
        end_queries = len(connection.queries)

        print(f'Function: {func.func.__name__}')
        print(f'Number of queries: {end_queries - start_queries}')
        # formats the elapsed time as a floating-point number with 3
        # decimal places - like 'Finished in: 0.23s':
        print(f'Finished in: {(end-start):.3f}s')
        return result

    return inner_func