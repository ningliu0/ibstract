"""
Testing data.
"""

from collections import namedtuple
from numpy import NaN
from io import StringIO
import pandas as pd
import pytz
from ibstract.utils import dtutc, dtest, estmax
from ibstract.marketdata import HistDataReq
from ibstract.brokers import IB


__all__ = [
    'testdata_ib_connect',
    'testdata_ib_req_hist_data',
    'testdata_db_info',
    'testdata_query_hist_data',
    'testdata_insert_hist_data',
    'testdata_download_insert_hist_data',
    'testdata_market_data_block_merge',
    'testdata_req_start_end',
    'testdata_query_hist_data_split_req',
    'testdata_get_hist_data',
]


east = pytz.timezone('US/Eastern')


# --- test_brokers.IBTests ---
testdata_ib_connect = ('127.0.0.1', 4002)
testdata_ib_req_hist_data = {
    'login': testdata_ib_connect,
    'reqs_tz_datalen': [
        (HistDataReq('Stock', 'GS', '1 hour', '5 d', dtest(2017, 9, 16)), east, 59),
        (HistDataReq('Stock', 'BAC', '1 day', '10 d', dtest(2017, 9, 16)), east, 10),
        (HistDataReq('Stock', 'GOOG', '30 mins', '3 d', dtest(2017, 9, 16)), east, 69),
        (HistDataReq('Stock', 'AMZN', '1 hour', '3 d', dtest(2017, 9, 16)), east, 41),
        (HistDataReq('Stock', 'FB', '10 mins', '5 d', dtest(2017, 9, 16)), east, 443),
        (HistDataReq('Stock', 'TVIX', '5 mins', '5 d', dtest(2017, 9, 16)), east, 883),
    ],
}


# --- test_marketdata.MarketDataBlockTests ---
DataRowClose = namedtuple('DataRowClose',
                          'symbol barsize datetime close')
DataRowCloseVolume = namedtuple(
    'DataRowCloseVolume',
    'symb barSize time c vol')
data_gs = [
    DataRowClose('GS', '5 min', '2016-07-12 10:35:00', 140.05),
    DataRowClose('GS', '5 min', '2016-07-12 11:20:00', 141.34),
]
data_gs_1line = [
    DataRowCloseVolume('GS', '5 min', '2016-07-12 10:35:00', 140.05, 344428),
]
data_gs_merged = [
    DataRowCloseVolume('GS', '5 min', '2016-07-12 10:35:00', 140.05, 344428),
    DataRowCloseVolume('GS', '5 min', '2016-07-12 11:20:00', 141.34, NaN),
]
data_fb = [
    DataRowCloseVolume('FB', '5 min', '2016-07-21 09:30:00', 120.05, 234242),
    DataRowCloseVolume('FB', '5 min', '2016-07-21 09:35:00', 120.32, 410842),
    DataRowCloseVolume('FB', '1 min', '2016-07-25 09:40:00', 120.47, 579638),
    DataRowCloseVolume('FB', '1 min', '2016-07-25 09:41:00', 120.82, 192476),
]
data_amzn = [
    DataRowCloseVolume('AMZN', '1 day', '2016-07-21', 749.22, 27917),
    DataRowCloseVolume('AMZN', '1 day', '2016-07-22', 738.87, 36662),
    DataRowCloseVolume('AMZN', '1 day', '2016-07-23', 727.23, 8766),
]
testdata_market_data_block_merge = [
    data_gs,
    (data_gs_1line, data_gs_merged),
    (data_fb, data_gs_merged+data_fb),
    (data_amzn, data_gs_merged+data_fb+data_amzn),
]


# --- test_marketdata.HistoricalDataTests ---
testdata_db_info = {'host': '127.0.0.1', 'user': 'root',
                    'password': 'ibstract', 'db': 'ibstract_test'}

gs1h_csv = StringIO("""
Symbol,DataType,BarSize,TickerTime,opening,high,low,closing,volume,barcount,average
GS,TRADES,1h,2017-08-30 12:00:00+00:00,220.69,221.3,220.01,220.11,22,17,220.867
GS,TRADES,1h,2017-08-30 13:00:00+00:00,220.2,222.65,220.09,222.11,3429,2153,221.534
GS,TRADES,1h,2017-08-30 14:00:00+00:00,222.14,222.94,221.72,222.88,2729,1823,222.436
GS,TRADES,1h,2017-08-30 15:00:00+00:00,222.84,223.01,222.64,222.91,2129,1426,222.858
GS,TRADES,1h,2017-08-30 16:00:00+00:00,222.87,223.59,222.74,223.59,1864,1143,223.082
GS,TRADES,1h,2017-08-30 17:00:00+00:00,223.61,224.22,223.58,223.78,2268,1419,223.893
GS,TRADES,1h,2017-08-30 18:00:00+00:00,223.8,223.8,223.23,223.65,1802,1182,223.572
GS,TRADES,1h,2017-08-30 19:00:00+00:00,223.64,223.69,222.29,222.41,4360,2942,222.871
GS,TRADES,1h,2017-08-30 20:00:00+00:00,222.42,222.42,222.25,222.25,1132,14,222.415
GS,TRADES,1h,2017-08-30 21:00:00+00:00,222.89,222.89,222.42,222.42,8,3,222.537
GS,TRADES,1h,2017-08-30 22:00:00+00:00,222.42,222.42,222.42,222.42,0,0,222.42
GS,TRADES,1h,2017-08-30 23:00:00+00:00,222.38,222.38,222.38,222.38,10,2,222.38
GS,TRADES,1h,2017-08-31 12:00:00+00:00,223.35,223.35,223.35,223.35,11,5,223.35
GS,TRADES,1h,2017-08-31 13:00:00+00:00,223.3,224.15,222.86,223.15,1723,1039,223.444
GS,TRADES,1h,2017-08-31 14:00:00+00:00,223.14,224.01,222.58,223.11,2481,1768,223.406
GS,TRADES,1h,2017-08-31 15:00:00+00:00,223.12,223.82,223.08,223.71,1873,1301,223.499
GS,TRADES,1h,2017-08-31 16:00:00+00:00,223.72,224.38,223.46,223.64,1724,1056,223.953
GS,TRADES,1h,2017-08-31 17:00:00+00:00,223.61,223.94,223.29,223.69,1382,790,223.606
GS,TRADES,1h,2017-08-31 18:00:00+00:00,223.7,224.34,223.59,224.15,1947,972,224.03
GS,TRADES,1h,2017-08-31 19:00:00+00:00,224.15,224.49,223.6,223.7,4372,3132,224.06
GS,TRADES,1h,2017-08-31 20:00:00+00:00,223.74,223.74,223.74,223.74,2949,1,223.74
GS,TRADES,1h,2017-08-31 21:00:00+00:00,223.74,223.74,223.74,223.74,0,0,223.74
GS,TRADES,1h,2017-08-31 22:00:00+00:00,223.78,223.78,223.78,223.78,2,1,223.78
GS,TRADES,1h,2017-08-31 23:00:00+00:00,223.78,223.78,223.78,223.78,0,0,223.78
GS,TRADES,1h,2017-09-01 12:00:00+00:00,224.5,224.5,223.5,224.0,31,16,223.847
GS,TRADES,1h,2017-09-01 13:00:00+00:00,224.89,225.57,223.53,225.5,2098,1168,224.829
GS,TRADES,1h,2017-09-01 14:00:00+00:00,225.4,227.56,225.25,227.41,3878,2563,226.521
GS,TRADES,1h,2017-09-01 15:00:00+00:00,227.36,227.38,226.18,226.6,3210,2361,226.676
GS,TRADES,1h,2017-09-01 16:00:00+00:00,226.63,227.56,226.58,227.47,1758,1173,227.05
GS,TRADES,1h,2017-09-01 17:00:00+00:00,227.51,227.54,226.4,226.45,1608,1041,227.01
GS,TRADES,1h,2017-09-01 18:00:00+00:00,226.43,226.63,226.24,226.43,1218,910,226.429
GS,TRADES,1h,2017-09-01 19:00:00+00:00,226.43,226.43,225.75,225.84,3170,2524,226.067
GS,TRADES,1h,2017-09-01 20:00:00+00:00,225.88,225.9,225.88,225.9,1410,3,225.88
GS,TRADES,1h,2017-09-01 21:00:00+00:00,225.9,225.9,225.9,225.9,0,0,225.9
GS,TRADES,1h,2017-09-01 22:00:00+00:00,225.9,225.9,225.9,225.9,0,0,225.9
GS,TRADES,1h,2017-09-01 23:00:00+00:00,225.9,225.9,225.9,225.9,0,0,225.9
GS,TRADES,1h,2017-09-05 12:00:00+00:00,224.5,224.5,223.98,223.98,23,18,224.302
GS,TRADES,1h,2017-09-05 13:00:00+00:00,224.25,224.25,220.01,220.39,6431,3782,221.423
GS,TRADES,1h,2017-09-05 14:00:00+00:00,220.39,220.7,217.3,218.12,11332,5881,218.82
GS,TRADES,1h,2017-09-05 15:00:00+00:00,218.09,219.64,218.07,219.45,6457,3843,218.795
GS,TRADES,1h,2017-09-05 16:00:00+00:00,219.45,219.46,218.11,218.67,4940,3550,218.633
GS,TRADES,1h,2017-09-05 17:00:00+00:00,218.72,219.19,218.13,218.73,3228,2527,218.657
GS,TRADES,1h,2017-09-05 18:00:00+00:00,218.72,218.86,217.62,217.67,4939,3219,218.285
GS,TRADES,1h,2017-09-05 19:00:00+00:00,217.68,218.3,217.46,217.85,8173,5594,217.747
GS,TRADES,1h,2017-09-05 20:00:00+00:00,217.79,218.85,217.78,217.92,2445,10,217.781
GS,TRADES,1h,2017-09-05 21:00:00+00:00,218.0,218.11,217.91,218.11,8,5,218.022
GS,TRADES,1h,2017-09-05 22:00:00+00:00,218.11,218.17,217.95,217.95,15,11,218.12
GS,TRADES,1h,2017-09-05 23:00:00+00:00,218.15,218.15,217.93,217.93,2,2,218.04
GS,TRADES,1h,2017-09-06 12:00:00+00:00,218.97,219.29,218.97,219.2,28,11,219.159
GS,TRADES,1h,2017-09-06 13:00:00+00:00,219.1,220.78,218.67,219.58,4729,2596,219.796
GS,TRADES,1h,2017-09-06 14:00:00+00:00,219.61,221.02,219.54,220.01,4451,2722,220.49
GS,TRADES,1h,2017-09-06 15:00:00+00:00,219.98,220.2,217.73,218.2,4222,2500,219.02
GS,TRADES,1h,2017-09-06 16:00:00+00:00,218.2,219.83,217.61,219.8,2680,1809,218.335
GS,TRADES,1h,2017-09-06 17:00:00+00:00,219.77,220.5,219.41,219.57,2470,1492,219.954
GS,TRADES,1h,2017-09-06 18:00:00+00:00,219.61,219.8,218.9,219.33,2127,1447,219.428
GS,TRADES,1h,2017-09-06 19:00:00+00:00,219.33,219.7,218.85,219.05,5587,3451,219.363
GS,TRADES,1h,2017-09-06 20:00:00+00:00,218.83,219.09,218.83,218.99,3634,6,218.83
GS,TRADES,1h,2017-09-06 21:00:00+00:00,218.98,218.98,218.98,218.98,2,1,218.98
GS,TRADES,1h,2017-09-06 22:00:00+00:00,218.7,218.7,218.7,218.7,1,1,218.7
GS,TRADES,1h,2017-09-06 23:00:00+00:00,218.69,218.7,218.69,218.7,8,2,218.696
GS,TRADES,1h,2017-09-07 11:00:00+00:00,219.0,219.0,219.0,219.0,1,1,219.0
GS,TRADES,1h,2017-09-07 12:00:00+00:00,219.21,219.4,218.5,218.5,31,16,219.015
GS,TRADES,1h,2017-09-07 13:00:00+00:00,218.57,218.83,216.07,216.31,3338,1726,217.503
GS,TRADES,1h,2017-09-07 14:00:00+00:00,216.35,216.35,214.64,215.77,7048,4299,215.392
GS,TRADES,1h,2017-09-07 15:00:00+00:00,215.74,216.41,214.96,215.28,4571,3190,215.666
GS,TRADES,1h,2017-09-07 16:00:00+00:00,215.24,216.28,215.06,216.07,2191,1541,215.518
GS,TRADES,1h,2017-09-07 17:00:00+00:00,216.04,216.41,215.26,215.6,2058,1495,215.708
GS,TRADES,1h,2017-09-07 18:00:00+00:00,215.58,215.74,215.25,215.37,2206,1509,215.428
GS,TRADES,1h,2017-09-07 19:00:00+00:00,215.4,215.94,214.95,215.83,6582,4149,215.313
GS,TRADES,1h,2017-09-07 20:00:00+00:00,215.84,216.88,215.8,216.02,1869,9,215.846
GS,TRADES,1h,2017-09-07 21:00:00+00:00,215.98,215.98,215.9,215.9,9,6,215.927
GS,TRADES,1h,2017-09-07 22:00:00+00:00,215.9,215.99,215.9,215.99,14,3,215.909
GS,TRADES,1h,2017-09-07 23:00:00+00:00,216.09,216.09,216.09,216.09,1,1,216.09
GS,TRADES,1h,2017-09-08 11:00:00+00:00,215.44,215.44,215.44,215.44,1,1,215.44
GS,TRADES,1h,2017-09-08 12:00:00+00:00,214.9,215.5,214.8,215.5,22,8,215.05
GS,TRADES,1h,2017-09-08 13:00:00+00:00,215.5,218.76,215.1,218.67,5788,3250,217.577
GS,TRADES,1h,2017-09-08 14:00:00+00:00,218.68,219.28,217.78,218.04,4696,3283,218.707
GS,TRADES,1h,2017-09-08 15:00:00+00:00,218.06,218.39,216.82,216.89,2574,1880,217.345
GS,TRADES,1h,2017-09-08 16:00:00+00:00,216.92,217.3,216.67,217.14,2049,1433,217.015
GS,TRADES,1h,2017-09-08 17:00:00+00:00,217.12,217.17,216.15,216.76,2254,1565,216.591
GS,TRADES,1h,2017-09-08 18:00:00+00:00,216.76,217.35,216.61,217.01,1921,1373,217.117
GS,TRADES,1h,2017-09-08 19:00:00+00:00,217.01,217.34,216.69,217.24,3980,2789,217.075
GS,TRADES,1h,2017-09-08 20:00:00+00:00,217.21,217.21,216.71,216.71,2222,6,217.209
GS,TRADES,1h,2017-09-08 21:00:00+00:00,217.0,217.0,217.0,217.0,2,1,217.0
GS,TRADES,1h,2017-09-08 22:00:00+00:00,216.46,216.8,216.46,216.8,3,2,216.698
GS,TRADES,1h,2017-09-08 23:00:00+00:00,216.8,216.8,216.8,216.8,0,0,216.8
GS,TRADES,1h,2017-09-11 11:00:00+00:00,219.01,219.06,219.0,219.0,19,15,219.004
GS,TRADES,1h,2017-09-11 12:00:00+00:00,219.0,219.5,218.02,219.25,86,52,218.883
GS,TRADES,1h,2017-09-11 13:00:00+00:00,219.25,221.72,218.99,219.66,4403,2345,219.964
GS,TRADES,1h,2017-09-11 14:00:00+00:00,219.66,221.35,219.54,220.66,4182,2712,220.819
GS,TRADES,1h,2017-09-11 15:00:00+00:00,220.69,221.89,220.43,220.78,2952,2094,221.137
GS,TRADES,1h,2017-09-11 16:00:00+00:00,220.85,221.68,220.4,221.11,1833,1314,221.104
GS,TRADES,1h,2017-09-11 17:00:00+00:00,221.13,221.58,220.98,221.4,2417,1639,221.304
GS,TRADES,1h,2017-09-11 18:00:00+00:00,221.41,221.54,220.97,221.27,2008,1576,221.248
GS,TRADES,1h,2017-09-11 19:00:00+00:00,221.26,221.63,220.92,221.09,4115,3177,221.246
GS,TRADES,1h,2017-09-11 20:00:00+00:00,221.06,221.07,221.0,221.06,1969,5,221.06
GS,TRADES,1h,2017-09-11 21:00:00+00:00,221.06,221.06,221.06,221.06,206,1,221.06
GS,TRADES,1h,2017-09-11 22:00:00+00:00,221.02,221.02,221.02,221.02,2,2,221.02
GS,TRADES,1h,2017-09-11 23:00:00+00:00,221.02,221.02,221.02,221.02,0,0,221.02
GS,TRADES,1h,2017-09-12 11:00:00+00:00,221.5,221.5,221.5,221.5,3,3,221.5
GS,TRADES,1h,2017-09-12 12:00:00+00:00,221.5,222.0,221.5,221.8,41,34,221.791
GS,TRADES,1h,2017-09-12 13:00:00+00:00,221.84,225.8,221.84,225.35,6492,3768,224.636
GS,TRADES,1h,2017-09-12 14:00:00+00:00,225.36,226.41,224.98,225.69,4994,3229,225.686
GS,TRADES,1h,2017-09-12 15:00:00+00:00,225.57,227.18,225.15,226.93,4580,2769,226.22
GS,TRADES,1h,2017-09-12 16:00:00+00:00,226.9,227.69,226.55,227.0,3184,2231,227.03
GS,TRADES,1h,2017-09-12 17:00:00+00:00,227.01,227.5,226.67,226.82,2173,1627,227.101
GS,TRADES,1h,2017-09-12 18:00:00+00:00,226.8,226.88,226.35,226.48,2386,1423,226.661
GS,TRADES,1h,2017-09-12 19:00:00+00:00,226.51,226.62,225.61,225.95,5800,3825,225.959
GS,TRADES,1h,2017-09-12 20:00:00+00:00,225.95,226.0,225.95,226.0,1602,2,225.95
GS,TRADES,1h,2017-09-12 21:00:00+00:00,226.05,226.05,226.01,226.01,2,2,226.03
GS,TRADES,1h,2017-09-12 22:00:00+00:00,226.01,226.01,226.01,226.01,0,0,226.01
GS,TRADES,1h,2017-09-12 23:00:00+00:00,226.15,226.15,226.15,226.15,4,2,226.15
""")

gs1h_full = pd.read_csv(gs1h_csv)
gs1h = gs1h_full.loc[
    (gs1h_full.TickerTime > '2017-09-05')
    & (gs1h_full.TickerTime < '2017-09-09')].reset_index(drop=True)

testdata_insert_hist_data = [
    gs1h.loc[gs1h.TickerTime < '2017-09-07 19:00:00+00:00'],
    gs1h.loc[gs1h.TickerTime > '2017-09-06 20:00:00+00:00'],
    gs1h
]

testdata_query_hist_data = [
    gs1h, ('Stock', 'GS', 'TRADES', '1h',
           dtutc(2017, 9, 6, 19), dtutc(2017, 9, 8, 14),)
]

testdata_download_insert_hist_data = {
    'req': HistDataReq('Stock', 'GS', '1h', '5d', dtest(2017, 9, 6)),
    'broker': (IB(), testdata_ib_connect),
    'insert_limit': (dtest(2017, 9, 1, 14), dtest(2017, 9, 5, 20)),
}

testdata_query_hist_data_split_req = [
    {
        'req': HistDataReq('Stock', 'GS', '1h', '8d', dtest(2017, 9, 13)),
        'df_db': gs1h[:24].append(gs1h[37:]),
        'dl_reqs': [
            HistDataReq('Stock', 'GS', '1h', '2d', estmax(dtest(2017, 9, 1))),
            HistDataReq('Stock', 'GS', '1h', '1d', estmax(dtest(2017, 9, 7))),
            HistDataReq('Stock', 'GS', '1h', '2d', estmax(dtest(2017, 9, 12))),
        ],
        'insert_limit': [
            (dtest(2017, 8, 31, 0, 0), estmax(dtest(2017, 9, 1))),
            (dtest(2017, 9, 7, 0, 0), estmax(dtest(2017, 9, 7))),
            (dtest(2017, 9, 11, 0, 0), estmax(dtest(2017, 9, 12))),
        ],
        'start_dt': dtest(2017, 8, 31, 0, 0),
        'end_dt': dtest(2017, 9, 13, 0, 0),
    },
    {
        'req': HistDataReq('Stock', 'GS', '1h', '2W', dtest(2017, 9, 13)),
        'df_db': gs1h,
        'dl_reqs': [
            HistDataReq(
                'Stock', 'GS', '1h', '3d', estmax(dtest(2017, 9, 1))),
            HistDataReq(
                'Stock', 'GS', '1h', '2d', estmax(dtest(2017, 9, 12))),
        ],
        'insert_limit': [
            (dtest(2017, 8, 30, 0, 0), estmax(dtest(2017, 9, 1))),
            (dtest(2017, 9, 11, 0, 0), estmax(dtest(2017, 9, 12))),
        ],
        'start_dt': dtest(2017, 8, 30, 0, 0),
        'end_dt': dtest(2017, 9, 13, 0, 0),
    },
]

testdata_get_hist_data = [
    {
        'testcase': 'All data requested exist in database',
        'df_db': gs1h,
        'req': HistDataReq('Stock', 'GS', '1h', '2d', dtest(2017, 9, 8)),
        'broker': (IB, testdata_ib_connect),
        'xchg_tz': east,
        'blk_exp.df': gs1h.loc[
            (gs1h.TickerTime > '2017-09-06') & (gs1h.TickerTime < '2017-09-08')
        ].reset_index(drop=True),
    },
    {
        'testcase': 'Data from both database and downloading',
        'df_db': gs1h,
        'req': HistDataReq('Stock', 'GS', '1h', '2W', dtest(2017, 9, 13)),
        'broker': (IB, testdata_ib_connect),
        'xchg_tz': east,
        'blk_exp.df': gs1h_full,
    }
]

testdata_req_start_end = [  # (req, start_dt, end_dt)
    # BarSize '1d', TimeDur in 'd'
    (HistDataReq('Stock', 'GS', '1d', '1d', dtest(2017, 9, 12)),
     dtest(2017, 9, 11, 0, 0), dtest(2017, 9, 12, 0, 0)),
    (HistDataReq('Stock', 'GS', '1d', '3d', dtest(2017, 9, 12)),
     dtest(2017, 9, 7, 0, 0), dtest(2017, 9, 12, 0, 0)),
    (HistDataReq('Stock', 'GS', '1d', '8d', dtest(2017, 9, 12)),
     dtest(2017, 8, 30, 0, 0), dtest(2017, 9, 12, 0, 0)),
    (HistDataReq('Stock', 'GS', '1d', '1d', dtest(2017, 9, 12, 14, 15)),
     dtest(2017, 9, 11, 14, 15), dtest(2017, 9, 12, 14, 15)),
    (HistDataReq('Stock', 'GS', '1d', '3d', dtest(2017, 9, 12, 14, 15)),
     dtest(2017, 9, 7, 14, 15), dtest(2017, 9, 12, 14, 15)),
    (HistDataReq('Stock', 'GS', '1d', '8d', dtest(2017, 9, 12, 14, 15)),
     dtest(2017, 8, 30, 14, 15), dtest(2017, 9, 12, 14, 15)),
    # BarSize '1d', TimeDur in 'h'
    (HistDataReq('Stock', 'GS', '1d', '2h', dtest(2017, 9, 12)),
     dtest(2017, 9, 11, 0, 0), dtest(2017, 9, 12, 0, 0)),
    (HistDataReq('Stock', 'GS', '1d', '10h', dtest(2017, 9, 12)),
     dtest(2017, 9, 11, 0, 0), dtest(2017, 9, 12, 0, 0)),
    (HistDataReq('Stock', 'GS', '1d', '24h', dtest(2017, 9, 12)),
     dtest(2017, 9, 11, 0, 0), dtest(2017, 9, 12, 0, 0)),
    (HistDataReq('Stock', 'GS', '1d', '36h', dtest(2017, 9, 12)),
     dtest(2017, 9, 8, 0, 0), dtest(2017, 9, 12, 0, 0)),
    (HistDataReq('Stock', 'GS', '1d', '39h', dtest(2017, 9, 12)),
     dtest(2017, 9, 8, 0, 0), dtest(2017, 9, 12, 0, 0)),
    (HistDataReq('Stock', 'GS', '1d', '2h', dtest(2017, 9, 12, 14, 15, 30)),
     dtest(2017, 9, 12, 0, 0, 0), dtest(2017, 9, 12, 14, 15, 30)),
    (HistDataReq('Stock', 'GS', '1d', '10h', dtest(2017, 9, 12, 14, 15, 30)),
     dtest(2017, 9, 12, 0, 0, 0), dtest(2017, 9, 12, 14, 15, 30)),
    (HistDataReq('Stock', 'GS', '1d', '20h', dtest(2017, 9, 12, 14, 15, 30)),
     dtest(2017, 9, 11, 0, 0, 0), dtest(2017, 9, 12, 14, 15, 30)),
    (HistDataReq('Stock', 'GS', '1d', '24h', dtest(2017, 9, 12, 14, 15, 30)),
     dtest(2017, 9, 11, 0, 0, 0), dtest(2017, 9, 12, 14, 15, 30)),
    (HistDataReq('Stock', 'GS', '1d', '36h', dtest(2017, 9, 12, 14, 15, 30)),
     dtest(2017, 9, 11, 0, 0, 0), dtest(2017, 9, 12, 14, 15, 30)),
    (HistDataReq('Stock', 'GS', '1d', '39h', dtest(2017, 9, 12, 14, 15, 30)),
     dtest(2017, 9, 8, 0, 0, 0), dtest(2017, 9, 12, 14, 15, 30)),
    (HistDataReq('Stock', 'GS', '1d', '48h', dtest(2017, 9, 12, 14, 15, 30)),
     dtest(2017, 9, 8, 0, 0, 0), dtest(2017, 9, 12, 14, 15, 30)),
    (HistDataReq('Stock', 'GS', '1d', '66h', dtest(2017, 9, 12, 14, 15, 30)),
     dtest(2017, 9, 7, 0, 0, 0), dtest(2017, 9, 12, 14, 15, 30)),
    # BarSize '1d', TimeDur in 'W/M/Y'
    (HistDataReq('Stock', 'GS', '1d', '2W', dtest(2017, 9, 12)),
     dtest(2017, 8, 29, 0, 0), dtest(2017, 9, 12, 0, 0)),
    (HistDataReq('Stock', 'GS', '1d', '2M', dtest(2017, 9, 12)),
     dtest(2017, 7, 12, 0, 0), dtest(2017, 9, 12, 0, 0)),
    (HistDataReq('Stock', 'GS', '1d', '2Y', dtest(2017, 9, 12)),
     dtest(2015, 9, 12, 0, 0), dtest(2017, 9, 12, 0, 0)),
    # BarSize '1W'
    (HistDataReq('Stock', 'GS', '1W', '2h', dtest(2017, 9, 12)),
     dtest(2017, 9, 11, 22, 0), dtest(2017, 9, 12, 0, 0)),
    (HistDataReq('Stock', 'GS', '1W', '2d', dtest(2017, 9, 12)),
     dtest(2017, 9, 8, 0, 0), dtest(2017, 9, 12, 0, 0)),
    (HistDataReq('Stock', 'GS', '1W', '2W', dtest(2017, 9, 12)),
     dtest(2017, 8, 29, 0, 0), dtest(2017, 9, 12, 0, 0)),
    (HistDataReq('Stock', 'GS', '1W', '2M', dtest(2017, 9, 12)),
     dtest(2017, 7, 12, 0, 0), dtest(2017, 9, 12, 0, 0)),
    (HistDataReq('Stock', 'GS', '1W', '2Y', dtest(2017, 9, 12)),
     dtest(2015, 9, 12, 0, 0), dtest(2017, 9, 12, 0, 0)),
    # BarSize '1M'
    (HistDataReq('Stock', 'GS', '1M', '2h', dtest(2017, 9, 12)),
     dtest(2017, 9, 11, 22, 0), dtest(2017, 9, 12, 0, 0)),
    (HistDataReq('Stock', 'GS', '1M', '2d', dtest(2017, 9, 12)),
     dtest(2017, 9, 8, 0, 0), dtest(2017, 9, 12, 0, 0)),
    (HistDataReq('Stock', 'GS', '1M', '2W', dtest(2017, 9, 12)),
     dtest(2017, 8, 29, 0, 0), dtest(2017, 9, 12, 0, 0)),
    (HistDataReq('Stock', 'GS', '1M', '2M', dtest(2017, 9, 12)),
     dtest(2017, 7, 12, 0, 0), dtest(2017, 9, 12, 0, 0)),
    (HistDataReq('Stock', 'GS', '1M', '2Y', dtest(2017, 9, 12)),
     dtest(2015, 9, 12, 0, 0), dtest(2017, 9, 12, 0, 0)),
    # BarSize '1m', TimeDur in 'd'
    (HistDataReq('Stock', 'GS', '1m', '1d', dtest(2017, 9, 12)),
     dtest(2017, 9, 11, 0, 0), dtest(2017, 9, 12, 0, 0)),
    (HistDataReq('Stock', 'GS', '1m', '3d', dtest(2017, 9, 12)),
     dtest(2017, 9, 7, 0, 0), dtest(2017, 9, 12, 0, 0)),
    (HistDataReq('Stock', 'GS', '1m', '8d', dtest(2017, 9, 12)),
     dtest(2017, 8, 30, 0, 0), dtest(2017, 9, 12, 0, 0)),
    (HistDataReq('Stock', 'GS', '1m', '1d', dtest(2017, 9, 12, 14, 15)),
     dtest(2017, 9, 11, 14, 15), dtest(2017, 9, 12, 14, 15)),
    (HistDataReq('Stock', 'GS', '1m', '3d', dtest(2017, 9, 12, 14, 15)),
     dtest(2017, 9, 7, 14, 15), dtest(2017, 9, 12, 14, 15)),
    (HistDataReq('Stock', 'GS', '1m', '8d', dtest(2017, 9, 12, 14, 15)),
     dtest(2017, 8, 30, 14, 15), dtest(2017, 9, 12, 14, 15)),
    # BarSize '1m', TimeDur in h/m/s
    (HistDataReq('Stock', 'GS', '1m', '5m', dtest(2017, 9, 12)),
     dtest(2017, 9, 11, 23, 55), dtest(2017, 9, 12, 0, 0)),
    (HistDataReq('Stock', 'GS', '1m', '1h', dtest(2017, 9, 12)),
     dtest(2017, 9, 11, 23, 0), dtest(2017, 9, 12, 0, 0)),
    (HistDataReq('Stock', 'GS', '1m', '18h', dtest(2017, 9, 12)),
     dtest(2017, 9, 11, 6, 0), dtest(2017, 9, 12, 0, 0)),
    (HistDataReq('Stock', 'GS', '1m', '25h', dtest(2017, 9, 12)),
     dtest(2017, 9, 11, 0, 0), dtest(2017, 9, 12, 0, 0)),
    (HistDataReq('Stock', 'GS', '1m', '5m', dtest(2017, 9, 12, 14, 15)),
     dtest(2017, 9, 12, 14, 10), dtest(2017, 9, 12, 14, 15)),
    (HistDataReq('Stock', 'GS', '1m', '1h', dtest(2017, 9, 12, 14, 15)),
     dtest(2017, 9, 12, 13, 15), dtest(2017, 9, 12, 14, 15)),
    (HistDataReq('Stock', 'GS', '1m', '8h', dtest(2017, 9, 12, 14, 15)),
     dtest(2017, 9, 12, 6, 15), dtest(2017, 9, 12, 14, 15)),
    (HistDataReq('Stock', 'GS', '1m', '18h', dtest(2017, 9, 12, 14, 15)),
     dtest(2017, 9, 12, 0, 0), dtest(2017, 9, 12, 14, 15)),
]
