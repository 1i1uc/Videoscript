from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import ElementNotInteractableException,NoSuchElementException,ElementNotInteractableException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from selenium.webdriver.edge.options import Options
def TimeToSecond(time_str) ->int: 
    """
    用于时间字符串转整数秒
    """
    t = time_str.split(":")
    if len(t) == 2:
        second=int(t[0])*60+int(t[1])
    elif len(t) == 3:
        second = int(t[0])*3600+int(t[1])*60+int(t[2])
    return second    


edge_options = Options()
edge_options.add_argument("--mute-audio")#添加静音参数
MyBrowser = webdriver.Edge(options=edge_options)                      
MyBrowser.get("https://higher.cq.smartedu.cn/course/detail/courseStudy?id=fc6abc90d5a7b474")
MyBrowser.maximize_window()# 窗口最大化
WebDriverWait(MyBrowser,10).until(EC.visibility_of_element_located((By.CLASS_NAME,"submit-btn")),message = "超时，未到达登录框")
AcountTexts = MyBrowser.find_elements(By.CLASS_NAME,"ant-input")
numbers = ("","")#用户名和密码
for i in range(2):
    AcountTexts[i].send_keys(numbers[i])
MyBrowser.find_element(By.CLASS_NAME,"submit-btn").click()
time.sleep(2)

if MyBrowser.find_element(By.CSS_SELECTOR,"#app > div > div:nth-child(2) > section > section > header > div > div > div.box-rights.ant-pro-global-header-index-right.ant-pro-global-header-index-dark > span > img.avatar-img"):
    MyBrowser.refresh()  

#进课程
try:
    MyBrowser.find_element(By.XPATH,"/html/body/div[1]/div/div[2]/section/section/main/div/div/div[2]/div[1]/div/div[2]/div[1]/div[1]")
    time.sleep(2)
except NoSuchElementException:
    MyBrowser.find_element(By.CSS_SELECTOR,"#app > div > div:nth-child(2) > section > section > header > div > div > div.box-rights.ant-pro-global-header-index-right.ant-pro-global-header-index-dark > span > img.avatar-img").click()#点人像图片
    time.sleep(2)
    MyBrowser.find_element(By.CSS_SELECTOR,"body > div:nth-child(6) > div > div > ul > li:nth-child(1) > div > img").click()#在学课程
    time.sleep(2)
    MyBrowser.find_element(By.XPATH,"/html/body/div/div/div[2]/section/section/main/div/div/div[2]/div[1]/div[2]/div/div[1]/div/div[1]/div[2]/div[2]/div[1]").click()#点击课程
    time.sleep(2)

#下面是提取章节文本
#['第1章 Python概述及安装配置', '第2章 数据类型、表达式和其它语法规则', '第3章 流程控制', '第4章 容器类型：序列、映射和集合', '第5章 文件操作及系统交互', '第6章 时间和日期', '第7章 函数', '第8章 面向对象编程', '第9章 模块和包', '第10章 异常处理']
Lists = []
AfterLists = []
blocks = MyBrowser.find_elements(By.CLASS_NAME,"title-big")
for i in range(len(blocks)):
    Lists.append(blocks[i].text)
for list in Lists:
    if '第' and '章' in list[0:7]:
        AfterLists.append(list.strip())

#下面是展开选项卡
for tag in range(1,(len(AfterLists))+1):
    MyBrowser.find_element(By.CSS_SELECTOR,f"#app > div > div:nth-child(2) > section > section > main > div > div > div.course-detail-container > div.menu-content > div > div.left-box > div > div:nth-child({tag})").click()                                    
    MyBrowser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(1)
LeftMenu_LastItem = MyBrowser.find_element(By.CSS_SELECTOR,"#second-level3d085313b0ffdc89ba1fa8dd8c08d61d > div > div > p")
MyBrowser.execute_script("arguments[0].scrollIntoView();", LeftMenu_LastItem)
time.sleep(1)
LeftMenu_FirstItem = MyBrowser.find_element(By.XPATH,"/html/body/div[1]/div/div[2]/section/section/main/div/div/div[2]/div[2]/div/div[1]/div/div[1]/div[1]/p")
MyBrowser.execute_script("arguments[0].scrollIntoView();", LeftMenu_FirstItem)
time.sleep(1)
MyBrowser.execute_script("window.scrollTo(0, 0);")# 滚到顶部

#点击选项卡(基于completeicon)
CompleteIcons = MyBrowser.find_elements(By.CLASS_NAME,"file-complete")
#也可以基于选项卡,这是找出全部选项卡thirdlevelboxs = MyBrowser.find_elements(By.CLASS_NAME,"third-level-inner-box")
for i in range(0,len(CompleteIcons)):
    #是否跳过选项卡
    if CompleteIcons[i].get_attribute("src") == "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAfhJREFUSEu9lj1oE2EYx//PqaDYDJHaQlCoH7k4dVYuUMFFERSHQIeCUcxiih/QpXS4u9Gp9MNJwSWC4CAKKgiClgSLg4hkMIkBISFrhwhKPu4p7zWXz7vLXWjMmPd5/r/3+XyP4PKbVS+e+Cc1rsPgqyCcARBqmVfAKEKit4eNg69/6J/KTjJkdxBRlRATdGbcAviA2yUAahLhGTHUnJ6p9NsOACKqco2BFIMD7sK9pwSqErCQ0zNvuk96AGEteg8wVsGQ/Ii3bQkGID0saOl16782QNzcIH41snhH0ZCYbliRmAAz58BPv2lxLqyZrnOiJiZA1pQnzHxnpLQ4OBHR07yWSZBoxb+o/x7eLX7x1DyCQzMk69EkG8amX3cv9iRJiySryjsGX/Hi0G8zHZhEeOo00sWvtu4Eek+ypuSYWfYLOHv8FFLxDRw7GsSltRhKOwMzBiLKC0CVmSf8ALrFPxe+IPF8yT4Coj+ugNsX5vGtlMX3crYt0C9+98Uy6s26K8A2RSeDIXy8/xK1Rg1CZOvXNvyIC+JeilyKvHL5AW6ej5mQRx8eIzkXN3Mu0uJ2885QiyIPaVMLYjl5FTcjEG3qZdAsiB9xscbNQfO6KkRN7FrRcR9Zq+K/LLsWZHzr2gpzrA+OBRnrk9kFGd+j390V+/HZsgvSIhcecicecAAAAABJRU5ErkJggg==":#已完成的
        time.sleep(1)
        print(f"第{i}被跳过{CompleteIcons[i].get_attribute('src')}\n")
        continue
    else:
        print(f"第{i}没打勾要判断")
        CompleteIcons[i].click()
        time.sleep(2) 
#权限逻辑
        try:
            if MyBrowser.find_element(By.CLASS_NAME,"ant-message-notice"): 
                print("无权限")
                break
        except NoSuchElementException:
            print("有权限")
            pass
#资料逻辑
    try:
        if  "倒计时" in MyBrowser.find_element(By.XPATH,"/html/body/div[1]/div/div[2]/section/section/main/div/div/div[2]/div[2]/div/div[2]/div/div[1]/div[1]/div/div").text:                                                                      
            print("是资料,暂停30秒\n")
            time.sleep(30)
            continue
    except NoSuchElementException:#若无倒计时
        print("无倒计时")
        pass
#播放逻辑    
    try:
        time.sleep(3)
        StartTime = MyBrowser.find_element(By.XPATH,"/html/body/div[1]/div/div[2]/section/section/main/div/div/div[2]/div[2]/div/div[2]/div/div[1]/div[2]/div/div/div/div[4]/div[2]/span/span[1]").text
        EndTime = MyBrowser.find_element(By.XPATH,"/html/body/div[1]/div/div[2]/section/section/main/div/div/div[2]/div[2]/div/div[2]/div/div[1]/div[2]/div/div/div/div[4]/div[2]/span/span[2]").text
        while EndTime == "00:00":#若暂时未加载出值
            EndTime = MyBrowser.find_element(By.XPATH,"/html/body/div[1]/div/div[2]/section/section/main/div/div/div[2]/div[2]/div/div[2]/div/div[1]/div[2]/div/div/div/div[4]/div[2]/span/span[2]").text
        second = TimeToSecond(EndTime) - TimeToSecond(StartTime)
        MyBrowser.find_element(By.XPATH,"/html/body/div[1]/div/div[2]/section/section/main/div/div/div[2]/div[2]/div/div[2]/div/div[1]/div[2]/div/div/div/div[4]/div[2]/button").click()#播放按钮
        print(StartTime,EndTime,second)
        print(f"视频播放{second}秒\n")
        time.sleep(second+5)
    except NoSuchElementException:
        pass
        print("未找到播放按钮或开始结束时间\n")        


input("输入quit关闭浏览器\n")
MyBrowser.quit()