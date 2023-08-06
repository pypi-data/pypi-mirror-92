#studentclass.py

class Student:
	def __init__(self,name):
		self.name = name
		self.exp = 0
		self.lesson = 0
		#Call function
		#self.AddExp(10)
		
	def Hello(self):
		print('สวัสดีจร้าาาาาาา เราชื่อ{}'.format(self.name))

	def Coding(self):
		print('{}: กำลังเขียน coding ..'.format(self.name))
		self.exp += 5
		self.lesson += 1

	def ShowExp(self):
		print('- {} มีประสบการณ์ {} exp'.format(self.name,self.exp))
		print('- เรียนไป {} ครั้งแล้ว'.format(self.lesson))

	def AddExp(self, score):
		self.exp += score # self.exp = self.exp + score
		self.lesson += 1


class SpecialStudent(Student):
	def __init__(self,name,father):
		super().__init__(name)
		self.father = father
		mafia = ['Big Tuu','Big Pom']
		if father in mafia:
			self.exp += 100

	def AddExp(self,score):
		self.exp += (score * 3)
		self.lesson +=1

	def AskExp(self,score=10):
		print('ครู!! ขอคะแนนพิเศษให้ผมหน่อยสิสัก {} EXP'.format(score))
		self.AddExp(score)

if __name__ == '__main__':
		

	print('=======1 Jan =======')
	student0 = SpecialStudent('Uncle Phol','Big Tuu')
	student0.AskExp()
	student0.ShowExp()



	student1 = PND69('pepper')
	print(student1.name)
	student1.Hello()

	print('----------')
	student2 = PND69('tukta')
	print(student2.name)
	student2.Hello()

	print('=======2 Jan =======')
	print('----ใครอยากเรียน coding บ้าง---(10 exp)---')
	student1.AddExp(10) # student1.exp = student1.exp + 10

	print('=======3 Jan =======')
	student1.name = 'pepper ch'

	print('ตอนนี้ exp ของแต่ล่ะคนได้เท่าไรกันแล้ว')

	print(student1.name, student1.exp)
	print(student2.name, student2.exp)

	print('=======4 Jan =======')

	for i in range (5):
		student1.Coding()

	student1.ShowExp()
	student2.ShowExp()	