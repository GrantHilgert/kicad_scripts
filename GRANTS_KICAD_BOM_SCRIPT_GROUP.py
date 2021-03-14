import xml.etree.ElementTree as ET
import sys


version_major="0"
version_minor="2"



print("============================================================")
print("Grant's KICAD BOM GENERATOR SCRIPT\nversion: "+str(version_major)+"."+str(version_minor))
print("Usage: GRANTS_KICAD_BOM_GROUP.PY <input XML> <output Filename>")
print("============================================================")


tree = ET.parse(str(sys.argv[1]))
root = tree.getroot()
output_filename=str(sys.argv[2])
bom_file = open(output_filename+"_GRANT_BOM_GROUP.csv", "w")

bom_file.write("ITEM")
bom_file.write(",")
bom_file.write("QTY")
bom_file.write(",")
bom_file.write("REFERENCE")
bom_file.write(",")
bom_file.write(str("VALUE"))
bom_file.write(",")
bom_file.write(str("FOOTPRINT"))
bom_file.write(",")
bom_file.write(str("DATASHEET"))
bom_file.write(",")
bom_file.write(str("MPN"))
bom_file.write(",")
bom_file.write(str("MANUFACTURE"))
bom_file.write(",")
bom_file.write(str("DIGIKEY"))
bom_file.write(",")
bom_file.write(str("PCBA"))
bom_file.write("\n")

component_count=1
temp_ref="N/A"
temp_value="N/A"
temp_footprint="N/A"
temp_datasheet="N/A"
temp_mpn="N/A"
temp_mn="N/A"
temp_digikey="N/A"
temp_pcba="N/A"


deliminator=","

part_buffer={}
part_index={}
part_ref_buffer={}
passive_buffer={}
passive_index={}
passive_ref_buffer={}
database=[]
#Database structure VALUE | FOOTPRINT | DATASHEET | MPN | MANUFACTURE | DIGIKEY | PCBA

for component in root.iter('comp'):
        print("=============================================")

        #Write Item Number
        #bom_file.write(str(component_count))
        #bom_file.write(deliminator)
        #Write Reference Designator
        temp_ref=str(component.get('ref'))
        print("REFERENCE: " + str(temp_ref))
        #bom_file.write(str(temp_ref))
        #bom_file.write(deliminator)

        #Gonna do this next part super dirty.
        #Scan through all the tags and pull out what we want
        for name in component.iter():
            #Some type of error checking, it was in the example code.
            if not name.tag==component.tag:
                if(name.tag == "value"):
                    temp_value = str(name.text)
                if(name.tag == "footprint"):
                    temp_footprint = str(name.text)
                if(name.tag == "datasheet"):
                    temp_datasheet = str(name.text)
                if(name.get('name') == "PCBA"):
                   temp_pcba = str(name.text)
                if(name.get('name') == 'digikey'):
                   temp_digikey = str(name.text)
                if(name.get('name') == "mn"):
                   temp_mn = str(name.text)
                if(name.get('name') == 'pn'):
                   temp_mpn = str(name.text)


        #Print to Terminal
        print("VALUE: " + temp_value)
        print("FOOTPRINT: " + temp_footprint)
        print("DATASHEET: " + temp_datasheet)
        print("MPN: " + temp_mpn)
        print("MANUFACTURE: " + temp_mn)
        print("DIGIKEY: " + temp_digikey)
        print("PCBA: " + temp_pcba)


        if not temp_mpn == "N/A":

            if temp_mpn in part_ref_buffer:
                temp_ref_b = part_ref_buffer.get(temp_mpn)
                part_ref_buffer.update({str(temp_mpn):str(temp_ref_b) + " " + str(temp_ref)})
            else:
                part_ref_buffer.update({str(temp_mpn):str(temp_ref)})

            if not temp_mpn in part_buffer: 
                print("Adding New part to buffer")          
                part_buffer.update({temp_mpn:1})
                part_index.update({(len(database)+1):temp_mpn})
                database.append(str(temp_value) + "," + str(temp_footprint) + "," + str(temp_datasheet) + "," + str(temp_mpn) + "," + str(temp_mn) + "," + str(temp_digikey) + "," + str(temp_pcba))
            else:
                print("Adding Exisiting part to buffer")
                temp_count=0
                temp_count=int(part_buffer.get(str(temp_mpn)))+1
                part_buffer.update({temp_mpn:temp_count})
                
        else:
            if temp_value in passive_ref_buffer:
                temp_ref_b = passive_ref_buffer.get(temp_value)
                passive_ref_buffer.update({str(temp_value):str(temp_ref_b) + " " + str(temp_ref)})
            else:
                passive_ref_buffer.update({str(temp_value):str(temp_ref)})

            if not temp_value in passive_buffer:

                print("Adding New part to passive buffer")
                temp_count=0
                part_index.update({len(database)+1:temp_value})
                database.append(str(temp_value) + "," + str(temp_footprint) + "," + str(temp_datasheet) + "," + str(temp_mpn) + "," + str(temp_mn) + "," + str(temp_digikey) + "," + str(temp_pcba))
                passive_buffer.update({temp_value:1})
            else:
                print("Adding Exisiting part to passive buffer")
                temp_count=int(passive_buffer.get(str(temp_value)))+1
                passive_buffer.update({temp_value:temp_count})          

            
              
            









        
        #Reset Values
        temp_ref="N/A"
        temp_value="N/A"
        temp_footprint="N/A"
        temp_datasheet="N/A"
        temp_mpn="N/A"
        temp_mn="N/A"
        temp_digikey="N/A"
        temp_pcba="N/A"         
              
        component_count+=1







print("Compiling File")

for part in range(len(database)):

     if not str(part_index.get(part+1)) in part_buffer:
        temp_qty = passive_buffer.get(str(part_index.get(part+1)))
        temp_ref_sum = passive_ref_buffer.get(str(part_index.get(part+1)))

        print("QTY: " + str(temp_qty) + "REF " + str(temp_ref_sum)+ database[part])


        #Write the buffer to file
        bom_file.write(str(part+1))
        bom_file.write(deliminator)       
        bom_file.write(str(temp_qty))
        bom_file.write(deliminator)
        bom_file.write(str(temp_ref_sum))
        bom_file.write(deliminator)
        bom_file.write(str(database[part]))

        bom_file.write("\n")










        

     else:
        #Non-Passive Routine
        #Get QTY
        temp_qty = part_buffer.get(str(part_index.get(part+1)))
        temp_ref_sum = part_ref_buffer.get(str(part_index.get(part+1)))

        print("QTY: " + str(temp_qty) + "REF " + str(temp_ref_sum)+ database[part])

        #Write the buffer to file
        bom_file.write(str(part+1))
        bom_file.write(deliminator)         
        bom_file.write(str(temp_qty))
        bom_file.write(deliminator)
        bom_file.write(str(temp_ref_sum))
        bom_file.write(deliminator)
        bom_file.write(str(database[part]))

        bom_file.write("\n")
    

print("=============================================")
print("DUMPING DICTONARY\n")

for part in part_buffer:
    print(part + " = " + str(part_buffer.get(part)))

for part in passive_buffer:
    print(part + " = " + str(passive_buffer.get(part)))

print("=============================================")
print("DUMPING DATABASE\n")    
for part in range(len(database)):
    print(database[part])
bom_file.close()
print("BOM FILE CREATED: "+ output_filename+"_GRANT_BOM_GROUP.csv")
print("=============================================")


    

