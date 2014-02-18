#! /usr/bin/env python
"""Simple test for egl and gles1/2 behaviour"""
from bcmwindow import bcm
import os 
import numpy
if not os.environ.get( 'PYOPENGL_PLATFORM' ):
    os.environ['PYOPENGL_PLATFORM'] = 'egl'

import OpenGL,ctypes
OpenGL.USE_ACCELERATE = False
from OpenGL.EGL import *

import sys
import os

def describe_config( display, config ):
    """Describe the given configuration"""
    parameters = (EGL_CONFIG_ID,
        EGL_BUFFER_SIZE,
        EGL_LEVEL,
        EGL_RED_SIZE,
        EGL_GREEN_SIZE,
        EGL_BLUE_SIZE,
        EGL_ALPHA_SIZE,
        EGL_DEPTH_SIZE,
        EGL_STENCIL_SIZE,
        EGL_SURFACE_TYPE)
    description = []
    for param in parameters:
        value = ctypes.c_long()
        eglGetConfigAttrib(display, config, param, value)
        description.append( '%s = %s'%( param, value.value, ))
    return '\n'.join( description )

def mainloop( displayfunc ):
    while True:
        displayfunc()
        

def main(displayfunc, api):
    major,minor = ctypes.c_long(),ctypes.c_long()
    display = eglGetDisplay(EGL_DEFAULT_DISPLAY)
    print 'Display return value', display 
    print 'Display address', display.address
    #display = display.as_voidp
    #print 'wrapped', display
    if not eglInitialize( display, major, minor):
        print 'Unable to initialize'
    print 'EGL version %s.%s'%(major.value,minor.value)
    
    num_configs = ctypes.c_long()
    eglGetConfigs(display, None, 0, num_configs)
    print '%s configs'%(num_configs.value)
    
    configs = (EGLConfig * num_configs.value)()
    eglGetConfigs(display,configs,num_configs.value,num_configs)
    for config_id in configs:
        #print config_id
        describe_config( display, config_id )
    
    print 'Attempting to bind and create contexts/apis'
    eglBindAPI(api)
    
    # now need to get a raw X window handle...
    window = bcm.create_window()
    surface = eglCreateWindowSurface(display, configs[0], ctypes.addressof(window), None )
    
    ctx = eglCreateContext(display, configs[0], EGL_NO_CONTEXT, None)
    if ctx == EGL_NO_CONTEXT:
        print 'Unable to create the regular context'
    else:
        print 'Created regular context'
        while True:
            try:
                displayfunc( display, surface, ctx )
            except KeyboardInterrupt as err:
                break
    
    pbufAttribs = (EGLint * 5)(* [EGL_WIDTH,500, EGL_HEIGHT, 500, EGL_NONE])
    pbuffer = eglCreatePbufferSurface(display, configs[0], pbufAttribs);
    if (pbuffer == EGL_NO_SURFACE):
        print 'Unable to create pbuffer surface'
    else:
        print 'created pbuffer surface'
    
    print 'Available EGL extensions', EGLQuerier.getExtensions()

def displayfunc_gles1(display, surface, ctx):
    from OpenGL import GLES1 as GL
    eglMakeCurrent( display, surface, surface, ctx )
    GL.glClearColor( 1,0,0, 0 )
    GL.glClear( GL.GL_COLOR_BUFFER_BIT|GL.GL_DEPTH_BUFFER_BIT )
    vertices = numpy.array( ( (1,0,0 ),(-1,0,0 ),(0,1,0 )), 'f')
    GL.glEnableClientState( GL.GL_VERTEX_ARRAY )
    GL.glVertexPointer( 3, GL.GL_FLOAT, 0, vertices )
    GL.glDrawArrays( GL.GL_TRIANGLES, 0, 3 )
    eglSwapBuffers( display, surface )
displayfunc_gles1.api = EGL_OPENGL_ES_API

def displayfunc_gles2(display, surface, ctx):
    from OpenGL import GLES2 as GL
    eglMakeCurrent( display, surface, surface, ctx )
    GL.glClearColor( 1,0,0, 0 )
    GL.glClear( GL.GL_COLOR_BUFFER_BIT|GL.GL_DEPTH_BUFFER_BIT )
    eglSwapBuffers( display, surface )
displayfunc_gles2.api = EGL_OPENGL_ES_API

if __name__ == "__main__":
    if sys.argv[1:]:
        name = sys.argv[1]
    else:
        name = 'gles1'
    if name == 'gles':
        name = 'gles1'
    function = globals().get( 'displayfunc_%s'%(name,), displayfunc_gl )
    print 'Using function', function
    try:
        main(function,function.api)
    finally:
        bcm.bcm.bcm_host_deinit()

