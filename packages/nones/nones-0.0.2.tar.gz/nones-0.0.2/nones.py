class _NONE:
	def __init__(self):
		pass
	type='simple_none'
	def __repr__(self):
		return self.type
	def __str__(self):
		return self.type
	def __eq__(self,other):
		if isinstance(other,NONE):
			return other.type==self.type
		return False
	def __ne__(self,other):
		return not self.__eq__(other)
class _NONE_AS_OBJ(NONE):
	type='obj'
class _NONE_AS_FUNC(NONE):
	type='func'
	def __call__(self,*args,**kwargs):
		raise NotImplementedError
NONE=_NONE()
NONE_AS_OBJ=_NONE_AS_OBJ()
NONE_AS_FUNC=_NONE_AS_FUNC()