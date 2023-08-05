import re
# Katarina Knezevic
# 19-Jan-2021
# Belgrade, Serbia

'''
#function parse_maya_file is for parsing maya ascii files
#input arguments: file_name - destination and name of maya ascii file (example: file_name = "example_file_1.ma")
#output arguments: node_list - for every createNode include all name, position, type, uid, atribute_list if they exist
				# node_list, type: list of dict
				# example: 
				# node_list = [{'position': 'Cylinder', 'type': 'mesh', 'name': 'CylinderShape', 'uid': '9BC8DE79-468E-8469-0D05-C19729563BCC'},
							#{'type': 'lightLinker', 'name': 'lightLinker1', 'uid': 'A6BBAD30-47D1-3DAE-3CB6-2F8644DE6469'},
							# ...
							#{'type': 'shapeEditorManager', 'name': 'shapeEditorManager', 'uid': '42F34E59-4147-7866-43E2-CAA38DF17FA4'}]
'''

def parse_maya_file(file_name):
	with open(file_name, "r") as maya_file:
		
		line = maya_file.readline()
		node_list = []
		#I will be using this while loot to go through every line of input file
		while line:
			#I are seraching for `createNode` keyword to find all Nodes in maya ascii file
			cn_pattern = re.search("createNode ", line)
			if cn_pattern:
				node_dict = {}
				#I use this regular expration to find name of node nad position of node
				node_names = re.findall(r'-n "(.*?)(?<!\\)"', line)
				node_positions = re.findall(r'-p "(.*?)(?<!\\)"', line)
				#Findall will return all results found in the string that match regular expration
				#I made assumption that only one will be present per line so I just take first in the list
				for node_name in node_names:
					node_dict["name"] = node_name
					break
				for node_position in node_positions:
					node_dict["position"] = node_position
					break
				#Then I split string by blank space to find it's type
				temp_parts = cn_pattern.string.split(" ")
				node_type = temp_parts[1]
				node_dict["type"] = node_type
				
				#Now I want to read all the atributes of the node to find uid and positions
				while True:
					line = maya_file.readline()
					#I are checking that first char of line is \t so that I know that I are inside Node definition
					if line[0] != "\t":
						break
					#I use regular expration to find uid if it is present
					uid_temp = re.findall(r'-uid "(.*?)(?<!\\)"', line)
					for t in uid_temp:
						node_dict["uid"] = t
						break
					#I use this regular expration to find numbers that describe position of the node
					atribute_temp = re.findall(r'setAttr "\.t" -type ".*" (-?\d+(?:\.\d+)?)* (-?\d+(?:\.\d+)?)* (-?\d+(?:\.\d+)?)*', line)
					if atribute_temp:
						for t in atribute_temp:
							node_atribute_list = []
							for i in t:
								node_atribute_list.append(i)
							node_dict["atribute_list"] = node_atribute_list
				node_list.append(node_dict)
			else:
				line = maya_file.readline()

	return node_list
	
'''
Function find_mash_objects is use to finds mash objects

input arguments: node_list - you can get adequat list with function parse_maya_file

output arguments: final_list - list of dictionaries describing mesh objects. Mesh object description has to include "name", "uid" and "position"

				 final_list, type: list of dict
				 
				 example: 
				 final_list = [{'position': ['1', '1', '-6'], 'name': 'SphereShape', 'uid': '94071E8E-4E72-008C-F8FD-62B8E4EF57DA'},
								{'position': ['-3', '2', '2'], 'name': 'CubeShape', 'uid': '47C059BB-4D70-AC70-532B-38A9A7C92F68'},
								{'position': ['0', '0', '5'], 'name': 'CylinderShape', 'uid': '9BC8DE79-468E-8469-0D05-C19729563BCC'}]
'''
def find_mash_objects(file_name):

	if not file_name:
		return

	node_list = parse_maya_file(file_name)

	final_list =[];
	# I will be using this for loop to go through every line of node_list
	for i in range(len(node_list)):
		final_dict =  {
					  "name": "",
					  "position": [],
					  "uid": []
						}
		# Our nodes of interests are nodes type mash 				
		if node_list[i]['type'] == 'mesh':
			#I get the name, position and uid of node of interest 
			final_dict['name'] = node_list[i]['name']
			final_dict['position_name'] = node_list[i]['position']
			final_dict['uid'] = node_list[i]['uid']		
			final_list.append(final_dict)
			
	#I have to add position into my final list of dictionary
	#I compare name and position form node types mash and transform respectively
	#So I get the real position of mash
	for j in range(len(final_list)):		
		for i in range(len(node_list)):
			if node_list[i]['type'] == 'transform':
				if "atribute_list" in node_list[i]:
					if final_list[j]['position_name'] == node_list[i]['name']:
						final_list[j]['position'] = node_list[i]['atribute_list']
		#I am using position name only as indicator to match with transform node, I don't need it in output of function 
		del final_list[j]['position_name']

	return final_list