from colorama import init,Fore,Style,Back
import sys

init()


print("Grants Trace Length by Net Report Generator")
print("For use with Kicad 5")

try:
	board_file_name=str(sys.argv[1])
	board_file = open(board_file_name, 'r')
	LINES = board_file.readlines()
	open_flag=0
	for line in LINES:
		if line.count('(') == line.count(')'):
			continue
		else:
			if line.count('(') > line.count(')'):
				open_flag=1
			if line.count('(') < line.count(')'):
				if open_flag == 1:
					open_flag = 0
				else:
					print(Fore.RED + "ERROR: Board file corruption. Bracket Parse Error")
		if open_flag == 0 and line.split().strip(')(') == "net":
			print("Found Net list")















except:
	print(Fore.RED + "Error Opening board file: " + str(board_file_name) + Style.RESET_ALL)
	print("Usage: python3 trace_length_by_net.py <board_file.kicad_pcb")

