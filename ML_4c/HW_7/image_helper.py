import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
from os import listdir
from os.path import isfile, join
import matplotlib.offsetbox as osb

def GetIntRGB(rgbTuple):
    rate = 85
    r,g,b,*alpha = rgbTuple
    rgb = int(r/rate)*rate
    rgb = (rgb << 8) + int(g/rate)*rate
    rgb = (rgb << 8) + int(b/rate)*rate
    return rgb

def GetRGBFromInt(rgb):
    r = (rgb >> 16) & 0xFF
    g = (rgb >> 8) & 0xFF
    b = rgb & 0xFF;
    return (r,g,b)

def GetDictFor3Colored(png):
    arr = np.array(png)
    totalPixels = arr.shape[0]*arr.shape[1]
    #print("GetDictFor3Colored")
    arr2 = arr.reshape((totalPixels, arr.shape[2]))
    colorLst = list(map(lambda x:GetIntRGB(tuple(x)), arr2))
    colorDic = {}
    for color in colorLst:
        if(color in colorDic):
            continue
        count = colorLst.count(color)
        if(count > totalPixels / 50):
            colorDic[color] = count/totalPixels
    return colorDic

def GetDictFor1Colored(png):
    #print("GetDictFor1Colored")
    im2 = png.convert("RGB")
    internalDic = im2.getcolors()
    totalPixels = np.array(internalDic)[:,0].sum()
    colorDic = {GetIntRGB(x[1]):x[0]/totalPixels for x in internalDic if x[0] > totalPixels/50}
    return colorDic

def GetFileDics():
    fileDics = {}
    fileNames = [f for f in listdir("Flags/") if isfile(join("Flags/", f))]
    for file in fileNames:
        png = Image.open("Flags/"+file)
        if(png.getcolors() is None):
            fileDics[file] = GetDictFor3Colored(png)
        else:
            fileDics[file] = GetDictFor1Colored(png)
    return fileDics

def GetCountryName(fileName):
    startIndex = fileName.find("Flag_of_")
    endIndex = fileName.find(".svg.png")
    return fileName[startIndex+8:endIndex].replace("_", " ")

def PrintGroup(names):
    rows = 7
    width = int(len(names)/rows) + 1
    f, axarr = plt.subplots(min(len(names),rows),max(2,width), facecolor='lightgray') #sharex=True, sharey=True,

    f.subplots_adjust(right= 2, top = 0.99, bottom=0.01, hspace=1, wspace=0.4)
    axflat = axarr.flat
    i=0
    for name in names:
        png = Image.open("Flags/"+name)
        axflat[i].figsize=(8,8)
        axflat[i].imshow(png)
        axflat[i].axes.xaxis.set_visible(False)
        axflat[i].axes.yaxis.set_visible(False)
        axflat[i].set_title(GetCountryName(name))
        i = i + 1

    for i in range(min(len(names),rows) * max(2,width) - len(names)):
        axflat[-1-i].set_visible(False)
        
def imscatter(x, y, image, ax=None, zoom=1):
    if ax is None:
        ax = plt.gca()
    try:
        image = plt.imread(image)
    except TypeError:
        # Likely already an array...
        pass
    im = osb.OffsetImage(image, zoom=zoom)
    x, y = np.atleast_1d(x, y)
    artists = []
    for x0, y0 in zip(x, y):
        ab = osb.AnnotationBbox(im, (x0, y0), xycoords='data', frameon=False)
        artists.append(ax.add_artist(ab))
    ax.update_datalim(np.column_stack([x, y]))
    ax.autoscale()
    return artists

def PlotOnPlane(x2D, flagNames):
    fig, ax = plt.subplots()
    fig.set_figheight(15)
    fig.set_figwidth(15)
    ax.set_xlim([-140, 165])
    ax.set_ylim([-160, 160])
    for xy, file in zip(x2D, flagNames):
        imscatter(xy[0]*80, xy[1]*80, "Flags/" + file, zoom=0.2, ax=ax)
        ax.plot(xy[0]*80, xy[1]*80)
    plt.show()