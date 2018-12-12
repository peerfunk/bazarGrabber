import json, requests, pprint,re
import csv
try: 
    from BeautifulSoup import BeautifulSoup
except ImportError:
    from bs4 import BeautifulSoup


class BazarGetter:
    __baseUrl="http://www.bazar.at"
    __url="/niederoesterreich-haus-anzeigen,dir,1,cId,15,fc,3,loc,0,tp,0,pack,"
    __page=0
    __maxPages=0
    filename=""
    allEntries =[]
    def __init__(self,filename):
        self.filename= filename
    def getNextPage(self):
        if(self.__page > self.__maxPages):
            return None
        r= requests.get(self.__baseUrl + self.__url + str(self.__page)).text
        ret = re.search('<td class="last"><a href="'+self.__url+'(.*?)".*</td>',r)
        if(ret == None or ret.groups==0):
            self.__maxPages=0
        else:
            self.__maxPages=int(ret.group(1))
        parsed_html = BeautifulSoup(r)
        allp = parsed_html.body.find('ul', attrs = {'class': 'normal'})
        allentries= allp.findAll("li")
        for i in range(len(allentries)):
            district = allentries[i].find('div', attrs={"class":"district"})
            if district != None:
                self.allEntries.append(allentries[i])
        AllData = []
        for entry in self.allEntries:
            data = {}
            data["district"] = entry.find('div', attrs={"class":"district"}).text
            title = entry.find('div', attrs={"class":"title"})
            title.a["href"]
            data['URL'] = title.a["href"]
            data["title"] = title.text
            price = entry.find('span', attrs={"class": "result-list-item-link-price productPrice"})
            if price != None: price = price.text
            else: price= ""
            data["cost"] = re.sub("[^0123456789\.]","",price )

            
            size = entry.find('div', attrs={"class":"adDescription"})
            if size != None: size = size.text
            else: size= ""
            
            data["size"] = re.sub("[^0123456789\.]","", size)
            AllData.append(data)
        self.__page+=1
        return AllData
    def WriteToFile(self):
        counter = 0
        with open(self.filename, 'w' , newline='',encoding='utf-8') as csvfile:
            spamwriter = csv.writer(csvfile, delimiter=';')
            spamwriter.writerow(["id", "title", "totalArea", "primaryPrice", "district", "url"])
            page = self.getNextPage()
            while(page != None):
                for entry in page:
                    spamwriter.writerow([counter, format(entry['title'].encode("utf-8")) ,entry['size'],entry['cost'],entry['district'],entry['URL']])
                    counter+=1
                page = self.getNextPage()
                   
    
        
        
        

x = BazarGetter("bazar.csv")
x.WriteToFile()
        

