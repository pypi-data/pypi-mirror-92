# About
This Python library can perform various calculations for scientific field.  
このPythonライブラリは科学分野の各種計算を行うことができます。
  
[Document](https://tanaka0079.github.io/libs/python/calc2/docs/html/index.html)   
[Pypl](https://pypi.org/project/calc2/)  
※Pyplで公開しているため、pipコマンドからインストールできます  

## Getting started
Install with `pip`.  
pipでインストールできます。

```
pip install calc2
```

## How to use, Sample code
introduce the main functions.
主な機能について紹介します。

### ①Parameter calculation for external short circuit test.外部短絡試験のパラメータ計算  
Calculate the configuration of the external short-circuit test equipment that satisfies the required test conditions (target voltage, target current).  
試験条件（目標電圧、目標電流）を満たす外部短絡試験装置の構成を計算します。  
●Document ●[Sample code](https://github.com/tanaka0079/libs/blob/master/python/calc2/examples/short_test/sample1.py
)  ●[Sample code（webアプリ版）](https://github.com/tanaka0079/libs/tree/master/python/calc2/examples/short_test_webapp)  

### ②Parameter calculation of three-phase AC circuit.三相交流回路のパラメータ計算
The parameters of the three-phase AC circuit can be calculated from the given conditions. For example, when "line voltage", "power consumption" and "power factor" are determined, "line current", "impedance" and "phase voltage" can be calculated.  
与えられた条件から三相交流回路の各パラメータを計算できます。例えば、「線間電圧」「消費電力」「力率」が決まっているとき、「線電流」「インピーダンス」「相電圧」を計算できます。  
●Document ●[Sample code](https://github.com/tanaka0079/libs/blob/master/python/calc2/examples/ac3_test/sample1.py)  


### ③Detailed analysis of pulse wave.パルス波の詳細解析  
Analyzes various parameters of pulse signals.  
パルス信号のさまざまなパラメーターを分析します。   
●Document ●[Sample code]()  

### ④Battery capacity measurement.電池の容量測定
Analyze the data obtained in the storage battery capacity measurement (discharge, charge, discharge).  
蓄電池の容量測定（捨て放電、充電、放電）で得られたデータを解析します。  
●Document ●[Sample code](
https://github.com/tanaka0079/libs/blob/master/python/calc2/examples/battery_capacity_ah/sample1.py
)  

## Source Code

●[Source Code](https://github.com/tanaka0079/libs/tree/master/python/calc2/calc2/electricity)
