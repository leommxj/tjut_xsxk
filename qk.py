import requests
from PIL import Image

username = input("帐号：")
passwd = input("密码：")

def login(username,passwd):
	session = requests.session()
	session.headers["User-Agent"] = "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
	session.headers["Connection"] = "close"
	session.get("http://xk.tjut.edu.cn/xsxk/")
	a = session.get("http://xk.tjut.edu.cn/xsxk/servlet/ImageServlet")
	with open("tmp.jpg","wb+") as f:
		f.write(a.content)
	b = Image.open("tmp.jpg")
	b.show()

	vld = input("验证码：")
	loginData={"username":username,"password":passwd,"verifyCode":vld}
	session.get("http://xk.tjut.edu.cn/xsxk/loadData.xk?method=checkLogin&username="+username+"&password="+passwd+"&verifyCode="+vld)

	l = session.post("http://xk.tjut.edu.cn/xsxk/login.xk",loginData)
	session.get("http://xk.tjut.edu.cn/xsxk/login.xk")
	session.get("http://xk.tjut.edu.cn/xsxk/main.xk")
	session.get("http://xk.tjut.edu.cn/xsxk/loadData.xk?method=cacheIsOpen")
	session.get("http://xk.tjut.edu.cn/xsxk/loadData.xk?method=getXsLoginCnt")
	session.get("http://xk.tjut.edu.cn/xsxk/loadData.xk?method=getXksj")
	session.get("http://xk.tjut.edu.cn/xsxk/loadData.xk?method=loginCheck")
	session.get("http://xk.tjut.edu.cn/xsxk/xkjs.xk?pyfaid=01773&jxqdm=1&data-frameid=main&data-timer=2000&data-proxy=proxy.xk")
	session.get("http://xk.tjut.edu.cn/xsxk/tjxk.xk")
	return session
def xk(s,jxbid):
	r = s.get("http://xk.tjut.edu.cn/xsxk/xkOper.xk?method=handleTjxk&jxbid="+jxbid,headers=headers)
	r = r.json()
	return r
s = login(username,passwd)
jxbid = input("课程id:")
headers = {"Referer": "http://xk.tjut.edu.cn/xsxk/tjxk.xk","X-Requested-With":"XMLHttpRequest","User-Agent":"Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"}
while True:
	r = xk(s,jxbid)
	print(r["message"])
	if(r["success"]=="true"):
		print("成功")
		break
	elif(r["message"]=="用户登录已失效请重新登录"):
		print("用户登录已失效请重新登录")
		s = login(username,passwd)
	else:
		print(r["message"])