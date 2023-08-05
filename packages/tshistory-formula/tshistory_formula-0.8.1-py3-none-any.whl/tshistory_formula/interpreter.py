import json
import inspect
from functools import partial
from datetime import datetime

import pytz
import pandas as pd
from psyl.lisp import (
    Env,
    parse
)

from tshistory.util import empty_series
from tshistory_formula.evaluator import (
    pevaluate,
    pexpreval,
    quasiexpreval
)

from tshistory_formula import (
    helper,
    registry
)


def functypes():
    return {
        name: helper.function_types(func)
        for name, func in registry.FUNCS.items()
    }


def jsontypes():
    return json.dumps(functypes())


class Interpreter:
    __slots__ = ('env', 'cn', 'tsh', 'getargs', 'histories', 'vcache', 'auto')
    FUNCS = None

    @property
    def operators(self):
        if Interpreter.FUNCS is None:
            Interpreter.FUNCS = registry.FUNCS
        return Interpreter.FUNCS

    def __init__(self, cn, tsh, getargs):
        self.cn = cn
        self.tsh = tsh
        self.getargs = getargs
        # bind funcs to the interpreter
        funcs = {}
        for name, func in self.operators.items():
            if '__interpreter__' in inspect.getfullargspec(func).args:
                func = partial(func, self)
            funcs[name] = func
        funcs['#t'] = True
        funcs['#f'] = False
        self.env = Env(funcs)
        self.histories = {}
        self.vcache = {}
        self.auto = set(registry.AUTO.values())

    def get(self, name, getargs):
        # `getarg` likey comes from self.getargs
        # but we allow it being modified hence
        # it comes back as a parameter there
        return self.tsh.get(self.cn, name, **getargs)

    def evaluate(self, tree):
        return pevaluate(tree, self.env, self.auto)

    def today(self, naive, tz):
        if naive:
            assert tz is None, f'date cannot be naive and have a tz'
        tz = pytz.timezone(tz or 'utc')

        key = ('today', naive, tz)
        if self.getargs.get('revision_date'):
            val = self.getargs['revision_date']
            if naive:
               val = val.replace(tzinfo=None)
            elif val.tzinfo is None:
                val = pd.Timestamp(val, tz=tz)
            self.vcache[key] = val
            return val

        val = self.vcache.get(key)
        if val is not None:
            return val

        if naive:
            val = pd.Timestamp(datetime.today())
        else:
            val = pd.Timestamp(datetime.today(), tz=tz)

        self.vcache[key] = val
        return val


class OperatorHistory(Interpreter):
    __slots__ = ('env', 'cn', 'tsh', 'getargs')
    FUNCS = None

    @property
    def operators(self):
        if OperatorHistory.FUNCS is None:
            OperatorHistory.FUNCS = {**registry.FUNCS, **registry.HISTORY}
        return OperatorHistory.FUNCS

    def evaluate_history(self, tree):
        return pexpreval(
            quasiexpreval(
                tree,
                self.env,
            ),
            self.env
        )


class HistoryInterpreter(Interpreter):
    __slots__ = 'env', 'cn', 'tsh', 'getargs', 'histories', 'tzaware', 'namecache', 'vcache'

    def __init__(self, name, *args, histories):
        super().__init__(*args)
        self.histories = histories
        # a callsite -> name mapping
        self.namecache = {}
        self.tzaware = self.tsh.metadata(self.cn, name)

    def _find_by_nearest_idate(self, name, idate):
        hist = self.histories[name]
        tzaware = idate.tzinfo is not None
        for date in reversed(list(hist.keys())):
            compdate = date
            if not tzaware:
                compdate = date.replace(tzinfo=None)
            if idate >= compdate:
                return hist[date]

        ts = empty_series(
            self.tzaware,
            name=name
        )
        return ts

    def get(self, name, _getargs):
        # getargs is moot there because histories
        # have been precomputed
        idate = self.env.get('__idate__')
        # provide ammo to .today
        self.getargs['revision_date'] = idate
        # get the nearest inferior or equal for the given
        # insertion date
        assert self.histories
        return self._find_by_nearest_idate(name, idate)

    def get_auto(self, tree):
        """ helper for autotrophic series that have pre built their
        history and are asked for one element
        (necessary since they bypass the above .get)
        """
        name = self.namecache.get(id(tree))
        if name is None:
            name = helper.name_of_expr(tree)
            self.namecache[id(tree)] = name
        idate = self.env.get('__idate__')
        assert idate
        return self._find_by_nearest_idate(name, idate)

    def evaluate(self, tree, idate, name):
        self.env['__idate__'] = idate
        self.env['__name__'] = name
        ts = pevaluate(tree, self.env, self.auto, hist=True)
        ts.name = name
        return ts


# staircase fast path


def has_compatible_operators(cn, tsh, tree, good_operators):
    operators = [tree[0]]
    for param in tree[1:]:
        if isinstance(param, list):
            operators.append(param[0])
    if any(op not in good_operators
           for op in operators):
        return False

    names = tsh.find_series(cn, tree)
    for name in names:
        formula = tsh.formula(cn, name)
        if formula:
            tree = parse(formula)
            if not has_compatible_operators(
                    cn, tsh, tree, good_operators):
                return False

    return True


class FastStaircaseInterpreter(Interpreter):
    __slots__ = ('env', 'cn', 'tsh', 'getargs', 'delta')

    def __init__(self, cn, tsh, getargs, delta):
        assert delta is not None
        super().__init__(cn, tsh, getargs)
        self.delta = delta

    def get(self, name, getargs):
        if self.tsh.type(self.cn, name) == 'primary':
            return self.tsh.staircase(
                self.cn, name, delta=self.delta, **getargs
            )
        return self.tsh.get(
            self.cn, name, **getargs,
            __interpreter__=self
        )


class NullIntepreter(Interpreter):

    def __init__(self):
        pass
