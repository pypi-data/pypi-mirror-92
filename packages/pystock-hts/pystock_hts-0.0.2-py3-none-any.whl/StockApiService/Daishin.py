
import sys, os
import win32com.client

class CpUtil():
    def __request(self, endpoint):
        return win32com.client.Dispatch("CpUtil."+str(endpoint))
    
    # 연결 상태 확인
    def getConnected(self):
        """
        1 (connected), 0 (disconnected) 의 값을 boolean 으로 return
        """
        res = self.__request("CpCybos").isConnect
        if res == 1:
            is_connected = True
        else:
            is_connected = False

        return is_connected

    # 전체 종목 수
    def getStockCount(self):
        """
        전체 종목 갯수 int로 return
        """
        res = self.__request('CpStockCode').GetCount()
        return res

    # 전체 종목 코드 리스트
    def getStockCodeList(self):
        """
        전체 종목 코드 리스트 return
        """
        res = self.__request('CpCodeMgr').GetStockListByMarket(1)
        return res

    # 종목코드에 대한 종목 이름 반환
    def getStockCodeToName(self, stock_code):
        """
        stock_code 에 대한 종목 이름을 str으로 return
        """
        res = self.__request('CpCodeMgr').CodeToName(stock_code)
        return res

    # 전체 종목에 대한 코드 (key), 이름 (value) 반환
    def getStockCodeAndNameAll(self):
        """
        전체 종목에 대한 코드와 이름을 dict 로 return
        """

        stock_code_list = self.getStockCodeList()
        stock_info_obj = {}
        for stock_code in stock_code_list:
            stock_name = self.getStockCodeToName(stock_code)
            stock_info_obj[stock_code] = stock_name
        return stock_info_obj


class CpSysDib():

    def getStockChartPriceToDate(self, date_count, stock_code):
        """
        stock_code 에 대한 chart return
        """
        stock_chart_list = []
        date_list = []
        fields = [5, 0]

        instStockChart = win32com.client.Dispatch("CpSysDib.StockChart")
        
        for field in fields:
            
            instStockChart.SetInputValue(0, stock_code) #종목코드
            instStockChart.SetInputValue(1, ord('2')) #1=기간, 2=갯수
            instStockChart.SetInputValue(4, date_count) #요청 갯수
            #요청 받을 필드값
            instStockChart.SetInputValue(5, field)
            #0: 날짜 / 1: 시간 / 2: 시가 / 3: 고가 / 4: 저가 / 5: 종가 / 8: 거래량 / 9: 거래대금
            instStockChart.SetInputValue(6, ord('D')) #차트 구분
            # D: 일 / W: 주 / M: 월 / m: 분 / T: 틱
            instStockChart.SetInputValue(9, ord('1'))
            instStockChart.Block__Request()

            data_count = instStockChart.GetHeaderValue(3)
                
            if stock_chart_list:
                for i in range(data_count):
                    year = str(instStockChart.GetDataValue(0, i))[0:4]
                    month = str(instStockChart.GetDataValue(0, i))[4:6]
                    day = str(instStockChart.GetDataValue(0, i))[6:]
                    date = f'{year}-{month}-{day}'
                    date_list.append(date)

            else:
                for i in range(data_count):
                    stock_chart_list.append(instStockChart.GetDataValue(0, i))

        return date_list, stock_chart_list


    def getStockPer(self, stock_code):
        """
        stock_code 에 대한 PER 지수 반환
        """
        instMarketEye = win32com.client.Dispatch("CpSysDib.StockUniMst")

        instMarketEye.SetInputValue(0, stock_code)
        instMarketEye.Block__Request()

        per = instMarketEye.GetHeaderValue(98)

        return per