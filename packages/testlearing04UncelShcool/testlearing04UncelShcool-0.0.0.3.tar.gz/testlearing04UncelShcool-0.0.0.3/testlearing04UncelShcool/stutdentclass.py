#studentclass.py

class Student:  
	def __init__ (self,name):
		self.name = name
		self.exp = 0
		self.lesson = 0
		#Call func
		# self.AddEXP(10)
	def Hello(self):
		print('sawatdeejaa Mu name is {}'.format(self.name))
		return ('sawatdeejaa')

	def Coding(self):
		print( '{} : Now is coding'.format(self.name))
		self.exp += 5
		self.lesson += 1

	def ShowExp(self):
		print('-{} has {} exp'.format(self.name,self.exp))
		print('-- lesson {} round'.format(self.lesson))

	def AddEXP(self,score):
		self.exp += score
		self.lesson += 1


class SpecialStudent(Student):

	def __init__(self,name,father):
		super().__init__(name)  ## Insert to class student
		self.father = father
		mafia=['Bill Gates','Thomas Edison']
		if father in mafia:
			self.exp += 100

	def AddEXP(self,score):
		self.exp += (score*3)
		self.lesson += 1

	def AskEXP(self,score=10):
		print('Teacher take a point at me , point {} EXP'.format(score))
		self.AddEXP(score)

print(__name__)

if __name__ == '__main__':  ### ทดสอบรันในโปรแกรมตัวถ้าถูก Import ไปใช้จะไม่รัน
	print('========== 1 Jan 2021 =========')
	student0 = SpecialStudent('Mark Zuckerberg','Bill Gates')
	student0.AskEXP()
	student0.ShowExp()


	student1 = Student('Albert')
	print(student1.name)
	print(student1.Hello())


	print('----------')

	student2 = Student('Steve')
	print(student2.name)
	print(student2.Hello())

	print('========== 2 Jan 2021 =========')
	print('------- Who are lern coding, get --- (10 exp) ---')
	student1.AddEXP(10)  # student1.exp = student.exp +10


	print('========== 3 Jan 2021 =========')

	student1.name = 'Albert Einst'

	print('ตอนนี้ exp ของแต่ละคนได้เท่าไหร่ กันแล้ว')
	print(student1.name,student1.exp)
	print(student2.name,student2.exp)



	print('========== 4 Jan 2021 =========')

	print(student1.name,student1.exp)
	print(student2.name,student2.exp)


	for i in range(5):
		student2.Coding()

	student1.ShowExp()
	student2.ShowExp()
