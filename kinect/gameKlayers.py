#!/usr/bin/env python
# PyKinect
# Copyright(c) Microsoft Corporation
# All rights reserved.
# 
# Licensed under the Apache License, Version 2.0 (the License); you may not use
# this file except in compliance with the License. You may obtain a copy of the
# License at http://www.apache.org/licenses/LICENSE-2.0
# 
# THIS CODE IS PROVIDED ON AN  *AS IS* BASIS, WITHOUT WARRANTIES OR CONDITIONS
# OF ANY KIND, EITHER EXPRESS OR IMPLIED, INCLUDING WITHOUT LIMITATION ANY
# IMPLIED WARRANTIES OR CONDITIONS OF TITLE, FITNESS FOR A PARTICULAR PURPOSE,
# MERCHANTABLITY OR NON-INFRINGEMENT.
# 
# See the Apache Version 2.0 License for specific language governing
# permissions and limitations under the License.

from gimpfu import *
import thread
import itertools
import ctypes

import pykinect
from pykinect import nui
from pykinect.nui import JointId

import pygame
from pygame.color import THECOLORS
from pygame.locals import *

def gameK():
    KINECTEVENT = pygame.USEREVENT
    DEPTH_WINSIZE = 320,240
    VIDEO_WINSIZE = 640,480
    pygame.init()

    SKELETON_COLORS = [THECOLORS["red"], 
                       THECOLORS["blue"], 
                       THECOLORS["green"], 
                       THECOLORS["orange"], 
                       THECOLORS["purple"], 
                       THECOLORS["yellow"], 
                       THECOLORS["violet"]]

    LEFT_ARM = (JointId.ShoulderCenter, 
                JointId.ShoulderLeft, 
                JointId.ElbowLeft, 
                JointId.WristLeft, 
                JointId.HandLeft)
    RIGHT_ARM = (JointId.ShoulderCenter, 
                 JointId.ShoulderRight, 
                 JointId.ElbowRight, 
                 JointId.WristRight, 
                 JointId.HandRight)
    LEFT_LEG = (JointId.HipCenter, 
                JointId.HipLeft, 
                JointId.KneeLeft, 
                JointId.AnkleLeft, 
                JointId.FootLeft)
    RIGHT_LEG = (JointId.HipCenter, 
                 JointId.HipRight, 
                 JointId.KneeRight, 
                 JointId.AnkleRight, 
                 JointId.FootRight)
    SPINE = (JointId.HipCenter, 
             JointId.Spine, 
             JointId.ShoulderCenter, 
             JointId.Head)

    skeleton_to_depth_image = nui.SkeletonEngine.skeleton_to_depth_image

    def draw_skeleton_data(pSkelton, index, positions, width = 4):
        start = pSkelton.SkeletonPositions[positions[0]]
           
        for position in itertools.islice(positions, 1, None):
            next = pSkelton.SkeletonPositions[position.value]
            
            curstart = skeleton_to_depth_image(start, dispInfo.current_w, dispInfo.current_h) 
            curend = skeleton_to_depth_image(next, dispInfo.current_w, dispInfo.current_h)

            pygame.draw.line(screen, SKELETON_COLORS[index], curstart, curend, width)
            
            start = next

    # recipe to get address of surface: http://archives.seul.org/pygame/users/Apr-2008/msg00218.html
    if hasattr(ctypes.pythonapi, 'Py_InitModule4'):
       Py_ssize_t = ctypes.c_int
    elif hasattr(ctypes.pythonapi, 'Py_InitModule4_64'):
       Py_ssize_t = ctypes.c_int64
    else:
       raise TypeError("Cannot determine type of Py_ssize_t")

    _PyObject_AsWriteBuffer = ctypes.pythonapi.PyObject_AsWriteBuffer
    _PyObject_AsWriteBuffer.restype = ctypes.c_int
    _PyObject_AsWriteBuffer.argtypes = [ctypes.py_object,
                                      ctypes.POINTER(ctypes.c_void_p),
                                      ctypes.POINTER(Py_ssize_t)]

    def surface_to_array(surface):
       buffer_interface = surface.get_buffer()
       address = ctypes.c_void_p()
       size = Py_ssize_t()
       _PyObject_AsWriteBuffer(buffer_interface,
                              ctypes.byref(address), ctypes.byref(size))
       bytes = (ctypes.c_byte * size.value).from_address(address.value)
       bytes.object = buffer_interface
       return bytes

    def draw_skeletons(skeletons):
        for index, data in enumerate(skeletons):
            # draw the Head
            #HeadPos = skeleton_to_depth_image(data.SkeletonPositions[JointId.Head], dispInfo.current_w, dispInfo.current_h) 
            #draw_skeleton_data(data, index, SPINE, 10)
            #pygame.draw.circle(screen, SKELETON_COLORS[index], (int(HeadPos[0]), int(HeadPos[1])), 20, 0)
            HandPos = skeleton_to_depth_image(data.SkeletonPositions[JointId.HandRight], dispInfo.current_w, dispInfo.current_h)
            pygame.draw.circle(screen, SKELETON_COLORS[5], (int(HandPos[0]), int(HandPos[1])), 10, 0)
            LHandPos = skeleton_to_depth_image(data.SkeletonPositions[JointId.HandLeft], dispInfo.current_w, dispInfo.current_h)
            pygame.draw.circle(screen, SKELETON_COLORS[5], (int(LHandPos[0]), int(LHandPos[1])), 10, 0)
            ZLayer = data.SkeletonPositions[JointId.HandRight].z
            # drawing the limbs
            #draw_skeleton_data(data, index, LEFT_ARM)
            #draw_skeleton_data(data, index, RIGHT_ARM)
            #draw_skeleton_data(data, index, LEFT_LEG)
            #draw_skeleton_data(data, index, RIGHT_LEG)
            
            #lastxy = 
            return (int(HandPos[0]),int(HandPos[1])),(int(LHandPos[0]),int(LHandPos[1])),int(ZLayer)
            #return lastxy


    def depth_frame_ready(frame):
        if video_display:
            return

        with screen_lock:
            address = surface_to_array(screen)
            frame.image.copy_bits(address)
            del address
            if skeletons is not None and draw_skeleton:
                draw_skeletons(skeletons)
            pygame.display.update()
            #pdb.gimp_displays_flush()    


    def video_frame_ready(frame):
        if not video_display:
            return

        with screen_lock:
            address = surface_to_array(screen)
            frame.image.copy_bits(address)
            del address
            if skeletons is not None and draw_skeleton:
                draw_skeletons(skeletons)
            pygame.display.update()
            #pdb.gimp_displays_flush()
    
    full_screen = False
    draw_skeleton = True
    video_display = False

    screen_lock = thread.allocate()

    screen = pygame.display.set_mode(DEPTH_WINSIZE,0,16)    
    pygame.display.set_caption('Python Kinect Demo')
    skeletons = None
    #screen.fill(THECOLORS["black"])
    #screen.fill(THECOLORS["red"])
    kinect = nui.Runtime()
    kinect.skeleton_engine.enabled = True
    
    def post_frame(frame):
        try:
            pygame.event.post(pygame.event.Event(KINECTEVENT, skeletons = frame.SkeletonData))
        except:
            # event queue full
            pass

    kinect.skeleton_frame_ready += post_frame
    
    kinect.depth_frame_ready += depth_frame_ready    
    kinect.video_frame_ready += video_frame_ready    
    
    kinect.video_stream.open(nui.ImageStreamType.Video, 2, nui.ImageResolution.Resolution640x480, nui.ImageType.Color)
    kinect.depth_stream.open(nui.ImageStreamType.Depth, 2, nui.ImageResolution.Resolution320x240, nui.ImageType.Depth)

    #print('Controls: ')
    #print('     d - Switch to depth view')
    #print('     v - Switch to video view')
    #print('     s - Toggle displaing of the skeleton')
    #print('     u - Increase elevation angle')
    #print('     j - Decrease elevation angle')

    #pdb.gimp_context_set_foreground((0,255,0))
    #pdb.gimp_context_set_background((255,255,255))
    #pdb.gimp_context_set_brush('Circle (01)')
    img = pdb.gimp_image_new(320,240,RGB)
    #set up four paint layers to use depth data
    drw=(img.new_layer('kinect0',alpha=0),img.new_layer('kinect1',opacity=80),img.new_layer('kinect2',opacity=60.0),img.new_layer('kinect3',opacity=40.0))
    '''
    drw=[pdb.gimp_layer_new(img,320,240,RGB,"kinect0",100.0,NORMAL_MODE),pdb.gimp_layer_new(img,320,240,RGB,"kinect1",100.0,NORMAL_MODE),pdb.gimp_layer_new(img,320,240,RGB,"kinect2",100.0,NORMAL_MODE)]
    img.add_layer(drw[0], 4)
    img.add_layer(drw[1], 1)
    img.add_layer(drw[2], 2)
    #dr3 = img.new_layer('kinect3',pos=3)
    dr3 = img.new_layer('kinect3', 320, 240, 0, 0, 1, 3, 100.00, RGB, NORMAL_MODE)
    '''
    #drw=pdb.gimp_layer_new(img,320,240,RGB,"kinect",100.0,NORMAL_MODE)
    #img.add_layer(drw, 0)
    #drw = pdb.gimp_image_active_drawable(img)
    width = pdb.gimp_image_width(img)
    height = pdb.gimp_image_height(img)
    lastxy = (width/2,height/2)
    pdb.gimp_display_new(img)
    # main game loop
    done = False

    while not done:
        e = pygame.event.wait()
        dispInfo = pygame.display.Info()
        #dispInfo.current_w = dispInfo.current_w*2
        #dispInfo.current_w = dispInfo.current_w*2
        if e.type == pygame.QUIT:
            done = True
            break
        elif e.type == KINECTEVENT:
            skeletons = e.skeletons
            if draw_skeleton:
                Hand,LHand,ZLayer=draw_skeletons(skeletons)
                pygame.display.update()
                ctrlPoints = [int(Hand[0]), int(Hand[1]),int(Hand[0]), int(Hand[1])]
                #lastxy = Hand
                #if Hand[0] > LHand[0]:
                #use left hand to control brush size
                pdb.gimp_context_set_brush_size(float(LHand[1]))
                #use distance from sensor to change layer
                pdb.gimp_paintbrush(drw[ZLayer%4],0,len(ctrlPoints),ctrlPoints,0,0)
                pdb.gimp_displays_flush()
        elif e.type == KEYDOWN:
            if e.key == K_ESCAPE:
                done = True
                break
            elif e.key == K_d:
                with screen_lock:
                    screen = pygame.display.set_mode(DEPTH_WINSIZE,0,16)
                    video_display = False
            elif e.key == K_v:
                with screen_lock:
                    screen = pygame.display.set_mode(VIDEO_WINSIZE,0,32)    
                    video_display = True
            elif e.key == K_s:
                draw_skeleton = not draw_skeleton
            elif e.key == K_u:
                kinect.camera.elevation_angle = kinect.camera.elevation_angle + 2
            elif e.key == K_j:
                kinect.camera.elevation_angle = kinect.camera.elevation_angle - 2
            elif e.key == K_x:
                kinect.camera.elevation_angle = 2

register(
    "Kinect",
    "Kinect gimp image",
    "Create Kinect GIMP painting",
    "pdbperks",
    "pdbperks",
    "2018",
    "Kinect(Py)",
    "",      # Create a new image, don't work on an existing one
    [],
    [],
    gameK, menu="<Image>/File/Create")

main()
