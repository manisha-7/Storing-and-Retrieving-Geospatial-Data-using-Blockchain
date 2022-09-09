import datetime
import hashlib
import json
import random
from datetime import date
from sqlite3 import Timestamp
from dateutil.relativedelta import relativedelta
from .models import isro123
class Blockchain:
	def __init__(self):
		self.currentdate = date.today()
		self.mainchain = []
		self.chain = []
		self.create_block(previous_hash='0', data={'coordinate' : 0,'date' : date(2022, 8, 10), 'place' : 'India', 'satellite' : 1, 'datatype' : 'None', 'ipfs_hash' : 'none', 'viewusers': ["dev","krupa"], 'userkanaam':['none', 'none']})
		self.filename = 'blockchain_data.json'
		
  
	def create_block(self, previous_hash, data):
		# checklocation = data['place']
		k = 0
		for i in range(len(self.mainchain)):
			checkk = str(self.mainchain[i][0]['datas']['date'])

			dd = int(checkk[8:])
			mm = int(checkk[5:7])
			yy = int(checkk[0:4])
			checkk = date(yy, mm, dd)
			kl = str(data['date'])
			dd = int(kl[8:])
			mm = int(kl[5:7])
			yy = int(kl[0:4])
			kl = date(yy, mm, dd)
			if kl >= checkk and kl < checkk+ relativedelta(months=3):
				print(self.mainchain[i][0])
				previous_block = self.mainchain[i][0]
				previous_hash = self.hashh(previous_block)
				block={
				'index': len(self.mainchain[i])+1,
				'nonce': random.randint(10**31, int('9'*32)),
				'timestamp': str(datetime.datetime.now()),
				'previous_hash': previous_hash,
				'datas': {
					'coordinate' : data['coordinate'],
					'date' : data['date'],
					'place' : data['place'],
					'satellite' : data['satellite'],
					'datatype' : data['datatype'],
					'ipfs_hash' : data['ipfs_hash'],
					'viewusers' : data['viewusers'],
					'userkanaam': [data['userkanaam']]
				} }
				k = 1
				self.mainchain[i].append(block)
		if k ==0:
			checkmonth = str(data['date'])
			dd = int(checkmonth[8:])
			mm = int(checkmonth[5:7])
			yy = int(checkmonth[0:4])
			checkmonth = date(yy, mm, dd)

			lkj = int(list(str(list(str((checkmonth - self.currentdate)).split(','))[0]).split(" "))[0])
			if lkj >= 90 or lkj <= -90:
				self.addendblock(self.currentdate, checkmonth, previous_hash)
				self.chain = []

				block={
					'index': 0,
					'nonce': random.randint(10**31, int('9'*32)),
					'timestamp': str(datetime.datetime.now()),
					'previous_hash': 0,
					'datas': {
						'coordinate' : '0',
						'date' : self.currentdate+relativedelta(months=3),
						'place' : 'india',
						'satellite' : '1',
						'datatype' : 'none',
						'ipfs_hash' : '111111',
						'viewusers' : ["dev","krupa"],
         				'userkanaam': ['none']
					}   ## coordinates, date, place, ??
				}
				self.currentdate = checkmonth
				self.chain.append(block)
				filename = 'Blockchain/blockchain_data.json'
				# with open(filename, 'r+') as file:
				# 	file_data = json.load(file)
				# 	file_data["datass"].append(block)
				# 	file.seek(0)
				# 	json.dump(file_data, file, indent=4, sort_keys=True, default=str)
				# fil = isro123(block=block)
				# fil.save()
			
			block={
				'index': len(self.chain)+1,
				'nonce': random.randint(10**31, int('9'*32)),
				'timestamp': str(datetime.datetime.now()),
				'previous_hash': previous_hash,
				'datas': {
					'coordinate' : data['coordinate'],
					'date' : data['date'],
					'place' : data['place'],
					'satellite' : data['satellite'],
					'datatype' : data['datatype'],
					'ipfs_hash' : data['ipfs_hash'],
					'viewusers' : data['viewusers'],
					'userkanaam': [data['userkanaam']]
				}   ## coordinates, date, place, ??
			}
			
			
			filename = 'Blockchain/blockchain_data.json'
			
			self.chain.append(block)
		
		# if block['datas']['coordinate'] != 0:
		# with open(filename, 'r+') as file:
		# 	file_data = json.load(file)
		# 	file_data["datass"].append(block)
		# 	file.seek(0)
		# 	json.dump(file_data, file, indent=4, sort_keys=True, default=str)
		# fil = isro123(block=block)
		# fil.save()
		return block


	def addendblock(self, startdate, enddate, previous_hash):
		block={
			'index': len(self.chain)+1,
			'nonce': random.randint(10**31, int('9'*32)),
			'startdate': startdate,
			'enddate' : enddate,
		}
		self.mainchain.append(self.chain)
  
  
	def hashh(self, block):
		encoded_block = json.dumps(block, sort_keys=True).encode()
		return hashlib.sha256(encoded_block).hexdigest()

	def chain_valid(self, chain):
		previos_block = len(self.chain)-2
		block = chain[len(self.chain)-1]
		if block['previous_hash'] != self.hashh(previos_block):
			return False
		else:
			return True

 
	def extract_data(self, coordinate, startdate, enddate, location, datatype, satellite):
		k = []
		l = []
		for i in reversed(range(len(self.mainchain))):
			startdate = str(startdate)
			dd = int(startdate[8:])
			mm = int(startdate[5:7])
			yy = int(startdate[0:4])
			startdate = date(yy, mm, dd)
			enddate = str(startdate)
			dd = int(enddate[8:])
			mm = int(enddate[5:7])
			yy = int(enddate[0:4])
			enddate = date(yy, mm, dd)
			if self.mainchain[i] and startdate >= self.mainchain[i][0]['datas']['date'] and enddate < self.mainchain[i][0]['datas']['date']+relativedelta(months=2):
				
				for j in reversed(range(len(self.mainchain[i]))):
					if self.mainchain[i][j]['datas']['coordinate'] == coordinate:
						
						if location == '' and datatype == 'none' and satellite == '':
							if l!=None:
								l.append(self.mainchain[i][j]['datas']['ipfs_hash'])
								k.append(self.mainchain[i][j]['datas'])
        
						elif datatype != 'none' and location == '' and satellite == '':
							if self.mainchain[i][j]['datas']['place'] == location:
								if l!=None:
									l.append(self.mainchain[i][j]['datas']['ipfs_hash'])
									k.append(self.mainchain[i][j]['datas'])
						elif datatype == 'none' and location != '' and satellite == '':
							if self.mainchain[i][j]['datas']['datatype'] == datatype:
								if l!=None:
									l.append(self.mainchain[i][j]['datas']['ipfs_hash'])
									k.append(self.mainchain[i][j]['datas'])
						elif datatype != 'none' and location != '' and satellite == '':
							if self.mainchain[i][j]['datas']['datatype'] == datatype and self.mainchain[i][j]['datas']['place'] == location:
								if l!=None:
									l.append(self.mainchain[i][j]['datas']['ipfs_hash'])
									k.append(self.mainchain[i][j]['datas'])
						elif datatype != 'none' and location != '' and satellite != '':
							if self.mainchain[i][j]['datas']['datatype'] == datatype and self.mainchain[i][j]['datas']['place'] == location and self.mainchain[i][j]['datas']['satellite'] == satellite:
								if l!=None:
									l.append(self.mainchain[i][j]['datas']['ipfs_hash'])
									k.append(self.mainchain[i][j]['datas'])
						elif datatype != 'none' and location == '' and satellite != '':
							if self.mainchain[i][j]['datas']['datatype'] == datatype and self.mainchain[i][j]['datas']['satellite'] == satellite:
								if l!=None:
									l.append(self.mainchain[i][j]['datas']['ipfs_hash'])
									k.append(self.mainchain[i][j]['datas'])
						elif datatype == 'none' and location != '' and satellite != '':
							if self.mainchain[i][j]['datas']['place'] == location and self.mainchain[i][j]['datas']['satellite'] == satellite:
								if l!=None:
									l.append(self.mainchain[i][j]['datas']['ipfs_hash'])
									k.append(self.mainchain[i][j]['datas'])
						elif datatype == 'none' and location == '' and satellite != '':
							if self.mainchain[i][j]['datas']['satellite'] == satellite:
								if l!=None:
									l.append(self.mainchain[i][j]['datas']['ipfs_hash'])
									k.append(self.mainchain[i][j]['datas'])
		if k:
			return k
		else:
			for i in reversed(range(len(self.chain))):
				if self.chain[i] and self.chain[i]['datas']['coordinate'] == str(coordinate):
					
					if location == '' and datatype == 'none' and satellite == '':
						if l!=None:
								l.append(self.chain[i]['datas']['ipfs_hash'])
								k.append(self.chain[i]['datas'])
					elif datatype != 'none' and location == '' and satellite == '':
						if self.chain[i]['datas']['place'] == location:
							if l!=None:
								l.append(self.chain[i]['datas']['ipfs_hash'])
								k.append(self.chain[i]['datas'])
					elif datatype == 'none' and location != '' and satellite == '':
						if self.chain[i]['datas']['datatype'] == datatype:
							if l!=None:
								l.append(self.chain[i]['datas']['ipfs_hash'])
								k.append(self.chain[i]['datas'])
					elif datatype != 'none' and location != '' and satellite == '':
						if self.chain[i]['datas']['datatype'] == datatype and self.chain[i]['datas']['place'] == location:
							if l!=None:
								l.append(self.chain[i]['datas']['ipfs_hash'])
								k.append(self.chain[i]['datas'])
					elif datatype != 'none' and location != '' and satellite != '':
						if self.chain[i]['datas']['datatype'] == datatype and self.chain[i]['datas']['place'] == location and self.chain[i]['datas']['satellite'] == satellite:
							if l!=None:
								l.append(self.chain[i]['datas']['ipfs_hash'])
								k.append(self.chain[i]['datas'])
					elif datatype != 'none' and location == '' and satellite != '':
						if self.chain[i]['datas']['datatype'] == datatype and self.chain[i]['datas']['satellite'] == satellite:
							if l!=None:
								l.append(self.chain[i]['datas']['ipfs_hash'])
								k.append(self.chain[i]['datas'])
					elif datatype == 'none' and location != '' and satellite != '':
						if self.chain[i]['datas']['place'] == location and self.chain[i]['datas']['satellite'] == satellite:
							if l!=None:
								l.append(self.chain[i]['datas']['ipfs_hash'])
								k.append(self.chain[i]['datas'])
					elif datatype == 'none' and location == '' and satellite != '':
						if self.chain[i]['datas']['satellite'] == satellite:
							if l!=None:
								l.append(self.chain[i]['datas']['ipfs_hash'])
								k.append(self.chain[i]['datas'])
					# k.append(self.chain[i]['datas'])
				if k:
					return k

		return 'Please enter the correct details!'

	def modify_perm(self, val):
		k = [0,0]
		l = [0]
		q = 0
		for i in range(len(self.mainchain)):
				for kk in range(len(self.mainchain[i])):
					if self.mainchain[i][kk]['datas']['ipfs_hash'] == val:
						q = 1
						k = [i,kk]
		if q == 0:
			for i in range(len(self.chain)):
				if self.chain[i]['datas']['ipfs_hash'] == val:
					l = [i]
					q = 1
		else:
			return self.mainchain[k[0]][k[1]]

		return self.chain[l[0]]
		
	def macc(self, val, addp, rp):
		l = self.modify_perm(val)
		addp = list(map(str, addp.split(',')))
		rp = list(map(str, rp.split(',')))
		if addp[0] == '':
			addp = []
		if rp[0] == '':
			rp = []
		

		if addp:
			for i in range(len(addp)):
				l['datas']['viewusers'].append(addp[i])
		if rp:
			for i in range(len(addp)):
				l['datas']['viewusers'].remove(rp[i])
		previous_block = len(self.chain)-1
		previous_hash = self.hashh(previous_block)
		print(l['datas']['viewusers'])
		self.create_block(previous_hash, l['datas'])
  
  
	def check_presence(self, hash, data, userkanaamm):
		milgeya = 0
		l = []
		val = data['ipfs_hash']
		
		for i in reversed(range(len(self.mainchain))):
			for j in reversed(range(len(self.mainchain[i]))):
				if self.mainchain[i][j]['datas']['ipfs_hash'] == val:
					milgeya = 1
					l.append(self.mainchain[i][j])
					print(l['datas']['userkanaam'])
					l['datas']['userkanaam'].append(userkanaamm)
					previous_block = len(self.chain)-1
					previous_hash = self.hashh(previous_block)
					self.create_block(previous_hash, l['datas'])
					return
		for i in (range(len(self.chain))):
			if self.chain[i]['datas']['ipfs_hash'] == val:
				milgeya = 1
				l.append(self.chain[i]['datas'])
				print(l[0])
				l[0]['userkanaam'].append(userkanaamm)
				previous_block = len(self.chain)-1
				previous_hash = self.hashh(previous_block)
				self.create_block(previous_hash, l[0])
				return
		if milgeya ==0:
			self.create_block(hash, data)

blockchain = Blockchain()




# for i in range(10000):
# 	# print(i)
# 	previous_block = len(blockchain.chain)-1
# 	previous_hash = blockchain.hashh(previous_block)
# 	data={'coordinate' : random.randint(1, 1000), 'date' : date(random.randint(1996, 2022), random.randint(1, 12),random.randint(1, 28)), 'place' : 'India', 'satellite' : random.randint(1, 1000), 'datatype' : 'None', 'ipfs_hash' : 'none','viewusers' : ['dev','krupa']}
# 	blockchain.create_block(previous_hash, data)