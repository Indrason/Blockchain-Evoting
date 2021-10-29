import random
import json
from hashlib import sha256
from datetime import datetime

# Generating sha256
def generateHash(txt):
	hash_result = sha256(str(txt).encode())
	return hash_result.hexdigest()


# Reading from file
def readFromFile(filename):
	file_read = open(filename,'r')
	file_data = file_read.read()
	file_read.close()
	file_data = json.loads(str(file_data))
	return file_data


# Writing data in the file
def writeToFile(filename, data):
	file_create = open(filename,'w')
	file_create.write(json.dumps(data))
	file_create.close()

	
# Setting up AADHAAR and EPIC
def setUpAADHAARandEPIC():
	aadhaar_list = []
	epic_list = []
	epic_suffix = ["CTN0", "JTN0"]
	thoubal_vil = ["Uchiwa", "Thoudam", "Khekman", "Lilong", "Kayam Siphai", "Kshetri Leikai"]
	khurai_vil = ["Kangla", "Angom", "Porompat", "Lamlai" ,"Top" ,"Khomidok"]
	all_address = thoubal_vil.copy()
	all_address.extend(khurai_vil)
	surnames = ["Ngangbam", "Sorokhaibam", "Sagolshem", "Laishram", "Yendrembam", "Thockchom", "Wahengbam", "Wangkheirakpam", "Irom", "Haobijam", "Longjam", "Aheibam", "Thounaojam"]
	
	# AADHAAR section
	adhar_num = int(input("Enter number of AADHAAR records: "))
	print("AADHAAR Numbers: \n")
	for i in range(adhar_num):
		value = random.randint(111111111111, 999999999999)
		print(str(i+1) + " -- AADHAAR Number: " + str(value))
		sel_surname = random.choice(surnames)
		name = input("Enter Name: ")
		fullname = sel_surname + " " + name
		father_name = input("Enter Father Name: ")
		fullfather_name = sel_surname + " " + father_name
		address = random.choice(all_address)
		aadhaar_detail = {"aadhaar_no": str(value), "name": fullname, "father_name": fullfather_name, "address": address}
		aadhaar_list.append(aadhaar_detail)
		
	writeToFile('list_aadhaar.dat', aadhaar_list)

	# EPIC section
	epic_num = int(input("\nEnter number of EPIC records: "))
	while epic_num >= adhar_num:
		print("Number of EPIC records cannot exceeds the number of AADHAAR records!")
		epic_num = int(input("Enter number of EPIC records: "))
	print("EPIC Numbers: \n")
	for j in range(epic_num): 
		name = aadhaar_list[j]['name']
		father_name = aadhaar_list[j]['father_name']
		address = aadhaar_list[j]['address']
		if address in thoubal_vil:
			value2 = "JTN0" + str(random.randint(111111, 999999))
			consty = "Thoubal"
		elif address in khurai_vil:
			value2 = "CTN0" + str(random.randint(111111, 999999))
			consty = "Khurai"
		print(str(j+1) + " -- EPIC Number: " + value2 + " -- " + consty)
		epic_detail = {"Sl.No": str(j+1), "epic_no": value2, "name": name, "father_name": father_name, "address": address, "constituency": consty}
		epic_list.append(epic_detail)

	writeToFile('list_epic.dat', epic_list)
	print('\n  -----------------------------------------------------------------')
	print('\n     Successfully saved the AADHAAR details and EPIC details !!!')
	main()

	
# Displaying AADHAAR and EPIC	
def displayAADHAARandEPIC():
	aadhaar_details = readFromFile('list_aadhaar.dat')
	print("\nSl. No. \tAADHAAR Number \tName \tFather Name \tAddress")
	print("\n--------------------------------------------------------")
	for i in range(len(aadhaar_details)):
		print("\n" + str(i+1) + "\t\t" + aadhaar_details[i]['aadhaar_no'] + "\t" + aadhaar_details[i]['name'] + "\t" + aadhaar_details[i]['father_name'] + "\t" + aadhaar_details[i]['address'])
		
	epic_details = readFromFile('list_epic.dat')
	print("\n\nSl. No. \tEPIC Number \tName \tFather Name \tAddress \tConstituency")
	print("\n---------------------------------------------------------------------")
	for j in range(len(epic_details)):
		print("\n" + epic_details[j]['Sl.No'] + "\t\t" + epic_details[j]['epic_no'] + "\t" + epic_details[j]['name'] + "\t" + epic_details[j]['father_name'] + "\t" + epic_details[j]['address'] + "\t" + epic_details[j]['constituency'])
	print('\n  -----------------------------------------------------------------')
	print('\n     Successfully displayed the AADHAAR and EPIC details !!!')	
	main()


# Setting up the candidates
def setUpCandidates():
	candidates_num = input('\nEnter the number of candidates: ')
	candidates = []
	epic_details = readFromFile('list_epic.dat')
	for i in range(int(candidates_num)):
		cand_epic = input('Enter candidate '+str(i+1)+' EPIC Number: ')
		found = 0
		for j in range(len(epic_details)):
			if cand_epic == epic_details[j]['epic_no']:
				candidates.append(epic_details[j])
				found = 1
				break
		if found == 0:
			print('No such candidate found, Please proceed again !')
			setUpCandidates()
				
	writeToFile('list_candidates.dat', candidates)
	print('\n  -----------------------------------------------------------------')
	print('\n     Successfully set up the candidates !!!')
	main()


# Display the candidates
def displayCandidates():
	print('\nList of candidates: ')
	all_candidates = readFromFile('list_candidates.dat')
	print("\n\nSl. No. \tEPIC Number \tName \tFather Name \tAddress \tConstituency")
	print("\n---------------------------------------------------------------------")
	for j in range(len(all_candidates)):
		print("\n" + all_candidates[j]['Sl.No'] + "\t\t" + all_candidates[j]['epic_no'] + "\t" + all_candidates[j]['name'] + "\t" + all_candidates[j]['father_name'] + "\t" + all_candidates[j]['address'] + "\t" + all_candidates[j]['constituency'])
	print('\n  -----------------------------------------------------------------')
	print('\n     Successfully displayed the candidates !!!')	
	main()


# Verification of votes
def verifyVotes():
	errors = []
	votes_data = readFromFile('e_votes.dat')
	total = len(votes_data)
	for i in range(total - 1):
		one_vote = str(votes_data[i]['vote_from']) + str(votes_data[i]['vote_to']) + str(votes_data[i]['vote_time']) + str(votes_data[i]['vote_val']) + str(votes_data[i]['prev_hash']) + str(votes_data[i]['nonce'])
		test_hash = generateHash(one_vote)
		if test_hash != votes_data[i]['cur_hash'] or test_hash != votes_data[i+1]['prev_hash']:
			errors.append(i+1)
	last_vote = str(votes_data[total - 1]['vote_from']) + str(votes_data[total - 1]['vote_to']) + str(votes_data[total - 1]['vote_time']) + str(votes_data[total - 1]['vote_val']) + str(votes_data[total - 1]['prev_hash']) + str(votes_data[total - 1]['nonce'])
	last_hash = generateHash(last_vote)
	if last_hash != votes_data[total - 1]['cur_hash']:
		errors.append(total)
	
	if len(errors) == 0:
		print("\nThere is no fault in the votes ledger !")
	else:
		print("\nThere is fault in the voting ledger ! And the faulty blocks are: ")
		print(errors)
	print('\n  -----------------------------------------------------------------')
	print('\n     Successfully verified the votes !!!')	
	main()


# Counting of votes
def countVotes():
	counts = []
	candidates = readFromFile('list_candidates.dat')
	votes = readFromFile('e_votes.dat')
	num_candi = len(candidates)
	num_votes = len(votes)
	for i in range(num_candi):
		total = 0
		for j in range(num_votes):
			if generateHash(candidates[i]['epic_no']) == votes[j]['vote_to']:
				total += 1
		counts.append({candidates[i]['epic_no']: total})
	writeToFile('e_counts.dat', counts)
		
	print("\nThe result of the votes: ")
	print(counts)
	
	print('\n  -----------------------------------------------------------------')
	print('\n     Successfully counted the votes !!!')	
	main()
	

# Setting up date and time for election
def setUpVotingTime():
	now = datetime.now()
	print('\n Current Date/Time: ',now)
	print('#Enter the start time and end time as the above format (YYYY-MM-DD HH:MM:SS)')
	startTime = input('Enter start Time: ')
	endTime = input('Enter end Time: ')
	print(startTime)
	print(endTime)

	if now > datetime.strptime(startTime, "%Y-%m-%d %H:%M:%S"):
		print('Error ! Voting start time cannot be earlier than the current time !')
		setUpVotingTime()
	elif now > datetime.strptime(endTime, "%Y-%m-%d %H:%M:%S"):
		print('Error ! Voting end time cannot be earlier than the current time !')
		setUpVotingTime()
	elif datetime.strptime(startTime, "%Y-%m-%d %H:%M:%S") > datetime.strptime(endTime, "%Y-%m-%d %H:%M:%S"):
		print('Error ! Voting end time cannot be earlier than the voting start time !')
		setUpVotingTime()
	else:
		data = [{"startTime": startTime}, {"endTime": endTime}]
		writeToFile('list_votingTime.dat',data)

	print('\n  -----------------------------------------------------------------')
	print('\n     Successfully setup the voting time !!!')
	main()


# Main function
def main():
	print('\n\n   ADMIN SECTION   ')
	#checkVotingTime()
	print('\nList of operations to perform: ')
	print('1. Set up the AADHAAR and EPIC')
	print('2. Display the AADHAAR and EPIC Details')
	print('3. Set up the candidates')
	print('4. Display the candidates')
	print('5. Verify the votes')
	print('6. Count the votes')
	print('7. Setting up Date/Time of the election')
	print('8. Exit')
	opt = input('\nSelect an option to proceed: ')
	
	if int(opt) == 1:
		setUpAADHAARandEPIC()
	elif int(opt) == 2:
		displayAADHAARandEPIC()
	elif int(opt) == 3:
		setUpCandidates()
	elif int(opt) == 4:
		displayCandidates()
	elif int(opt) == 5:
		verifyVotes()
	elif int(opt) == 6:
		countVotes()
	elif int(opt) == 7:
		setUpVotingTime()
	elif int(opt) == 8:
		print('\n  -----------------------------------------------------------------')
		print('\n     Thank you. Have a nice day !!!')
		exit()
	else:
		print('\n  -----------------------------------------------------------------')
		print('\n     Please choose a valid option !')
		main()

if __name__ == '__main__':
	main()
	
