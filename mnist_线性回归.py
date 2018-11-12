# -*- coding: utf-8 -*-
"""
Created on Thu Nov  8 16:58:59 2018

@author: Orcs_bin
"""

import time
import tensorflow as tf
import scipy.misc
import os
import numpy as np
from tensorflow.examples.tutorials.mnist import input_data
mnist = input_data.read_data_sets("MNIST_data/",one_hot= True)
#查看训练数据集的大小
#print(mnist.train.images.shape)#输出样本数量及其维数
#print(mnist.train.labels.shape)#输出标签数量及其维度
#
##查看验证数据集的大小
#print(mnist.validation.images.shape)#输出样本数量及其维数
#print(mnist.validation.labels.shape)#输出标签数量及其维数
#
##查看测试数据集的大小
#print(mnist.test.images.shape)#输出样本数量及其维数
#print(mnist.test.labels.shape)#输出标签数量及其维数

#查看数据的向量表示
#print(mnist.train.images[0,:])
#print(mnist.train.labels[0,:])

#创建文件夹
save_dir = "MNIST_data/raw/"
if os.path.exists(save_dir) is False:
    os.mkdir(save_dir)
    
    
def get_num(i):       
    ls = mnist.train.labels[i,:]
    return ls.tolist().index(1)

def save_image():
    for i in range(0,100):
        image_array = mnist.train.images[i,:]
        image_array = image_array.reshape(28,28)
        num = get_num(i)
        file_name = save_dir+'number{}is{}.jpg'.format(i+1,num)
        print(file_name)
#        scipy.misc.imsave(file_name,image_array)
        scipy.misc.toimage(image_array, cmin=0.0, cmax=1.0).save(file_name)
        #time.sleep(1)
#save_image()
#print(np.argmax(mnist.train.labels[0,:]))#另一种得到标签的方法

x = tf.placeholder(tf.float32,[None,784])# 占位符 None表示可以传递任意数量的784维样本给x
W = tf.Variable(tf.zeros([784,10]))#变量参数，存储计算后的模型参数 创建变量时要指定初值
b = tf.Variable(tf.zeros([10]))#偏置项
y = tf.nn.softmax(tf.matmul(x,W)+b)#模型的输出

y_ = tf.placeholder(tf.float32,[None,10])#实际的图像标签
#接下来需要通过y和y_计算损失。
cross_entropy = tf.reduce_mean(-tf.reduce_sum(y_*tf.log(y)))
#然后使用梯度下降法优化参数（W，b）
train_step = tf.train.GradientDescentOptimizer(0.001).minimize(cross_entropy)  #0.01代表学习率

#接下来创建会话，只有在会话中才能运行优化步骤
sess = tf.InteractiveSession()
tf.global_variables_initializer().run() #对所有变量初始化

#进行100步梯度下降：
#每一次使用100个数据
for i in range(100):
    batch_xs,batch_ys = mnist.train.next_batch(100) #batch_xs,batch_ys对应着x 和y_两个占位符
    sess.run(train_step,feed_dict={x:batch_xs,y_:batch_ys})

correct_prediction = tf.equal(tf.argmax(y,1),tf.argmax(y_,1))# tf.equal()函数比较他们是否相等

accuracy = tf.reduce_mean(tf.cast(correct_prediction,tf.float32))#ty.cast()函数将bool值转化为32位浮点数 Ture->1.0 Falose->0.0
#tf.reduce_mean()函数计算数组的平均值，此处数组的结构类似与[1.,0.,1.,1.,1.,0.,0.,0.,1.,0.,1.,0.,....]
print("模型正确率：",sess.run(accuracy,feed_dict={x:mnist.test.images,y_:mnist.test.labels}))





