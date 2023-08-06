Library สำหรับประมวลข้อมูลตลาดหุ้นไทย Stock Exchange of Thailand https://www.set.or.th และการจัดการ Portfolio

พื้นฐานที่ต้องการ

    $ conda install -c conda-forge matplotlib

จาก https://anaconda.org/conda-forge/matplotlib


การติดตั้ง

    $ pip install starfishX  หรือ  $ pip install starfishX --upgrade

หรือ

    $ pip3 install starfishX --upgrade

Quantitative 
- sx.loadHistData(str|list,start="2018-01-01",end="2018-12-31") ``end ถ้าไม่ใส่คือวันที่ล่าสุด``
- df,k = sx.MonthlyReturn([str],"2016-01-01")
- sx.linregressIndicator(basket,periodDay) ``int periodDay`` จำนวนวันล่าสุดที่จะใช้ใน Linear least-squares regression
- sx.getNVDRVolume ดึงข้อมูลปริมาณการซื้อขายของ NVDR

ข้อมูลงบการเงินและข้อมูลตลาด
- sx.commonsizeBS(str)
- sx.commonsizeIS(str)
- sx.getFinanceRatio(str|list) 
  ``str,list`` ส่งค่าเป็น str จะ return ค่าย้อนหลังได้หลายปี หากส่งค่าเป็น array list จะ return แบบเปรียบเทียบ
  
- sx.spiderCompare([str1,str2]) 
  ``ใช้คู่กับ sx.getFinanceRatio และ list ความยาว 2 เท่านั้น``
  
- sx.getIncomeStatement(str)
- sx.getIncomeStatementCompare(list)
- sx.getBalanceSheet(str)
- sx.getBalanceSheetCompare(list)
- sx.getMemberOfIndex("set50") 
  ``SET50,SET100,sSET,SETCLMV,SETHD,SETTHSI,SETWB``
  
- sx.listStockInSector("kbank") 
  ``สุ่มอะไรก็ได้ในกลุ่มอุตสาหกรรมนั้นๆ``
  
- sx.getFundamentalInSector("kbank") 
  ``สุ่มอะไรก็ได้ในกลุ่มอุตสาหกรรมนั้นๆ``
- sx.findCASH("aot")
- sx.listShareholders(str|list,csv="file.csv") 
  ``csv สำหรับบันทึกข้อมูลเป็น csv``
- sx.listSecurities()
- sx.findMarketCap(str|list)
- sx.DuPontROE(str,int,firstLine=False)
  ``str Symbol ของหุ้นรายตัว`` 
  ``int Year เป็นปีพ.ศ. เช่น 2562 หรือ 2561``
  ``firstLine True`` คือ SALE ใช้บรรทัดแรก แต่ถ้าเป็น False SALE จะใช้รายได้รวมทั้งหมด ถ้าไม่ใส่ปกติจะเป็น False

- sx.InterestBearingDebt(str) ``str Symbol ของหุ้นรายตัว`` ใช้หาหนี้ที่มีคาดว่ามีภาระดอกเบี้ย
- sx.DA(str) ``str Symbol `` ใช้หาค่าเสื่อมราคาและค่าตัดจำหน่าย

- sx.morningstarGetfn(str,Indicates=sx.MStar) ดึงค่าปัจจัยพื้นฐานจาก morningstar 
  ``str Symbol ของหุ้นรายตัว``
  ``sx.MStar`` คือ ตัวคัดกรองที่ต้องการ เช่น ปันผลใช้ sx.MStar.Dividends , รายได้ใช้ sx.MStar.Revenue เป็นต้น
  จาก Cr.http://financials.morningstar.com

- sx.marketview(indexMarket,start=year) 
  ``str year ใช้ปีค.ศ. เช่น 2010-01-01 YYYY-MM-DD``
  ``indexMarket Class เช่น sx.indexMarket.SET50``

- rp = sx.marketViewForeignTrade(indexMarket,start="2016-01-01") 
  ``indexMarket ของต่างชาติซื้อขายมีเพียง SET และ mai เท่านั้น`` ``str year ใช้ปีค.ศ. เช่น 2010-01-01 YYYY-MM-DD``

- sx.AnomalyDetectionVolume(DataSet,contamination=0.01,viewplot=True) 
  ``DataSet เป็น DataFrame ของปริมาณการซื้อขาย`` ``contamination ส่วนของสิ่งผิดปกติใน DataSet ``

ประเมินมูลค่าหุ้น
- sx.getEVEBITDA(symbol,year) ``int Year เป็นปีพ.ศ. เช่น 2562 หรือ 2561 ``
- sx.analyseEVEBITDA(basket,yearstart,yearend) ``วิเคราะห์คุณภาพ EV/EBITDA``
- sx.DividendDiscountModel(symbol,year,k) 
  ``int Year เป็นปีพ.ศ. เช่น 2562 หรือ 2561 ``
  ``k อัตราผลตอบแทนที่คาดหวัง``

- sx.thaibma(year,bondtype=sx.BondType.ThaiGovernmentBond10Year) 
``strFormat ใช้ค.ศ. เช่น 2019-06-10 YYYY-MM-DD``
Cr.http://www.thaibma.or.th

- sx.thaibma_series(year,bondtype=sx.BondType.ThaiGovernmentBond10Year) 

- sx.beta(str) ``str Symbol ``

- sx.EarningYieldGap(indexMarket,bondtype,start=year) ``str year ใช้ปีค.ศ. เช่น 2010-01-01 YYYY-MM-DD``

Optimization
- sx.MarkowitzProcess(df,alias=symbols,random=5000)

ดึงวันหยุดของตลาด (วันหยุดตามประเพณีของสถาบันการเงิน)
- df = sx.getHolidayMarket('2021') ``int Year เป็นปีค.ศ. เช่น 2010-01-01 YYYY-MM-DD ``

สถิติข้อมูล IPO ของหุ้น ราคา IPO /ข้อมูล ณ วันแรกที่ซื้อขาย / บริษัทที่ปรึกษาทางการเงิน
- df = sx.ipoStat(start,end) ``int start,end เป็นปีค.ศ. เช่น 2020 ``

ดึงราคา Warrant หรือใบสําคัญแสดงสิทธิ symbol : string เช่น mint-w7,jmart-w4
- df = sx.getWarrant('mint-w7')

ตัวอย่าง Data Type และอื่นๆ
- list เช่น ["aot","ptt"]
- str เช่น "aot" 
- sx.checkServices() เป็นการตรวจสอบการทำงานของ Server โดยภาพรวมว่า function ยังทำงานโดยปกติไหม

ตัวอย่างการใช้งาน

    import starfishX as sx

    print(sx.__version__)

    sx.getBalanceSheet("aot")

ตัวอย่างการใช้งาน

    import starfishX as sx

    symbol = ["aot","ptt"]

    df = sx.loadHistData(symbol,start="2018-01-01")

ตัวอย่างการใช้งาน

    import starfishX as sx

    symbols = ["ptt","cpf","mint","aav"]

    df = sx.loadHistData(symbols,start="2018-01-01")

    sx.MarkowitzProcess(df,alias=symbols,random=5000)


ค้นหาหุ้นตามแนวทางของ Peter Lynch โดยใช้เนื้อหาจากหนังสือ “เหนือกว่าวอลสตรีท One Up On Wall Street” สร้างเป็น Package เสริมโดยใช้ฟังก์ชั่นพื้นฐานจาก starfishX

    import starfishX.peterlynch as pl 

- อัตราการเติบโตของกำไรเป็นอย่างไร
- P/E อุตสาหกรรม และ P/E บริษัทที่คล้ายกัน
- P/E ต่ออัตราการเติบโตของกำไร
- P/E ย้อนหลัง 10 ปี
- นักวิเคราะห์สนใจหุ้นเราไหม
- บริษัทมีข่าวการซื้อหุ้นคืนบ้างหรือเปล่า
- เปอร์เซ็นต์การถือหุ้นของสถาบัน
- มีบุคคลภายในกำลังซื้อหุ้นของบริษัทบ้างไหม ตรวจสอบรายงาน 59-2 และรายงาน 246-2
- โครงสร้างหนี้เป็นอย่างไร
- มีงบดุลที่แข็งแกร่งขนาดไหน
- เงินสดต่อหุ้นเป็นยังไงบ้าง
- อัตราการปันผลสม่ำเสมอหรือเปล่า
- อัตรา Payout เป็นอย่างไรบ้าง
- กระแสเงินสดอิสระ Free Cash Flow เป็นยังไง
- หาบริษัทที่ยอดเยี่ยมในอุตสาหกรรมที่ยอดแย่
- สัญญานหนึ่งของการเพื่องฟู
- หุ้นทรัพย์สินมาก ประยุกต์ใช้เทคนิค Sum Of The Part
- การคัดกรอง หุ้นโตช้า ,หุ้นแข็งแกร่ง ,หุ้นโตเร็ว ตามอัตราการเติบโต

Historical Volatility

    import starfishX.volatility as vol

    from starfishX.volatility.vol import TypeVol as tv

    df = sx.loadHistData("JMART",OHLC=True,start="2020-01-01") 

    N = 30 #sma 

    vol.historicalVolatility(df,N,tv.hvCloseToClose)
    
    vol.historicalVolatility(df,N,tv.hvParkinson)

starfishX.volatility ตอนนี้ก็จะมี 6 ฟังก์ชัน
- 1.Close To Close
- 2.Parkinson  (High-Low)
- 3.Garman-Klass (Open-High-Low-Close)
- 4.Rogers-Satchell  (Open-High-Low-Close + จัดการราคาที่ไม่เปลี่ยนแปลงได้)
- 5.GARMAN-KLASS YANG-ZHANG EXTENSION (Open-High-Low-Close + จัดการราคาที่มีการเปิดกระโดดได้)
- 6.Yang-Zhang (Open-High-Low-Close + จัดการราคาที่ไม่เปลี่ยนแปลงได้ + จัดการราคาที่มีการเปิดกระโดดได้)

ติดต่อฉัน แจ้ง BUG แจ้ง Error ได้ที่

 Facebook : https://www.facebook.com/Superstarman-1464755373546185/

 Email    : tapattan@จีเมล์ดอทคอม