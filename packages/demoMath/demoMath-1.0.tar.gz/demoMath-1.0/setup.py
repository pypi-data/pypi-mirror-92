from distutils.core import setup
setup(
        name='demoMath',
        # 对外我们模块的名字
        version='1.0', # 版本号
        description='这是第一个对外发布的模块,测试哦',
        #描述
        author='lynn', # 作者
        author_email='895425634@qq.com',
        py_modules=['demoMath.demo1','demoMath.demo2'] # 要发布的模块
        )
