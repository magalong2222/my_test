'''
import matplotlib.pyplot as plt
import numpy as np
import scipy as sp
from scipy.stats import norm
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn import linear_model
from sklearn import preprocessing
from sklearn.model_selection import train_test_split

import pdb



#class Fitting(object):
#    def __init__(self):
#        pass

class Polynomial(object):
    ### Reference https://blog.csdn.net/lsldd/article/details/41251583
    def __init__(self, x, y):
        pdb.set_trace()
        x = np.array(x)
        y = preprocessing.scale(np.array(y))
        self.x = x[:-100]
        self.y = y[:-100]
        self.x_test = x[-100:]
        self.y_test = y[-100:]
        #self.x = np.array(x)
        #self.y = np.array(y)
        #self.y = preprocessing.scale(np.array(y))
        # other setup
        plt.scatter(self.x, self.y, s=5)
        plt.scatter(self.x_test, self.y_test, s=5)
        #self.y_test = np.array([])

    ### 均方误差根 
    def rmse(self, y_test, y):
        return sp.sqrt(sp.mean((y_test - y) ** 2))

    ### 与均值相比的优秀程度，介于[0~1]。0表示不如均值。1表示完美预测.
    ### 这个版本的实现是参考scikit-learn官网文档
    def r2(self, y_test, y_true):
        return 1 - ((y_test - y_true) ** 2).sum() / ((y_true - y_true.mean()) ** 2).sum()

    ### 这是Conway&White《机器学习使用案例解析》里的版本
    def r22(self, y_test, y_true):
        y_mean = np.array(y_true)
        y_mean[:] = y_mean.mean()
        return 1 - self.rmse(y_test, y_true) / self.rmse(y_mean, y_true)

    def fit(self, degree=[1,2,3]):
        for d in degree:
            clf = Pipeline([('poly', PolynomialFeatures(degree=d)),
            #                ('linear', LinearRegression(fit_intercept=False))])
                            ('linear', linear_model.Ridge())])
            clf.fit(self.x[:, np.newaxis], self.y)
            pdb.set_trace()
            #tmp = np.array([444,445,446,447,448])
            #np.hstack((self.x, tmp)) 
            self.y_predit = clf.predict(self.x_test[:, np.newaxis])
  
            print(clf.named_steps['linear'].coef_)
            print('rmse=%.2f, R2=%.2f, R22=%.2f, clf.score=%.2f' %
                    (self.rmse(self.y_predit, self.y_test),
                    self.r2(self.y_predit, self.y_test),
                    self.r22(self.y_predit, self.y_test),
                    clf.score(self.x_test[:, np.newaxis], self.y_test)))
            
            whole_data = np.hstack((self.x, self.x_test))
            whole_data_y = clf.predict(whole_data[:, np.newaxis])
            plt.plot(whole_data, whole_data_y, linewidth=2)
        plt.grid()
        plt.legend(['1','2','3'], loc='upper left')
        plt.show()
'''

'''
from scipy.optimize import leastsq
class Polynomial(object):
    def __init__(self):
        self.window = 100
        self.degree = 4
        self.reg = True
        pass

    def func(self, x, p):
        f = np.poly1d(p)
        return f(x)

    def residuals(self, p, x, y, reg):
        regularization = 0.1  # 正则化系数lambda
        ret = y - self.func(x, p)
        if reg == 1:
            ret = np.append(ret, np.sqrt(regularization) * p)
        return ret

    def LeastSquare(self, data, k=100, order=4, reg=1, show=1):  # k为求导窗口宽度,order为多项式阶数,reg为是否正则化
        l = self.len
        step = 2 * k + 1
        p = [1] * order
        #for i in range(0, l, step):
        #    if i + step < l:
        #        y = data[i:i + step]
        #        x = np.arange(i, i + step)
        #    else:
        #        y = data[i:]
        #        x = np.arange(i, l)
        #    try:  
        #        r = leastsq(self.residuals, p, args=(x, y, reg))
        #    except:
        #        print("Error - curve_fit failed")
        #    fun = np.poly1d(r[0])  # 返回拟合方程系数
        #    df_1 = np.poly1d.deriv(fun)  # 求得导函数
        #    df_2 = np.poly1d.deriv(df_1)
        #    df_3 = np.poly1d.deriv(df_2)
        #    df_value = df_1(x)
        #    df3_value = df_3(x)
        r = leastsq(self.residuals, p, args=(x, y, reg))
'''

from common.db_access import Database
from common.position import Position
import matplotlib.pyplot as plt
import numpy as np
import time
import pdb

class Polynomial(object):
    def __init__(self, x, y):
        self.x = np.array(x)
        self.y = np.array(y)
        self.degree = 2

    def show(self):
        y_predit = self.poly1d(self.x)
        y_df1 = self.df_1(self.x)
        plt.figure('111')
        plt.scatter(self.x, self.y, color='g', label='scatter')
        plt.plot(self.x, self.y, color='r', label='line')
        plt.plot(self.x, y_predit, color='b',label='fit')
        #plt.figure('222')
        #plt.plot(self.x, y_df1, color='y',label='df_1')
        plt.show()
        
    def fit(self):
        poly_expression = np.polyfit(self.x, self.y, self.degree)
        self.poly1d = np.poly1d(poly_expression)
        self.df_1 = np.poly1d.deriv(self.poly1d)
        self.df_2 = np.poly1d.deriv(self.df_1)

    def maxOrMin(self):
        # First derivative
        self.df_1 = np.poly1d.deriv(self.poly1d)
        # Find max/min points
        #latest_solution = self.df_1.r.max()
        latest_solution = int(self.df_1.r.max())
        # Ingore image root
        if type(latest_solution) == np.complex128:
            print('Image root has found.') 
            return False
        # Only take care about min/max point bigger window
        if latest_solution >= self.x[0]:
            # Second derivative
            df_2 = np.poly1d.deriv(self.df_1)
            if df_2(latest_solution) == 0:
                # How to deal with stop point(Second derivative = 0)?
                print('Second derivative == 0.') 
                return False
            elif df_2(latest_solution) > 0:
                # Second derivative >0 means min point of original curve
                #print('(%s, Min)' % latest_solution)
                # Only pickup min point which bigger than max x of window
                return latest_solution, 'Min'
            else:
                # Second derivative <0 means max point of original curve
                #print('(%s, Max)' % latest_solution)
                # Only pickup max point which smaller than min x of window
                return latest_solution, 'Max'
        else:
            #print('Root out of range. %s' % latest_solution) 
            return False
        

class MovePloyFit(object):
    def __init__(self, env, window_size=90, step=1):
        #self.env = env
        self.db = Database(env)
        self.window_size = window_size
        self.step = step
        self.pre_status = (1,'Max')
        self.pos = Position()
        self.pos.show()
        self.x = []
        self.y = []

    def execute(self, data):
        for pair in data:
            # Check if begin analysis
            if len(self.x) == self.window_size:
                poly = Polynomial(self.x, self.y)
                poly.fit()
                #print('x=%s, y=%s' % (self.x[-1], self.y[-1]))
                check_point = poly.maxOrMin()
                # Find min/max point
                if check_point:
                    # Current extremum status != previous extremum status
                    if check_point[1] != self.pre_status[1]:
                        # Previous fit center point must samller than right side of window
                        if self.pre_status[0] < self.x[-1]:
                            # Trend change, remove pre_fit half curve
                            self.x = self.x[self.pre_status[0]:]
                            self.y = self.y[self.pre_status[0]:]
                            self.pre_status = check_point
                    if check_point[1] == 'Min':
                        # Min point find, Buy process
                        self.pos.buy(pair[1])
                    else:
                        # Max point find, Sell process
                        self.pos.sell(pair[1])
                #poly.show()
                self.x = self.x[self.step:]
                self.y = self.y[self.step:]
            # Just fill x,y list
            self.x.append(pair[0])
            self.y.append(pair[1])

    def regression(self, trade_pair='eos_usdt'):
        sql = 'select rowid,last,time from %s' % trade_pair
        result = self.db.execute(sql)
        data = result.fetchall()
        self.execute(data)
        self.pos.show()

    def realtime(self, trade_pair='eos_usdt'):
        # call select every <xxx> second
        sql = 'select rowid,last from %s order by rowid desc limit %s' % (trade_pair, self.window_size)
        while(True):
            result = self.db.execute(sql)
            data = result.fetchall()
            self.execute(data)
            if self.pos.ifStop():
                break
            # Waitting for next loop
            time.sleep(self.step * 10)

    def showData(self):
        sql = 'select rowid,last,time from eos_usdt'
        result = self.db.execute(sql)
        data = result.fetchall()
        for pair in data:
            self.x.append(pair[0])
            self.y.append(pair[1])
        poly = Polynomial(self.x, self.y)
        poly.fit()



if __name__ == '__main__':
    poly = Polynomial()
    poly.fit()
