import xml.etree.ElementTree as ET
tree = ET.parse('BE_4990_Fall_2018.xml')
root = tree.getroot()
bom_file = open("GRANT_PYTHON_BOM.csv", "w")

bom_file.write("ITEM")
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
temp_value="N/A"
temp_footprint="N/A"
temp_datasheet="N/A"
temp_mpn="N/A"
temp_mn="N/A"
temp_digikey="N/A"
temp_pcba="N/A"


deliminator=","

part_buffer={}
passive_buffer={}


for component in root.iter('comp'):
        print("=============================================")

        #Write Item Number
        bom_file.write(str(component_count))
        bom_file.write(deliminator)
        #Write Reference Designator
        print("REFERENCE: " + component.get('ref'))
        bom_file.write(component.get('ref'))
        bom_file.write(deliminator)

        #Gonna do this next part super dirty.
        #Scan through all the tags and pull out what we want
        for name in component.iter():
            #Some type of error checking, it was in the example code.
            if not name.tag==component.tag:
                if(name.tag == "value"):
                    temp_value = name.text
                if(name.tag == "footprint"):
                    temp_footprint = name.text
                if(name.tag == "datasheet"):
                    temp_datasheet = name.text
                if(name.get('name') == "PCBA"):
                   temp_pcba = name.text
                if(name.get('name') == 'digikey'):
                   temp_digikey = name.text
                if(name.get('name') == "mn"):
                   temp_mn = name.text
                if(name.get('name') == 'pn'):
                   temp_mpn = name.text


        #Print to Terminal
        print("VALUE: " + temp_value)
        print("FOOTPRINT: " + temp_footprint)
        print("DATASHEET: " + temp_datasheet)
        print("MPN: " + temp_mpn)
        print("MANUFACTURE: " + temp_mn)
        print("DIGIKEY: " + temp_digikey)
        print("PCBA: " + temp_pcba)


        if not temp_mpn == "N/A":

            if not temp_mpn in part_buffer: 
                print("Adding New part to buffer")
                part_buffer.update({temp_mpn:1})
            else:
                print("Adding Exisiting part to buffer")
                temp_count=int(part_buffer.get(str(temp_mpn)))+1
                part_buffer.update({temp_mpn:temp_count})
        else:
            if not temp_value in passive_buffer: 
                print("Adding New part to passive buffer")
                passive_buffer.update({temp_value:1})
            else:
                print("Adding Exisiting part to passive buffer")
                temp_count=int(passive_buffer.get(str(temp_value)))+1
                passive_buffer.update({temp_value:temp_count})          

            
              
            









        #Write the buffer to file
        
        bom_file.write(str(temp_value))
        bom_file.write(deliminator)
        bom_file.write(str(temp_footprint))
        bom_file.write(deliminator)
        bom_file.write(str(temp_datasheet))
        bom_file.write(deliminator)
        bom_file.write(str(temp_mpn))
        bom_file.write(deliminator)
        bom_file.write(str(temp_mn))
        bom_file.write(deliminator)
        bom_file.write(str(temp_digikey))
        bom_file.write(deliminator)
        bom_file.write(str(temp_pcba))
        bom_file.write("\n")
        
        #Reset Values
        temp_value="N/A"
        temp_footprint="N/A"
        temp_datasheet="N/A"
        temp_mpn="N/A"
        temp_mn="N/A"
        temp_digikey="N/A"
        temp_pcba="N/A"         
              
        component_count+=1











print("=============================================")
print("DUMPING DICTONARY\n")

for part in part_buffer:
    print(part + " = " + str(part_buffer.get(part)))

for part in passive_buffer:
    print(part + " = " + str(passive_buffer.get(part)))

bom_file.close()
print("BOM FILE CREATED")
print("=============================================")


    

