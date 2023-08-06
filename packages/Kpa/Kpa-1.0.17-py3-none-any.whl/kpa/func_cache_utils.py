
import shelve, json, os.path


def _jsonify(obj):
    return json.dumps(obj, default=_jsonify_default)
def _jsonify_default(obj):
    try:
        import pandas as pd
    except ImportError:
        pass
    else:
        if isinstance(obj, pd.DataFrame):
            return {'type=pandas.DataFrame': obj.to_json()}
    raise TypeError('Object of type {obj.__class__.__name__} is not JSON serializable!'.format(**locals()))


def shelve_cache(func):
    def new_f(*args, **kwargs):
        key = _jsonify([args, kwargs])
        filename = '.cache-{func.__name__}.shelve'.format(**locals())
        # with shelve.open(filename) as shelf:
        #     if key not in shelf: shelf[key] = func(*args, **kwargs)
        #     return shelf[key]
        with shelve.open(filename) as shelf:
            if key in shelf: return shelf[key]
        # release the file to allow other processes to use it
        # this function is meant for slow functions, so this extra closing and opening isn't significant
        ret = func(*args, **kwargs)
        with shelve.open(filename) as shelf: shelf[key] = ret
        return ret
    return new_f


def cached_generator(record_maker=lambda x:x):
    '''
    caches a generator into jsonlines format.
    calls record_maker on each un-serialized line before yielding it.
    doesn't track args, so don't use any.
    '''
    def decorator(func):
        cache_fpath = os.path.join('.cache-{func.__name__}.jsonlines'.format(**locals()))
        def newf(*args, **kwargs):
            if args or kwargs: raise Exception('cached_generator() cannot handle args or kwargs')
            if not os.path.exists(cache_fpath):
                with open(cache_fpath+'.tmp', 'wt') as f:
                    for r in func():
                        f.write(json.dumps(r) + '\n')
                        yield r
                os.rename(cache_fpath+'.tmp', cache_fpath)
            else:
                with open(cache_fpath, 'rt') as f:
                    for line in f:
                        yield record_maker(json.loads(line))
        return newf
    return decorator
