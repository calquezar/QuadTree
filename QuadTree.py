#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul  9 09:40:03 2019

@author: calquezar
"""
###########################################################################
from matplotlib import pyplot as plt
from matplotlib import patches
###########################################################################
class QPoint:
  
  def __init__(self,posX,posY):
    self.x=posX
    self.y=posY
  def __str__(self):
    return "(x: "+str(self.x)+", y: "+str(self.y)+")"
  
  def getMinX(points):
    return min([p.x for p in points])
  
  def getMaxX(points):
    return max([p.x for p in points])
  
  def getMinY(points):
    return min([p.y for p in points])
  
  def getMaxY(points):
    return max([p.y for p in points])
###########################################################################
class QNode:
  
  def __init__(self,minx,miny,width,height):
    self.position = QPoint(minx,miny) #bottom-left corner
    self.width = width
    self.height = height
    self.points = []
    self.children = []
    self.nodeID = "0"
    self.centerOfMass = []
    
  def __str__(self,tabs=1):
    output = "Node:"+self.nodeID+", Number of points: "+str(len(self.points))+ \
             ", Number of children: "+str(len(self.children))
    if (len(self.children)==0):
      return output
    else:
      children = ""
      for c in self.children:
        children+= "\n"+"\t"*tabs+"|+" + c.__str__(tabs+1)
      return output+children
  
  def setCenterOfMass(self):
    if(len(self.points)>0):
      x = ((float)(sum([p.x for p in self.points])))/len(self.points)
      y = ((float)(sum([p.y for p in self.points])))/len(self.points)
      self.centerOfMass = QPoint(x,y)
    
  def getAllCentersOfMasses(self):
    if(len(self.children)==0):
        return []
    else:
      centers = []
      for c in self.children:
        centers+= c.getCenterOfMass()
      centers+=[self.centerOfMass]
      return centers
    
  def getLeaves(self):
    if(len(self.children)==0):
      return [self]
    else:
      leaves = []
      for c in self.children:
        leaves+= c.getLeaves()
      return leaves
###########################################################################
class QuadTree:
  
  def __init__(self, points,threshold = 1):
    self.threshold = threshold
    self.root = self.generateTree(points)
    
  def __str__(self):
    if(self.root!=[]):
      return self.root.__str__()
    else:
      return "Empty tree"
    
  def generateTree(self,points,x=0,y=0,w=0,h=0,nodeID="0"):

    if(len(points)>self.threshold):      
      if(nodeID=="0"): #root node
        minx = QPoint.getMinX(points)
        miny = QPoint.getMinY(points)
        width = QPoint.getMaxX(points)-minx
        height = QPoint.getMaxY(points)-miny
      else:
        minx =x
        miny =y
        width = w
        height = h
      node = QNode(minx,miny,width,height)
      node.nodeID=nodeID
      node.points = points
      node.setCenterOfMass()
      """
                  +-------+-------+ ^
                  |       |       | |
                  | ch21  | ch22  | |
                  +-------+-------+ (height)
                  |       |       | |
                  | ch11  | ch12  | |
      (minx,miny) +-------+-------+ v
                  <----(width)---->
      """
#      print(minx,miny,minx+width,miny+height)
      points11 = [p for p in points if (p.x < minx+width/2) & (p.y < miny+height/2)]
      ch11 = self.generateTree(points11,minx,miny,width/2,height/2,"11")
      
      points12 = [p for p in points if (p.x >= minx+width/2) & (p.y < miny+height/2)]
      ch12 = self.generateTree(points12,minx+width/2,miny,width/2,height/2,"12")
      
      points21 = [p for p in points if (p.x < minx+width/2) & (p.y >= miny+height/2)]
      ch21 = self.generateTree(points21,minx,miny+height/2,width/2,height/2,"21")
      
      points22 = [p for p in points if (p.x >= minx+width/2) & (p.y >= miny+height/2)]
      ch22 = self.generateTree(points22,minx+width/2,miny+height/2,width/2,height/2,"22")
      
      node.children = [ch11,ch12,ch21,ch22]
      return node
    else:
      node = QNode(x,y,w,h)
      node.nodeID=nodeID
      node.points = points
      node.setCenterOfMass()
      return node

  def plot(self):
    fig = plt.figure(figsize=(12, 8))
    plt.title("Quadtree")
    ax = fig.add_subplot(111)
    leaves = self.root.getLeaves()
    for region in leaves:
        ax.add_patch(patches.Rectangle((region.position.x, region.position.y),\
                                       region.width, region.height, fill=False))
    x = [point.x for point in self.root.points]
    y = [point.y for point in self.root.points]
    plt.plot(x, y, 'ro',color='r',markersize=3)
    plt.show()
    return
##############################################################
import random
points = [QPoint(random.uniform(0, 10), random.uniform(0, 10)) for x in range(10)]
q = QuadTree(points,1)
print(q)
q.plot()
