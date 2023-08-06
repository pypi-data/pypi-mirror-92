from pykrx.website.comm import dataframe_empty_handler
from pykrx.website.krx.market.ticker import get_stock_ticker_isin
from pykrx.website.krx.market.core import (개별종목시세, 전종목등락률, PER_PBR_배당수익률_전종목,
                                           PER_PBR_배당수익률_개별, 전종목시세, 외국인보유량_개별추이,
                                           외국인보유량_전종목, 투자자별_순매수상위종목,
                                           투자자별_거래실적_개별종목_기간합계, 투자자별_거래실적_개별종목_일별추이_일반,
                                           투자자별_거래실적_개별종목_일별추이_상세, 투자자별_거래실적_전체시장_기간합계,
                                           투자자별_거래실적_전체시장_일별추이_일반, 투자자별_거래실적_전체시장_일별추이_상세)
from pykrx.website.krx.market.core import (개별종목_공매도_종합정보, SRT02020300,
                                           SRT02020400, SRT02030100, SRT02030400)
from pykrx.website.krx.market.core import (전체지수기본정보, 개별지수시세, 전체지수등락률, 지수구성종목)
import numpy as np
import pandas as pd
from pandas import Series, DataFrame
import datetime


# ------------------------------------------------------------------------------------------
# Market
@dataframe_empty_handler
def get_market_ohlcv_by_date(fromdate: str, todate: str, ticker: str) -> DataFrame:
    """일자별로 정렬된 특정 종목의 OHLCV

    Args:
        fromdate (str): 조회 시작 일자 (YYYYMMDD)
        todate   (str): 조회 종료 일자 (YYYYMMDD)
        ticker   (str): 조회 종목의 ticker

    Returns:
        DataFrame:

        >> get_market_ohlcv_by_date("20150720", "20150810", "005930")

                           시가     고가     저가     종가  거래량      거래대금    등락률
            날짜
            2015-07-20  1291000  1304000  1273000  1275000  128928  165366199000 -2.300781
            2015-07-21  1275000  1277000  1247000  1263000  194055  244129106000 -0.939941
            2015-07-22  1244000  1260000  1235000  1253000  268323  333813094000 -0.790039
            2015-07-23  1244000  1253000  1234000  1234000  208965  259446564000 -1.519531
    """
    isin = get_stock_ticker_isin(ticker)
    df = 개별종목시세().fetch(fromdate, todate, isin)

    df = df[['TRD_DD', 'TDD_OPNPRC', 'TDD_HGPRC', 'TDD_LWPRC', 'TDD_CLSPRC', 'ACC_TRDVOL', 'ACC_TRDVAL', 'FLUC_RT']]
    df.columns = ['날짜', '시가', '고가', '저가', '종가', '거래량', '거래대금', '등락률']
    df = df.set_index('날짜')
    df.index = pd.to_datetime(df.index, format='%Y/%m/%d')
    df = df.replace('[^-\w\.]', '', regex=True)
    df = df.replace('\-$', '0', regex=True)
    df = df.replace('', '0')
    df = df.astype({
        "시가":np.int32, "고가":np.int32, "저가":np.int32, "종가":np.int32,
        "거래량":np.int32, "거래대금":np.int64, "등락률":np.float16} )
    return df.sort_index()


@dataframe_empty_handler
def get_market_ohlcv_by_ticker(date: str, market: str="KOSPI") -> DataFrame:
    """티커별로 정리된 전종목 OHLCV

    Args:
        date   (str): 조회 일자 (YYYYMMDD)
        market (str): 조회 시장 (KOSPI/KOSDAQ/ALL). Defaults to KOSPI.

    Returns:
        DataFrame:
                     시가   고가   저가   종가  거래량    거래대금
            티커
            060310   2150   2390   2150   2190  981348  2209370985
            095570   3135   3200   3100   3130   89871   282007385
            006840  17050  17200  16500  16500   30567   512403000
            054620   8550   8740   8400   8650  647596  5525789290
            265520  22150  23100  22050  22400  255846  5798313650
    """

    market = {"ALL": "ALL", "KOSPI": "STK", "KOSDAQ": "KSQ", "KONEX": "KNX"}[market]
    df = 전종목시세().fetch(date, market)
    df = df[['ISU_SRT_CD', 'TDD_OPNPRC', 'TDD_HGPRC', 'TDD_LWPRC', 'TDD_CLSPRC', 'ACC_TRDVOL', 'ACC_TRDVAL', 'FLUC_RT']]
    df.columns = ['티커', '시가', '고가', '저가', '종가', '거래량', '거래대금', '등락률']
    df = df.replace('[^-\w\.]', '', regex=True)
    df = df.replace('\-$', '0', regex=True)
    df = df.replace('', '0')
    df = df.set_index('티커')
    df = df.astype({
        "시가":np.int32, "고가":np.int32, "저가":np.int32, "종가":np.int32,
        "거래량":np.int32, "거래대금":np.int64, "등락률":np.float16 } )
    return df


@dataframe_empty_handler
def get_market_cap_by_date(fromdate: str, todate: str, ticker: str) -> DataFrame:
    """일자별로 정렬된 시가총액

    Args:
        fromdate (str): 조회 시작 일자 (YYYYMMDD)
        todate   (str): 조회 종료 일자 (YYYYMMDD)
        ticker   (str): 티커

    Returns:
        DataFrame:
                               시가총액  거래량      거래대금 상장주식수
            날짜
            2015-07-20  187806654675000  128928  165366199000  147299337
            2015-07-21  186039062631000  194055  244129106000  147299337
            2015-07-22  184566069261000  268323  333813094000  147299337
            2015-07-23  181767381858000  208965  259446564000  147299337
            2015-07-24  181030885173000  196584  241383636000  147299337
    """
    isin = get_stock_ticker_isin(ticker)
    df = 개별종목시세().fetch(fromdate, todate, isin)
    df = df[['TRD_DD', 'MKTCAP', 'ACC_TRDVOL', 'ACC_TRDVAL', 'LIST_SHRS']]
    df.columns = ['날짜', '시가총액', '거래량', '거래대금', '상장주식수']

    df = df.replace('/', '', regex=True)
    df = df.replace(',', '', regex=True)
    df = df.set_index('날짜')
    df = df.astype(np.int64)
    df.index = pd.to_datetime(df.index, format='%Y%m%d')
    return df.sort_index()


@dataframe_empty_handler
def get_market_cap_by_ticker(date: str, market: str="KOSPI", ascending: bool=False) -> DataFrame:
    """티커별로 정렬된 시가총액

    Args:
        date                 (str): 조회 일자 (YYYYMMDD)
        market     (str, optional): 조회 시장 (KOSPI/KOSDAQ/ALL). Defaults to KOSPI.
        ascending (bool, optional): 정렬 기준. Defaults to False.

    Returns:
        DataFrame :
                      종가         시가총액    거래량         거래대금   상장주식수
            티커
            005930   51900  309831714345000  18541624  309831714345000   5969782550
            000660   84300   61370599369500   3397112   61370599369500    728002365
            207940  815000   53924475000000    163339   53924475000000     66165000
            035420  269500   44268984952500   1196267   44268984952500    164263395
            068270  316000   42640845660000    918369   42640845660000    134939385
    """
    market = {"ALL": "ALL", "KOSPI": "STK", "KOSDAQ": "KSQ", "KONEX": "KNX"}[market]
    df = 전종목시세().fetch(date, market)
    df = df[['ISU_SRT_CD', 'TDD_CLSPRC', 'MKTCAP', 'ACC_TRDVOL', 'ACC_TRDVAL', 'LIST_SHRS']]
    df.columns = ['티커', '종가', '시가총액', '거래량', '거래대금', '상장주식수']

    df = df.set_index('티커')
    df = df.replace(np.NaN, 0)
    df = df.replace('/', '', regex=True)
    df = df.replace(',', '', regex=True)
    df = df.astype(np.int64)
    return df.sort_values('시가총액', ascending=ascending)


@dataframe_empty_handler
def get_market_fundamental_by_ticker(date: str, market: str="KOSPI") -> DataFrame:
    """티커별로 정리된 특정 일자의 BPS/PER/PBR/배당수익률

    Args:
        date (str): 조회 일자 (YYYYMMDD)
        market (str, optional): 조회 시장 (KOSPI/KOSDAQ/ALL)

    Returns:
        DataFrame:
                         종목명    BPS    PER   PBR    EPS   DIV  DPS
            티커
            060310          3S     704   0.00  3.38      0  0.00    0
            095570  AJ네트웍스    6168  15.03  0.78    320  1.79   86
            068400    AJ렌터카   11091  20.45  1.05    572  0.00    0
            006840    AK홀딩스   52954   6.78  0.99   7727  1.24  650
            054620   APS홀딩스   13639   0.10  0.32  46508  0.00    0
    """
    market = {"ALL": "ALL", "KOSPI": "STK", "KOSDAQ": "KSQ", "KONEX": "KNX"}.\
        get(market, "ALL")
    df = PER_PBR_배당수익률_전종목().fetch(date, market)

    df = df[['ISU_ABBRV', 'ISU_SRT_CD', 'BPS', 'PER', 'PBR', 'EPS', 'DVD_YLD', 'DPS']]
    df.columns = ['종목명', '티커', 'BPS', 'PER', 'PBR', 'EPS', 'DIV', 'DPS']
    df.set_index('티커', inplace=True)

    df = df.replace('-', '0', regex=True)
    df = df.replace('', '0', regex=True)
    df = df.replace(',', '', regex=True)
    df = df.astype({"종목명": str, "DIV": np.float32, "BPS": np.int32,
                    "PER": np.float16, "PBR": np.float16, "EPS": np.int32,
                    "DIV": np.float16, "DPS": np.int32}, )
    return df


@dataframe_empty_handler
def get_market_fundamental_by_date(fromdate: str, todate: str, ticker:str, market: str="KOSPI") -> DataFrame:
    """날짜로 정렬된 종목별 BPS/PER/PBR/배당수익률

    Args:
        fromdate (str          ): 조회 시작 일자 (YYYYMMDD)
        todate   (str          ): 조회 종료 일자 (YYYYMMDD)
        ticker   (str          ): 종목의 티커
        market   (str, optional): 조회 시장 (KOSPI/KOSDAQ/ALL)

    Returns:
        DataFrame:
                           BPS       PER       PBR     EPS       DIV    DPS
            날짜
            2015-07-20  953266  8.328125  1.339844  153105  1.570312  20000
            2015-07-21  953266  8.250000  1.320312  153105  1.580078  20000
            2015-07-22  953266  8.179688  1.309570  153105  1.599609  20000
            2015-07-23  953266  8.062500  1.290039  153105  1.620117  20000
            2015-07-24  953266  8.031250  1.290039  153105  1.629883  20000
    """
    market = {"ALL": "ALL", "KOSPI": "STK", "KOSDAQ": "KSQ", "KONEX": "KNX"}.\
        get(market, "ALL")
    isin = get_stock_ticker_isin(ticker)

    df = PER_PBR_배당수익률_개별().fetch(fromdate, todate, market, isin)

    df = df[['TRD_DD', 'BPS', 'PER', 'PBR', 'EPS', 'DVD_YLD', 'DPS']]
    df.columns = ['날짜', 'BPS', 'PER', 'PBR', 'EPS', 'DIV', 'DPS']

    df = df.replace('-', '0', regex=True)
    df = df.replace('/', '', regex=True)
    df = df.replace('', '0', regex=True)
    df = df.replace(',', '', regex=True)
    df = df.astype({"DIV": np.float32, "BPS": np.int32, "PER": np.float16,
                    "PBR": np.float16, "EPS": np.int32, "DIV": np.float16,
                    "DPS": np.int32}, )
    df = df.set_index('날짜')
    df.index = pd.to_datetime(df.index, format='%Y%m%d')
    return df.sort_index()


@dataframe_empty_handler
def get_market_ticker_and_name(date: str, market: str="KOSPI") -> Series:
    """티커이름 (index), 종목명 (value)으로 구성된 시리즈 반환

    Note:
        KRX가 20000101 이후의 데이터만을 제공

    Args:
        date   (str): 조회 일자 (YYYYMMDD)
        market (str): 조회 시장 (KOSPI/KOSDAQ/ALL)

    Returns:
        Series:
            095570    AJ네트웍스
            068400     AJ렌터카
            006840     AK홀딩스
            027410       BGF
            282330    BGF리테일
    """
    market = {"ALL": "ALL", "KOSPI": "STK", "KOSDAQ": "KSQ", "KONEX": "KNX"}. \
        get(market, "ALL")

    df = 전종목시세().fetch(date, market)
    df = df[['ISU_SRT_CD', 'ISU_ABBRV']]
    df.columns = ['티커', '종목명']
    df = df.set_index('티커')
    return df['종목명']


@dataframe_empty_handler
def get_market_price_change_by_ticker(fromdate: str, todate: str, market: str="KOSPI", adjusted: bool=True) -> DataFrame:
    """입력된 기간동안의 전 종목 수익률 반환

    Args:
        fromdate (str           ): 조회 시작 일자 (YYYYMMDD)
        todate   (str           ): 조회 종료 일자 (YYYYMMDD)
        market   (str , optional): 조회 시장 (KOSPI/KOSDAQ/ALL)
        adjusted (book, optional): 수정 종가 여부 (True/False)

    Returns:
        DataFrame:
    """
    market = {"ALL": "ALL", "KOSPI": "STK", "KOSDAQ": "KSQ", "KONEX": "KNX"}.\
        get(market, "ALL")
    adjusted = 2 if adjusted else 1

    df = 전종목등락률().fetch(fromdate, todate, market, adjusted)
    df = df[['ISU_ABBRV', 'ISU_SRT_CD', 'BAS_PRC', 'TDD_CLSPRC',
             'CMPPREVDD_PRC', 'FLUC_RT', 'ACC_TRDVOL', 'ACC_TRDVAL']]
    df.columns = ['종목명', '티커', '시가', '종가', '변동폭',
                  '등락률', '거래량', '거래대금']
    df = df.set_index('티커')

    df = df.replace(',', '', regex=True)
    df = df.astype({"시가": np.int32, "종가": np.int32,
                    "변동폭": np.int32, "등락률": np.float64,
                    "거래량": np.int64, "거래대금": np.int64})
    return df

def get_exhaustion_rates_of_foreign_investment_by_date(fromdate: str, todate: str, ticker: str) -> DataFrame:
    """[12023] 외국인보유량(개별종목) - 개별추이

    Args:
        fromdate (str): 조회 시작 일자 (YYYYMMDD)
        todate   (str): 조회 종료 일자 (YYYYMMDD)
        ticker   (str): 종목의 티커

    Returns:
        DataFrame:
                        상장주식수    보유수량    지분율    한도수량 한도소진율
            날짜
            2021-01-08  5969782550  3314966371  55.53125  5969782550   55.53125
            2021-01-11  5969782550  3324115988  55.68750  5969782550   55.68750
            2021-01-12  5969782550  3318676206  55.59375  5969782550   55.59375
            2021-01-13  5969782550  3316551070  55.56250  5969782550   55.56250
            2021-01-14  5969782550  3314652740  55.53125  5969782550   55.53125
    """
    isin = get_stock_ticker_isin(ticker)

    df = 외국인보유량_개별추이().fetch(fromdate, todate, isin)

    df = df[['TRD_DD', 'LIST_SHRS', 'FORN_HD_QTY', 'FORN_SHR_RT', 'FORN_ORD_LMT_QTY', 'FORN_LMT_EXHST_RT']]
    df.columns = ['날짜', '상장주식수', '보유수량', '지분율', '한도수량', '한도소진율']

    df = df.replace('/', '', regex=True)
    df = df.replace('', '0', regex=True)
    df = df.replace(',', '', regex=True)
    df = df.astype({"상장주식수": np.int64, "보유수량": np.int64, "지분율": np.float16,
                    "한도수량": np.int64, "한도소진율": np.float16})
    df = df.set_index('날짜')
    df.index = pd.to_datetime(df.index, format='%Y%m%d')
    return df.sort_index()


def get_exhaustion_rates_of_foreign_investment_by_ticker(date: str, market: str, balance_limit: bool) -> DataFrame:
    """[12023] 외국인보유량(개별종목) - 전종목

    Args:
        date          (str ): 조회 일자 (YYYYMMDD)
        market        (str ): 조회 시장 (KOSPI/KOSDAQ/ALL)
        balance_limit (bool): 외국인보유제한종목
            - 0 : check X
            - 1 : check O

    Returns:
        DataFrame:
                   상장주식수   보유수량     지분율   한도수량 한도소진율
            티커
            003490   94844634   12350096  13.023438   47412833  26.046875
            003495    1110794      29061   2.619141     555286   5.230469
            015760  641964077  127919592  19.937500  256785631  49.812500
            017670   80745711   28962369  35.875000   39565398  73.187500
            020560  223235294   13871465   6.210938  111595323  12.429688
    """
    market = {"ALL": "ALL", "KOSPI": "STK", "KOSDAQ": "KSQ", "KONEX": "KNX"}.get(market, "ALL")
    balance_limit = 1 if True else 0
    df = 외국인보유량_전종목().fetch(date, market, balance_limit)

    df = df[['ISU_SRT_CD', 'LIST_SHRS', 'FORN_HD_QTY', 'FORN_SHR_RT', 'FORN_ORD_LMT_QTY', 'FORN_LMT_EXHST_RT']]
    df.columns = ['티커', '상장주식수', '보유수량', '지분율', '한도수량', '한도소진율']
    df = df.replace('', '0', regex=True)
    df = df.replace(',', '', regex=True)
    df = df.astype({"상장주식수": np.int64, "보유수량": np.int64, "지분율": np.float16,
                    "한도수량": np.int64, "한도소진율": np.float16})
    df = df.set_index('티커')
    return df.sort_index()


@dataframe_empty_handler
def get_market_trading_value_and_volume_on_ticker_by_investor(fromdate: str, todate: str, ticker: str) -> DataFrame:
    """[12009] 투자자별 거래실적 기간합계(개별 종목)

    다음 메뉴의 내용을 스크래핑 함

    거래실적
         ㄴ 투자자별 거래실적(개별종목)
            http://data.krx.co.kr/contents/MDC/MDI/mdiLoader/index.cmd?menuId=MDC0201020302

    Args:
        fromdate (str ): 조회 시작 일자 (YYMMDD)
        todate   (str ): 조회 종료 일자 (YYMMDD)
        ticker   (str ): 조회 종목 티커

    Returns:
        DataFrame:

            >> get_market_trading_value_and_volume_on_ticker_by_investor("20210113", "20210120", "005930")

                         거래량                             거래대금
                           매도       매수    순매수            매도            매수         순매수
            투자자구분
            금융투자   31324444   28513421   2811023   2765702311200   2510494630400   255207680800
            보험        1790469     561307   1229162    158120209600     49570523900   108549685700
            투신        3966211    1486178   2480033    351753222200    130513380300   221239841900
            사모         756726     541912    214814     67202238800     47475872700    19726366100
            은행         105323      70598     34725      9360874400      6170507400     3190367000
    """
    isin = get_stock_ticker_isin(ticker)
    df = 투자자별_거래실적_개별종목_기간합계().fetch(fromdate, todate, isin)

    df = df.set_index('INVST_TP_NM')
    df.index.name = '투자자구분'
    df.columns = pd.MultiIndex.from_product([['거래량', '거래대금'], ['매도','매수', '순매수']])
    df = df.replace('[^-\w]', '', regex=True)
    df = df.replace('', '0')
    return df.astype(np.int64)


@dataframe_empty_handler
def get_market_trading_value_and_volume_on_market_by_investor(fromdate: str, todate: str, market: str, etf: bool=True,
                                                              etn: bool=True, elw: bool=True) -> DataFrame:
    """[12008] 투자자별 거래실적 기간합계

    다음 메뉴의 내용을 스크래핑 함

    거래실적
         ㄴ 투자자별 거래실적
            http://data.krx.co.kr/contents/MDC/MDI/mdiLoader/index.cmd?menuId=MDC0201020301

    Args:
        fromdate    (str ): 조회 시작 일자 (YYMMDD)
        todate      (str ): 조회 종료 일자 (YYMMDD)
        market      (str ): 조회 시장 (KOSPI/KOSDAQ/KONEX/ALL)
        etf         (bool): 시장 포함 여부
        etn         (bool): 시장 포함 여부
        elw         (bool): 시장 포함 여부

    Returns:
        DataFrame:

            >> get_market_trading_value_and_volume_on_market_by_investor("20210115", "20210122", "KOSPI", True, True)

                            거래량                                 거래대금
                              매도         매수     순매수             매도             매수         순매수
            투자자구분
            금융투자    1857447354   1660620713 -196826641   15985568261831   15006116511544  -979451750287
            보험          29594468     19872165   -9722303    1219035502445     757575677208  -461459825237
            투신          69348190     60601427   -8746763    2235561259511    1799363743367  -436197516144
            사모          31673292     26585281   -5088011     999084910863     846067212945  -153017697918
            은행          44279242     51690814    7411572     886226324790     936210985810    49984661020

            >> get_market_trading_value_and_volume_on_market_by_investor("20210115", "20210122", "KOSPI", True, True, True)

                            거래량                                 거래대금
                              매도         매수     순매수             매도             매수         순매수
            투자자구분
            금융투자    1857447354   1660620713 -196826641   15985568261831   15006116511544  -979451750287
            보험          29594468     19872165   -9722303    1219035502445     757575677208  -461459825237
            투신          69348190     60601427   -8746763    2235561259511    1799363743367  -436197516144
            사모          31673292     26585281   -5088011     999084910863     846067212945  -153017697918
            은행          44279242     51690814    7411572     886226324790     936210985810    49984661020
    """
    etf = "EF" if etf else ""
    etn = "EN" if etn else ""
    elw = "EW" if elw else ""
    market = {"ALL": "ALL", "KOSPI": "STK", "KOSDAQ": "KSQ", "KONEX": "KNX"}.get(market, "ALL")
    df = 투자자별_거래실적_전체시장_기간합계().fetch(fromdate, todate, market, etf, etn, elw)

    df = df.set_index('INVST_TP_NM')
    df.index.name = '투자자구분'
    df.columns = pd.MultiIndex.from_product([['거래량', '거래대금'], ['매도','매수', '순매수']])
    df = df.replace('[^-\w]', '', regex=True)
    df = df.replace('', '0')
    return df.astype(np.int64)


@dataframe_empty_handler
def get_market_trading_value_and_volume_on_market_by_date(fromdate: str, todate: str, market: str, etf: bool, etn: bool,
                                                          elw: bool, option_a: str, option_b: str, detail_view: bool) -> DataFrame:
    """[12008] 투자자별 거래실적

    Args:
        fromdate    (str ): 조회 시작 일자 (YYMMDD)
        todate      (str ): 조회 종료 일자 (YYMMDD)
        market      (str ): 조회 시장 (KOSPI/KOSDAQ/KONEX/ALL)
        etf         (bool): 시장 포함 여부
        etn         (bool): 시장 포함 여부
        elw         (bool): 시장 포함 여부
        option_a    (str ): 일별 추이 옵션 1 (거래량/거래대금)
        option_b    (str ): 일별 추이 옵션 2 (매수/매도/순매수)
        detail_view (bool): 상세조회 여부

    Returns:
        DataFrame:

                       TRD_DD     TRDVAL1     TRDVAL2        TRDVAL3      TRDVAL4     TRDVAL_TOT
                0  2021/01/22  67,656,491   6,020,990    927,119,399  110,426,104  1,111,222,984
                1  2021/01/21  69,180,642  13,051,423  1,168,810,381  109,023,034  1,360,065,480
    """
    etf = "EF" if etf else ""
    etn = "EN" if etn else ""
    elw = "EW" if elw else ""
    option_a = {"거래량": 1, "거래대금": 2}.get(option_a, 1)
    option_b = {"매도": 1, "매수": 2, "순매수": 3}.get(option_b, 3)
    market = {"ALL": "ALL", "KOSPI": "STK", "KOSDAQ": "KSQ", "KONEX": "KNX"}.get(market, "ALL")

    if detail_view:
        df = 투자자별_거래실적_전체시장_일별추이_상세().fetch(fromdate, todate, market, etf, etn, elw, option_a, option_b)
        df.columns = ['날짜', '금융투자', '보험', '투신', '사모', '은행', '기타금융', '연기금', '기타법인', '개인', '외국인',
            '기타외국인', '전체']
    else:
        df = 투자자별_거래실적_전체시장_일별추이_일반().fetch(fromdate, todate, market, etf, etn, elw, option_a, option_b)
        df.columns = ['날짜', '기관합계', '기타법인', '개인', '외국인합계', '전체']

    df = df.set_index('날짜')
    df.index = pd.to_datetime(df.index, format='%Y/%m/%d')
    df = df.replace('[^-\w]', '', regex=True)
    df = df.replace('', '0')
    df = df.astype(np.int64)
    return df.sort_index()


@dataframe_empty_handler
def get_market_trading_value_and_volume_on_ticker_by_date(fromdate: str, todate: str, ticker: str, option_a: str, option_b: str,
                                                          detail_view: bool) -> DataFrame:
    """[12008] 투자자별 거래실적

    Args:
        fromdate    (str ): 조회 시작 일자 (YYMMDD)
        todate      (str ): 조회 종료 일자 (YYMMDD)
        ticker      (str ): 조회 종목 티커
        option_a    (str ): 일별 추이 옵션 1 (거래량/거래대금)
        option_b    (str ): 일별 추이 옵션 2 (매수/매도/순매수)
        detail_view (bool): 상세조회 여부

    Returns:
        DataFrame:

                       TRD_DD     TRDVAL1     TRDVAL2        TRDVAL3      TRDVAL4     TRDVAL_TOT
                0  2021/01/22  67,656,491   6,020,990    927,119,399  110,426,104  1,111,222,984
                1  2021/01/21  69,180,642  13,051,423  1,168,810,381  109,023,034  1,360,065,480
    """
    isin = get_stock_ticker_isin(ticker)

    option_a = {"거래량": 1, "거래대금": 2}.get(option_a, 1)
    option_b = {"매도": 1, "매수": 2, "순매수": 3}.get(option_b, 3)

    if detail_view:
        df = 투자자별_거래실적_개별종목_일별추이_상세().fetch(fromdate, todate, isin, option_a, option_b)
        df.columns = ['날짜', '금융투자', '보험', '투신', '사모', '은행', '기타금융', '연기금', '기타법인', '개인', '외국인',
            '기타외국인', '전체']
    else:
        df = 투자자별_거래실적_개별종목_일별추이_일반().fetch(fromdate, todate, isin, option_a, option_b)
        df.columns = ['날짜', '기관합계', '기타법인', '개인', '외국인합계', '전체']

    df = df.set_index('날짜')
    df.index = pd.to_datetime(df.index, format='%Y/%m/%d')
    df = df.replace('[^-\w]', '', regex=True)
    df = df.replace('', '0')
    df = df.astype(np.int64)
    return df.sort_index()


@dataframe_empty_handler
def get_market_net_purchases_of_equities_by_ticker(fromdate: str, todate: str, market: str, investor: str) -> DataFrame:
    """[12010] 투자자별 순매수상위종목

    Args:
        fromdate (str): 조회 시작 일자 (YYYYMMDD)
        todate   (str): 조회 종료 일자 (YYYYMMDD)
        market   (str): 조회 시장 (KOSPI/KOSDAQ/KONEX/ALL)
        investor (str): 투자자
             - 1000 - 금융투자
             - 2000 - 보험
             - 3000 - 투신
             - 3100 - 사모
             - 4000 - 은행
             - 5000 - 기타금융
             - 6000 - 연기금
             - 7050 - 기관합계
             - 7100 - 기타법인
             - 8000 - 개인
             - 9000 - 외국인
             - 9001 - 기타외국인
             - 9999 - 전체

    Returns:
        DataFrame:
                       종목명  매도거래량  매수거래량  순매수거래량  매도거래대금  매수거래대금  순매수거래대금
            티커
            034730         SK     1581633     1767494        185861  448072973000  511094137000     63021164000
            010130   고려아연      188718      296707        107989   79480106000  126281029000     46800923000
            039490   키움증권      374940      715079        340139   53685623500   99770954000     46085330500
            011070   LG이노텍      743878      929876        185998  137990915000  173082664000     35091749000
            352820     빅히트      247298      442325        195027   39722470000   73131351500     33408881500
    """
    market = {"ALL": "ALL", "KOSPI": "STK", "KOSDAQ": "KSQ", "KONEX": "KNX"}.get(market, "ALL")
    investor = {"금융투자": 1000, "보험": 2000, "투신": 3000, "사모": 3100, "은행": 4000,
                "기타금융": 5000, "연기금": 6000, "기관": 7050, "기타법인": 7100,
                "개인": 8000, "외국인": 9000, "기타외국인": 9001, "전체": 9999}.get(investor, "9999")

    df = 투자자별_순매수상위종목().fetch(fromdate, todate, market, investor)

    df.columns = ['티커', '종목명', '매도거래량', '매수거래량', '순매수거래량', '매도거래대금', '매수거래대금', '순매수거래대금']
    df = df.replace('/', '', regex=True)
    df = df.replace(',', '', regex=True)
    df = df.astype(
        {'티커': str, '종목명': str, '매수거래량': np.int32, '매도거래량': np.int32,
         '순매수거래량': np.int32, '매수거래대금': np.int64, '매도거래대금': np.int64,
         '순매수거래대금': np.int64})
    df['티커'] = df['티커'].apply(lambda x: x.zfill(6))
    return df.set_index('티커')


# ------------------------------------------------------------------------------------------
# index
@dataframe_empty_handler
def get_index_ohlcv_by_date(fromdate: str, todate: str, ticker: str) -> DataFrame:
    """일자별 특정 지수의 OHLCV

    Args:
        fromdate (str): 조회 시작 일자 (YYYYMMDD)
        todate   (str): 조회 종료 일자 (YYYYMMDD)
        ticker   (str): 인덱스 ticker

    Returns:
        DataFrame:
                              시가        고가        저가        종가     거래량       거래대금
            날짜
            2019-04-12  765.599976  769.090027  762.989990  767.849976  926529303  4342635071383
            2019-04-11  762.150024  766.559998  762.130005  766.489990  760873641  4329711935026
            2019-04-10  755.729980  760.150024  754.049988  760.150024  744528283  4692968086240
            2019-04-09  753.719971  756.919983  749.869995  756.809998  836573253  4701168278265
            2019-04-08  755.320007  756.159973  750.020020  751.919983  762374091  4321665707119
    """

    df = 개별지수시세().fetch(ticker[1:], ticker[0], fromdate, todate)
    df = df[['TRD_DD', 'OPNPRC_IDX', 'HGPRC_IDX', 'LWPRC_IDX',
             'CLSPRC_IDX', 'ACC_TRDVOL', 'ACC_TRDVAL']]
    df.columns = ['날짜', '시가', '고가', '저가', '종가', '거래량', '거래대금']
    df = df.replace(',', '', regex=True)
    df = df.replace('', '0', regex=True)
    df = df.replace('/', '', regex=True)
    df = df.set_index('날짜')
    df = df.astype({'시가': np.float32, '고가': np.float32,
                    '저가': np.float32, '종가': np.float32,
                    '거래량': np.int64, '거래대금': np.int64})
    df.index = pd.to_datetime(df.index, format='%Y%m%d')
    return df.sort_index()


@dataframe_empty_handler
def get_index_listing_date(계열구분: str="KOSPI") -> DataFrame:
    """[11004] 전체지수 기본정보

    Args:
        계열구분 (str, optional): KRX/KOSPI/KOSDAQ/테마

    Returns:
        DataFrame:
                                   기준시점    발표시점   기준지수  종목수
            지수명
            코스피               1980.01.04  1983.01.04      100.0       1
            코스피 200           1990.01.03  1994.06.15      100.0      28
            코스피 100           2000.01.04  2000.03.02     1000.0      34
            코스피 50            2000.01.04  2000.03.02     1000.0      35
            코스피 200 중소형주  2010.01.04  2015.07.13     1000.0     167
    """
    계열구분 = {"KRX": "01", "KOSPI": "02", "KOSDAQ": "03", "테마": "04"}[계열구분]
    df = 전체지수기본정보().fetch(계열구분)
    df = df[['IDX_NM', 'BAS_TM_CONTN', 'ANNC_TM_CONTN', 'BAS_IDX_CONTN', 'IDX_IND_CD']]
    df.columns = ['지수명', '기준시점', '발표시점', '기준지수', '종목수']
    df = df.set_index('지수명')
    df = df.replace(',', '', regex=True)
    df = df.replace('', 0)
    df = df.astype({"기준지수": np.float16, "종목수": np.int16}, )
    return df


@dataframe_empty_handler
def get_index_price_change_by_ticker(fromdate: str, todate: str, market: str) -> DataFrame:
    """지정된 기간 동안의 전종목 OHLCV

    Args:
        fromdate (str): 조회 시작 일자 (YYYYMMDD)
        todate   (str): 조회 종료 일자 (YYYYMMDD)
        market   (str): 검색 시장 (KRX/KOSPI/KOSDAQ/테마)

    Returns:
        DataFrame:
                                                   시가          종가     등락률       거래량        거래대금
            지수명
            코스닥                           696.500000    724.500000   4.050781  10488319776  62986196230829
            코스닥 150                      1065.000000   1103.000000   3.490234    729479528  18619100922088
            코스닥 150 정보기술              603.500000    631.500000   4.648438    268338653   5203201290465
            코스닥 150 헬스케어             3450.000000   3532.000000   2.369141    135927364   7874689575610
            코스닥 150 커뮤니케이션서비스   2037.000000   2090.000000   2.599609     25001250    816778277690
    """
    market = {"KRX": "01", "KOSPI": "02", "KOSDAQ": "03", "테마": "04"}.get(market, "02")
    df = 전체지수등락률().fetch(fromdate, todate, market)
    df = df[['IDX_IND_NM', 'OPN_DD_INDX', 'END_DD_INDX', 'FLUC_RT', 'ACC_TRDVOL', 'ACC_TRDVAL']]
    df.columns = ['지수명', '시가', '종가', '등락률', '거래량', '거래대금']
    df = df.set_index('지수명')
    df = df.replace(',', '', regex=True)
    df = df.replace('', 0)
    df = df.astype({"시가": np.float16, "종가": np.float16, "등락률": np.float16, "거래량": np.int64, "거래대금": np.int64})
    return df


# def _get_index_volume_by_date(df):
#     if 'stk' in df.columns:
#         sort_idx = ['tot', 'stk', 'sect', 'reit', 'fm', 'rpt_mass', 'mktd_mass', 'mktd_bsk',
#                     'mktd_dkpl', 'tme_end_pr', 'tme_mass', 'tme_bsk', 'tme_unit', 'tme_dkpl',
#                     'bz_termnl_ask', 'cable_termnl_ask', 'wrls_termnl_ask', 'hts_ask', 'etc_ask',
#                     'bz_termnl_bid', 'cable_termnl_bid', 'wrls_termnl_bid', 'hts_bid', 'etc_bid']
#         category = ['전체', '종류', '종류', '종류', '세션', '세션', '세션', '세션', '세션', '세션', '세션',
#                     '세션', '세션', '세션', '매도', '매도', '매도', '매도', '매도', '매수', '매수', '매수', '매수',
#                     '매수', ]

#         columns = ['전체', '주권', '투자회사', '부동산투자회사', '정규매매', '정규신고대량', '장중대량', '장중바스켓', '장중경쟁대량',
#                    '시간외종가', '시간외대량', '시간외바스켓', '시간외단일가', '시간외경쟁대량', '영업단말', '유선단말', '무선단말', 'HTS',
#                    '기타', '영업단말', '유선단말', '무선단말', 'HTS', '기타']

#     else:
#         sort_idx = ['tot', 'fm', 'rpt_mass', 'mktd_mass', 'mktd_bsk',
#                     'mktd_dkpl', 'tme_end_pr', 'tme_mass', 'tme_bsk', 'tme_unit', 'tme_dkpl',
#                     'bz_termnl_ask', 'cable_termnl_ask', 'wrls_termnl_ask', 'hts_ask', 'etc_ask',
#                     'bz_termnl_bid', 'cable_termnl_bid', 'wrls_termnl_bid', 'hts_bid', 'etc_bid']

#         category = ['전체', '세션', '세션', '세션', '세션', '세션', '세션', '세션',
#                     '세션', '세션', '세션', '매도', '매도', '매도', '매도', '매도', '매수', '매수', '매수', '매수',
#                     '매수', ]

#         columns = ['전체', '정규매매', '정규신고대량', '장중대량', '장중바스켓', '장중경쟁대량',
#                    '시간외종가', '시간외대량', '시간외바스켓', '시간외단일가', '시간외경쟁대량', '영업단말', '유선단말', '무선단말', 'HTS',
#                    '기타', '영업단말', '유선단말', '무선단말', 'HTS', '기타']

#     df = df.set_index('dt')
#     df.index.name = "날짜"
#     df = df[sort_idx]
#     df.columns = pd.MultiIndex.from_tuples(list(zip(category, columns)))

#     df = df.replace(',', '', regex=True)
#     df = df.replace('', 0)
#     df = df.astype(np.int64)
#     df.index = pd.to_datetime(df.index, format='%Y/%m/%d')
#     return df


@dataframe_empty_handler
def get_index_portfolio_deposit_file(date: str, ticker: str) -> list:
    """지수구성종목을 리스트로 반환

    Args:
        date   (str): 조회 일자 (YYMMDD)
        ticker (str): 인덱스 ticker

    Returns:
        list:

    """
    df = 지수구성종목().fetch(date, ticker[1:], ticker[0])
    print(df.columns)
    return df['ISU_SRT_CD'].tolist()


# ------------------------------------------------------------------------------------------
# shorting
@dataframe_empty_handler
def get_shorting_status_by_date(fromdate, todate, ticker):
    """일자별 공매도 종합 현황
    :param fromdate: 조회 시작 일자   (YYYYMMDD)
    :param todate  : 조회 종료 일자 (YYYYMMDD)
    :param ticker  : 종목 번호
    :return        : 종합 현황 DataFrame
                  공매도    잔고   공매도금액     잔고금액
        날짜
        20180105   41726  177954   3303209900  14111752200
        20180108   32411  167754   2528196100  13118362800
        20180109   50486  175261   3885385100  13477570900
    """
    isin = get_stock_ticker_isin(ticker)
    df = 개별종목_공매도_종합정보().fetch(fromdate, todate, isin)

    df.columns = ['날짜', '거래량', '잔고수량', '거래대금', '잔고금액']
    df = df.set_index('날짜')
    df.index = pd.to_datetime(df.index, format='%Y/%m/%d')

    # '-'는 데이터가 집계되지 않은 것을 의미한다.
    # 최근 2일 간의 데이터 ([:2])에서 '-'가 하나는 행의 갯수를 계산함
    idx = (df.iloc[:2] == '-').any(axis=1).sum()
    df = df.iloc[idx:]

    df = df.replace('\D', '', regex=True)
    df = df.replace('', 0)
    df = df.astype({"거래량": np.int32, "잔고수량": np.int32,
                    "거래대금": np.int64, "잔고금액": np.int64})
    return df.sort_index()


@dataframe_empty_handler
def get_shorting_volume_by_date(fromdate, todate, isin, market):
    """종목별 공매도 거래 현황 조회
    :param date: 조회 일자 (YYYYMMDD)
    :param market  : 코스피/코스닥
    :return        : 거래 현황 DataFrame
                       종목명   수량  거래량   비중
        000020       동화약품    454  196429   0.23
        000030       우리은행      0       0   0.00
        000040       KR모터스     69  175740   0.04
        000042   KR모터스 1WR      0    2795   0.00
        000050           경방    264   39956   0.66
    """
    market = {"KOSPI": 1, "KOSDAQ": 3, "KONEX": 6}.get(market, 1)
    df = SRT02020100().fetch(fromdate, todate, market, isin)

    df = df[['일자', '공매도거래량', '총거래량', '비중', '공매도거래대금']]
    df = df.replace('/', '', regex=True)
    df = df.replace(',', '', regex=True)
    df = df.set_index('일자')
    df = df.astype({"공매도거래량": np.int64, "총거래량": np.int64,
                    "공매도거래대금": np.int64, "비중": np.float64})
    return df.sort_index()


@dataframe_empty_handler
def get_shorting_volume_by_ticker(date, market="코스피"):
    """종목별 공매도 거래 현황 조회
    :param date: 조회 일자 (YYYYMMDD)
    :param market  : 코스피/코스닥
    :return        : 거래 현황 DataFrame
                       종목명   수량  거래량   비중
        000020       동화약품    454  196429   0.23
        000030       우리은행      0       0   0.00
        000040       KR모터스     69  175740   0.04
        000042   KR모터스 1WR      0    2795   0.00
        000050           경방    264   39956   0.66
    """
    market = {"KOSPI": 1, "KOSDAQ": 3, "KONEX": 6}.get(market, 1)
    df = SRT02020100().fetch(date, date, market, "")

    df = df[['종목코드', '공매도거래량', '총거래량', '비중', '공매도거래대금']]
    df = df.replace('/', '', regex=True)
    df = df.replace(',', '', regex=True)
    df = df.set_index('종목코드')
    df.index = df.index.str[3:9]
    df = df.astype({"공매도거래량": np.int64, "총거래량": np.int64,
                    "공매도거래대금": np.int64, "비중": np.float64})
    return df


@dataframe_empty_handler
def get_shorting_investor_by_date(fromdate, todate, market, inquery="거래량"):
    """투자자별 공매도 거래 현황
    :param fromdate: 조회 시작 일자   (YYYYMMDD)
    :param todate  : 조회 종료 일자 (YYYYMMDD)
    :param market  : 코스피/코스닥
    :param inquery : 거래량 / 거래대금
    :return        : 거래 현황 DataFrame
                     기관   개인   외국인   기타      합계
        날짜
        20180119  1161522  37396  6821963      0   8020881
        20180118   970406  41242  8018997  13141   9043786
        20180117  1190006  28327  8274090   6465   9498888
    """
    market = {"KOSPI": 1, "KOSDAQ": 2, "KONEX": 6}.get(market, 1)
    inquery = {"거래량": 1, "거래대금": 2}.get(inquery, 1)

    df = SRT02020300().fetch(fromdate, todate, market, inquery)

    df = df[
        ['str_const_val1', 'str_const_val2', 'str_const_val3', 'str_const_val4',
         'str_const_val5', 'trd_dd']]
    df.columns = ['기관', '개인', '외국인', '기타', '합계', '날짜']

    df = df.replace('/', '', regex=True)
    df = df.set_index('날짜')
    df = df.replace(',', '', regex=True).astype(np.int64)
    df.index = pd.to_datetime(df.index, format='%Y%m%d')
    return df.sort_index()


@dataframe_empty_handler
def get_shorting_volume_top50(date, market="코스피"):
    """공매도 거래 비중 TOP 50
    :param date    : 조회 일자   (YYYYMMDD)
    :param market  : 코스피/코스닥/코넥스
    :return        : 거래 비중 DataFrame
                        순위 공매도거래대금 총거래대금 공매도비중 직전40일거래대금평균 공매도거래대금증가율 직전40일공매도평균비중 공매도비중증가율  주가수익률
        아모레퍼시픽      1  15217530000  35660149500  42.674   7945445875       1.915        14.834     2.877  0.334
        영원무역홀딩스    2     69700600    176886900  39.404     20449658       3.408         9.251     4.259  2.698
        한샘              3   9034795500  27690715500  32.628   2131924250       4.238        21.142     1.543 -5.233
        동서              4    701247550   2444863350  28.682    255763771       2.742        10.172     2.820 -0.530
    """
    market = {"KOSPI": 1, "KOSDAQ": 3, "KONEX": 6}.get(market, 1)
    df = SRT02020400().fetch(date, market)

    df = df[['isu_abbrv', 'rank', 'cvsrtsell_trdval', 'acc_trdval',
             'tdd_srtsell_wt',
             'srtsell_trdval_avg', 'tdd_srtsell_trdval_incdec_rt',
             'valu_pd_avg_srtsell_wt', 'srtsell_rto',
             'prc_yd']]
    df.columns = ['종목명', '순위', '공매도거래대금', '총거래대금', '공매도비중', '직전40일거래대금평균',
                  '공매도거래대금증가율', '직전40일공매도평균비중', '공매도비중증가율', '주가수익률']
    df = df.set_index('종목명')

    df = df.replace(',', '', regex=True)
    df = df.replace(r'^\s*$', 0, regex=True)

    df = df.astype({"순위": np.int32, "공매도거래대금": np.int64, "총거래대금": np.int64,
                    "직전40일거래대금평균": np.int64, "공매도비중": np.float64,
                    "공매도거래대금증가율": np.float64,
                    "직전40일공매도평균비중": np.float64, "공매도비중증가율": np.float64,
                    "주가수익률": np.float64})
    return df


@dataframe_empty_handler
def get_shorting_balance_by_date(fromdate, todate, isin, market="KOSPI"):
    """종목별 공매도 잔고 현황
    :param fromdate: 조회 시작 일자   (YYYYMMDD)
    :param todate  : 조회 종료 일자 (YYYYMMDD)
    :param ticker  : 종목 번호
    :param market  : KOSPI/KOSDAQ
    :return        : 잔고 현황 DataFrame
                      공매도잔고  상장주식수   공매도금액        시가총액  비중
        2018/01/15        164825   728002365  11982777500  52925771935500  0.02
        2018/01/12        167043   728002365  12427999200  54163375956000  0.02
        2018/01/11        183158   728002365  13297270800  52852971699000  0.02
        2018/01/10        200200   728002365  14594580000  53071372408500  0.03
    """
    market = {"KOSPI": 1, "KOSDAQ": 3, "KONEX": 6}.get(market, 1)
    df = SRT02030100().fetch(fromdate, todate, market, isin)

    df = df[['공시의무발생일', '공매도잔고수량', '상장주식수', '공매도잔고금액', '시가총액', '비중']]
    df.columns = ['날짜', '공매도잔고', '상장주식수', '공매도금액', '시가총액', '비중']

    df = df.replace('/', '', regex=True)
    df = df.replace(',', '', regex=True)
    df = df.set_index('날짜')
    df = df.astype({"공매도잔고": np.int32, "상장주식수": np.int64, "공매도금액": np.int64,
                    "시가총액": np.int64, "비중": np.float64})
    df.index = pd.to_datetime(df.index, format='%Y/%m/%d')
    return df.sort_index()


@dataframe_empty_handler
def get_shorting_balance_top50(date, market="KOSPI"):
    """종목별 공매도 잔고 TOP 50
    :param date    : 조회 일자   (YYYYMMDD)
    :param market  : KOSPI/KOSDAQ
    :return        : 잔고 현황 DataFrame
                       종목명    잔고수량  상장주식수      잔고금액        시가총액   비중
        009150        삼성전기   10074742   74693696  1077997394000   7992225472000  13.49
        042670   두산인프라코어  21415517  208158077   182674360010   1775588396810  10.29
        068270        셀트리온   11826917  125456133  2548700613500  27035796661500   9.43
        008770        호텔신라    3085595   39248121   223397078000   2841563960400   7.86
        001820       삼화콘덴서    617652   10395000    39220902000    660082500000   5.94
    """
    market = {"KOSPI": 1, "KOSDAQ": 2, "KONEX": 6}.get(market, 1)
    df = SRT02030400().fetch(date, market)

    df = df[["isu_cd", 'isu_abbrv', 'rank', 'bal_qty', 'list_shrs', 'bal_amt',
             'mktcap', 'bal_rto']]
    df.columns = ['티커', '종목명', '순위', '잔고수량', '주식수', '잔고금액', '시가총액', '비중']
    df['티커'] = df.티커.str[3:9]
    df = df.set_index('티커')

    df = df.replace(',', '', regex=True)
    df = df.astype(
        {"잔고수량": np.int32, "주식수": np.int64, "잔고금액": np.int64, "시가총액": np.int64,
         "비중": np.float64})
    return df


if __name__ == "__main__":
    pd.set_option('display.expand_frame_repr', False)
    # print(get_shorting_status_by_date("20201222", "20210122", "005930"))
    print(get_market_ohlcv_by_date("20150720", "20150810", "005930"))