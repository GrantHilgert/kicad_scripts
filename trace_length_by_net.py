from colorama import init,Fore,Style,Back
import sys
import math



def print_status(message,status):
	if status == 1:
		print(str(message) + " [" + Fore.GREEN + "Complete" + Style.RESET_ALL + "]")
	if status == 0:
		print(str(message) + " [" + Fore.RED + "FAIL" + Style.RESET_ALL + "]")


init()


print("Grants Trace Length by Net Report Generator")
print("For use with Kicad 5")

try:
	board_file_name=str(sys.argv[1])
	board_file = open(board_file_name, 'r')
	LINES = board_file.readlines()
	open_flag=0
except:
	print(Fore.RED + "Error Opening board file: " + str(board_file_name) + Style.RESET_ALL)
	print("Usage: python3 trace_length_by_net.py <board_file.kicad_pcb")


net_list=[]
net_list_flag=0
segment_flag=0
for line in LINES:
	#print(line)
	if line.count('(') != line.count(')'):
		if line.count('(') > line.count(')'):
			open_flag+=1
			if net_list_flag == 1:
				net_list_flag = 0
				print_status("Netlist Extraction",1)
			if segment_flag == 1:
				segment_flag = 0
				print_status("Segment Extraction",1)
			#print("Flag open(" + str(open_flag) + ")")
		if line.count('(') < line.count(')'):
			if open_flag >= 1:
				open_flag-=1
				#print("flag Closed(" + str(open_flag) + ")")
			#else:
				
				#print(Fore.RED + "ERROR: Board file corruption. Bracket Parse Error")
	#Compile netlist
	if open_flag == 1 and len(line.split()) > 0:
		if line.split()[0].strip('(') == "net":
			net_list_flag=1
			net_name=""
			for index in range(len(line.split())-2):
				net_name+=line.split()[index+2]
			
			net_name = net_name.strip(")")
			net_name = net_name.strip('"')

			#print("Found Net! Number: " + str(line.split()[1]) + " Name: " + str(net_name))
			net_list.append({"name":str(net_name), "number":int(line.split()[1]),"length":float(0)})
	#Calculate Segments
		if line.split()[0].strip('(') == "segment":
			segment_flag = 1
			
			x1=float(line.split()[2])
			y1=float(line.split()[3].strip(')'))
			x2=float(line.split()[5])
			y2=float(line.split()[6].strip(')'))
			length = math.sqrt( ((x1-x2)**2) + ((y1-y2)**2))
			#print("Found Segment: Length: " +str(length) + " x1:" + str(x1) + " x2: " + str(x2) + " y1: " + str(y1) + " y2: " + str(y2))

			if line.split()[11].strip('(') == "net":
				net_id = int(line.split()[12].strip(')'))
				for net in net_list:
					if int(net.get("number")) == int(net_id):
						#print("Found Match: " + str(net.get("name")))
						current_length=float(net.get("length"))
						current_length+=length
						net.update({"length": float(current_length)})






			else:
				print(Fore.RED + "ERROR: File Segment Corruption" + Style.RESET_ALL)
				print_status("Segment Extraction",0)		




report_file = open("report.csv", 'w')

report_file.write("Net Name, Etch Length\n")

for net in net_list:
	temp_name=str(net.get("name"))
	temp_name=temp_name.split('/')[len(temp_name.split('/'))-1]
	temp_length=str(net.get("length"))
	report_file.write(temp_name + "," + temp_length + "\n")

print_status("Writing Report",1)	










