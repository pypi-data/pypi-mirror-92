class Student:
	def __init__(self,name,lastname):
		self.name = name
		self.lastname = lastname
		self.exp = 0
		self.lesson = 0
		self.vehicle = 'รถเมลล์'
	@property

	def fullname(self):
		return '{} {}'.format(self.name,self.lastname)

	def Coding(self):
		self.AddExp()
		print('{} กำลังเรียนเขียนโปรแกรม'.format(self.fullname))

	def ShowEXP(self):
		print('{} ได้คะแนน {} exp (เรียนไปกี่ครั้ง {} )'.format(self.name,self.exp,self.lesson))

	def AddExp(self):
		self.exp += 10
		self.lesson += 1

	def __str__(self):
		return self.fullname

	def __repr__(self):
		return self.fullname
class Tesla: 
	def __init__(self):
		self.Model = 'Tesla Model S'

	def SelfDriving(self):
		print('ระบบชับอัตโนมัติกำลังทำงาน...'+ ' ' + 'กำลังพาคุณ {} กลับบ้าน'.format(stp1.name))

	def __str__(self):
		return self.Model


class SpecialStudent(Student):
	def __init__(self,name,lastname,father):
		super().__init__(name,lastname)
		self.father = father
		self.vehicle = Tesla()
		print('รู้ไหมฉันลูกใคร?...! {}'.format(self.father))
		self.AddExp()

	def AddExp(self):
		self.exp += 30
		self.lesson += 2 
		print('{} ได้คะแนน {} exp (เรียนไปกี่ครั้ง {} )'.format(self.name,self.exp,self.lesson))

class Teacher:
	def __init__(self,fullname):
		self.fullname = fullname
		self.students = []

	def CheckStudent(self):
		for i,st in enumerate(self.students):
			print('----นักเรียนของคุณครู{}----'.format(self.fullname))
			print('{} --> {} [{} exp][เรียนไป {} ครั้ง]'.format(i+1,st.fullname,st.exp,st.lesson))

	def AddStudent(self,st):
		self.students.append(st)

### print('FILE : '+ __name__)
if __name__ == '__main__':
	

	allstudent = []

	teacher1 = Teacher('Ada Lovelace')
	teacher2 = Teacher('Bill Gates')
	print(teacher1.students)
	########  DAY 1  ########
	print('-------- DAY 1 ---------')
	st1 = Student('Albert','Einstein')
	allstudent.append(st1)
	teacher2.AddStudent(st1)
	print(st1.fullname)

	########  DAY 2  ########
	print('-------- DAY 2 ---------')
	st2 = Student('Steve','Jobs')
	allstudent.append(st2)
	teacher2.AddStudent(st2)
	print(st2.fullname)

	########  DAY 3  ########
	print('-------- DAY 3 ---------')
	for i in range(3):
		st1.Coding()
	st2.Coding()
	st1.ShowEXP()
	st2.ShowEXP()

	########  DAY 4  ########
	print('-------DAY 4--------')

	stp1 = SpecialStudent('Thomas','Edison','Hitler')
	allstudent.append(stp1)
	teacher1.AddStudent(stp1)
	print(stp1.name + ' ' + stp1.lastname)
	stp1.AddExp


	print('-------DAY 5--------')
	print('นักเรียนกลับบ้านยังไง?')
	print(allstudent)
	for st in allstudent:
		print('ผม {} กลับบ้านด้วย {}'.format(st.name,st.vehicle))
		if isinstance(st,SpecialStudent):
			st.vehicle.SelfDriving()

	######## DAY 6 #########
	print('-------DAY 6-------')

	teacher1.CheckStudent()
	teacher2.CheckStudent()
