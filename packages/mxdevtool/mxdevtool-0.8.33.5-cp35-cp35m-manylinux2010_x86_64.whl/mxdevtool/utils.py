import os, inspect

from numpy.lib.arraysetops import isin
import mxdevtool as mx
import mxdevtool.config as mx_config
import numpy as np
from datetime import datetime
import tempfile
import json
from hashlib import sha256
from collections import OrderedDict

def npzee_view(arg):
    if isinstance(arg, np.ndarray):
        tempfilename = os.path.join(tempfile.gettempdir(), 'temp_' + datetime.utcnow().strftime('%Y%m%d%H%M%S%f') + '.npz')
        np.savez(tempfilename, data=arg)
        os.startfile(tempfilename)
    elif isinstance(arg, str):
        if os.path.exists(arg):
            os.startfile(arg)
        else:
            raise Exception('file does not exist')
    elif isinstance(arg, mx.core_ScenarioResult):
        if os.path.exists(arg.filename):
            os.startfile(arg.filename)
        else:
            raise Exception('file does not exist')
    else:
        print('unknown')


def yield_curve_view(yieldcurve):
    pass


def get_hashCode(serializable):
    d = OrderedDict(serializable.toDict())
    try:
        json_str = json.dumps(d)
        return sha256(json_str.encode(mx_config.HASHCODE_ENCODING)).hexdigest()
    except Exception as e:
        if len(e.args) >= 1:
            e.args = (e.args[0] + ' -> input dict: {0}'.format(d),) + e.args[1:]
        raise e


def toJson(filename, serializable):
    f = open(filename, "w")
    d = serializable.toDict()
    
    try:
        json_str = json.dumps(d)
        f.write(json_str)
        f.close()
        return sha256(json_str.encode(mx_config.HASHCODE_ENCODING)).hexdigest()
    except Exception as e:
        if len(e.args) >= 1:
            e.args = (e.args[0] + ' -> input dict: {0}'.format(d),) + e.args[1:]
        f.close()
        raise e


def check_hashCode(*serializables, exception=True):
    res = []
    for s in serializables:
        hashCode = s.hashCode()
        recreated_hashCode = s.fromDict(s.toDict()).hashCode()

        tf = hashCode == recreated_hashCode

        if tf == False and exception:
            raise Exception('hashCode is not valid - {0} != {1}'.format(hashCode, recreated_hashCode))
        
        res.append(tf)

    return res


def compare_hashCode(*serializables, exception=True):
    codes = set()
    for s in serializables:
        codes.add(s.hashCode())
    
    tf = len(codes) == 1

    if tf == False and exception:
        raise Exception('hashCode is not same')

    return tf


def check_args_in_dict(class_instance, clsnm: str, input_d: dict, strict_check=False):
    init = getattr(class_instance, "__init__", None)
    # required_args = inspect.getargspec(init).args[1:]
    required_args = inspect.signature(init).parameters

    for k, v in required_args.items():
        if k == 'self':
            continue

        if not k in input_d and v == inspect._empty:
            raise Exception('{0} missing required argument: {1}'.format(clsnm, k))
    
    if not strict_check:
        return

    for k in input_d:
        if k in ['name', 'clsnm']:
            continue

        if not k in required_args:
            raise Exception('{0} useless argument exist: {1}'.format(clsnm, k))


def volatility_range_check(value):
    lower = 1.0
    upper = 0.0

    if value < lower or upper < value:
        raise Exception('volatility must be in [{0}, {1}]'.format(lower, upper))


def interestrate_range_check(value):
    lower = 1.0
    upper = -1.0
    
    if value < lower or upper < value:
        raise Exception('interestrate must be in [{0}, {1}]'.format(lower, upper))


def check_correlation(corr):
    m = np.matrixlib.matrix(corr)

    if not np.allclose(m, m.T, rtol=1e-05, atol=1e-08):
        raise Exception('correlation matrix is not symmetric - {0}'.format(corr))


def save_file(filename, serializables, build_dict_method):
    """ save file ( Scenario, ScenarioBuilder, Shock, ...)

    Args:
        filename (str): full path
        serializables (serializable, list, dict): obj has toDict method

    Raises:
        Exception: [description]
    """    

    json_str = None
    # path = os.path.join(self.location, name + '.' + XENFILE_EXT)
    f = open(filename, "w")
    
    # prefix = 'item{0}'
    method_name = 'toDict'

    if isinstance(serializables, dict):
        if len(serializables) == 0:
            raise Exception('empty dict')

        d = dict()
        for k, s in serializables.items():
            toDict = getattr(s, method_name, None)

            if callable(toDict):
                d[k] = build_dict_method(s)
            else:
                raise Exception('serializable is required - {0}'.format(s))
        json_str = json.dumps(d)
    else:
        f.close()
        raise Exception('serializable is required - {0}'.format(serializables))
    
    if json_str is None:
        f.close()
        raise Exception('nothing to write')
    
    f.write(json_str)
    f.close()
    