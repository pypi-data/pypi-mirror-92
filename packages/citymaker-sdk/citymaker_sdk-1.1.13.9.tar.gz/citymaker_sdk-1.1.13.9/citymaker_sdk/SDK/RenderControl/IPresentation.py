#!/usr/bin/env Python
# coding=utf-8#
#作者： tony1
import os, sys,json
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
import Utils.classmake as CM
import Utils.globalData as glodata
import Utils.wsInit  as wsObj 
from SDK.RenderControl.IRObject import IRObject
Props={"_HashCode":{"t":"S","v":"","F":"g"},
"propertyType":{"t":"S","v":"IPresentation","F":"g"}}
class IPresentation(IRObject):
	def __init__(self,args):
		CM.AddProps(self, Props, args)
		#CM.AddDefineProperty(self, Props)

	def initParam(self,args):
		self._HashCode=args.get("_HashCode")
		self._propertyType=args.get("propertyType")

	def cancelExport(self,):  # 先定义函数 
		args = {}
		state = ""
		CM.AddPrototype(self,args, 'cancelExport', 0, state)


	def closeEditor(self,):  # 先定义函数 
		args = {}
		state = ""
		CM.AddPrototype(self,args, 'closeEditor', 0, state)


	def continue_(self,):  # 先定义函数 
		args = {}
		state = ""
		CM.AddPrototype(self,args, 'continue', 0, state)


	def createCaptionStep(self,arg0,arg1,arg2,arg3,arg4,arg5):  # 先定义函数 
		args = {
				"advancedType":{"t": "gviPresentationStepContinue","v": arg0},
				"waitTime":{"t": "N","v": arg1},
				"description":{"t": "S","v": arg2},
				"captionText":{"t": "S","v": arg3},
				"captionTimeout":{"t": "N","v": arg4},
				"insertIndex":{"t": "N","v": arg5}
		}
		state = ""
		return CM.AddPrototype(self,args, 'createCaptionStep', 1, state)


	def createClearCaptionStep(self,arg0,arg1,arg2,arg3):  # 先定义函数 
		args = {
				"advancedType":{"t": "gviPresentationStepContinue","v": arg0},
				"waitTime":{"t": "N","v": arg1},
				"description":{"t": "S","v": arg2},
				"insertIndex":{"t": "N","v": arg3}
		}
		state = ""
		return CM.AddPrototype(self,args, 'createClearCaptionStep', 1, state)


	def createFlightSpeedFactorStep(self,arg0,arg1,arg2,arg3,arg4):  # 先定义函数 
		args = {
				"advancedType":{"t": "gviPresentationStepContinue","v": arg0},
				"waitTime":{"t": "N","v": arg1},
				"description":{"t": "S","v": arg2},
				"flightSpeedFactor":{"t": "gviPresentationStepFlightSpeed","v": arg3},
				"insertIndex":{"t": "N","v": arg4}
		}
		state = ""
		return CM.AddPrototype(self,args, 'createFlightSpeedFactorStep', 1, state)


	def createFollowDynamicObjectStep(self,arg0,arg1,arg2,arg3,arg4):  # 先定义函数 
		args = {
				"advancedType":{"t": "gviPresentationStepContinue","v": arg0},
				"waitTime":{"t": "N","v": arg1},
				"description":{"t": "S","v": arg2},
				"objectID":{"t": "G","v": arg3},
				"insertIndex":{"t": "N","v": arg4}
		}
		state = ""
		return CM.AddPrototype(self,args, 'createFollowDynamicObjectStep', 1, state)


	def createLocationStep(self,arg0,arg1,arg2,arg3,arg4):  # 先定义函数 
		args = {
				"advancedType":{"t": "gviPresentationStepContinue","v": arg0},
				"waitTime":{"t": "N","v": arg1},
				"description":{"t": "S","v": arg2},
				"position":{"t": "IPosition","v": arg3},
				"insertIndex":{"t": "N","v": arg4}
		}
		state = ""
		return CM.AddPrototype(self,args, 'createLocationStep', 1, state)


	def createMovie(self,arg0,arg1,arg2,arg3):  # 先定义函数 
		args = {
				"name":{"t": "S","v": arg0},
				"width":{"t": "N","v": arg1},
				"height":{"t": "N","v": arg2},
				"fps":{"t": "N","v": arg3}
		}
		state = ""
		return CM.AddPrototype(self,args, 'createMovie', 1, state)


	def createRestartDynamicObjectStep(self,arg0,arg1,arg2,arg3,arg4):  # 先定义函数 
		args = {
				"advancedType":{"t": "gviPresentationStepContinue","v": arg0},
				"waitTime":{"t": "N","v": arg1},
				"description":{"t": "S","v": arg2},
				"objectID":{"t": "G","v": arg3},
				"insertIndex":{"t": "N","v": arg4}
		}
		state = ""
		return CM.AddPrototype(self,args, 'createRestartDynamicObjectStep', 1, state)


	def createShowGroupStep(self,arg0,arg1,arg2,arg3,arg4,arg5):  # 先定义函数 
		args = {
				"advancedType":{"t": "gviPresentationStepContinue","v": arg0},
				"waitTime":{"t": "N","v": arg1},
				"description":{"t": "S","v": arg2},
				"groupID":{"t": "G","v": arg3},
				"show":{"t": "B","v": arg4},
				"insertIndex":{"t": "N","v": arg5}
		}
		state = ""
		return CM.AddPrototype(self,args, 'createShowGroupStep', 1, state)


	def createShowObjectStep(self,arg0,arg1,arg2,arg3,arg4,arg5):  # 先定义函数 
		args = {
				"advancedType":{"t": "gviPresentationStepContinue","v": arg0},
				"waitTime":{"t": "N","v": arg1},
				"description":{"t": "S","v": arg2},
				"objectID":{"t": "G","v": arg3},
				"show":{"t": "B","v": arg4},
				"insertIndex":{"t": "N","v": arg5}
		}
		state = ""
		return CM.AddPrototype(self,args, 'createShowObjectStep', 1, state)


	def createShowUndergroundModeStep(self,arg0,arg1,arg2,arg3,arg4):  # 先定义函数 
		args = {
				"advancedType":{"t": "gviPresentationStepContinue","v": arg0},
				"waitTime":{"t": "N","v": arg1},
				"description":{"t": "S","v": arg2},
				"show":{"t": "B","v": arg3},
				"insertIndex":{"t": "N","v": arg4}
		}
		state = ""
		return CM.AddPrototype(self,args, 'createShowUndergroundModeStep', 1, state)


	def deleteStep(self,arg0):  # 先定义函数 
		args = {
				"index":{"t": "N","v": arg0}
		}
		state = ""
		CM.AddPrototype(self,args, 'deleteStep', 0, state)


	def moveStepTo(self,arg0,arg1):  # 先定义函数 
		args = {
				"fromIndex":{"t": "N","v": arg0},
				"toIndex":{"t": "N","v": arg1}
		}
		state = ""
		CM.AddPrototype(self,args, 'moveStepTo', 0, state)


	def nextStep(self,):  # 先定义函数 
		args = {}
		state = ""
		CM.AddPrototype(self,args, 'nextStep', 0, state)


	def pause(self,):  # 先定义函数 
		args = {}
		state = ""
		CM.AddPrototype(self,args, 'pause', 0, state)


	def play(self,arg0):  # 先定义函数 
		args = {
				"startIndex":{"t": "N","v": arg0}
		}
		state = ""
		CM.AddPrototype(self,args, 'play', 0, state)


	def playStep(self,arg0):  # 先定义函数 
		args = {
				"index":{"t": "N","v": arg0}
		}
		state = ""
		CM.AddPrototype(self,args, 'playStep', 0, state)


	def previousStep(self,):  # 先定义函数 
		args = {}
		state = ""
		CM.AddPrototype(self,args, 'previousStep', 0, state)


	def resetPresentation(self,):  # 先定义函数 
		args = {}
		state = ""
		CM.AddPrototype(self,args, 'resetPresentation', 0, state)


	def resume(self,):  # 先定义函数 
		args = {}
		state = ""
		CM.AddPrototype(self,args, 'resume', 0, state)


	def showEditor(self,):  # 先定义函数 
		args = {}
		state = ""
		CM.AddPrototype(self,args, 'showEditor', 0, state)


	def startRecord(self,):  # 先定义函数 
		args = {}
		state = ""
		CM.AddPrototype(self,args, 'startRecord', 0, state)


	def stop(self,):  # 先定义函数 
		args = {}
		state = ""
		CM.AddPrototype(self,args, 'stop', 0, state)


	def stopRecord(self,):  # 先定义函数 
		args = {}
		state = ""
		CM.AddPrototype(self,args, 'stopRecord', 0, state)


	def updateEditor(self,):  # 先定义函数 
		args = {}
		state = ""
		CM.AddPrototype(self,args, 'updateEditor', 0, state)


	def createPresentationLocationStep(self,arg0,arg1,arg2,arg3,arg4):  # 先定义函数 
		args = {
				"presentationGuid":{"t": "S","v": arg0},
				"stepContinue":{"t": "gviPresentationStepContinue","v": arg1},
				"waitTime":{"t": "N","v": arg2},
				"description":{"t": "S","v": arg3},
				"index":{"t": "N","v": arg4}
		}
		state = "new"
		return CM.AddPrototype(self,args, 'createPresentationLocationStep', 1, state)

	@property
	def propertyType(self):
		if hasattr(self,"_HashCode") is False:
			return
		PropsValueData = glodata.PropsValueDataGet(self._HashCode)
		return PropsValueData["propertyType"]

	def to_json(self):
		result={}
		for k, v in self.__dict__.items():
			if k=="_HashCode":
				result[k] = v
			else:
				result[k.strip("_")] = v
		return result
