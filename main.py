import os
import imageio
import numpy as np
import cv2
from matplotlib import pyplot as plt
import matplotlib.cm as cm
#Calculate DCT freqeuncy coefficients
"""
          N-1
y[k] = 2* sum x[n]*cos(pi*(2k+1)*(2n+1)/(4*N)), 0 <= k < N.
          n=0
"""

def readImages(imgFolder='img/'):
    """read all images in a given folder"""
    #Each image in images is a numpy array of shape 192x168(x1) (heightxwidth)
    #images datatype is a regular numpy list
    filenames = os.listdir(imgFolder)
    images = [imageio.imread('img/'+fn+'/image0.jpg')[::,::].astype(np.float32)/255. for fn in filenames]#glob.glob(imgFolder+'*.jpg')]
    return images

#Get DCT coefficients.
def dct_1d(image, numberCoefficients=0):
    
    nc = numberCoefficients
    n = len(image)
    newImage= np.zeros_like(image).astype(float)

  
    for k in range(n):
        sum = 0
        for i in range(n):
            sum += image[i] * cos(2 * pi * k / (2.0 * n) * i + (k * pi) / (2.0 * n))
        ck = sqrt(0.5) if k == 0 else 1
        newImage[k] = sqrt(2.0 / n) * ck * sum
    
    #Get top coefficients.
    if nc > 0:
        newImage.sort()
        for i in range(nc, n):
            newImage[i] = 0

    return newImage

def dct_2d(image, numberCoefficients=0):
    
    nc = numberCoefficients 
    height,width = image.shape[0],image.shape[1]
    imageRow = np.zeros_like(image).astype(float)
    imageCol = np.zeros_like(image).astype(float)

    for h in range(height):
        imageRow[h, :] = dct_1d(image[h, :], nc) 
    for w in range(width):
        imageCol[:, w] = dct_1d(imageRow[:, w], nc) 

    return imageCol
def gaussianBlur(img,ksize=(5,5),sigma=10):
    #kernel = cv2.getGaussianKernel(ksize,sigma)
    dst = np.zeros_like(img)
    cv2.GaussianBlur(src=img,dst=dst,ksize=ksize,sigmaX=0)
    return dst

        

if __name__=="__main__":
    images = readImages('img/')
    print('Found images:',len(images))
    dct={}
    for i in range(len(images)):
        plt.figure(i)
        dst = gaussianBlur(images[i])
        plt.subplot(121),plt.imshow(images[i],cmap=cm.Greys_r),plt.title('Original')
        plt.xticks([]), plt.yticks([])
        plt.subplot(122),plt.imshow(dst,cmap=cm.Greys_r),plt.title('Gaussian Blurred')
        plt.xticks([]), plt.yticks([])
        imgResult = cv2.dct(images[i])
        dct[i]=imgResult
        img = np.uint8(imgResult*255.0)
        print('Writing dct256_B'+str(i)+'.png...')
        imageio.imwrite('dct256_B'+str(i)+'.png', img)
    #WARNING:
    plt.show() #--> Figures created through the pyplot interface will consume too much memory until explicitly closed.
        

