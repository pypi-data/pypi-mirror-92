import os
import mxdevtool as mx
import mxdevtool.xenarix as xen
import mxdevtool.utils as utils
import json, inspect
from fnmatch import fnmatch

from mxdevtool.shock.traits import *

SHOCKFILE_EXT = 'shk'
SHOCKTRAITFILE_EXT = 'sht'
SHOCKMODELFILE_EXT = 'shm'

class Shock:
    def __init__(self, name):
        self.name = name
        self.shocktrait_d_list = []

    def __getitem__(self, shocktrait_name):
        for st_d in self.shocktrait_d_list:
            if st_d['name'] == shocktrait_name:
                return st_d['shocktrait']

        raise KeyError(shocktrait_name)

    @staticmethod
    def fromDict(d: dict):
        mx.check_fromDict(d, mx.CLASS_TYPE_NAME, Shock.__name__)
        
        shock = Shock(d['name'])
        shocktrait_d_list = d['shocktrait_d_list']

        for st_d in shocktrait_d_list:
            shock.addShockTrait(target=st_d['target'], shocktrait=parseClassFromDict(st_d['shocktrait']))

        return shock

    def toDict(self):
        d = dict()

        d[mx.CLASS_TYPE_NAME] = Shock.__name__
        d['name'] = self.name
        d['shocktrait_d_list'] = self.shocktrait_d_list

        return d

    def hashCode(self):
        return utils.get_hashCode(self)

    def shockTraitList(self):
        return self.shocktrait_d_list

    def clone(self, name=None):
        d = copy.deepcopy(self.toDict())

        if name is None:
            d['name'] += '_clone'
        else:
            d['name'] = name

        return Shock.fromDict(d)

    def addShockTrait(self, target: str, shocktrait: ShockTrait):
        d = dict()
        
        d['target'] = target
        d['shocktrait'] = shocktrait.toDict()

        # for st_d in self.shocktrait_d_list:
        #     if st_d['shocktrait']['name'] == shocktrait.name:
        #         raise Exception('shocktrait name exist - {0}'.format(shocktrait.name))

        self.shocktrait_d_list.append(d)

    def removeShockTrait(self, target=None, shocktrait=None):
        shocktrait_d_newlist = []

        for st_d in self.shocktrait_d_list:
            shocktrait_name = st_d['shocktrait']['name']
            _name = shocktrait_name if shocktrait is None else shocktrait.name
            _target = st_d['target'] if target is None else target

            if st_d['target'] != _target or shocktrait_name != _name:
                shocktrait_d_newlist.append(st_d)
            
        self.shocktrait_d_list = shocktrait_d_newlist

    def removeShockTraitAt(self, i):
        del self.shocktrait_d_list[i]


class ShockScenarioModel:
    def __init__(self, name, *shock_list):
        self.name = name

        if isinstance(shock_list[0], list):
            self.shock_list = shock_list[0]
        else:
            self.shock_list = list(shock_list)

        self.greeks_d = dict()

    def toDict(self):
        d = dict()

        d[mx.CLASS_TYPE_NAME] = ShockScenarioModel.__name__
        d['name'] = self.name
        d['shock_list'] = [ shock.toDict() for shock in self.shock_list ]
        d['greeks_d'] = self.greeks_d

        return d

    @staticmethod
    def fromDict(d: dict):
        mx.check_fromDict(d, mx.CLASS_TYPE_NAME, ShockScenarioModel.__name__)

        shock_list = [ Shock.fromDict(shock_d) for shock_d in d['shock_list'] ]
        sm = ShockScenarioModel(d['name'], *shock_list)
        sm.greeks_d = d['greeks_d']

        return sm

    def hashCode(self):
        return utils.get_hashCode(self)

    def addGreeks(self, greek_name: str, **kwargs):
        d = dict()

        shock_names = [ shock.name for shock in self.shock_list ]

        for k, v in kwargs.items():
            shock_name = None

            if isinstance(v, Shock):
                shock_name = v.name
            elif isinstance(v, str):
                shock_name = v
            else:
                raise Exception('shock or str type is required - {0}, {1}'.format(k ,v))
            
            # if not any(shock.name for shock in self.shock_list if shock_name == shock.name):
            if not shock_name in shock_names:
                raise Exception('no exist shock - {0}, {1}, {2}'.format(k ,v, shock_names))

        self.greeks_d[greek_name] = d
    
    def removeGreeks(self, greek_name):
        self.greeks_d.pop(greek_name)


## shock manager
class ShockFileManager(mx.ManagerBase):
    def __init__(self, config):
        mx.ManagerBase.__init__(self, config)

        self.location = config['location']

        if not os.path.exists(self.location):
            raise Exception('directory does not exist - {0}'.format(self.location))
    
    def _build_dict(self, serializable):
        return serializable.toDict()

    def _save(self, name, ext, *args):
        json_str = None
        path = os.path.join(self.location, name + '.' + ext)

        d = dict()
        for arg in args:
            d[arg.name] = arg

        utils.save_file(path, d, self._build_dict)

    def _load(self, name, ext):
        path = os.path.join(self.location, name + '.' + ext)

        f = open(path, "r")
        json_str = f.read()
        shock_d = json.loads(json_str)

        res = dict()
        
        for k, v in shock_d.items():
            if ext == SHOCKTRAITFILE_EXT:
                res[k] = parseClassFromDict(v)
            elif ext == SHOCKFILE_EXT:
                res[k] = Shock.fromDict(v)
            elif ext == SHOCKMODELFILE_EXT:
                res[k] = ShockScenarioModel.fromDict(v)
            else:
                raise Exception('unknown shock file - {0}'.format(path))

        return res

    def save_sht(self, name, *args):
        self._save(name, SHOCKTRAITFILE_EXT, *args)

    def load_sht(self, name):
        return self._load(name, SHOCKTRAITFILE_EXT)

    def save_shk(self, name, *args):
        self._save(name, SHOCKFILE_EXT, *args)

    def load_shk(self, name):
        return self._load(name, SHOCKFILE_EXT)

    def save_shm(self, name, *args):
        self._save(name, SHOCKMODELFILE_EXT, *args)

    def load_shm(self, name):
        return self._load(name, SHOCKMODELFILE_EXT)


def build_shockedMrk(shock: Shock, mrk: mx.MarketData):
    mrk_clone = mrk.clone()
    
    target = None

    try:
        for st_d in shock.shocktrait_d_list:
            target = st_d['target']
            shocktrait = parseClassFromDict(st_d['shocktrait'])

            d = {}
            d_clone = {}

            if isinstance(shocktrait, QuoteShockTrait):
                d = mrk.quote
                d_clone = mrk_clone.quote
            elif isinstance(shocktrait, YieldCurveShockTrait):
                d = mrk.yieldCurve
                d_clone = mrk_clone.yieldCurve
            elif isinstance(shocktrait, VolTsShockTrait):
                d = mrk.volTs
                d_clone = mrk_clone.volTs

            for k, v in d.items():
                if fnmatch(k, target):
                    shocktrait.calculate(d_clone[k]) 

    except Exception as e:
        if len(e.args) >= 1:
            e.args = (e.args[0] + ' - {0}, {1}'.format(shock.name, target),) + e.args[1:]
        raise

    return mrk_clone


def build_shockedScen(shock_list: list, sb: xen.ScenarioBuilder, mrk: mx.MarketData):
    res = []

    for shock in shock_list:
        shocked_mrk = build_shockedMrk(shock, mrk)
        shocked_scen = sb.build_scenario(shocked_mrk)
        res.append(shocked_scen)

    return res
        
