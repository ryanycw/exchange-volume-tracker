import pandas as pd
from functools import reduce
import plotly.express as px
from plotly.subplots import make_subplots

FILES = ['documents/Binance1D.csv', 'documents/Coinbase1D.csv', 'documents/FTX1D.csv', 'documents/GateIO1D.csv', 'documents/Huobi1D.csv', 'documents/Kraken1D.csv', 'documents/KuCoin1D.csv', 'documents/OKX1D.csv']
FILES_NEW = ['documents/BINANCE_BTCUSDT, 1D_bdcef.csv',
             'documents/COINBASE_BTCUSD, 1D_2bb7b.csv',
             'documents/FTX_BTCUSDT, 1D_3e66d.csv',
             'documents/GATEIO_BTCUSDT, 1D_fbac9.csv',
             'documents/HUOBI_BTCUSDT, 1D_98f98.csv',
             'documents/KRAKEN_BTCUSD, 1D_4521a.csv',
             'documents/KUCOIN_BTCUSDT, 1D_09e4a.csv',
             'documents/OKX_BTCUSDT, 1D_3befa.csv']
FILES_RM_BN = ['documents/COINBASE_BTCUSD, 1D_2bb7b.csv',
             'documents/FTX_BTCUSDT, 1D_3e66d.csv',
             'documents/GATEIO_BTCUSDT, 1D_fbac9.csv',
             'documents/HUOBI_BTCUSDT, 1D_98f98.csv',
             'documents/KRAKEN_BTCUSD, 1D_4521a.csv',
             'documents/KUCOIN_BTCUSDT, 1D_09e4a.csv',
             'documents/OKX_BTCUSDT, 1D_3befa.csv']

def recordPreprocess(file):
    record = pd.read_csv(file)
    record = record.loc[::-1]
    record = record.reset_index(drop=True)
    record = record.loc[:89, ['time', '24H Volume']]
    record = record.loc[::-1]
    record = record.reset_index(drop=True)
    times = record['time'].str.split('T')
    times = [x[0] for x in times]
    record['time'] = times
    record.rename(columns = {'time':'time', '24H Volume':f"Volume_{file.split('/')[-1].split('.')[0]}"}, inplace = True)
    return record

def main():
    mergeFile = []
    for file in FILES_RM_BN:
        record = recordPreprocess(file)
        mergeFile.append(record)
    
    mergeFile = reduce(lambda left, right: pd.merge(left, right, on=['time'], how='outer'), mergeFile)
    fig = px.line(mergeFile, y=mergeFile.columns[1:])

    subfig = make_subplots(specs=[[{"secondary_y": True}]])

    subfig.add_traces(fig.data)
    subfig.layout.xaxis.title="Datetime"
    subfig.layout.yaxis.title="TVL"
    subfig.for_each_trace(lambda t: t.update(line=dict(color=t.marker.color)))
    subfig.show()
    print(mergeFile)

if __name__ == "__main__":
    main()