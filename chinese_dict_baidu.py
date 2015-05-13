#Python3 ONLY!
import urllib.request
from html.parser import HTMLParser
from xml.etree import ElementTree

from bs4 import BeautifulSoup


class DictHTML():
    def __init__(self):
        self.charset ='utf-8'
        self.html_doc =''
        
    def _getKeycode(self, key):   ##将汉字转为ASCII码，用于url搜索关键字。私有函数 turn Chinese characters to ASCII code
        key_ascii =''
        data = key.encode(self.charset)
        for i in data:
            temp = str(hex(i))
            key_ascii = key_ascii+temp.replace('0x','%',1)
        return key_ascii.upper()  #转大写  to upper

    def getHTML(self, key):
        
        key_ascii =self._getKeycode(key)
        url =r'http://dict.baidu.com/s?wd='+key_ascii
        header ={'User-Agent':'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.102 Safari/537.36'}
        #print(url)
            
        request =urllib.request.Request(url, None, header)
        response =urllib.request.urlopen(request)
        self.html_doc =response.read().decode(self.charset,'ignore')
        response.close()
        
        ##save as utf-8 encoding file
        ##保存为utf-8编码的文件
        
        f=open(r'C:\Users\Chi\Documents\中转站\output0.html','wb')
        html_u = self.html_doc.encode(self.charset,'ignore')
        f.write(html_u)
        print(':-)')
        f.close()
        return self.html_doc
    
class MySpider():
    def __init__(self):
        self.soup =None
        self.xml_doc =''
        
    ## 解析抓取的HTML，将结果保存为XML格式
    def spider(self,html_doc):
        soup =BeautifulSoup(html_doc)
        #截取div_pronounce块,获得查询关键字和拼音。
        pronounce_div =soup.find(id ='pronounce')
        key =pronounce_div.find('strong').string
        self.xml_doc ='\t<item name=\"'+key+'\">\n'
        pronounce0 =pronounce_div.find('b').string[1:-1]        #除去字符串第一和最后一个字符
        
        #截取div_cn_basicmean,获得发音(多音字有不同发音，单音字的发音使用div_pronounce块所截取的拼英)及其对应的意义
        cn_basicmean_div =soup.find(id ='cn-basicmean')
        cn_basicmean_pronounces =cn_basicmean_div.findAll('dl')
        for cn_basicmean_pronounce in cn_basicmean_pronounces:
            cn_pronounce =cn_basicmean_pronounce.find('dt')
            if(cn_pronounce ==None):        #单音字没有dt标签
                pronounce =pronounce0
            else:
                pronounce =cn_pronounce.string
                pronounce =pronounce[pronounce.find('[')+1: pronounce.find(']')]        #截取[...]之间的数据
            self.xml_doc +='\t\t<pronounce value=\"'+ pronounce +'\">\n'
            
            cn_basicmean_means =cn_basicmean_pronounce.findAll('li')        #获得对应发音的意义列表
            for cn_basicmean_mean in cn_basicmean_means:
                self.xml_doc +='\t\t\t<mean>\n'
                cn_basicmean_mean_ps =cn_basicmean_mean.findAll('p')        #分段问题
                for cn_basicmean_mean_p in cn_basicmean_mean_ps:
                    self.xml_doc +=('\t\t\t\t<p>'+ cn_basicmean_mean_p.string +'</p>\n')
                    #print(cn_basicmean_mean_p.string)
                self.xml_doc +='\t\t\t</mean>\n'
            self.xml_doc +='\t\t</pronounce>\n'
        self.xml_doc +='\t</item>\n'
                    
    def getxml(self):
        return(self.xml_doc)
    
    #解析XML文件，现实结果
    def printxml(self):
        count_mean=0
        flag_mean=0
        item =ElementTree.fromstring(self.xml_doc)   #得到root节点，即item
        #print(item.get('name'))
        #print('----------------------------')
        pronounces = item.getchildren()
        for pronounce in pronounces:
            print('【'+ pronounce.get('value') +'】')
            means =pronounce.getchildren()
            for mean in means:
                ps = mean.getchildren()
                count_mean +=1
                for p in ps:
                    if(flag_mean==0):
                        print(' %-3s%s'%(count_mean,p.text))
                        flag_mean=1
                    else:
                        print(' %-3s%s'%('',p.text))
                flag_mean =0
            count_mean =0
        

#__MAIN__
dictHTML =DictHTML()
spider =MySpider()
#key ='长'

while(1):
    print("\n输入汉字：")
    key =input()
    if(key =='0'):
        exit(0)
    html_doc =dictHTML.getHTML(key)
    spider.spider(html_doc)
    spider.printxml()
    

