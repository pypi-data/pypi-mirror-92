#!/usr/bin/env Python
# coding=utf-8#
#作者： tony1
import os, sys,json
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
import Utils.classmake as CM
import Utils.classPath as CP
import Utils.SocketApiServe as socketApi 
from SDK.RenderControl.IRenderable import IRenderable
Props={"cullMode":{"t":"gviCullFaceMode","v":0,
"F":"gs"},"forceCullMode":{"t":"bool","v":False,
"F":"gs"},"showOutline":{"t":"bool","v":False,
"F":"gs"},"_HashCode":{"t":"S","v":"","F":"g"},
"propertyType":{"t":"S","v":"IRenderGeometry","F":"g"}}
#Events = {toolTipText:{fn:null}}
class IRenderGeometry(IRenderable):
	def __init__(self,args):
		CM.AddProps(self, Props, args)
		#CM.AddDefineProperty(self, Props)

	def initParam(self,args):
		self.cullMode=args.get("cullMode")
		self.forceCullMode=args.get("forceCullMode")
		self.showOutline=args.get("showOutline")
		self._HashCode=args.get("_HashCode")
		self.propertyType=args.get("propertyType")

	def bind(self,arg0,arg1,arg2,arg3,arg4):  # 先定义函数 
		args = {
				"path":{"t": "IMotionPath","v": arg0},
				"posOffset":{"t": "IVector3","v": arg1},
				"headingOffset":{"t": "N","v": arg2},
				"pitchOffset":{"t": "N","v": arg3},
				"rollOffset":{"t": "N","v": arg4}
		}
		state = ""
		CM.AddPrototype(self,args, 'bind', 0, state)


	def bind2(self,arg0,arg1,arg2,arg3,arg4):  # 先定义函数 
		args = {
				"path":{"t": "IDynamicObject","v": arg0},
				"posOffset":{"t": "IVector3","v": arg1},
				"headingOffset":{"t": "N","v": arg2},
				"pitchOffset":{"t": "N","v": arg3},
				"rollOffset":{"t": "N","v": arg4}
		}
		state = ""
		CM.AddPrototype(self,args, 'bind2', 0, state)


	def getMotionPathId(self,):  # 先定义函数 
		args = {}
		state = ""
		return CM.AddPrototype(self,args, 'getMotionPathId', 1, state)


	def unbind(self,):  # 先定义函数 
		args = {}
		state = ""
		CM.AddPrototype(self,args, 'unbind', 0, state)


	def motionableBindDynamicObject(self,arg0,arg1,arg2,arg3):  # 先定义函数 
		args = {
				"modelGuid":{"t": "S","v": arg0},
				"dynamicGuid":{"t": "S","v": arg1},
				"posOffset":{"t": "IVector3","v": arg2},
				"angleOffset":{"t": "IEulerAngle","v": arg3}
		}
		state = "new"
		CM.AddPrototype(self,args, 'motionableBindDynamicObject', 0, state)


	def getFdeGeometry(self,):  # 先定义函数 
		args = {}
		state = ""
		return CM.AddPrototype(self,args, 'getFdeGeometry', 1, state)


	def glow(self,arg0):  # 先定义函数 
		args = {
				"duration":{"t": "N","v": arg0}
		}
		state = ""
		CM.AddPrototype(self,args, 'glow', 0, state)


	def setFdeGeometry(self,arg0):  # 先定义函数 
		args = {
				"newVal":{"t": "IGeometry","v": arg0}
		}
		state = ""
		CM.AddPrototype(self,args, 'setFdeGeometry', 0, state)

	def __getattr__(self,name):
		if name in Props:
			attrVal=Props[name]
			if name =="_HashCode":
				return CM.dict_get(attrVal, "v", None)
			F = CM.dict_get(attrVal, "F", None)
			t = CM.dict_get(attrVal, "t", None)
			if F.find("g") > -1:
				if CP.ClassFN.get(t) is not None and "PickResult" not in Props["propertyType"]["v"] and name != "propertyType":
					PropsTypeData = CM.getPropsTypeData(self._HashCode)
					PropsValueData = CM.getPropsValueData(self._HashCode)
					jsonData = CM.setJsonData("get_",PropsValueData.get("_HashCode"),name,None)
					res=socketApi.postMessage({"propertyType": PropsTypeData["propertyType"]["v"],"_HashCode": PropsValueData["_HashCode"]},name,jsonData)
					CM.addPropsValue(PropsValueData["_HashCode"], name, res)
					return PropsValueData[name]
				else:
					PropsValueData = CM.getPropsValueData(self._HashCode)
					if name == "fullScreen":
						res=CM.isFull()
					CM.addPropsValue(PropsValueData.get("_HashCode"), name, res)
					return PropsValueData[name]

	def __setattr__(self,name,value):
		if name in Props:
			attrVal=Props[name]
			F = CM.dict_get(attrVal, "F", None)
			t = CM.dict_get(attrVal, "t", None)
			if F.find("s") > -1:
				if name =="_HashCode":
					CM.dict_set(attrVal, "F", value)
					return
				PropsTypeData = CM.getPropsTypeData(self._HashCode)
				PropsValueData = CM.getPropsValueData(self._HashCode)
				CM.addPropsValue(PropsValueData.get("_HashCode"), name, value)
				if name == "fullScreen":
					res=CM.isFull()
					return
				args = {}
				args[name] = PropsTypeData.get(name)
				args[name]["v"] = value
				JsonData = CM.setJsonData("set_",PropsValueData.get("_HashCode"),name, args)
				socketApi.postMessage({"propertyType": PropsTypeData["propertyType"]["v"],"_HashCode": PropsValueData["_HashCode"]},name,JsonData)
				super(IRenderGeometry, self).__setattr__(name, value)

	def to_json(self):
		result={}
		for k, v in self.__dict__.items():
			if k=="_HashCode":
				result[k] = v
			else:
				result[k.strip("_")] = v
		return result
