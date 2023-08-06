class Student:
	def __init__(self,name):
		self.name = name
		self.exp = 0
		self.lesson = 0

	def Hello(self):
		print("Hello, I'm {}.".format(self.name))

	def Coding(self):
		print('{}: coding'.format(self.name))
		self.exp += 5
		self.lesson += 1

	def ShowEXP(self):
		print("{} has exp equal to {} EXP due to complete {} lesson.".format(self.name,self.exp, self.lesson))

	def AddEXP(self, score):
		self.exp += score
		self.lesson += 1



class SpecialStudent(Student):
	"""docstring for SpecialStudent"""
	def __init__(self, name, father):
		super().__init__(name)
		self.father = father
		mafia = ['Bill Gates', 'Thomas Edison']
		if father in mafia:
			self.exp += 100

	def AddEXP(self, score):
		self.exp += score*3
		self.lesson += 1

	def AskEXP(self, score=10):
		print('Teacher gimme {} more point!!!!'.format(score))
		self.AddEXP(score)




if __name__ == '__main__':
	
print('===========2020, 1 JAN===========')
student0 = SpecialStudent('Mark Zuckerberg', 'Bill Gates')
student0.AskEXP()
student0.ShowEXP()

student1 = Student('Albert')
print(student1.name)
student1.Hello()

print('-------------------')
student2 = Student('Steve')
print(student2.name)
student2.Hello()
print('===========2020, 2 JAN===========')
print('Learning coding course for 10 exp')
student1.AddEXP(10)
print('===========2020, 3 JAN===========')

print(' show me your exp')
print(student1.name, student1.exp)
print(student2.name,student2.exp)

print('===========2020, 4 JAN===========')

for i in range(5):
	student2.Coding()

student2.ShowEXP()
student1.ShowEXP()