import subprocess
from bs4 import BeautifulSoup
import threading, urllib2
import time
import Queue
import pymongo
from pymongo import MongoClient

# connect to database
def dbconnect() :
        
	client = MongoClient()
	db = client["scrap"]
	return db

# To save the array into the collection 
def save_collection(collection,arr):

	db = dbconnect()
        coll = db[collection]
        data = coll.insert(arr)
        return data


def find_all_in_collection(collection):
      
	db = dbconnect()
        coll = db[collection]
        cursor = coll.find()
        result = [item for item in cursor]
        return result









def read_url(url, queue):


	data, status1 = subprocess.Popen(['curl', '--data','student_rno='+url+'', 'http://biselahore.com/hsscResult_2014.php'], stdout=subprocess.PIPE).communicate()

	#print data
	try:
		soup1=BeautifulSoup(data)
		a1=soup1.find_all('td', {'width':"20%"})
		ft=[]
		for fThree in a1:
			ft.append(fThree.text.strip())
		#print ft




		candAndfatherNameSearch=soup1.find_all('td', {"class":"pagetext","align":"left","style":"font-size:12px"})
		candName=candAndfatherNameSearch[0].text.strip()
		fatherName=candAndfatherNameSearch[1].text.strip()
		#print candName
		#print fatherName


		collegeNameSearch=soup1.find_all('td', {"rowspan":"3","style":"font-size:12px"})
		collegeName=collegeNameSearch[0].text.strip()
		#print collegeName

		subjectSearch=soup1.find_all('td',{"class":"TextHeading"})
		subjectArray=[]
		for subject in subjectSearch:
			 if len(subject.attrs) == 1 :
			 	subjectArray.append(subject.text.strip())
		#print subjectArray

		markSearch=soup1.find_all('td',{"class":"pagetext","align":"center"})
		markArray=[]
		for mark in markSearch:
			markArray.append(mark.text.strip())
		#print markArray
		markArray1=[]
		for x in xrange(3,len(markArray),5):
			markArray1.append(markArray[x])
		#print markArray1

		markArray2=[]
		for x1 in xrange(4,len(markArray),5):
			markArray2.append(markArray[x1])
		#print markArray2

		com=[]
		for comb in range(0,len(subjectArray)):
			com.append({"subject":subjectArray[comb],"totalmarks":markArray1[comb],"marks_status":markArray2[comb]})

		#print com

		studentRecords={"RollNo":ft[0],"Reg_No":ft[2],"Result_Status":ft[3],"Name":candName,"Fname":fatherName,"collegeName":collegeName,"subject":com}
		save_collection("studentRecords2",studentRecords)

		print studentRecords
		queue.put(data)
	except:
		print "wait for sometime"




def fetch_parallel(urls):
	result = Queue.Queue()
	threads = [threading.Thread(target=read_url, args = (url,result)) for url in urls]
	for t in threads:
		time.sleep(2)
		t.start()

	for t in threads:
		t.join()


	return result




db=find_all_in_collection("clgdetails")
print len(db[0]["clgdata"])

for x in range(350,410):
	header, status = subprocess.Popen(['curl', '--data','institute_code='+str(int(db[0]['clgdata'][x]['cid']))+'', 'http://biselahore.com/Zaidi_12th.php'], stdout=subprocess.PIPE).communicate()
	#print header
	
	soup=BeautifulSoup(header)
	a=soup.table.tbody.find_all("tr")
	rollNo=[]
	for tr in a:
		td=tr.find_all("td")
		rollNo.append(td[1].text.strip())
	fetch_parallel(rollNo)




