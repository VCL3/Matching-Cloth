########################################################################
#
# File:   FourierDemo.py
# Author: Matt Zucker
# Date:   2013-2015
#
# Written for ENGR 27 - Computer Vision
#
########################################################################

import cv2
import numpy
import math
import sys

######################################################################

def wrapImage(src, x, y, dst=None):

    if ( dst is None or 
         len(dst.shape) != len(src.shape) or 
         dst.shape != src.shape or 
         dst.dtype  != src.dtype ):
        dst = numpy.empty_like(src)

    h = src.shape[0]
    w = src.shape[1]
    x = x % w
    y = y % h

    dst[0:h-y, 0:w-x] = src[y:h, x:w]
    dst[0:h-y, w-x:w] = src[y:h, 0:x]
    dst[h-y:h, 0:w-x] = src[0:y, x:w]
    dst[h-y:h, w-x:w] = src[0:y, 0:x]

    return dst

######################################################################

def wrapForward(src, dst=None):
    return wrapImage(src, src.shape[1]/2, src.shape[0]/2, dst)

######################################################################

def wrapInv(src, dst=None):
    return wrapImage(src, -src.shape[1]/2, -src.shape[0]/2, dst)

######################################################################

def dftToRGB(F, dst=None):

    dmag = numpy.log( 1 + numpy.sqrt((F**2).sum(axis=2)) )
    normalize(dmag)

    hsv = numpy.empty((F.shape[0], F.shape[1], 3), dtype=F.dtype)
    hsv[:,:,0] = numpy.arctan2(F[:,:,1], F[:,:,0])*180.0/math.pi + 180.0
    hsv[:,:,1] = 0
    hsv[:,:,2] = dmag
    
    return cv2.cvtColor(hsv, cv2.COLOR_HSV2RGB)

######################################################################

def display(win, I):
    cv2.imshow(win, I)
    while cv2.waitKey(5) < 0: pass

def sinusoid(dims, wavelength_px, offset_px, angle):

    X, Y = numpy.meshgrid(numpy.arange(0, dims[0]),
                          numpy.arange(0, dims[1]))

    freq = 2*math.pi / wavelength_px
    ca = math.cos(angle)
    sa = math.sin(angle)

    return numpy.sin(freq*(X*ca + Y*sa + offset_px)).astype('f')*0.5 + 0.5

def load(filename):
    return cv2.imread(filename, cv2.CV_LOAD_IMAGE_GRAYSCALE).astype('f')/255.0

def normalize(img):
    cv2.normalize(img, img, 0, 1, cv2.NORM_MINMAX)


######################################################################

class FourierDemo:

    def compose(self):

        w, h, tsize = self.w, self.h, self.tsize

        self.composite[0:h, 0:w] = (self.image_rgb*255.0).astype('uint8')
        self.composite[0:h, w:2*w] = (self.freq_rgb*255.0).astype('uint8')
        self.composite[h:h+tsize,:,:] = 255


    def circle(self,x,y):
        dist = numpy.sqrt((self.gx-x)**2+(self.gy-y)**2)
        s = 1
        numpy.clip(s*self.radius-s*dist, -0.5, 0.5, dist)
        dist += 0.5
        return dist

    def gauss(self,x,y):
        dsqr = (self.gx-x)**2+(self.gy-y)**2
        return numpy.exp(-dsqr / (self.radius*self.radius))
    

    def mouseEvent(self, event, x, y, flags, param):

        self.mousePos = (x,y)

        dragging = ( event == cv2.EVENT_LBUTTONDOWN or
                     flags & cv2.EVENT_FLAG_LBUTTON)

        if not dragging or not self.which:
            self.which = None
            if y > 0 and y < self.h:
                if x > 0 and x < self.w:
                    self.which = 'left'
                elif x < 2*self.w:
                    self.which = 'right'
                    

        if ( self.which and dragging ):

            if self.which == 'left':

                g = self.gauss(x,y)
                if not (flags & cv2.EVENT_FLAG_SHIFTKEY):
                    self.image_bw -= g
                else:
                    self.image_bw += g
                numpy.clip(self.image_bw, 0, 1, self.image_bw)
                self.imageUpdated()
                self.compose()

            if self.which == 'right':

                x -= self.w
                g1 = self.gauss(x,y)
                g2 = self.gauss(self.w-x, self.h-y)
                g = numpy.maximum(g1,g2)

                gg = numpy.tile(g.reshape(self.h,self.w,1), (1,1,2))
                if not (flags & cv2.EVENT_FLAG_SHIFTKEY):
                    gg = 1-gg

                self.freq_centered *= gg
                self.freqUpdated()
                self.compose()
                    
        self.display()

    def display(self):
        display = self.composite.copy()
        if self.which:
            if self.which == 'left':
                color = (255,0,0)
            else:
                color = (0, 0, 255)
            cv2.circle(display, self.mousePos, self.radius, color, 2, cv2.CV_AA)
        cv2.imshow(self.window, display)

    def imageUpdated(self,display=True):

        I = self.image_bw
        self.image_rgb = cv2.cvtColor(I, cv2.COLOR_GRAY2RGB)
        self.image_cmp = numpy.zeros((I.shape[0], I.shape[1], 2), dtype='f')
        self.image_cmp[:,:,0] = 2*I-1
        self.freq = cv2.dft(self.image_cmp)
        self.freq_centered = wrapForward(self.freq)
        self.freq_rgb = dftToRGB(self.freq_centered)

        if display:
            self.compose()
            self.display()

    def freqUpdated(self,display=True):

        self.freq = wrapInv(self.freq_centered)
        self.freq_rgb = dftToRGB(self.freq_centered)
        cv2.dft(self.freq, self.image_cmp, cv2.DFT_INVERSE | cv2.DFT_SCALE)
        self.image_bw = self.image_cmp[:,:,0]*0.5+0.5
        numpy.clip(self.image_bw, 0, 1, self.image_bw)
        self.image_rgb = cv2.cvtColor(self.image_bw, cv2.COLOR_GRAY2RGB)

        if display:
            self.compose()
            self.display()


    def useImage(self,idx,display=True):
        I = self.images[idx].copy()
        (self.h,self.w) = I.shape
        ix = numpy.arange(0,self.w).astype('f')
        iy = numpy.arange(0,self.h).astype('f')
        self.gx, self.gy = numpy.meshgrid(ix,iy)
        self.image_idx = idx
        self.image_bw = I
        self.imageUpdated(display)

    def __init__(self):

        self.images = [
            sinusoid((256,256), 16, 34, 0),
            sinusoid((256,256), 32*math.sqrt(2), 20, math.pi/4),
            sinusoid((256,256), 32, 30, math.pi/2),
            load('bricks.png'),
            load('zebra-crop-bw.png'),
            load('pattern1008.png'),
            load('pattern1028.png'),
            load('pattern1004.png')

        ]
            
        self.useImage(0, False)

        self.tsize = 0
        self.imgw = max(2*self.w, 512)
        
        self.window = 'Fourier Demo'
        self.composite = 255*numpy.ones((self.h+self.tsize, self.imgw, 3), dtype='uint8')

        cv2.namedWindow(self.window)
        cv2.setMouseCallback(self.window, self.mouseEvent, None)

        self.mousePos = None
        self.which = None

        self.radius = 32

        self.compose()
        self.display()

        while True: 
            k = cv2.waitKey(100)
            if k < 0:
                continue
            else:
                k = chr(k)
                if k == chr(27):
                    break
                elif k == '+' or k == '=':
                    self.radius = min(self.radius + 5, 101)
                    self.display()
                elif k == '-':
                    self.radius = max(self.radius - 5, 1)
                    self.display()
                elif k == 'r':
                    self.useImage(self.image_idx)
                elif k == 'b':
                    self.image_bw[:] = 1
                    self.imageUpdated()
                elif k == 'n':
                    normalize(self.image_bw)
                    self.imageUpdated()
                elif k == ']':
                    self.useImage((self.image_idx + 1) % len(self.images))
                elif k == '[':
                    self.useImage((self.image_idx - 1) % len(self.images))


if __name__ == '__main__':

    help_strs = [
        'Click in spatial domain (LHS) to darken, Shift+click to lighten',
        'Click in frequency domain (RHS) to clamp frequencies, Shift+click to pass frequencies',
        '',
        'Keys:',
        '',
        '  Esc     quit',
        '  + or =  increase pen size',
        '  -       decrease pen size',
        '  r       reset image',
        '  b       blank image',
        '  n       re-normalize spatial domain',
        '  [ or ]  seek to prev/next image',
    ]

    print '\n'.join(help_strs)

    FourierDemo()



