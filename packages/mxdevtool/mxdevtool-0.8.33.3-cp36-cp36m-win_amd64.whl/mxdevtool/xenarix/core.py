import os, json, numbers
import mxdevtool as mx
import mxdevtool.utils as utils
import numpy as np
#import mxdevtool.termstructures as ts
from mxdevtool.termstructures import *
from mxdevtool.xenarix.pathcalc import *
from mxdevtool import TimeGrid, TimeEqualGrid, TimeArrayGrid

XENFILE_EXT = 'xen'
HASHCODES_KEY = 'hashcodes'


class NameHelper:

    @staticmethod
    def isCompounding(name):
        return 'compounding' == name or 'Compounding' == name[-len('Compounding'):]

    @staticmethod
    def isCalendar(name):
        return 'calendar' == name or 'Calendar' == name[-len('Calendar'):]

    @staticmethod
    def isDayCounter(name):
        return 'dayCounter' == name or 'DayCounter' == name[-len('DayCounter'):]

    @staticmethod
    def isBusinessDayConvention(name):
        return 'businessDayConvention' == name or 'BusinessDayConvention' == name[-len('BusinessDayConvention'):]

    @staticmethod
    def isInterpolationType(name):
        return 'interpolationType' == name or 'InterpolationType' == name[-len('InterpolationType'):]

    @staticmethod
    def isExtrapolationType(name):
        return 'extrapolationType' == name or 'ExtrapolationType' == name[-len('ExtrapolationType'):]

    @staticmethod
    def isTenor(name):
        return 'tenor' == name or 'Tenor' == name[-len('Tenor'):]

    @staticmethod
    def isDate(name):
        return 'date' == name or 'Date' == name[-len('Date'):]

    @staticmethod
    def getTypeFrom(name):
        res = None

        if NameHelper.isCompounding(name):
            res = 'compounding'
        elif NameHelper.isCalendar(name):
            res = 'calendar'
        elif NameHelper.isDayCounter(name):
            res = 'dayCounter'
        elif NameHelper.isBusinessDayConvention(name):
            res = 'businessDayConvention'
        elif NameHelper.isInterpolationType(name):
            res = 'interpolationType'
        elif NameHelper.isExtrapolationType(name):
            res = 'extrapolationType'
        elif NameHelper.isTenor(name):
            res = 'tenor'
        elif NameHelper.isDate(name):
            res = 'date'
        
        return res

    @staticmethod
    def toDictArg(name, value):
        res = None

        if NameHelper.isCompounding(name):
            res = mx.compoundingToString(value)
        elif NameHelper.isCalendar(name):
            res = str(value)
        elif NameHelper.isDayCounter(name):
            res = str(value)
        elif NameHelper.isBusinessDayConvention(name):
            res = mx.businessDayConventionToString(value)
        elif NameHelper.isInterpolationType(name):
            res = mx.interpolator1DToString(value)
        elif NameHelper.isExtrapolationType(name):
            res = mx.extrapolator1DToString(value)
        elif NameHelper.isTenor(name):
            res = str(value)
        elif NameHelper.isDate(name):
            res = str(value)
        elif isinstance(value, (numbers.Number, str, list)):
            res = value

        return res

    @staticmethod
    def toClassArg(name, value):
        arg = None

        if NameHelper.isDate(name):
            arg = mx.Date(value)
        elif NameHelper.isCompounding(name):
            arg = mx.compoundingParse(value) if isinstance(value, str) else value
        elif NameHelper.isCalendar(name):
            arg = mx.calendarParse(value)
        elif NameHelper.isDayCounter(name):
            arg = mx.dayCounterParse(value)
        elif NameHelper.isBusinessDayConvention(name):
            arg = mx.businessDayConventionParse(value) if isinstance(value, str) else value
        elif NameHelper.isInterpolationType(name):
            arg = mx.interpolator1DParse(value) if isinstance(value, str) else value
        elif NameHelper.isExtrapolationType(name):
            arg = mx.extrapolator1DParse(value) if isinstance(value, str) else value
        elif NameHelper.isTenor(name):
            arg = mx.Period(value)
        elif isinstance(value, (numbers.Number, str, list)):
            arg = value
        else:
            raise Exception('unsupported argument name : {0}'.format(value))

        return arg

        
def check_args_in_dict(clsnm: str, input_d: dict, strict_check=False):
    class_instance = globals()[clsnm]
    utils.check_args_in_dict(class_instance, clsnm, input_d, strict_check)


# arguments parse from arg name
def get_arg_fromValue(name: str, arg_v, mrk: mx.MarketData, models_calcs):
    arg = None

    # class type case
    if not isinstance(arg_v, (numbers.Number, str, dict)):
        return arg_v

    if 'Curve' == name[-len('Curve'):]:
        curve_d = mrk.get_yieldCurve_d(arg_v)
        curveType = curve_d[mx.CLASS_TYPE_NAME]

        class_instance = globals()[curveType]
        arg = class_instance.fromDict(curve_d, mrk)

    elif 'volTs' == name or 'VolTs' == name[-len('VolTs'):]:
        volTs_d = mrk.get_volTs_d(arg_v)
        volType = volTs_d[mx.CLASS_TYPE_NAME]

        class_instance = globals()[volType]
        arg = class_instance.fromDict(volTs_d, mrk)

    elif 'Para' == name[-len('Para'):]:
        arg = DeterministicParameter.fromDict(arg_v)

    elif NameHelper.getTypeFrom(name) != None:
        arg = NameHelper.toClassArg(name, arg_v)

    elif name in ['ir_pc', 'pc', 'pc1', 'pc2'] and isinstance(arg_v, str):
        if not arg_v in models_calcs:
            raise Exception('model or calc does not exist - {0}, {1}'.format(arg_v, models_calcs.keys()))
        arg = models_calcs[arg_v]

    elif name == 'pc_list':
        for pc in arg_v:
            if not arg_v in models_calcs:
                raise Exception('model or calc does not exist - {0}'.format(arg_v, models_calcs.keys()))
        arg = [models_calcs[pc] for pc in arg_v]

    elif name == 'name' or 'type' == name[-len('type'):]:
        arg = arg_v

    elif isinstance(arg_v, numbers.Number):
        arg = arg_v

    else:
        quote_d = mrk.get_quote_d(arg_v)
        arg = quote_d['v']

    if arg is None:
        raise Exception('unsupported argument name : {0}'.format(arg_v))

    return arg


def get_args_fromDict(d: dict, mrk: mx.MarketData, models_calcs, arg_names):
    args = []
    for name in arg_names:
        arg_v = d[name]
        # curve
        args.append(get_arg_fromValue(name, d[name], mrk, models_calcs))

    return args


# model parse
def parseClassFromDict(d: dict, models_calcs=[], mrk=mx.MarketData()):
    if not isinstance(d, dict):
        raise Exception('dictionary type is required')
    
    classTypeName = d[mx.CLASS_TYPE_NAME]

    if not classTypeName in globals():
        raise Exception('unknown classTypeName - {0}'.format(classTypeName))

    try:
        class_instance = globals()[classTypeName]
        init = getattr(class_instance, "__init__", None)
        args = get_args_fromDict(d, mrk, models_calcs, inspect.getargspec(init).args[1:])
        return class_instance(*args)
    except Exception as e:
        if len(e.args) >= 1:
            e.args = (e.args[0] + '\ninput dict: {0}'.format(d),) + e.args[1:]
        raise


class Rsg(mx.core_Rsg):
    def __init__(self, sampleNum, dimension=365, seed=0, skip=0, isMomentMatching=False, randomType='pseudo', subType='mersennetwister', randomTransformType='boxmullernormal'):
        
        self._randomType = randomType
        self._subType = subType
        self._randomTransformType = randomTransformType

        mx.core_Rsg.__init__(self, sampleNum, dimension, seed, skip, isMomentMatching, randomType, subType, randomTransformType)

    @staticmethod
    def fromDict(d: dict, mrk=mx.MarketData()):
        mx.check_fromDict(d, mx.CLASS_TYPE_NAME, Rsg.__name__)

        sampleNum = d['sampleNum']
        dimension = d['dimension']
        seed = d['seed']
        skip = d['skip']
        isMomentMatching = d['isMomentMatching']
        randomType = d['randomType']
        subType = d['subType']
        randomTransformType = d['randomTransformType']

        return Rsg(sampleNum, dimension, seed, skip, isMomentMatching, randomType, subType, randomTransformType)

    def toDict(self):
        res = dict()

        res[mx.CLASS_TYPE_NAME] = self.__class__.__name__

        res['sampleNum'] = self.sampleNum
        res['dimension'] = self.dimension
        res['seed'] = self.seed
        res['skip'] = self.skip
        res['isMomentMatching'] = self.isMomentMatching
        res['randomType'] = self.randomType
        res['subType'] = self.subType
        res['randomTransformType'] = self.randomTransformType

        return res

    randomType = property(lambda self: self._randomType,None,None)
    subType = property(lambda self: self._subType,None,None)
    randomTransformType = property(lambda self: self._randomTransformType,None,None)




class ScenarioBuilder:
    def __init__(self, json_dict: dict = None):
        if json_dict is None:
            self.reset()
        else:
            self.check_json_dict(json_dict)
            self.__dict__ = json_dict

    @staticmethod
    def fromDict(d: dict):
        return ScenarioBuilder(d)

    def toDict(self):
        import copy
        return copy.deepcopy(self.__dict__)

    def hashCode(self):
        return utils.get_hashCode(self)

    def check_json_dict(self, d: dict):
        keys = ['models', 'calcs', 'timegrid', 'corr', 'rsg', 'filename', 'isMomentMatching']

        for k in keys:
            if not k in d:
                raise Exception("invalid json for scenario building. '{0}' is required\n{1}".format(k, d))

    def build_scenario(self, mrk: mx.MarketData()):
        if mrk is None:
            mrk = mx.MarketData()

        # models
        models_calcs = dict()

        models = []
        for m in self.models:
            model = parseClassFromDict(m, models_calcs, mrk)
            models_calcs[model.name] = model
            models.append(model)
        
        calcs = []
        for c in self.calcs:
            calc = parseClassFromDict(c, models_calcs, mrk)
            models_calcs[calc.name] = calc
            calcs.append(calc)
        
        corr = mx.Matrix(self.corr)

        if len(models) != corr.rows() or len(models) != corr.columns():
            raise Exception("correlation matrix's rows({0}) and columns({1}) size must be same to model size({2})".format(corr.rows(), corr.columns(), len(models)))

        timegrid = parseClassFromDict(self.timegrid)
        rsg = Rsg.fromDict(self.rsg, mrk)

        return Scenario(models, calcs, corr, timegrid, rsg, self.filename, self.isMomentMatching)

    def reset(self):
        d = dict()

        d['models'] = []
        d['calcs'] = []
        d['corr'] = mx.IdentityMatrix(1).toList()
        d['timegrid'] = mx.TimeEqualGrid().toDict()
        d['rsg'] = Rsg(sampleNum=1000).toDict()
        d['filename'] = 'temp.npz'
        d['isMomentMatching'] = False

        self.__dict__ = d

    def _toDictArgs(self, d: dict):
        res = dict()

        for k, v in d.items():
            toDict = getattr(v, "toDict", None)

            if toDict is None:
                res[k] = NameHelper.toDictArg(k, v)
            else:
                res[k] = v.toDict()

        return res

    def getModel(self, name):
        for m in self.models:
            if m.name == name:
                return m

    def addModel(self, clsnm: str, name: str, **kwargs):
        d = dict()

        d['name'] = name
        d[mx.CLASS_TYPE_NAME] = clsnm
        d = { **d, **self._toDictArgs(kwargs)}
        check_args_in_dict(clsnm, d)
        
        self.models.append(d)

        self.resetCorrelation()

    def removeModel(self, name: str):
        self.models.remove(self.getModel(name))
        self.resetCorrelation()
    
    def getCalc(self, name):
        for c in self.calcs:
            if c['name'] == name:
                return c

    def addCalc(self, clsnm: str, name: str, **kwargs):
        d = dict()
        d['name'] = name
        d[mx.CLASS_TYPE_NAME] = clsnm
        d = { **d, **self._toDictArgs(kwargs)}
        check_args_in_dict(clsnm, d)
        
        self.calcs.append(d)

    def removeCalc(self, name: str):
        self.calcs.remove(self.getCalc(name))

    def setTimeGrid(self, tg):
        pass

    def resetCorrelation(self):
        self.corr = mx.IdentityMatrix(len(self.models)).toList()
    

# class Scenario(mx.core_ScenarioGenerator2):
class Scenario:
    def __init__(self, models, calcs, corr, timegrid, rsg, filename, isMomentMatching = False):
        _corr = mx.Matrix(corr)

        # _dimension = (len(timegrid) - 1) * len(models)
        # _rsg = Rsg(rsg.sampleNum, _dimension, rsg.seed, rsg.skip, rsg.isMomentMatching, rsg.randomType, rsg.subType, rsg.randomTransformType)

        self.models = models
        self.calcs = calcs
        self.corr = _corr
        self.timegrid = timegrid
        self.rsg = rsg
        self.filename = filename
        self.isMomentMatching = isMomentMatching

    @staticmethod
    def fromDict(d: dict, mrk: mx.MarketData = None):
        if not isinstance(d, dict):
            raise Exception('dictionary type is required')

        sjb = ScenarioBuilder(d)

        if mrk == None:
            mrk = mx.MarketData()
        
        return sjb.build_scenario(mrk)
        # args = sjb.build_scenario(mrk)
        # return Scenario(*args)

    def toDict(self):
        res = dict()
        
        res['models'] = [ m.toDict() for m in self.models]
        res['calcs'] = [ c.toDict() for c in self.calcs]
        res['corr'] = self.corr.toList()
        res['timegrid'] = self.timegrid.toDict()
        res['rsg'] = self.rsg.toDict()
        res['filename'] = self.filename
        res['isMomentMatching'] = self.isMomentMatching

        return res

    def hashCode(self):
        return utils.get_hashCode(self)
    
    def clone(self, **kwargs):
        try:
            _dimension = (len(self.timegrid) - 1) * len(self.models)
            _rsg = Rsg(self.rsg.sampleNum, _dimension, self.rsg.seed, self.rsg.skip, self.rsg.isMomentMatching, 
                       self.rsg.randomType, self.rsg.subType, self.rsg.randomTransformType)

            models = kwargs['models'] if 'models' in kwargs else self.models
            calcs = kwargs['calcs'] if 'calcs' in kwargs else self.calcs
            corr = kwargs['corr'] if 'corr' in kwargs else self.corr
            timegrid = kwargs['timegrid'] if 'timegrid' in kwargs else self.timegrid
            rsg = kwargs['rsg'] if 'rsg' in kwargs else _rsg
            filename = kwargs['filename'] if 'filename' in kwargs else self.filename
            isMomentMatching = kwargs['isMomentMatching'] if 'isMomentMatching' in kwargs else self.isMomentMatching

            if not filename[-4:] == '.npz':
                filename += '.npz'

            scen = Scenario(models, calcs, corr, timegrid, rsg, filename, isMomentMatching)

            return scen

        except Exception as e:
            if len(e.args) >= 1:
                e.args = (e.args[0] + '\nscenario inputs: {0}'.format((self.models, self.calcs, self.corr, self.timegrid, 
                        self.rsg, self.filename, self.isMomentMatching)),) + e.args[1:]
            raise

    def generate(self, **kwargs):
        scen = self.clone(**kwargs)

        core = mx.core_ScenarioGenerator2(scen.models, scen.calcs, scen.corr, scen.timegrid, scen.rsg, scen.filename, scen.isMomentMatching)
        core.generate()

        return ScenarioResults(scen.filename)
    

class ScenarioResults(mx.core_ScenarioResult):
    def __init__(self, filename):
        mx.core_ScenarioResult.__init__(self, filename)
        self.shape = (self.simulNum, self.assetNum, self.timegridNum) 

    def toNumpyArr(self):
        npz = np.load(self.filename)
        arr = npz['data']
        arr.reshape(self.shape)

        return arr

    def __getitem__(self, scenCount):
        return self._multiPath(scenCount)

    def tPosSlice(self, t_pos, scenCount=None):
        if scenCount is None:
            return self._multiPathAllTPos(t_pos)
        else:
            return self._multiPathTPos(scenCount, t_pos)

    def timeSlice(self, time, scenCount=None):
        if scenCount is None:
            return self._multiPathAllTPosInterpolateTime(time)
        else:
            return self._multiPathTPosInterpolateTime(scenCount, time)

    def dateSlice(self, date, scenCount=None):
        if scenCount is None:
            return self._multiPathAllTPosInterpolateDate(date)
        else:
            return self._multiPathTPosInterpolateDate(scenCount, date)

    def show(self):
        import mxdevtool.utils as mx_u
        mx_u.npzee_view(self)


class XenarixFileManager(mx.ManagerBase):
    def __init__(self, config):
        mx.ManagerBase.__init__(self, config)

        self.location = config['location']

        if not os.path.exists(self.location):
            raise Exception('directory does not exist - {0}'.format(self.location) )

    def _build_dict(self, scen):
        scen_d = scen.toDict()
        hashcodes_d = dict()
        
        hashcodes_d['base'] = scen.hashCode()

        scen_d[HASHCODES_KEY] = hashcodes_d

        return scen_d

    def save(self, name, **kwargs):
        json_str = None
        path = os.path.join(self.location, name + '.' + XENFILE_EXT)
        
        utils.save_file(path, kwargs, self._build_dict)

    def load(self, name):
        path = os.path.join(self.location, name + '.' + XENFILE_EXT)
        f = open(path, "r")
        json_str = f.read()
        scen_d = json.loads(json_str)

        res = dict()
        
        for k, v in scen_d.items():
            sb = ScenarioBuilder(v)
            # inputs = sb.build_scenario(mrk=None)
            # res[k] = Scenario(*inputs)
            res[k] = sb.build_scenario(mrk=None)

        return res

    def scenList(self):
        included_extensions = [ XENFILE_EXT ]
        file_names = [os.path.splitext(fn)[0] for fn in os.listdir(self.location)
            if any(fn.endswith(ext) for ext in included_extensions)]
        
        return file_names


def generate1d(model, calcs, timegrid, rsg, filename, isMomentMatching = False):
    _calcs = calcs

    if calcs is None:
        _calcs = []

    corr = mx.IdentityMatrix(1)

    scen = Scenario([model], _calcs, corr, timegrid, rsg, filename, isMomentMatching)
    scen.generate()

    return ScenarioResults(filename)


def generate(models, calcs, corr, timegrid, rsg, filename, isMomentMatching = False):
    if calcs is None:
        calcs = []

    scen = Scenario(models, calcs, corr, timegrid, rsg, filename, isMomentMatching)
    scen.generate()

    return ScenarioResults(filename)

