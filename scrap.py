import subprocess
from bs4 import BeautifulSoup

header, status = subprocess.Popen(['curl', '--data','institute_code=1101', 'http://biselahore.com/Zaidi_12th.php'], stdout=subprocess.PIPE).communicate()

soup=BeautifulSoup(header)
a=soup.table.tbody.find_all("tr")
rollNo=[]
for tr in a:
	td=tr.find_all("td")
	rollNo.append(td[1].text.strip())
# print rollNo
# print "@@@@@@@@@@@@@@"
# print rollNo[0] 


header1, status1 = subprocess.Popen(['curl', '--data','student_rno='+rollNo[0]+'', 'http://biselahore.com/hsscResult_2014.php'], stdout=subprocess.PIPE).communicate()

print header1
soup1=BeautifulSoup(header1)
a1=soup1.find_all('td', {'width':"20%"})
ft=[]
for fThree in a1:
	ft.append(fThree.text.strip())
print ft




candAndfatherNameSearch=soup1.find_all('td', {"class":"pagetext","align":"left","style":"font-size:12px"})
candName=candAndfatherNameSearch[0].text.strip()
fatherName=candAndfatherNameSearch[1].text.strip()
print candName
print fatherName


collegeNameSearch=soup1.find_all('td', {"rowspan":"3","style":"font-size:12px"})
collegeName=collegeNameSearch[0].text.strip()
print collegeName




# D:\MSDEV\PACS\dev_working_stable\main\Projects\RadSpeed\Build_Script\RIS-PACS
