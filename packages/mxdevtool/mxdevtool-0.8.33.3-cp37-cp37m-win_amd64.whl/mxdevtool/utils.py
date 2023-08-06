import os, inspect
import mxdevtool as mx
import mxdevtool.config as mx_config
import numpy as np
from datetime import datetime
import tempfile
import json
from hashlib import sha256


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
    d = serializable.toDict()
    try:
        json_str = json.dumps(d)
        return sha256(json_str.encode(mx_config.HASHCODE_ENCODING)).hexdigest()
    except Exception as e:
        if len(e.args) >= 1:
            e.args = (e.args[0] + ' -> input dict: {0}'.format(d),) + e.args[1:]
        raise e


def toJson(filename, serializable):
    f = open(filename, "w")
    try:
        d = serializable.toDict()
        json_str = json.dumps(d)
        f.write(json_str)
        f.close()
        return sha256(json_str.encode(mx_config.HASHCODE_ENCODING)).hexdigest()
    except Exception as e:
        if len(e.args) >= 1:
            e.args = (e.args[0] + ' -> input dict: {0}'.format(d),) + e.args[1:]
        f.close()
        raise e

def check_hashCode(*serializables):
    for s in serializables:
        assert s.hashCode() == s.fromDict(s.toDict()).hashCode()


def compare_hashCode(*serializables):
    codes = set()
    for s in serializables:
        codes.add(s.hashCode())
    
    assert len(codes) == 1


def check_args_in_dict(class_instance, clsnm: str, input_d: dict, strict_check=False):
    init = getattr(class_instance, "__init__", None)
    required_args = inspect.getargspec(init).args[1:]

    for k in required_args:
        if not k in input_d:
            raise Exception('{0} missing required argument: {1}'.format(clsnm, k))
    
    if not strict_check:
        return

    for k in input_d:
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
    