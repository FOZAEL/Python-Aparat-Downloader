from os import chdir
from os import getcwd
from sys import argv
from urllib.parse import urlparse
from bs4 import BeautifulSoup
from download import download
import requests

chdir(getcwd()+"/")
print("Directory: "+getcwd()+"/")

# Extract download links
def mylinks(Downlink,DException):
    mainpage=urlparse(Downlink)
    al0=BeautifulSoup(requests.get(Downlink).content,features="html.parser")
    newlist=[]
    for i in al0.find_all('a'):
        n=i.get("href")
        if None != n and DException in n:
            if list(n)[0] == '/':
                newlist.append("{}{}".format("{}://{}".format(mainpage[0],mainpage[1]),n))
            else:
                newlist.append(n)
    newlist.sort()
    na=al0.title.string;na=na.replace("\n","");na=na.replace("        ","")
    return newlist,na

# Extract playlist
def aparatPlayList(AparatUrl):
    li=BeautifulSoup(requests.get(AparatUrl).content,"html.parser").find_all('a')
    myli=[]
    for i in li:
        n=i.get('href')
        if None != n and "?" in n and list(n)[1]== 'v':
            myli.append("https://www.aparat.com{}".format(n).split("?")[0])
    # remove dublicated item
    myli = list(dict.fromkeys(myli))
    return myli

# get argument from user
if len(argv) == 3:
    PlayListLinks=(aparatPlayList(argv[1]))
    quality=argv[2]
else :
    print('(X)  Incorrect arguments\nEx: aparat https://aparat.com/YourAparatPlayListVideos 720p ')

# download
print("\nTotal Videos : "+str(len(PlayListLinks))+"")

for i in PlayListLinks:
    tmp=mylinks(i,quality)
    print("\n{}\n".format(tmp[1]))
    path = download(tmp[0][0], getcwd()+"/"+tmp[1]+".mp4")

