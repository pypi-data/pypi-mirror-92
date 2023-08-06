'''
Author: shy
Description: 计量，距离，时间相关的
LastEditTime: 2021-01-27 10:15:59
'''

class AverageMeter:
	"""Computes and stores the average and current value"""
	
	def __init__(self):
		self.reset()

	def reset(self):
		self.val   = 0
		self.avg   = 0
		self.sum   = 0
		self.count = 0

	def update(self, val, n = 1):
		self.val   = val
		self.sum   += val * n
		self.count += n
		self.avg   = self.sum / self.count