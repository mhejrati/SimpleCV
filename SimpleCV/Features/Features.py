# SimpleCV Feature library
#
# Tools return basic features in feature sets


#load system libraries
from SimpleCV.base import *
from SimpleCV.Color import *
import copy
import types

class FeatureSet(list):
    """
    **SUMMARY**

    FeatureSet is a class extended from Python's list which has special functions so that it is useful for handling feature metadata on an image.
    
    In general, functions dealing with attributes will return numpy arrays, and functions dealing with sorting or filtering will return new FeatureSets.
    
    **EXAMPLE**

    >>> image = Image("/path/to/image.png")
    >>> lines = image.findLines()  #lines are the feature set
    >>> lines.draw()
    >>> lines.x()
    >>> lines.crop()
    """
    def __getitem__(self,key):
        """
        **SUMMARY**

        Returns a FeatureSet when sliced. Previously used to
        return list. Now it is possible to use FeatureSet member
        functions on sub-lists

        """
        if type(key) is types.SliceType: #Or can use 'try:' for speed
            return FeatureSet(list.__getitem__(self, key))
        else:
            return list.__getitem__(self,key)
        
    def __getslice__(self, i, j):
        """
        Deprecated since python 2.0, now using __getitem__
        """
        return self.__getitem__(slice(i,j))
        
    def draw(self, color = Color.GREEN,width=1, autocolor = False):
        """
        **SUMMARY**

        Call the draw() method on each feature in the FeatureSet. 

        **PARAMETERS**
        
        * *color* - The color to draw the object. Either an BGR tuple or a member of the :py:class:`Color` class.
        * *width* - The width to draw the feature in pixels. A value of -1 usually indicates a filled region.
        * *autocolor* - If true a color is randomly selected for each feature. 

        **RETURNS**
        
        Nada. Nothing. Zilch. 

        **EXAMPLE**

        >>> img = Image("lenna")
        >>> feats = img.findBlobs()
        >>> feats.draw(color=Color.PUCE, width=3)
        >>> img.show()

        """
        for f in self:
            if(autocolor):
                color = Color().getRandom()
            f.draw(color=color,width=width)
    
    def show(self, color = Color.GREEN, autocolor = False,width=1):
        """
        **EXAMPLE**

        This function will automatically draw the features on the image and show it.
        It is a basically a shortcut function for development and is the same as:

        **PARAMETERS**
        
        * *color* - The color to draw the object. Either an BGR tuple or a member of the :py:class:`Color` class.
        * *width* - The width to draw the feature in pixels. A value of -1 usually indicates a filled region.
        * *autocolor* - If true a color is randomly selected for each feature. 

        **RETURNS**
        
        Nada. Nothing. Zilch. 


        **EXAMPLE**
        >>> img = Image("logo")
        >>> feat = img.findBlobs()
        >>> if feat: feat.draw()
        >>> img.show()

        """
        self.draw(color, width, autocolor)
        self[-1].image.show()
                
  
    def x(self):
        """
        **SUMMARY**

        Returns a numpy array of the x (horizontal) coordinate of each feature.

        **RETURNS**
        
        A numpy array.

        **EXAMPLE**

        >>> img = Image("lenna")
        >>> feats = img.findBlobs()
        >>> xs = feats.x()
        >>> print xs
        
        """
        return np.array([f.x for f in self])
  
    def y(self):
        """
        **SUMMARY**

        Returns a numpy array of the y (vertical) coordinate of each feature.

        **RETURNS**
        
        A numpy array.

        **EXAMPLE**

        >>> img = Image("lenna")
        >>> feats = img.findBlobs()
        >>> xs = feats.y()
        >>> print xs

        """
        return np.array([f.y for f in self])
  
    def coordinates(self):
        """
        **SUMMARY**

        Returns a 2d numpy array of the x,y coordinates of each feature.  This 
        is particularly useful if you want to use Scipy's Spatial Distance module 
        
        **RETURNS**
        
        A numpy array of all the positions in the featureset. 

        **EXAMPLE**

        >>> img = Image("lenna")
        >>> feats = img.findBlobs()
        >>> xs = feats.coordinates()
        >>> print xs


        """
        return np.array([[f.x, f.y] for f in self]) 
  
    def area(self):
        """
        **SUMMARY**

        Returns a numpy array of the area of each feature in pixels.

        **RETURNS**
        
        A numpy array of all the positions in the featureset. 

        **EXAMPLE**

        >>> img = Image("lenna")
        >>> feats = img.findBlobs()
        >>> xs = feats.area()
        >>> print xs

        """
        return np.array([f.area() for f in self]) 
  
    def sortArea(self):
        """
        **SUMMARY**
        
        Returns a new FeatureSet, with the largest area features first. 
        
        **RETURNS**
        
        A featureset sorted based on area.

        **EXAMPLE**

        >>> img = Image("lenna")
        >>> feats = img.findBlobs()
        >>> feats = feats.sortArea()
        >>> print feats[-1] # biggest blob
        >>> print feats[0] # smallest blob

        """
        return FeatureSet(sorted(self, key = lambda f: f.area()))
  
    def distanceFrom(self, point = (-1, -1)):
        """
        **SUMMARY**

        Returns a numpy array of the distance each Feature is from a given coordinate.
        Default is the center of the image. 

        **PARAMETERS**
        
        * *point* - A point on the image from which we will calculate distance. 
        
        **RETURNS**
        
        A numpy array of distance values. 

        **EXAMPLE**

        >>> img = Image("lenna")
        >>> feats = img.findBlobs()
        >>> d = feats.distanceFrom()
        >>> d[0]  #show the 0th blobs distance to the center. 

        **TO DO**

        Make this accept other features to measure from. 

        """
        if (point[0] == -1 or point[1] == -1 and len(self)):
            point = self[0].image.size()
            
        return spsd.cdist(self.coordinates(), [point])[:,0]
  
    def sortDistance(self, point = (-1, -1)):
        """
        **SUMMARY**

        Returns a sorted FeatureSet with the features closest to a given coordinate first.
        Default is from the center of the image. 

        **PARAMETERS**
        
        * *point* - A point on the image from which we will calculate distance. 
        
        **RETURNS**
        
        A numpy array of distance values. 

        **EXAMPLE**

        >>> img = Image("lenna")
        >>> feats = img.findBlobs()
        >>> d = feats.sortDistance()
        >>> d[-1].show()  #show the 0th blobs distance to the center. 


        """
        return FeatureSet(sorted(self, key = lambda f: f.distanceFrom(point)))
        
    def distancePairs(self):
        """
        **SUMMARY**

        Returns the square-form of pairwise distances for the featureset.
        The resulting N x N array can be used to quickly look up distances
        between features.

        **RETURNS**

        A NxN np matrix of distance values. 

        **EXAMPLE**

        >>> img = Image("lenna")
        >>> feats = img.findBlobs()
        >>> d = feats.distancePairs()
        >>> print d
                
        """
        return spsd.squareform(spsd.pdist(self.coordinates()))
  
    def angle(self):
        """
        **SUMMARY**

        Return a numpy array of the angles (theta) of each feature.
        Note that theta is given in degrees, with 0 being horizontal.

        **RETURNS**

        An array of angle values corresponding to the features.

        **EXAMPLE**

        >>> img = Image("lenna")
        >>> l = img.findLines()
        >>> angs = l.angle()
        >>> print angs
        

        """
        return np.array([f.angle() for f in self])
  
    def sortAngle(self, theta = 0):
        """
        Return a sorted FeatureSet with the features closest to a given angle first.
        Note that theta is given in radians, with 0 being horizontal.

        **RETURNS**

        An array of angle values corresponding to the features.

        **EXAMPLE**

        >>> img = Image("lenna")
        >>> l = img.findLines()
        >>> l = l.sortAngle()
        >>> print angs
        
        """
        return FeatureSet(sorted(self, key = lambda f: abs(f.angle() - theta)))
  
    def length(self):
        """
        **SUMMARY**

        Return a numpy array of the length (longest dimension) of each feature.

        **RETURNS**
        
        A numpy array of the length, in pixels, of eatch feature object.

        **EXAMPLE**
        
        >>> img = Image("Lenna")
        >>> l = img.findLines()
        >>> lengt = l.length()
        >>> lengt[0] # length of the 0th element. 
        
        """
       
        return np.array([f.length() for f in self])
  
    def sortLength(self):
        """
        **SUMMARY**
        
        Return a sorted FeatureSet with the longest features first. 

        **RETURNS**
        
        A sorted FeatureSet.

        **EXAMPLE**

        >>> img = Image("Lenna")
        >>> l = img.findLines().sortLength()
        >>> lengt[-1] # length of the 0th element. 
        
        """
        return FeatureSet(sorted(self, key = lambda f: f.length()))
  
    def meanColor(self):
        """
        **SUMMARY**

        Return a numpy array of the average color of the area covered by each Feature.

        **RETURNS**

        Returns an array of RGB triplets the correspond to the mean color of the feature.

        **EXAMPLE**

        >>> img = Image("lenna")
        >>> kp = img.findKeypoints()
        >>> c = kp.meanColor()

        
        """
        return np.array([f.meanColor() for f in self])
  
    def colorDistance(self, color = (0, 0, 0)):
        """
        **SUMMARY**

        Return a numpy array of the distance each features average color is from
        a given color tuple (default black, so colorDistance() returns intensity)

        **PARAMETERS**
        
        * *color* - The color to calculate the distance from.

        **RETURNS**
        
        The distance of the average color for the feature from given color as a numpy array.

        **EXAMPLE**

        >>> img = Image("lenna")
        >>> circs = img.findCircle()
        >>> d = circs.colorDistance(color=Color.BLUE)
        >>> print d

        """
        return spsd.cdist(self.meanColor(), [color])[:,0]
    
    def sortColorDistance(self, color = (0, 0, 0)):
        """
        Return a sorted FeatureSet with features closest to a given color first.
        Default is black, so sortColorDistance() will return darkest to brightest
        """
        return FeatureSet(sorted(self, key = lambda f: f.colorDistance(color)))
  
    def filter(self, filterarray):
        """
        **SUMMARY**

        Return a FeatureSet which is filtered on a numpy boolean array.  This
        will let you use the attribute functions to easily screen Features out
        of return FeatureSets.  
    
        **PARAMETERS**
        
        * *filterarray* - A numpy array, matching  the size of the feature set, 
          made of Boolean values, we return the true values and reject the False value.

        **RETURNS**
        
        The revised feature set. 

        **EXAMPLE**

        Return all lines < 200px

        >>> my_lines.filter(my_lines.length() < 200) # returns all lines < 200px
        >>> my_blobs.filter(my_blobs.area() > 0.9 * my_blobs.length**2) # returns blobs that are nearly square    
        >>> my_lines.filter(abs(my_lines.angle()) < numpy.pi / 4) #any lines within 45 degrees of horizontal
        >>> my_corners.filter(my_corners.x() - my_corners.y() > 0) #only return corners in the upper diagonal of the image
    
        """
        return FeatureSet(list(np.array(self)[np.array(filterarray)]))
  
    def width(self):
        """
        **SUMMARY**
        
        Returns a nparray which is the width of all the objects in the FeatureSet.

        **RETURNS**
        
        A numpy array of width values.

        
        **EXAMPLE**
        
        >>> img = Image("NotLenna")
        >>> l = img.findLines()
        >>> l.width()
        
        """
        return np.array([f.width() for f in self])
  
    def height(self):
        """
        Returns a nparray which is the height of all the objects in the FeatureSet

        **RETURNS**
        
        A numpy array of width values.

        
        **EXAMPLE**
        
        >>> img = Image("NotLenna")
        >>> l = img.findLines()
        >>> l.height()
        
        """
        return np.array([f.height() for f in self])
  
    def crop(self):
        """
        **SUMMARY**

        Returns a nparray with the cropped features as SimpleCV image.

        **RETURNS**

        A SimpleCV image cropped to each image.

        **EXAMPLE**

        >>> img = Image("Lenna")
        >>> blobs = img.findBlobs(128)
        >>> for b in blobs:
        >>>   newImg = b.crop()
        >>>   newImg.show()
        >>>   time.sleep(1)

        """
        return np.array([f.crop() for f in self])  

    def inside(self,region):
        """
        **SUMMARY**
        
        Return only the features inside the region. where region can be a bounding box,
        bounding circle, a list of tuples in a closed polygon, or any other featutres. 
        
        **PARAMETERS**
        
        * *region*

          * A bounding box - of the form (x,y,w,h) where x,y is the upper left corner
          * A bounding circle of the form (x,y,r)
          * A list of x,y tuples defining a closed polygon e.g. ((x,y),(x,y),....)
          * Any two dimensional feature (e.g. blobs, circle ...)
          
        **RETURNS**

        Returns a featureset of features that are inside the region.

        **EXAMPLE**
        
        >>> img = Image("Lenna")
        >>> blobs = img.findBlobs()
        >>> b = blobs[-1]
        >>> lines = img.findLines()
        >>> inside = lines.inside(b)

        **NOTE**
        
        This currently performs a bounding box test, not a full polygon test for speed. 


        """
        fs = FeatureSet()
        for f in self:
            if(f.isContainedWithin(region)):
                fs.append(f)
        return fs

        
    def outside(self,region):
        """
        **SUMMARY**
        
        Return only the features outside the region. where region can be a bounding box,
        bounding circle, a list of tuples in a closed polygon, or any other featutres. 
        
        **PARAMETERS**
        
        * *region*

          * A bounding box - of the form (x,y,w,h) where x,y is the upper left corner
          * A bounding circle of the form (x,y,r)
          * A list of x,y tuples defining a closed polygon e.g. ((x,y),(x,y),....)
          * Any two dimensional feature (e.g. blobs, circle ...)
          
        **RETURNS**
       
        Returns a featureset of features that are outside the region.


        **EXAMPLE**
        
        >>> img = Image("Lenna")
        >>> blobs = img.findBlobs()
        >>> b = blobs[-1]
        >>> lines = img.findLines()
        >>> outside = lines.outside(b)

        **NOTE**
        
        This currently performs a bounding box test, not a full polygon test for speed. 

        """
        fs = FeatureSet()
        for f in self:
            if(f.isNotContainedWithin(region)):
                fs.append(f)
        return fs

    def overlaps(self,region):
        """
        **SUMMARY**
        
        Return only the features that overlap or the region. Where region can be a bounding box,
        bounding circle, a list of tuples in a closed polygon, or any other featutres. 
        
        **PARAMETERS**
        
        * *region*

          * A bounding box - of the form (x,y,w,h) where x,y is the upper left corner
          * A bounding circle of the form (x,y,r)
          * A list of x,y tuples defining a closed polygon e.g. ((x,y),(x,y),....)
          * Any two dimensional feature (e.g. blobs, circle ...)
          
        **RETURNS**
       
        Returns a featureset of features that overlap the region.

        **EXAMPLE**
        
        >>> img = Image("Lenna")
        >>> blobs = img.findBlobs()
        >>> b = blobs[-1]
        >>> lines = img.findLines()
        >>> outside = lines.overlaps(b)

        **NOTE**
        
        This currently performs a bounding box test, not a full polygon test for speed. 

        """
        fs = FeatureSet()
        for f in self: 
            if( f.overlaps(region) ):
                fs.append(f)
        return fs

    def above(self,region):
        """
        **SUMMARY**
        
        Return only the features that are above a  region. Where region can be a bounding box,
        bounding circle, a list of tuples in a closed polygon, or any other featutres. 
        
        **PARAMETERS**
        
        * *region*

          * A bounding box - of the form (x,y,w,h) where x,y is the upper left corner
          * A bounding circle of the form (x,y,r)
          * A list of x,y tuples defining a closed polygon e.g. ((x,y),(x,y),....)
          * Any two dimensional feature (e.g. blobs, circle ...)
          
        **RETURNS**
       
        Returns a featureset of features that are above the region.

        **EXAMPLE**
        
        >>> img = Image("Lenna")
        >>> blobs = img.findBlobs()
        >>> b = blobs[-1]
        >>> lines = img.findLines()
        >>> outside = lines.above(b)

        **NOTE**
        
        This currently performs a bounding box test, not a full polygon test for speed. 

        """
        fs = FeatureSet()
        for f in self: 
            if(f.above(region)):
                fs.append(f)
        return fs

    def below(self,region):
        """
        **SUMMARY**
        
        Return only the features below the region. where region can be a bounding box,
        bounding circle, a list of tuples in a closed polygon, or any other featutres. 
        
        **PARAMETERS**
        
        * *region*

          * A bounding box - of the form (x,y,w,h) where x,y is the upper left corner
          * A bounding circle of the form (x,y,r)
          * A list of x,y tuples defining a closed polygon e.g. ((x,y),(x,y),....)
          * Any two dimensional feature (e.g. blobs, circle ...)
          
        **RETURNS**

        Returns a featureset of features that are below the region.

        **EXAMPLE**
        
        >>> img = Image("Lenna")
        >>> blobs = img.findBlobs()
        >>> b = blobs[-1]
        >>> lines = img.findLines()
        >>> inside = lines.below(b)

        **NOTE**
        
        This currently performs a bounding box test, not a full polygon test for speed. 

        """
        fs = FeatureSet()
        for f in self: 
            if(f.below(region)):
                fs.append(f)
        return fs

    def left(self,region):
        """
        **SUMMARY**
        
        Return only the features left of the region. where region can be a bounding box,
        bounding circle, a list of tuples in a closed polygon, or any other featutres. 
        
        **PARAMETERS**
        
        * *region*

          * A bounding box - of the form (x,y,w,h) where x,y is the upper left corner
          * A bounding circle of the form (x,y,r)
          * A list of x,y tuples defining a closed polygon e.g. ((x,y),(x,y),....)
          * Any two dimensional feature (e.g. blobs, circle ...)
          
        **RETURNS**

        Returns a featureset of features that are left of the region.

        **EXAMPLE**
        
        >>> img = Image("Lenna")
        >>> blobs = img.findBlobs()
        >>> b = blobs[-1]
        >>> lines = img.findLines()
        >>> left = lines.left(b)

        **NOTE**
        
        This currently performs a bounding box test, not a full polygon test for speed. 

        """
        fs = FeatureSet()
        for f in self: 
            if(f.left(region)):
                fs.append(f)
        return fs

    def right(self,region):
        """
        **SUMMARY**
        
        Return only the features right of the region. where region can be a bounding box,
        bounding circle, a list of tuples in a closed polygon, or any other featutres. 
        
        **PARAMETERS**
        
        * *region*

          * A bounding box - of the form (x,y,w,h) where x,y is the upper left corner
          * A bounding circle of the form (x,y,r)
          * A list of x,y tuples defining a closed polygon e.g. ((x,y),(x,y),....)
          * Any two dimensional feature (e.g. blobs, circle ...)
          
        **RETURNS**

        Returns a featureset of features that are right of the region.

        **EXAMPLE**
        
        >>> img = Image("Lenna")
        >>> blobs = img.findBlobs()
        >>> b = blobs[-1]
        >>> lines = img.findLines()
        >>> right = lines.right(b)

        **NOTE**
        
        This currently performs a bounding box test, not a full polygon test for speed. 

        """
        fs = FeatureSet()
        for f in self: 
            if(f.right(region)):
                fs.append(f)
        return fs
    
    @property
    def image(self):
        if not len(self):
            return None
        return self[0].image
    
    @image.setter
    def image(self, i):
        for f in self:
            f.image = i


class Feature(object):
    """
    **SUMMARY**

    The Feature object is an abstract class which real features descend from.
    Each feature object has:
    
    * a draw() method, 
    * an image property, referencing the originating Image object 
    * x and y coordinates
    * default functions for determining angle, area, meanColor, etc for FeatureSets
    * in the Feature class, these functions assume the feature is 1px  
    
    """
    x = 0.00
    y = 0.00 
    mMaxX = None
    mMaxY = None
    mMinX = None
    mMinY = None
    image = "" #parent image
    points = []
    boundingBox = []

    def __init__(self, i, at_x, at_y):
        self.x = at_x
        self.y = at_y
        self.image = i
  
    def coordinates(self):
        """
        **SUMMARY**

        Returns the x,y position of the feature. This is usually the center coordinate.

        **RETURNS**
        
        Returns an (x,y) tuple of the position of the feature. 

        **EXAMPLE**
        
        >>> img = Image("aerospace.png")
        >>> blobs = img.findBlobs()
        >>> for b in blobs:
        >>>    print b.coordinates()

        """
        return np.array([self.x, self.y])  
  
    def draw(self, color = Color.GREEN):
        """
        **SUMMARY**
        
        This method will draw the feature on the source image. 

        **PARAMETERS**
        
        * *color* - The color as an RGB tuple to render the image.
        
        **RETURNS**
        
        Nothing. 

        **EXAMPLE**
        
        >>> img = Image("RedDog2.jpg")
        >>> blobs = img.findBlobs()
        >>> blobs[-1].draw()
        >>> img.show()

        """
        self.image[self.x, self.y] = color
    
    def show(self, color = Color.GREEN):
        """
        **SUMMARY**

        This function will automatically draw the features on the image and show it.
       
        **RETURNS**

        Nothing.

        **EXAMPLE**

        >>> img = Image("logo")
        >>> feat = img.findBlobs()
        >>> feat[-1].show() #window pops up. 

        """
        self.draw(color)
        self.image.show()
  
    def distanceFrom(self, point = (-1, -1)): 
        """
        **SUMMARY**

        Given a point (default to center of the image), return the euclidean distance of x,y from this point. 

        **PARAMETERS**
        
        * *point* - The point, as an (x,y) tuple on the image to measure distance from. 

        **RETURNS**
        
        The distance as a floating point value in pixels. 

        **EXAMPLE**
        
        >>> img = Image("OWS.jpg")
        >>> blobs = img.findBlobs(128)
        >>> blobs[-1].distanceFrom(blobs[-2].coordinates())
        
        
        """
        if (point[0] == -1 or point[1] == -1):
            point = np.array(self.image.size()) / 2
        return spsd.euclidean(point, [self.x, self.y]) 
  
    def meanColor(self):
        """
        **SUMMARY**

        Return the average color within the feature as a tuple. 
        
        **RETURNS**

        An RGB color tuple. 

        **EXAMPLE**

        >>> img = Image("OWS.jpg")
        >>> blobs = img.findBlobs(128)
        >>> for b in blobs:
        >>>    if (b.meanColor() == color.WHITE):
        >>>       print "Found a white thing"
        
        """
        return self.image[self.x, self.y]
  
    def colorDistance(self, color = (0, 0, 0)): 
        """
        **SUMMARY**
        
        Return the euclidean color distance of the color tuple at x,y from a given color (default black).

        **PARAMETERS**
        
        * *color* - An RGB triplet to calculate from which to calculate the color distance.

        **RETURNS**
        
        A floating point color distance value. 

        **EXAMPLE**

        >>> img = Image("OWS.jpg")
        >>> blobs = img.findBlobs(128)
        >>> for b in blobs:
        >>>    print b.colorDistance(color.WHITE):
         
        """
        return spsd.euclidean(np.array(color), np.array(self.meanColor())) 
  
    def angle(self):
        """
        **SUMMARY**

        Return the angle (theta) in degrees of the feature. The default is 0 (horizontal).
        
        .. Warning:: 
          This is not a valid operation for all features.

         
        **RETURNS**
        
        An angle value in degrees. 

        **EXAMPLE**
        
        >>> img = Image("OWS.jpg")
        >>> blobs = img.findBlobs(128)
        >>> for b in blobs:
        >>>    if b.angle() == 0:
        >>>       print "I AM HORIZONTAL."

        **TODO**
        
        Double check that values are being returned consistently. 
        """
        return 0
  
    def length(self):
        """
        **SUMMARY**
        
        This method returns the longest dimension of the feature (i.e max(width,height)). 
        
        **RETURNS**
        
        A floating point length value. 

        **EXAMPLE**
       
        >>> img = Image("OWS.jpg")
        >>> blobs = img.findBlobs(128)
        >>> for b in blobs:
        >>>    if b.length() > 200:
        >>>       print "OH MY! - WHAT A BIG FEATURE YOU HAVE!" 
        >>>       print "---I bet you say that to all the features."
       
        **TODO**

        Should this be sqrt(x*x+y*y)?
        """
        return 1
  
    def area(self):
        """
        **SUMMARY** 

        Returns the area (number of pixels)  covered by the feature.

        **RETURNS**
        
        An integer area of the feature.

        **EXAMPLE**

        >>> img = Image("OWS.jpg")
        >>> blobs = img.findBlobs(128)
        >>> for b in blobs:
        >>>    if b.area() > 200:
        >>>       print b.area()       
        
        """
        return self.width() * self.height()
  
    def width(self):
        """
        **SUMMARY**
        
        Returns the height of the feature. 

        **RETURNS**

        An integer value for the feature's width.

        **EXAMPLE**

        >>> img = Image("OWS.jpg")
        >>> blobs = img.findBlobs(128)
        >>> for b in blobs:
        >>>    if b.width() > b.height():
        >>>       print "wider than tall"
        >>>       b.draw()
        >>> img.show()

        """
        maxX = float("-infinity")
        minX = float("infinity")
        if(len(self.points) <= 0):
            return 1
        
        for p in self.points:
            if(p[0] > maxX):
                maxX = p[0]
            if(p[0] < minX):
                minX = p[0]
            
        return maxX - minX
  
    def height(self):
        """
        **SUMMARY**
        
        Returns the height of the feature. 

        **RETURNS**

        An integer value of the feature's height.

        **EXAMPLE**

        >>> img = Image("OWS.jpg")
        >>> blobs = img.findBlobs(128)
        >>> for b in blobs:
        >>>    if b.width() > b.height():
        >>>       print "wider than tall"
        >>>       b.draw()
        >>> img.show()
        """
        maxY = float("-infinity")
        minY = float("infinity")
        if(len(self.points) <= 0):
            return 1
      
        for p in self.points:
            if(p[1] > maxY):
                maxY = p[1]
            if(p[1] < minY):
                minY = p[1]
        
        return maxY - minY

   
    def crop(self):
        """
        **SUMMARY**

        This function crops the source image to the location of the feature and returns 
        a new SimpleCV image.
        
        **RETURNS**
        
        A SimpleCV image that is cropped to the feature position and size.

        **EXAMPLE**

        >>> img = Image("OWS.jpg")
        >>> blobs = img.findBlobs(128)
        >>> big = blobs[-1].crop()
        >>> big.show()

        """
    
        return self.image.crop(self.x, self.y, self.width(), self.height(), centered = True)
    
    def __repr__(self):
        return "%s.%s at (%d,%d)" % (self.__class__.__module__, self.__class__.__name__, self.x, self.y)


    def _updateExtents(self):
        if( self.mMaxX is None or self.mMaxY is None or 
            self.mMinX is None or self.mMinY is None):
            self.mMaxX = float("-infinity")
            self.mMaxY = float("-infinity")
            self.mMinX = float("infinity")
            self.mMinY = float("infinity")
            for p in self.points:
                if( p[0] > self.mMaxX):
                    self.mMaxX = p[0] 
                if( p[0] < self.mMinX):
                    self.mMinX = p[0]
                if( p[1] > self.mMaxY):
                    self.mMaxY = p[1]
                if( p[1] < self.mMinY):
                    self.mMinY = p[1]
            
            self.boundingBox = [(self.mMinX,self.mMinY),(self.mMinX,self.mMaxY),(self.mMaxX,self.mMaxY),(self.mMaxX,self.mMinY)]
            
    def boundingBox(self):
        """
        **SUMMARY**
        
        This function calculates the corners of the feature and returns them as 
        a list of (x,y) tuples.

        **RETURNS**
        
        A list of (x,y) corner tuples. The order is top left, bottom left, bottom right, top right. 
        **EXAMPLE**

        >>> img = Image("OWS.jpg")
        >>> blobs = img.findBlobs(128)
        >>> print blobs[-1].boundingBox()
        
        **TO DO**

        Make the order of points go from the top left glockwise.

        """
        self._updateExtents()
        return self.boundingBox

    def extents(self):
        """
        **SUMMARY**
        
        This function returns the maximum and minimum x and y values for the feature and 
        returns them as a tuple. 

        **RETURNS**
        
        A tuple of the extents of the feature. The order is (MaxX,MaxY,MinX,MinY).

        **EXAMPLE**

        >>> img = Image("OWS.jpg")
        >>> blobs = img.findBlobs(128)
        >>> print blobs[-1].extents()
        
        """
        self._updateExtents()
        return (self.mMaxX,self.mMaxY,self.mMinX,self.mMinY)

    def minY(self):
        """
        **SUMMARY**

        This method return the minimum y value of the bounding box of the
        the feature.

        **RETURNS**
        
        An integer value of the minimum y value of the feature.

        **EXAMPLE**

        >>> img = Image("OWS.jpg")
        >>> blobs = img.findBlobs(128)
        >>> print blobs[-1].minY()
        
        """
        self._updateExtents()
        return self.mMinY
        
    def maxY(self):
        """
        **SUMMARY**

        This method return the maximum y value of the bounding box of the
        the feature.

        **RETURNS**
        
        An integer value of the maximum y value of the feature.

        **EXAMPLE**

        >>> img = Image("OWS.jpg")
        >>> blobs = img.findBlobs(128)
        >>> print blobs[-1].maxY()

        """       
        self._updateExtents()
        return self.mMaxY


    def minX(self):
        """
        **SUMMARY**

        This method return the minimum x value of the bounding box of the
        the feature.

        **RETURNS**
        
        An integer value of the minimum x value of the feature.

        **EXAMPLE**

        >>> img = Image("OWS.jpg")
        >>> blobs = img.findBlobs(128)
        >>> print blobs[-1].minX()

        """
        self._updateExtents()
        return self.mMinX
        
    def maxX(self):
        """
        **SUMMARY**

        This method return the minimum x value of the bounding box of the
        the feature.

        **RETURNS**
        
        An integer value of the maxium x value of the feature.

        **EXAMPLE**

        >>> img = Image("OWS.jpg")
        >>> blobs = img.findBlobs(128)
        >>> print blobs[-1].maxX()

        """       
        self._updateExtents()
        return self.mMaxX

    def topLeftCorner(self):
        """
        **SUMMARY**

        This method returns the top left corner of the bounding box of
        the blob as an (x,y) tuple.

        **RESULT**
        
        Returns a tupple of the top left corner.

        **EXAMPLE**
        
        >>> img = Image("OWS.jpg")
        >>> blobs = img.findBlobs(128)
        >>> print blobs[-1].topLeftCorner() 

        """
        self._updateExtents()
        return (self.mMinX,self.mMinY)

    def bottomRightCorner(self):
        """
        **SUMMARY**

        This method returns the bottom right corner of the bounding box of
        the blob as an (x,y) tuple.

        **RESULT**
        
        Returns a tupple of the bottom right corner.

        **EXAMPLE**
        
        >>> img = Image("OWS.jpg")
        >>> blobs = img.findBlobs(128)
        >>> print blobs[-1].bottomRightCorner() 

        """        
        self._updateExtents()
        return (self.mMaxX,self.mMaxY)
        
    def bottomLeftCorner(self):
        """
        **SUMMARY**

        This method returns the bottom left corner of the bounding box of
        the blob as an (x,y) tuple.

        **RESULT**
        
        Returns a tupple of the bottom left corner.

        **EXAMPLE**
        
        >>> img = Image("OWS.jpg")
        >>> blobs = img.findBlobs(128)
        >>> print blobs[-1].bottomLeftCorner() 

        """ 
        self._updateExtents()
        return (self.mMinX,self.mMaxY)
        
    def topRightCorner(self):
        """
        **SUMMARY**

        This method returns the top right corner of the bounding box of
        the blob as an (x,y) tuple.

        **RESULT**
        
        Returns a tupple of the top right  corner.

        **EXAMPLE**
        
        >>> img = Image("OWS.jpg")
        >>> blobs = img.findBlobs(128)
        >>> print blobs[-1].topRightCorner() 

        """        
        self._updateExtents()
        return (self.mMaxX,self.mMinY)


    def above(self,object):
        """
        **SUMMARY**
        
        Return true if the feature is above the object, where object can be a bounding box,
        bounding circle, a list of tuples in a closed polygon, or any other featutres. 
        
        **PARAMETERS**
        
        * *object*

          * A bounding box - of the form (x,y,w,h) where x,y is the upper left corner
          * A bounding circle of the form (x,y,r)
          * A list of x,y tuples defining a closed polygon e.g. ((x,y),(x,y),....)
          * Any two dimensional feature (e.g. blobs, circle ...)
          
        **RETURNS**

        Returns a Boolean, True if the feature is above the object, False otherwise.

        **EXAMPLE**
        
        >>> img = Image("Lenna")
        >>> blobs = img.findBlobs()
        >>> b = blobs[0]
        >>> if( blobs[-1].above(b) ):
        >>>    Print "above the biggest blob"

        """
        if( isinstance(object,Feature) ): 
            return( self.maxY() < object.minY() )
        elif( isinstance(object,tuple) or isinstance(object,np.ndarray) ):
            return( self.maxY() < object[1]  )
        elif( isinstance(object,float) or isinstance(object,int) ):
            return( self.maxY() < object )
        else:
            warnings.warn("SimpleCV did not recognize the input type to feature.above(). This method only takes another feature, an (x,y) tuple, or a ndarray type.")
            return None
    
    def below(self,object):
        """
        **SUMMARY**
        
        Return true if the feature is below the object, where object can be a bounding box,
        bounding circle, a list of tuples in a closed polygon, or any other featutres. 
        
        **PARAMETERS**
        
        * *object*

          * A bounding box - of the form (x,y,w,h) where x,y is the upper left corner
          * A bounding circle of the form (x,y,r)
          * A list of x,y tuples defining a closed polygon e.g. ((x,y),(x,y),....)
          * Any two dimensional feature (e.g. blobs, circle ...)
          
        **RETURNS**

        Returns a Boolean, True if the feature is below the object, False otherwise.

        **EXAMPLE**
        
        >>> img = Image("Lenna")
        >>> blobs = img.findBlobs()
        >>> b = blobs[0]
        >>> if( blobs[-1].below(b) ):
        >>>    Print "above the biggest blob"

        """    
        if( isinstance(object,Feature) ): 
            return( self.minY() > object.maxY() )
        elif( isinstance(object,tuple) or isinstance(object,np.ndarray) ):
            return( self.minY() > object[1]  )
        elif( isinstance(object,float) or isinstance(object,int) ):
            return( self.minY() > object )
        else:
            warnings.warn("SimpleCV did not recognize the input type to feature.below(). This method only takes another feature, an (x,y) tuple, or a ndarray type.")
            return None
 
     
    def right(self,object):
        """
        **SUMMARY**
        
        Return true if the feature is to the right object, where object can be a bounding box,
        bounding circle, a list of tuples in a closed polygon, or any other featutres. 
        
        **PARAMETERS**
        
        * *object*

          * A bounding box - of the form (x,y,w,h) where x,y is the upper left corner
          * A bounding circle of the form (x,y,r)
          * A list of x,y tuples defining a closed polygon e.g. ((x,y),(x,y),....)
          * Any two dimensional feature (e.g. blobs, circle ...)
          
        **RETURNS**

        Returns a Boolean, True if the feature is to the right object, False otherwise.

        **EXAMPLE**
        
        >>> img = Image("Lenna")
        >>> blobs = img.findBlobs()
        >>> b = blobs[0]
        >>> if( blobs[-1].right(b) ):
        >>>    Print "right of the the blob"

        """
        if( isinstance(object,Feature) ): 
            return( self.minX() > object.maxX() )
        elif( isinstance(object,tuple) or isinstance(object,np.ndarray) ):
            return( self.minX() > object[0]  )
        elif( isinstance(object,float) or isinstance(object,int) ):
            return( self.minX() > object )
        else:
            warnings.warn("SimpleCV did not recognize the input type to feature.right(). This method only takes another feature, an (x,y) tuple, or a ndarray type.")
            return None

    def left(self,object):
        """
        **SUMMARY**
        
        Return true if the feature is to the left of  the object, where object can be a bounding box,
        bounding circle, a list of tuples in a closed polygon, or any other featutres. 
        
        **PARAMETERS**
        
        * *object*

          * A bounding box - of the form (x,y,w,h) where x,y is the upper left corner
          * A bounding circle of the form (x,y,r)
          * A list of x,y tuples defining a closed polygon e.g. ((x,y),(x,y),....)
          * Any two dimensional feature (e.g. blobs, circle ...)
          
        **RETURNS**

        Returns a Boolean, True if the feature is to the left of  the object, False otherwise.

        **EXAMPLE**
        
        >>> img = Image("Lenna")
        >>> blobs = img.findBlobs()
        >>> b = blobs[0]
        >>> if( blobs[-1].left(b) ):
        >>>    Print "left of  the biggest blob"


        """           
        if( isinstance(object,Feature) ): 
            return( self.maxX() < object.minX() )
        elif( isinstance(object,tuple) or isinstance(object,np.ndarray) ):
            return( self.maxX() < object[0]  )
        elif( isinstance(object,float) or isinstance(object,int) ):
            return( self.maxX() < object )
        else:
            warnings.warn("SimpleCV did not recognize the input type to feature.left(). This method only takes another feature, an (x,y) tuple, or a ndarray type.")
            return None

    def contains(self,other):
        """
        **SUMMARY**
        
        Return true if the feature contains  the object, where object can be a bounding box,
        bounding circle, a list of tuples in a closed polygon, or any other featutres. 
        
        **PARAMETERS**
        
        * *object*

          * A bounding box - of the form (x,y,w,h) where x,y is the upper left corner
          * A bounding circle of the form (x,y,r)
          * A list of x,y tuples defining a closed polygon e.g. ((x,y),(x,y),....)
          * Any two dimensional feature (e.g. blobs, circle ...)
          
        **RETURNS**

        Returns a Boolean, True if the feature contains the object, False otherwise.

        **EXAMPLE**
        
        >>> img = Image("Lenna")
        >>> blobs = img.findBlobs()
        >>> b = blobs[0]
        >>> if( blobs[-1].contains(b) ):
        >>>    Print "this blob is contained in the biggest blob"

        **NOTE**
        
        This currently performs a bounding box test, not a full polygon test for speed. 

        """
        retVal = False
        bounds = self.boundingBox
        if( isinstance(other,Feature) ):# A feature
            retVal = True
            for p in other.points: # this isn't completely correct - only tests if points lie in poly, not edges.            
                p2 = (int(p[0]),int(p[1]))
                retVal = self._pointInsidePolygon(p2,bounds)
                if( not retVal ):
                    break
        # a single point        
        elif( (isinstance(other,tuple) and len(other)==2) or ( isinstance(other,np.ndarray) and other.shape[0]==2) ):
            retVal = self._pointInsidePolygon(other,bounds)

        elif( isinstance(other,tuple) and len(other)==3 ): # A circle
            #assume we are in x,y, r format 
            retVal = True
            rr = other[2]*other[2]
            x = other[0]
            y = other[1]
            for p in bounds:
                test = ((x-p[0])*(x-p[0]))+((y-p[1])*(y-p[1]))
                if( test < rr ):
                    retVal = False
                    break

        elif( isinstance(other,tuple) and len(other)==4 and ( isinstance(other[0],float) or isinstance(other[0],int))): 
            retVal = ( self.maxX() <= other[0]+other[2] and
                       self.minX() >= other[0] and
                       self.maxY() <= other[1]+other[3] and
                       self.minY() >= other[1] )
        elif(isinstance(other,list) and len(other) >= 4): # an arbitrary polygon
            #everything else .... 
            retVal = True
            for p in other:
                test = self._pointInsidePolygon(p,bounds)
                if(not test):
                    retVal = False
                    break
        else:
            warnings.warn("SimpleCV did not recognize the input type to features.contains. This method only takes another blob, an (x,y) tuple, or a ndarray type.")
            return False  

        return retVal

    def overlaps(self, other):
        """
        **SUMMARY**
        
        Return true if the feature overlaps the object, where object can be a bounding box,
        bounding circle, a list of tuples in a closed polygon, or any other featutres. 
        
        **PARAMETERS**
        
        * *object*

          * A bounding box - of the form (x,y,w,h) where x,y is the upper left corner
          * A bounding circle of the form (x,y,r)
          * A list of x,y tuples defining a closed polygon e.g. ((x,y),(x,y),....)
          * Any two dimensional feature (e.g. blobs, circle ...)
          
        **RETURNS**

        Returns a Boolean, True if the feature overlaps  object, False otherwise.

        **EXAMPLE**
        
        >>> img = Image("Lenna")
        >>> blobs = img.findBlobs()
        >>> b = blobs[0]
        >>> if( blobs[-1].overlaps(b) ):
        >>>    Print "This blob overlaps the biggest blob"

        Returns true if this blob contains at least one point, part of a collection
        of points, or any part of a blob.        

        **NOTE**
        
        This currently performs a bounding box test, not a full polygon test for speed. 
 
       """
        retVal = False
        bounds = self.boundingBox
        if( isinstance(other,Feature) ):# A feature
            retVal = True            
            for p in other.boundingBox: # this isn't completely correct - only tests if points lie in poly, not edges. 
                retVal = self._pointInsidePolygon(p,bounds)
                if( retVal ):
                    break
                
        elif( (isinstance(other,tuple) and len(other)==2) or ( isinstance(other,np.ndarray) and other.shape[0]==2) ):
            retVal = self._pointInsidePolygon(other,bounds)

        elif( isinstance(other,tuple) and len(other)==3 and not isinstance(other[0],tuple)): # A circle
            #assume we are in x,y, r format 
            retVal = False
            rr = other[2]*other[2]
            x = other[0]
            y = other[1]
            for p in bounds:
                test = ((x-p[0])*(x-p[0]))+((y-p[1])*(y-p[1]))
                if( test < rr ):
                    retVal = True
                    break

        elif( isinstance(other,tuple) and len(other)==4 and ( isinstance(other[0],float) or isinstance(other[0],int))): 
            retVal = ( self.contains( (other[0],other[1] ) ) or # see if we contain any corner
                       self.contains( (other[0]+other[2],other[1] ) ) or
                       self.contains( (other[0],other[1]+other[3] ) ) or
                       self.contains( (other[0]+other[2],other[1]+other[3] ) ) )
        elif(isinstance(other,list) and len(other)  >= 3): # an arbitrary polygon
            #everything else .... 
            retVal = False
            for p in other:
                test = self._pointInsidePolygon(p,bounds)
                if(test):
                    retVal = True
                    break
        else:
            warnings.warn("SimpleCV did not recognize the input type to features.overlaps. This method only takes another blob, an (x,y) tuple, or a ndarray type.")
            return False  

        return retVal

    def doesNotContain(self, other):
        """
        **SUMMARY**
        
        Return true if the feature does not contain  the other object, where other can be a bounding box,
        bounding circle, a list of tuples in a closed polygon, or any other featutres. 
        
        **PARAMETERS**
        
        * *other*

          * A bounding box - of the form (x,y,w,h) where x,y is the upper left corner
          * A bounding circle of the form (x,y,r)
          * A list of x,y tuples defining a closed polygon e.g. ((x,y),(x,y),....)
          * Any two dimensional feature (e.g. blobs, circle ...)
          
        **RETURNS**

        Returns a Boolean, True if the feature does not contain the object, False otherwise.

        **EXAMPLE**
        
        >>> img = Image("Lenna")
        >>> blobs = img.findBlobs()
        >>> b = blobs[0]
        >>> if( blobs[-1].doesNotContain(b) ):
        >>>    Print "above the biggest blob"

        Returns true if all of features points are inside this point.
        """
        return not self.contains(other)

    def doesNotOverlap( self, other):
        """
        **SUMMARY**
        
        Return true if the feature does not overlap the object other, where other can be a bounding box,
        bounding circle, a list of tuples in a closed polygon, or any other featutres. 
        
        **PARAMETERS**
        
        * *other*

          * A bounding box - of the form (x,y,w,h) where x,y is the upper left corner
          * A bounding circle of the form (x,y,r)
          * A list of x,y tuples defining a closed polygon e.g. ((x,y),(x,y),....)
          * Any two dimensional feature (e.g. blobs, circle ...)
          
        **RETURNS**

        Returns a Boolean, True if the feature does not Overlap  the object, False otherwise.

        **EXAMPLE**
        
        >>> img = Image("Lenna")
        >>> blobs = img.findBlobs()
        >>> b = blobs[0]
        >>> if( blobs[-1].doesNotOverlap(b) ):
        >>>    Print "does not over overlap biggest blob"


        """
        return not self.overlaps( other)


    def isContainedWithin(self,other):
        """
        **SUMMARY**
        
        Return true if the feature is contained withing  the object other, where other can be a bounding box,
        bounding circle, a list of tuples in a closed polygon, or any other featutres. 
        
        **PARAMETERS**
        
        * *other*

          * A bounding box - of the form (x,y,w,h) where x,y is the upper left corner
          * A bounding circle of the form (x,y,r)
          * A list of x,y tuples defining a closed polygon e.g. ((x,y),(x,y),....)
          * Any two dimensional feature (e.g. blobs, circle ...)
          
        **RETURNS**

        Returns a Boolean, True if the feature is above the object, False otherwise.

        **EXAMPLE**
        
        >>> img = Image("Lenna")
        >>> blobs = img.findBlobs()
        >>> b = blobs[0]
        >>> if( blobs[-1].isContainedWithin(b) ):
        >>>    Print "inside the blob"

        """
        retVal = True
        bounds = self.boundingBox

        if( isinstance(other,Feature) ): # another feature do the containment test
            retVal = other.contains(self)
        elif( isinstance(other,tuple) and len(other)==3 ): # a circle
            #assume we are in x,y, r format 
            rr = other[2]*other[2] # radius squared
            x = other[0]
            y = other[1]
            for p in bounds:
                test = ((x-p[0])*(x-p[0]))+((y-p[1])*(y-p[1]))
                if( test > rr ):
                    retVal = False
                    break
        elif( isinstance(other,tuple) and len(other)==4 and  # a bounding box
            ( isinstance(other[0],float) or isinstance(other[0],int))): # we assume a tuple of four is (x,y,w,h)
            retVal = ( self.maxX() <= other[0]+other[2] and
                       self.minX() >= other[0] and
                       self.maxY() <= other[1]+other[3] and
                       self.minY() >= other[1] )
        elif(isinstance(other,list) and len(other) > 2 ): # an arbitrary polygon
            #everything else .... 
            retVal = True
            for p in bounds:
                test = self._pointInsidePolygon(p,other)
                if(not test):
                    retVal = False
                    break

        else:
            warnings.warn("SimpleCV did not recognize the input type to features.contains. This method only takes another blob, an (x,y) tuple, or a ndarray type.")
            retVal = False
        return retVal


    def isNotContainedWithin(self,shape):
        """
        **SUMMARY**
        
        Return true if the feature is not contained within the shape, where shape can be a bounding box,
        bounding circle, a list of tuples in a closed polygon, or any other featutres. 
        
        **PARAMETERS**
        
        * *shape*

          * A bounding box - of the form (x,y,w,h) where x,y is the upper left corner
          * A bounding circle of the form (x,y,r)
          * A list of x,y tuples defining a closed polygon e.g. ((x,y),(x,y),....)
          * Any two dimensional feature (e.g. blobs, circle ...)
          
        **RETURNS**

        Returns a Boolean, True if the feature is not contained within the shape, False otherwise.

        **EXAMPLE**
        
        >>> img = Image("Lenna")
        >>> blobs = img.findBlobs()
        >>> b = blobs[0]
        >>> if( blobs[-1].isNotContainedWithin(b) ):
        >>>    Print "Not inside the biggest blob"

        """
        return not self.isContainedWithin(shape)

    def _pointInsidePolygon(self,point,polygon):
        """
        returns true if tuple point (x,y) is inside polygon of the form ((a,b),(c,d),...,(a,b)) the polygon should be closed
        Adapted for python from:
        Http://paulbourke.net/geometry/insidepoly/
        """
        if( len(polygon) < 3 ):
            warnings.warn("feature._pointInsidePolygon - this is not a valid polygon")
            return False 
 
        counter = 0
        retVal = True
        p1 = None
        
        poly = copy.deepcopy(polygon)
        poly.append(polygon[0])
   #     for p2 in poly:
        N = len(poly)
        p1 = poly[0]
        for i in range(1,N+1):
            p2 = poly[i%N]
            if( point[1] > np.min((p1[1],p2[1])) ):
                if( point[1] <= np.max((p1[1],p2[1])) ):
                    if( point[0] <= np.max((p1[0],p2[0])) ):
                        if( p1[1] != p2[1] ):
                            test = float((point[1]-p1[1])*(p2[0]-p1[0]))/float(((p2[1]-p1[1])+p1[0]))
                            if( p1[0] == p2[0] or point[0] <= test ):
                                counter = counter + 1
            p1 = p2                
                                    
        if( counter % 2 == 0 ):
            retVal = False
        return retVal

#--------------------------------------------- 
