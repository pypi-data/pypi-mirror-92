#!/usr/bin/env Python
# coding=utf-8
#作者： tony
from citymaker_sdk.Utils.RenderViewer3D import RenderViewer3D
from citymaker_sdk  import Config


#cm=ICacheManager(None)

def initAxControl():
    config =Config()
    config.serverAddress = "ws://127.0.0.1:8181/"
    config.clientdir = "D:\\bin\\WebSocket3Server.bat"
    root ="renderControl"
    renderViewer3D=RenderViewer3D()
    renderViewer3D.setConfig(root, config)
    renderControl = renderViewer3D.getRenderControl()
    renderControl.interactMode = 1
    return renderControl

def loadSkyBox(renderControl):
    skyboxPath = "D:\\bin\\skybox"
    renderControl.objectManager.setSkybox(0,skyboxPath,1)

def initCamera(renderControl):
    camera = renderControl.camera
    pos = renderControl.new_Vector3
    ang = renderControl.new_EulerAngle
    pos.set(15415.2, 35211.31, 200)
    ang.heading = 0
    ang.tilt = -20
    camera.lookAt(pos, 600, ang)

def loadFDB(renderControl):
    server = "124.193.151.44"
    port = 8040
    database = "SDKDEMO"
    renderControl.loadFDBByService(server, port, database, "", "")

def loadCep(renderControl):#---------------------------------------------加载CEP
    cepPath = "D:/cep/Package_乾隆花园/乾隆花园.cep"
    project = renderControl.project
    project.open(cepPath, False, "")
    camera = renderControl.camera
    camera.flyTime = 1

def fnMouseClickSelect(pickResult,intersectPoint,mask,eventSender):
    position = intersectPoint.position
        # if (!renderControl) {
        #   alert("renderControl未初始化完成!");
        #   return;
        # }
    label = g.objectManager.createLabel(
        {"x": position.x, "y": position.y,"z": position.z },
        "标签123",
        "#000000",
        15,
        "宋体",
        1,
        1000
        )
    g.onMouseClickSelect = None

def initCamera1(renderControl):
    camera = renderControl.camera
    pos = renderControl.new_Vector3
    ang = renderControl.new_EulerAngle
    pos.set(14415.2, 34211.31, 200)
    ang.heading = 0
    ang.tilt = -20
    camera.lookAt(pos, 600, ang)

if __name__ == '__main__':
    g=initAxControl()
    loadSkyBox(g)
    initCamera(g)
    loadFDB(g)
    g.interactMode = 2
    g.onMouseClickSelect = fnMouseClickSelect
    initCamera1(g)

    # time.sleep(4)
    # loadCep(g)