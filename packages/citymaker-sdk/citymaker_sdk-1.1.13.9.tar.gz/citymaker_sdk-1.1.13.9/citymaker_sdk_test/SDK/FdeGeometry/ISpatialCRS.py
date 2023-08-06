#!/usr/bin/env Python
# coding=utf-8#
#作者： tony1
import os, sys,json
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
import Utils.classmake as CM
import Utils.classPath as CP
import Utils.SocketApiServe as socketApi 
from SDK.FdeGeometry.ICoordinateReferenceSystem import ICoordinateReferenceSystem
Props={"highPrecision":{"t":"bool","v":False,
"F":"gs"},"mResolution":{"t":"double","v":0,
"F":"gs"},"mTolerance":{"t":"double","v":0,
"F":"gs"},"xYResolution":{"t":"double","v":0,
"F":"gs"},"xYTolerance":{"t":"double","v":0,
"F":"gs"},"zResolution":{"t":"double","v":0,
"F":"gs"},"zTolerance":{"t":"double","v":0,
"F":"gs"},"_HashCode":{"t":"S","v":"","F":"g"},
"propertyType":{"t":"S","v":"ISpatialCRS","F":"g"}}
class ISpatialCRS(ICoordinateReferenceSystem):
	def __init__(self,args):
		CM.AddProps(self, Props, args)
		#CM.AddDefineProperty(self, Props)

	def initParam(self,args):
		self.highPrecision=args.get("highPrecision")
		self.mResolution=args.get("mResolution")
		self.mTolerance=args.get("mTolerance")
		self.xYResolution=args.get("xYResolution")
		self.xYTolerance=args.get("xYTolerance")
		self.zResolution=args.get("zResolution")
		self.zTolerance=args.get("zTolerance")
		self._HashCode=args.get("_HashCode")
		self.propertyType=args.get("propertyType")

	def constructFromHorizon(self,):  # 先定义函数 
		args = {}
		state = ""
		CM.AddPrototype(self,args, 'constructFromHorizon', 0, state)


	def isPrecisionEqual(self,arg0):  # 先定义函数 
		args = {
				"src":{"t": "ISpatialCRS","v": arg0}
		}
		state = ""
		return CM.AddPrototype(self,args, 'isPrecisionEqual', 1, state)


	def setDefaultMResolution(self,):  # 先定义函数 
		args = {}
		state = ""
		CM.AddPrototype(self,args, 'setDefaultMResolution', 0, state)


	def setDefaultMTolerance(self,):  # 先定义函数 
		args = {}
		state = ""
		CM.AddPrototype(self,args, 'setDefaultMTolerance', 0, state)


	def setDefaultXYResolution(self,):  # 先定义函数 
		args = {}
		state = ""
		CM.AddPrototype(self,args, 'setDefaultXYResolution', 0, state)


	def setDefaultXYTolerance(self,):  # 先定义函数 
		args = {}
		state = ""
		CM.AddPrototype(self,args, 'setDefaultXYTolerance', 0, state)


	def setDefaultZResolution(self,):  # 先定义函数 
		args = {}
		state = ""
		CM.AddPrototype(self,args, 'setDefaultZResolution', 0, state)


	def setDefaultZTolerance(self,):  # 先定义函数 
		args = {}
		state = ""
		CM.AddPrototype(self,args, 'setDefaultZTolerance', 0, state)

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
				super(ISpatialCRS, self).__setattr__(name, value)

	def to_json(self):
		result={}
		for k, v in self.__dict__.items():
			if k=="_HashCode":
				result[k] = v
			else:
				result[k.strip("_")] = v
		return result
