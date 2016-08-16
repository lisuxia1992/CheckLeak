# CheckLeak
检测iOS项目里面的内存泄露（block）

检测iOS项目中block中使用self而引起的内存泄露

##需要安装的库
1.pyobjc
参考教程[https://pythonhosted.org/pyobjc/install.html](https://pythonhosted.org/pyobjc/install.html)
##需要设置的参数

1.projectPath(工程所在路径)

	如:projectPath = "/Users/yuyang/Documents/techwolf/mobile_ios"
	
2.noPath(不检测路径)

	如:noPath = ['ThirdLibs','iosTools']
	
	或:noPath = None(检测工程下所有路径)
	
3.NormalCheck(普通模式,False:检测所有,True:不检测不检测路径和动画产生的self)

	如:True
	
##使用

python checkLeak.py

###如果有self引起的内存泄露会在mac的通知中心通知你
