
# --- libs ---
import openpyxl as px
import os

# --- class ---
letters = "ABCDEFGHIJKLMNOPQRSTUVXYZ"

class Database:
	def __init__(self, name, values=[], ids='id'):
		path = os.path.join(os.getcwd(), 'DataPackages', name + '_package')
		if not os.path.exists(path):
			os.makedirs(path)
		
		#print(os.listdir(path))

		self.ids = ids
		self.name = os.path.join(path, 'data_' + name + '.xlsx')
		if 'data_' + name + '.xlsx' not in os.listdir(path):
			workbook = px.Workbook()
			
			self.dataTypes = list(values)
			self.sheetLenghts = 0

			sheet = workbook.active
			for i in range(len(values)):
				sheet[letters[i]+"1"] = values[i]

			workbook.save(filename=self.name)
			count_file = open(os.path.join(path, 'count_file_REST.txt'), 'w')
			count_file.write('0')
			count_file.close()
			self.new = True

		else:
			
			print('retrieving from ' + self.name)
			self.new = False

		self.wb = px.load_workbook(self.name)
		self.sheet = self.wb.active
		
		r = self.get()
		self.dataTypes = r['dataTypes']
		self.sheetLenghts = r['lenght']

		self.count_file = os.path.join(path, 'count_file_REST.txt')


	def append(self, change):


		if type(change) is str:
			print(colors.fg.red+'Please use a list, even for one value'+colors.reset)
			return None
			#assert false
			#raise

		if len(self.get()['dataTypes']) < len(change):
			print(colors.fg.red+'Not enough values'+colors.reset)
			return None

		for i in range(len(change)):
				
			cell = letters[i] + str(self.sheetLenghts+2)
			self.sheet[cell] = change[i]

		self.sheetLenghts += 1

		self.wb.save(filename=self.name)
		
		# - write and close -
		f = open(self.count_file, 'r')
		curId = int(f.read())
		f.close()
		f = open(self.count_file, 'w')
		f.write(str(curId+1))
		f.close()

	def _clear_line(self):
		
		done = False
		while not done:
			done = True

			pl = 'A' + str(place+2) + ':' + letters[len(self.dataTypes)-1] + str(place + self.sheetLenghts - place + 2)
			print(pl)
		
		#ws.move_range("D4:F10", rows=-1)


	def remove(self, id_):
		
		if id_:
			l = self.get()[self.ids]
			
			if id_ in l:
				line = l.index(id_)
				self.sheet.delete_rows(line+2)
				#self._clear_line()
			else:
				print(colors.fg.red+ '"' + id_ + '" not in database'+colors.reset)

		self.wb.save(filename=self.name)


	def get(self):
		
		r_dict = {'dataTypes':[], 'lenght':0}

		# - datatypes -
		l_type = []
		l_values = []
		for i in range(len(letters)):
			r = self.sheet[letters[i] + '1'].value
			if r:
				l_type.append(r)
			

				# - values -
				c = 2
				l_values.append([])
				while True:
					r = self.sheet[letters[i] + str(c)].value

					if r:
						l_values[i].append(r)
					else:
						break

					c += 1

			else:
				break

		l_lenght = []
		for i in l_values:
			l_lenght.append(len(i))


		r_dict = {'dataTypes':l_type, 'values':l_values, 'lenght':max(l_lenght)}
		
		for i in range(len(l_values)):
			r_dict.update({l_type[i]:l_values[i]})

		return r_dict


	def distinct_id(self):
		
		f = open(self.count_file, 'r')
		id_ = f.read()
		f.close()

		while id_ in self.get()[self.ids]:
			id_ = str(int(id_) + 1)

		return id_


	def close(self):
		self.wb.close()
