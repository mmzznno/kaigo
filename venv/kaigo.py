from time import sleep
from selenium.webdriver import Chrome, ChromeOptions
from webdriver_manager.chrome  import ChromeDriverManager
import pandas as pd

def scraping():
    #都道府県
    pre = input("都道府県名を入力してください")
    
    #判別
    if pre == "広島" :
        preno = 34
    else:
        pass
      
    #広島県
    driver_path = ChromeDriverManager().install()
    driver = Chrome(driver_path)
    url ="https://www.kaigokensaku.mhlw.go.jp/"+ str(preno) +"/index.php"
    #driver.get("https://www.kaigokensaku.mhlw.go.jp/{preno}/index.php")
    print(url)

    sleep(3)

    #介護事業所をクリック
    driver.find_element_by_id("searchselect_centerMenu1").click()

    #qurery = "大野"
    search_box = driver.find_element_by_class_name("form-control")
    qurery = input("市町村名を入力してください")
    search_box.send_keys(qurery)
    #print(qurery)
    search_box.submit()
    sleep(3)

    #各要素の初期化
    list_post = []
    list_adress = []
    list_telno = []
    list_name = []
    list_code = []
   
    while True :

    #郵便番号
        postal_codes = driver.find_elements_by_class_name("postalCode")

        for postal_code in postal_codes:
        
                 postal_block = postal_code.text

                 list_post.append(postal_block)

        if  list_post[-1] == '':
                 list_post.pop(-1    )
       
    #住所
        jigyosyoAdresses = driver.find_elements_by_class_name("jigyosyoAddress")

        for jigyosyoAdress  in jigyosyoAdresses:

                adress_block = jigyosyoAdress.text
                list_adress.append(adress_block)
    
        if  list_adress[-1] == '':
                   list_adress.pop(-1)

    #電話番号
        telNumbbers = driver.find_elements_by_class_name("telNumber")

        for telNumbber  in telNumbbers:

                 telno_block = telNumbber.text
                 list_telno.append(telno_block)
    
        if list_telno[-1] == '':
                  list_telno.pop(-1)
  
    #事業所名
        jigyosyoNames = driver.find_elements_by_class_name("jigyosyoName")

        for jigyosyoName in jigyosyoNames:

                  jigyosyoName_block = jigyosyoName.text
                  list_name.append(jigyosyoName_block)

        if list_name[-1] == '':
                  list_name.pop(-1)

        #print(list_name)

    #事業所コード
        jigyosyoCDs = driver.find_elements_by_class_name("jigyosyoCd")

       
        for jigyosyocd in jigyosyoCDs:

                jigyosyocde_block = jigyosyocd.text
                list_code.append(jigyosyocde_block)

        if list_code[-1] == '':
                list_code.pop(-1)

        sleep(3)
    #次ページ
            
        try:
             driver.find_element_by_xpath('/html/body/main/div[1]/div[1]/article/section/form/div[1]/nav[2]/ul/li[12]/a').click()
             sleep(3)                      
        except:
            break
    
    
    #あまの　の場合「4」
    #/html/body/main/div[1]/div[1]/article/section/form/div[1]/nav[2]/ul/li[4]/a

    #出力ファイルに書き出す
    df = pd.DataFrame({"郵便番号":list_post,"住所":list_adress,"電話番号":list_telno,"事業者名":list_name,"事業者番号":list_code})
    df.to_csv("kaigo.csv")
    

    driver.quit()

scraping()