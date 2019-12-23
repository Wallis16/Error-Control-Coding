# Error-Control-Coding
Python implementations about Error Control Coding topics

# hard_soft.py
Python implementation based on matlab code available in http://www.dsplog.com/2012/03/15/hamming-code-soft-hard-decode/?fbclid=IwAR3t38pYyOJGesULKauqVFTYh6ZQX68iy5PjeI-Yjo63ncIw9wo4ZJWBEBU 

N = 10^5

![10^5](https://user-images.githubusercontent.com/26671424/66720822-0985e700-edd8-11e9-89fb-8977a06b157e.png)

# hard_soft_interleaving.py

N = 10^5

### without interleaving codewords

![image](https://user-images.githubusercontent.com/26671424/71371574-5f24ff80-2590-11ea-8f03-5608ce02f15f.png)

### interleaving codewords

![image](https://user-images.githubusercontent.com/26671424/71371667-ac08d600-2590-11ea-9ff0-bb1fa9260df5.png)

### BER ratio between (without interleaving/with interleaving)

uncoded -- [1. 1. 1. 1. 1. 1. 1. 1. 1. 1. 1.] 
soft decision -- [0.99914904 0.9699905  1.05453206 1.00445765 1.03533569 1.38686131 0.88235294 0.45454545 0.5 nan nan] 
hard decision -- [0.98597045 0.98971266 1.04815166 0.99338791 1.04435995 1.19171779 1.15246637 0.74285714 0.6 nan nan]

# GNUradio implementation using float vectors

![image](https://user-images.githubusercontent.com/26671424/71335017-5c3df680-251f-11ea-8591-a12f773743e0.png)

![image](https://user-images.githubusercontent.com/26671424/71335189-454bd400-2520-11ea-9977-24f6d28b233d.png)
