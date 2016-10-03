import urllib.request
import urllib
import re

# class of the student grades
class StuAchi():
    """docstring for StuAchi"""
    def __init__(self):
        self.gradeUrl='http://zhjw.cic.tsinghua.edu.cn/cj.cjCjbAll.do?m=bks_cjdcx&cjdlx=yw'
        
        with open('grade_cookie.txt','r') as f:
            cookie=f.read()
        
        user_agent='Mozilla/5.0 (Windows NT 10.0; WOW64)'

        self.header={
        'Cookie':cookie,
        'User-Agent':user_agent 
        }

        self.course=[]
        self.credit=[]
        self.grade=[]

    #get the page of the web recording the grade
    def GetPage(self):
        request=urllib.request.Request(self.gradeUrl,headers=self.header)
        response=urllib.request.urlopen(request)

        if response:
            return response.read().decode('GBK')
            pass
        else:
            return None
        pass

    #get the list that recording the course, credit and grade
    def GetList(self,NowPage):
        self.course=[]
        self.credit=[]
        self.grade=[]
        pattern=re.compile('</tr>.*?<tr>.*?<td style="text-align:center;" height="30">.*?<td style="text-align:left;">(.*?)</td>.*?<td style="text-align:center;">(.*?)</td>.*?<td style="text-align:left;">(.*?)</td>',re.S)
        space_rm=re.compile('\s*')

        for item in re.finditer(pattern,NowPage):
            achi1=re.sub(space_rm,'',item.group(1))
            achi2=re.sub(space_rm,'',item.group(2))
            achi3=re.sub(space_rm,'',item.group(3))
            self.course.append(achi1)
            self.credit.append(achi2)
            self.grade.append(achi3)
            
        pass

    # print the list
    def PrintList(self):
        i=0
        print("%-60s  %-8s   %-8s"%('Course Title','Credit','Grade'))
        print('')
        print('-------------------------------------------------------------------------------------------------')
        for x in self.course:
            if len(x)>40:
                print('%-60s  %-8s   %-8s'%(x[:40],self.credit[i],self.grade[i]))
                print('%-60s  %-8s   %-8s'%(x[40:],'',''))
                print('-------------------------------------------------------------------------------------------------')
                pass
            else:
                print("%-60s  %-8s   %-8s"%(x,self.credit[i],self.grade[i]))
                print('-------------------------------------------------------------------------------------------------')
            i=i+1
            pass
        pass

    # get the total credit
    def GetTotalCredit(self):
        total_credit=0
        for x in self.credit:
            if int(x):
                total_credit=total_credit+int(x)
            pass
        return total_credit
        pass

    # get the average grade the the total course
    def GetAvGrade(self):
        actual_credit=0
        grade=0
        i=0
        for x in self.credit:
            try:
                grade=grade+int(self.grade[i])*int(x)
                actual_credit=actual_credit+int(x)
                pass
            except:
                pass
            i=i+1
            pass
        avgrade=float(grade)/float(actual_credit)
        return avgrade
        pass

# the main function
if __name__=='__main__':
    myStu=StuAchi()
    mypage=myStu.GetPage()
    myStu.GetList(mypage)
    myStu.PrintList()
    print('AvGrade: ',str(myStu.GetAvGrade()))
    print('Total_Credits: ',str(myStu.GetTotalCredit()))
    pass