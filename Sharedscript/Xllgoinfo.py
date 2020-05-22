import time,sys
from openpyxl import Workbook

class Xllgoinfo(object):
    '''
    新建结果报告
    '''
    def __init__(self,resultname="结果"):
        self.wb = Workbook()
        fname = time.strftime('%Y-%m-%d', time.gmtime())
        self.dest_filename = fname + '-%s.xlsx'% resultname
        self.ws = self.wb.active
        ws =self.ws
        ws.title = resultname
        time.sleep(0.02)

    def log_info(self,strings):
        wb = self.wb
        ws = self.ws
        ws.append(strings)
        filename = self.dest_filename
        #wb.save(str(sys.__path[0])+'\\'+ 'Result_file_xlsx' + '\\' +'%s' % filename)
        wb.save(sys.path[0]+ "\\Result_file_xlsx\\"+'%s' % filename)
        print((str(sys.path[0])+'\\'+ 'Result_file_xlsx' + '\\' +'%s' % filename))
        #print((str(sys.__path)))
        #(str(sys.__path[0]) + '\\' + 'Result_file' + '\\' + gettime)

if __name__ == '__main__':
    xinfo = Xllgoinfo("中国")
    strs = [1,2,3]
    xinfo.log_info(strs)