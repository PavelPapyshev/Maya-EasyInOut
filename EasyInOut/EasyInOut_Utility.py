import maya.cmds as mc


def newSliderValue(value=0, comboText="In/Out"):
	
	"""
	calculates new key values for animation curves
		
	accepts arguments:
		@value[int] - slider value
		@comboText[str] - type of transaction
	"""
			
	value = value/1000.0	
	selCurves = mc.keyframe(selected=1, q=1, name=1)
	
	#no curve selected
	if not selCurves:
		return
	
	for channel in selCurves:
		
		totalKeys = mc.keyframe(channel, q=1, keyframeCount=1)
		selectedIndices = mc.keyframe(channel, selected=1, q=1, indexValue=1)
		
		prevKey = selectedIndices[0] - 1
		nextKey = selectedIndices[-1] + 1
		
		if prevKey == -1:
			prevKey = 0
		
		if nextKey == totalKeys:
			nextKey = totalKeys - 1
		
		prevKeyValue = mc.keyframe(channel, index=(prevKey, prevKey), q=1, valueChange=1)
		nextKeyValue = mc.keyframe(channel, index=(nextKey, nextKey), q=1, valueChange=1)
		
		prevFrame = mc.keyframe(channel, index=(prevKey, prevKey), q=1, timeChange=1)
		nextFrame = mc.keyframe(channel, index=(nextKey, nextKey), q=1, timeChange=1)
		
		changeFrame = nextFrame[0] - prevFrame[0]
		sumValue = 1.0/changeFrame
		tmpSumValue = sumValue
		
		frame = prevFrame[0] + 1
		
		while frame < nextFrame[0]:
			
			currentTime = value + sumValue #t
			startValue = prevKeyValue[0] #b
			changeValue = nextKeyValue[0] - prevKeyValue[0] #c
			duration = 1.0 #d
			
			if currentTime < 0:
				currentTime = 0
			
			if currentTime > 1:
				currentTime = 1
			
			#In/Out------------------------
			if comboText == "In/Out":
				currentTime /= duration/2
				
				if currentTime < 1:
					newKeyValue = changeValue/2*currentTime*currentTime+startValue
				
				else:
					currentTime = currentTime-1
					newKeyValue = (-1*changeValue)/2*(currentTime*(currentTime-2)-1)+startValue
			
			
			#In------------------------
			if comboText == "In":
				newCurrentTime = currentTime
				newCurrentTime /= duration
				newKeyValue = changeValue*newCurrentTime*currentTime+startValue
			
			
			#Out------------------------
			if comboText == "Out":
				newCurrentTime = currentTime
				newCurrentTime /= duration
				newKeyValue = -changeValue*newCurrentTime*(currentTime-2)+startValue

			mc.keyframe(channel, absolute=1, time=(frame, frame), valueChange=newKeyValue)
			
			sumValue += tmpSumValue
			frame += 1
			