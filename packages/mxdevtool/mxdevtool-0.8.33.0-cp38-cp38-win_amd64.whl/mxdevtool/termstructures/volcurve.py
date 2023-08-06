import mxdevtool as mx


class BlackConstantVol(mx.core_BlackConstantVol):
    def __init__(self, refDate, vol, calendar=None, dayCounter=mx.Actual365Fixed()):
        if isinstance(refDate, mx.Date):
            _refDate = refDate
        else:
            _refDate = mx.Date(refDate)

        _calendar = calendar

        if _calendar is None:
            _calendar = mx.default_calendar()
        
        self._refDate = refDate
        self._vol = vol
        self._calendar = _calendar # prevent None 
        self._dayCounter = dayCounter

        mx.core_BlackConstantVol.__init__(self, _refDate, vol, _calendar, dayCounter)

    @staticmethod
    def fromDict(d: dict, mrk=mx.MarketData()):
        mx.check_fromDict(d, mx.CLASS_TYPE_NAME, BlackConstantVol.__name__)

        refDate = mx.Date(d['refDate'])
        vol = d['vol']
        calendar = mx.calendarParse(d['calendar'])
        dayCounter = mx.dayCounterParse(d['dayCounter'])

        return BlackConstantVol(refDate, vol, calendar, dayCounter)

    def toDict(self):
        res = dict()

        res[mx.CLASS_TYPE_NAME] = self.__class__.__name__
        res['refDate'] = str(self._refDate)
        res['vol'] = self._vol
        res['calendar'] = str(self._calendar)
        res['dayCounter'] = str(self._dayCounter)

        return res


class BlackVarianceCurve(mx.core_BlackVarianceCurve):
    def __init__(self, refDate, periods, volatilities, 
                   interpolationType=mx.Interpolator1D.Linear, 
                   calendar=None,
                   dayCounter=mx.Actual365Fixed(), 
                   businessDayConvention=mx.ModifiedFollowing):
        if isinstance(refDate, mx.Date):
            _refDate = refDate
        else:
            _refDate = mx.Date(refDate)

        _periods = periods
        _calendar = calendar

        if _calendar is None:
            _calendar = mx.default_calendar()

        self._refDate = refDate
        self._periods = periods
        self._volatilities = volatilities
        self._interpolationType = interpolationType
        self._calendar = _calendar # prevent None 
        self._dayCounter = dayCounter
        self._businessDayConvention = businessDayConvention

        mx.core_BlackVarianceCurve.__init__(self, _refDate, _periods, volatilities, interpolationType,
                                    _calendar, dayCounter, businessDayConvention)

    @staticmethod
    def fromDict(d: dict, mrk=mx.MarketData()):
        mx.check_fromDict(d, mx.CLASS_TYPE_NAME, BlackVarianceCurve.__name__)

        refDate = mx.Date(d['refDate'])
        periods = d['vol']
        volatilities = d['volatilities']
        interpolationType = mx.interpolator1DParse(d['interpolationType'])
        calendar = mx.calendarParse(d['calendar'])
        dayCounter = mx.dayCounterParse(d['dayCounter'])
        businessDayConvention = mx.businessDayConventionParse(d['businessDayConvention'])

        return BlackVarianceCurve(refDate, vol, calendar, dayCounter)

    def toDict(self):
        res = dict()

        res[mx.CLASS_TYPE_NAME] = self.__class__.__name__
        res['refDate'] = str(self._refDate)
        res['periods'] = str(self._periods)
        res['volatilities'] = self._volatilities
        res['interpolationType'] = mx.interpolator1DToString(self._interpolationType)
        res['calendar'] = str(self._calendar)
        res['dayCounter'] = str(self._dayCounter)
        res['businessDayConvention'] = mx.businessDayConventionToString(self._businessDayConvention)

        return res


class BlackVarianceSurface(mx.core_BlackVarianceSurface):
    def __init__(self, refDate, periods, strikes, blackVols,
                   calendar=None,
                   dayCounter=mx.Actual365Fixed(), 
                   businessDayConvention=mx.ModifiedFollowing):
        if isinstance(refDate, mx.Date):
            _refDate = refDate
        else:
            _refDate = mx.Date(refDate)

        _periods = periods
        _calendar = calendar

        if _calendar is None:
            _calendar = mx.default_calendar()

        _blackVols = mx.Matrix(blackVols)

        self._refDate = refDate
        self._periods = periods
        self._strikes = strikes
        self._blackVols = blackVols
        self._calendar = _calendar # prevent None 
        self._dayCounter = dayCounter
        self._businessDayConvention = businessDayConvention

        mx.core_BlackVarianceSurface.__init__(self, _refDate, _periods, strikes, blackVols,
                                    _calendar, dayCounter, businessDayConvention)

    @staticmethod
    def fromDict(d: dict, mrk=mx.MarketData()):
        mx.check_fromDict(d, mx.CLASS_TYPE_NAME, BlackVarianceCurve.__name__)

        refDate = mx.Date(d['refDate'])
        periods = d['periods']
        strikes = d['strikes']
        blackVols = d['blackVols']
        calendar = mx.calendarParse(d['calendar'])
        dayCounter = mx.dayCounterParse(d['dayCounter'])
        businessDayConvention = mx.businessDayConventionParse(d['businessDayConvention'])

        return BlackVarianceCurve(refDate, vol, calendar, dayCounter)

    def toDict(self):
        res = dict()

        res[mx.CLASS_TYPE_NAME] = self.__class__.__name__
        res['refDate'] = str(self._refDate)
        res['periods'] = self._periods
        res['strikes'] = self._strikes
        res['blackVols'] = self._blackVols
        res['calendar'] = str(self._calendar)
        res['dayCounter'] = str(self._dayCounter)
        res['businessDayConvention'] = mx.businessDayConventionToString(self._businessDayConvention)

        return res