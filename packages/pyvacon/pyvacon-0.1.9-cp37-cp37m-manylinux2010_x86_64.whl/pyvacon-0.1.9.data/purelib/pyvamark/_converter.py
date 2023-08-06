# -*- coding: utf-8 -*-

import sys
import numpy as np
from functools import wraps
import inspect
import pandas as pd
from datetime import datetime
from datetime import timedelta
import pyvamark.pyvamark_swig as _swig


def date_range(start, end, delta = timedelta(days=1)):
    """
    generate a range of dates from start to end for a given timestep 
    
    start start date
    end end date
    delta timedelta, if not set, 1 day is used (datetime.timedelta(days=1))
    """
    date_list = []
    date_list.append(start)
    #if delta is None:
    #    delta = datetime.timedelta(days=1)
    while date_list[-1] < end:
        d = date_list[-1] + delta
        date_list.append(d)  
    return date_list        

def get_ptime(d, refdate = None):
    #print(str(d))
    if type(d) is _swig.ptime:
        return d
    
    if type(d) is pd.Timestamp:
        tmp = d.to_pydatetime()
        result = _swig.ptime(tmp.year, tmp.month, tmp.day, tmp.hour, tmp.minute, tmp.second)
        return result
    
    if type(d) is np.datetime64:
        tmp = pd.to_datetime(d)
        result = _swig.ptime(tmp.year, tmp.month, tmp.day, tmp.hour, tmp.minute, tmp.second)
        return result

    if type(d) is datetime:
        result = _swig.ptime(d.year, d.month, d.day, d.hour, d.minute, d.second)
        return result
    
    if refdate is None:
        Exception('Either reference date must be given or date must be of type datetime or ptime')
    
    refdate2 = get_ptime(refdate)
    result = _swig.ptime()
    refdate2.addDays(result, d)
    return result


def _convert(x):
    if isinstance(x, datetime) | isinstance(x, np.datetime64) | isinstance(x, pd.Timestamp):
        return get_ptime(x)
    if isinstance(x,list) and len(x)>0:
        if isinstance(x[0], datetime) | isinstance(x[0], np.datetime64) | isinstance(x[0], pd.Timestamp):
            return [get_ptime(y) for y in x]
        if isinstance(x[0], _swig.CouponDescription):
            coupons = _swig.vectorCouponDescription()
            for coupon in x: 
                coupons.append(coupon)
            return coupons

    return x

def converter(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        new_args = [_convert(x) for x in args]
        result = f(*new_args, **kwargs)        
        return result
    return wrapper

def _get_dict_repr(obj):
    import json

    def cleanup_dict(d):
        if not isinstance(d, dict):
            return d
        if len(d) == 1:
            for v in d.values():
                return v
        new_dict = {}
        for item, value in d.items():
            if item != 'cereal_class_version' and item != 'polymorphic_id' and item != 'UID_':
                if isinstance(value, dict):
                    if len(value) == 1:
                        for v in value.values():
                            new_dict[item] = v
                    else:
                        new_dict[item] = cleanup_dict(value)
                elif isinstance(value, list):
                    new_dict[item] = [cleanup_dict(vv) for vv in value]
                else:
                    new_dict[item] = value
        return new_dict
        
    repr = str(_swig.Clonable.getString(obj)) + '}'
    d = json.loads(repr)
    return cleanup_dict(d['value0'])

def _get_string_rep(obj):
    d = _get_dict_repr(obj)
    return str(d)

def _add_converter(cls):
    if sys.version_info >= (3,0,):    
        for attr, item in inspect.getmembers(cls, inspect.isfunction): #for python 2 : ismethod
            setattr(cls, attr, converter(item))
            if (attr == 'getDataTable'):
                setattr(cls, 'getDataFrame', _create_dataframe)
        for name, method in inspect.getmembers(cls, lambda o: isinstance(o, property)):
            setattr(cls,name, property(converter(method.fget), converter(method.fset)))
        setattr(cls, '__str__', _get_string_rep)
        setattr(cls, 'get_dictionary', _get_dict_repr)
        return cls
    else:
        Exception('python2 not supported')
        #for attr, item in inspect.getmembers(cls, inspect.ismethod): #for python 2 : ismethod
        #    setattr(cls, attr, converter(item))
        #for name, method in inspect.getmembers(cls, lambda o: isinstance(o, property)):
        #    setattr(cls,name, property(converter(method.fget), converter(method.fset)))
        #setattr(cls, '__str__', _get_string_rep)
        #setattr(cls, 'get_dictionary', _get_dict_repr)
        #return cls



def convert_from_vector(x):
    result = []
    for i in x:
        result.append(i)
    return result
    
def convert_to_vector(x):
    result = _swig.vectorDouble(len(x))
    for i in range(len(x)):
        result[i] = x[i]
    return result        
    
def create_ptime_list(refDate, dates):
    #ptimes = []
    #print(str(dates))
    ptimes = _swig.vectorPTime(len(dates))
    for i in range(len(dates)):
        ptimes[i] = get_ptime(dates[i], refDate)
    return ptimes
    
def create_datetime(ptime):
    return datetime(ptime.year(), ptime.month(), ptime.day(), ptime.hours(), ptime.minutes(), ptime.seconds())

def create_datetime_list(ptimes):
    result = []
    for x in ptimes:
        result.append(create_datetime(x))
    return result

def _create_dataframe(obj):

    data_table = None
    try:
        data_table = obj.getDataTable()
    except:
        pass
    
    return create_dataframe(data_table)


def create_dataframe(data_table):
    """
    converts a Utilities::DataTable object to a pandas DataFrame

    @returns DataFrame
    """
    tmp ={}
    date_columns = []

    if ((data_table != None) & (data_table.nRows() * data_table.nColumns()>0)):
        columns = data_table.getHeaderInformations().split(';')
        for i in range(data_table.nColumns()):
            dType = data_table.getColumnDataType(i)
            if dType == 'DATE':
                tmp[columns[i]] = [datetime.strptime(data_table.getCellInformation(j,i),'%Y-%b-%d %H:%M:%S') for j in range(data_table.nRows())]
                date_columns.append(columns[i])
            if dType == 'DOUBLE':
                tmp[columns[i]] = [float(data_table.getCellInformation(j,i)) for j in range(data_table.nRows())]
            else:
                tmp[columns[i]] = [data_table.getCellInformation(j,i) for j in range(data_table.nRows())]
        
    df = pd.DataFrame(tmp)
    for x in date_columns:
        df[x] = pd.to_datetime(df[x], format = '%Y-%b-%d %H:%M:%S')
        
    return df



def relative_to_absolute(refDate, ndays):
    result = []
    for i in ndays:
        tmp = _swig.ptime()
        refDate.addDays(tmp, i)
        result.append(tmp)
    return result

def np_matrix_from_correlation_dictionary(correlation_dict, factor_list, missing_value):
    """
    This method builds up a (correlation) matrix from a dictionary of single pairwise correlations and a list of factors included into the correlation list. It fills 
    the missing elements with the value specified as missing_value
    """
    result = np.full([len(factor_list),len(factor_list)], missing_value)
    for i in range(len(factor_list)):
        result[i,i] = 1.0
        for j in range(len(factor_list)):
            if (factor_list[i],factor_list[j]) in correlation_dict:
               result[i,j] = correlation_dict[(factor_list[i],factor_list[j])]
               result[j,i] = correlation_dict[(factor_list[i],factor_list[j])]
    return result

def to_np_matrix(mat):
    """
    Convert a vector<vector<double>> to a numpy matrix
    """
    if len(mat) == 0:
        return np.empty([0,0])
    result = np.empty([len(mat), len(mat[0])])
    for i in range(len(mat)):
        for j in range(len(mat[i])):
            result[i][j] = mat[i][j]
    return result

def from_np_matrix(mat):
    rows, cols = mat.shape
    result = _swig.vectorVectorDouble(rows)
    for i in range(rows):
        tmp = _swig.vectorDouble(cols)
        for j in range(cols):
            tmp[j] = mat[i][j]
        result[i] = tmp
    return result

def np_matrix_from_transition(trans_matrix, time_to_maturity):
    """
    returns a numpy matrix form the given transition matrix and given time horizon
    
    trans_matrix transition matrix
    time_to_maturity time horizon for which transition matrix is created
    """
    matrix = _swig.vectorDouble()
    trans_matrix.computeTransition(matrix, time_to_maturity)
    tmp = []
    for i in range(_swig.Rating.nRatings()):
        tmp1 = []
        for j in range(_swig.Rating.nRatings()):
            tmp1.append(matrix[i*_swig.Rating.nRatings() + j])
        tmp.append(tmp1)
    plot_matrix = np.matrix(tmp)
    return plot_matrix
    
def transition_from_np_matrix(trans_matrix, np):
    """
    set the entries of the given transition matrix to the values of the numpy matrix
    
    
    """
    for i in range(_swig.Rating.nRatings()):
        for j in range(_swig.Rating.nRatings()):
            trans_matrix.setEntry(i,j,np[i,j])

def adjust_transition(name, trans_matrix_orig, ratings, factor, refdate):
    if isinstance(ratings, str):
        ratings = [ratings]
    np_matrix = np_matrix_from_transition(trans_matrix_orig, 1.0)
    transition_new = _swig.TimeScaledRatingTransition(name, refdate, 1.0)
    for rating in ratings:
        i = _swig.Rating.getRatings().index(rating)
        row_sum = 0
        for j in range(_swig.Rating.nRatings()-1):
            correction = factor*np_matrix[i,j] 
            row_sum += correction
            np_matrix[i,j] -= correction 
        #print(str(np_matrix[i,i]) + ' ' + str(np_matrix[i,i+1]))
        np_matrix[i,_swig.Rating.nRatings()-1] += row_sum
        transition_from_np_matrix(transition_new, np_matrix)
    return transition_new
