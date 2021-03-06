# -*- coding: utf-8 -*-
"""
Created on Thu Nov  8 22:15:33 2018

@author: Orcs_bin
"""
'''
使用两层卷积神经网络将准确率提升到99%
'''

import tensorflow as tf
from tensorflow.examples.tutorials.mnist import input_data

mnist = input_data.read_data_sets("MNIST_data/",one_hot= True)

#print(mnist.train.images[0,:].reshape(28,28))
x = tf.placeholder(tf.float32,[None,784])#图片数据的占位符
y_ = tf.placeholder(tf.float32,[None,10])#输出结果的占位符

x_image = tf.reshape(x,[-1,28,28,1])#将784维向量还原为28*28的矩阵图片

#卷积的相关代码
def weight_variable(shape):
    '''
    用来初始化卷积的核
    返回一个给定形状的变量，并自动已截断正态分布初始化
    '''
    inital = tf.truncated_normal(shape,stddev=0.1)
    return tf.Variable(inital)

def bise_variable(shape):
    '''
    用来初始化卷积的偏执项
    返回一个给定形状的变量，并将所有值初始化为0.1
    '''
    inital = tf.constant(0.1,shape = shape)
    return tf.Variable(inital)

def conv2d(x, W):
    '''
    卷积计算函数
    返回计算结果
    '''
    return tf.nn.conv2d(x, W, strides=[1,1,1,1],padding='SAME')

def max_pool_2x2(x):
    '''
    池化函数
    '''
    return tf.nn.max_pool(x,ksize=[1,2,2,1],strides=[1,2,2,1],padding='SAME')

#第一层卷积层
W_conv1 = weight_variable([5,5,1,32])
b_conv1 = bise_variable([32])
h_conv1 = tf.nn.relu(conv2d(x_image,W_conv1)+b_conv1)#真正的卷积计算，用relu作为激活函数
h_pool1 = max_pool_2x2(h_conv1)#池化操作

#第二层卷积层
W_conv2 = weight_variable([5,5,32,64])
b_conv2 = bise_variable([64])
h_conv2 = tf.nn.relu(conv2d(h_pool1,W_conv2)+b_conv2)
h_pool2 = max_pool_2x2(h_conv2)


#全连接层
W_fc1 = weight_variable([7*7*64,1024])
b_fc1 = bise_variable([1024])
h_pool2_flat = tf.reshape(h_pool2,[-1,7*7*64])
h_fc1 = tf.nn.relu(tf.matmul(h_pool2_flat,W_fc1)+b_fc1)
keep_prob = tf.placeholder(tf.float32) #定义一个占位符
h_fcl_drop = tf.nn.dropout(h_fc1,keep_prob=keep_prob) #dropout是一种防止过拟合的方法，每一步都随机的去除网络中的某些连接，
#在训练时每次都有keep_prob的连接被暂时“去除”，在测试时则保留所有的连接

#再加入一层全连接层，将上一步的h_fcl_drop转化为10个类别的打分
W_fc2 = weight_variable([1024,10])
b_fc2 = bise_variable([10])
y_conv = tf.matmul(h_fcl_drop, W_fc2)+b_fc2

#定义交叉熵损失
cross_entropy = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(labels=y_,logits=y_conv))
train_step = tf.train.AdamOptimizer(1e-4).minimize(cross_entropy)

#定义测试准确率
correct_prediction = tf.equal(tf.argmax(y_conv,1),tf.argmax(y_,1))
#将结果与答案对比，返回类似[True,true,False,.....]的数组
accuracy = tf.reduce_mean(tf.cast(correct_prediction,tf.float32))
#将数组结果转化为[1.,1.,1.,0.,0.,0.,0.,0.,...]并计算平均值作为准确率

#创建会话，对变量进行初始化
sess = tf.InteractiveSession()
sess.run(tf.global_variables_initializer())#初始化所有变量

#训练20000步
for i in range(20000):
    batch = mnist.train.next_batch(50)
    #每100步报告一次在验证集上的准确率
    if i%100==0:
        train_accuracy = accuracy.eval(feed_dict={x:batch[0],y_:batch[1],keep_prob:1.0})
        print("第%d步，准确率：%g" % (i,train_accuracy))    
    train_step.run(feed_dict = {x:batch[0],y_:batch[1],keep_prob:0.5})
    


