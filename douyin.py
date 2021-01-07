import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

class douyin:

    def videourl(self,max_cursor=0,link=dict()):
    	try:
    		#change this url link to your desired link make sure to replace max_cursor with +str(max_cursor)+
            url = "https://www.iesdouyin.com/web/api/v2/aweme/post/?sec_uid=MS4wLjABAAAA9Sh2pE1yxTu4Z1QVWYrU7Ihl3Q0uX2hTHwHJ_8E8oHCZf0-rL1SDzcCIydw7eO-f&count=21&"+str(max_cursor)+"=0&aid=1128&_signature=auOTMgAANRgyzTpna6Bb6mrjky&dytk="
            headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.2 Safari/605.1.15"}
            status = True
            while status:
                response = requests.get(url, headers=headers)
                data = response.json()
                if response.headers['content-type'] == "application/json; charset=utf-8":
                    for videos in data["aweme_list"]:
                        chrome_options = Options()
                        chrome_options.add_argument('--headless')
                        chrome_options.add_argument('--disable-gpu')
                        #change this to your chromedriver path making sure to download the chromedriver first 
                        path = "/Users/a/upload/chromedriver"
                        video_id = videos['aweme_id']
                        video_title = videos['desc']
                        video_url = 'https://www.iesdouyin.com/share/video/{}/?mid=1'
                        video_douyin = video_url.format(video_id)
                        driver = webdriver.Chrome(executable_path=path, options=chrome_options)
                        driver.get(video_douyin)
                        time.sleep(2)
                        url = driver.find_element_by_xpath('//*[@id="pageletReflowVideo"]/div/div[1]/div[1]/div[1]/video').get_attribute("src")
                        headers = {"user-agent":"Mozilla/5.0 (iPhone; CPU iPhone OS 9_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13B137 Safari/601.1"}
                        r = requests.get(url.replace("wm",""), allow_redirects=True,headers=headers)
                        #you can the path where you want to store.
                        with open(video_title+".mp4", 'wb') as f:
                            print("Downloading: ",video_title)
                            f.write(r.content)
                            f.close()
                        driver.close()
                        link[video_title]=url.replace("wm","")
                        max_cursor=data['max_cursor']
                        status=False
                    if max_cursor==0:
                        return link
                    else:
                        print(max_cursor)
                        self.videourl(max_cursor,link)
                         
    	except:
    		print("error")

if __name__ == '__main__':
     obj =douyin()
     print(obj.videourl())