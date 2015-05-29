import subprocess
from bs4 import BeautifulSoup

header, status = subprocess.Popen(['curl', '--data','institute_code=1101', 'http://biselahore.com/Zaidi_12th.php'], stdout=subprocess.PIPE).communicate()

soup=BeautifulSoup(header)
a=soup.table.tbody.find_all("tr")
rollNo=[]
for tr in a:
	td=tr.find_all("td")
	rollNo.append(td[1].text.strip())
print rollNo
print "@@@@@@@@@@@@@@"
print rollNo[0] 


header1, status1 = subprocess.Popen(['curl', '--data','student_rno='+rollNo[0]+'', 'http://biselahore.com/hsscResult_2014.php'], stdout=subprocess.PIPE).communicate()

print header1
