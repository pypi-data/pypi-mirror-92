def parse_file(file_path):
    """Parse .ma (maya ascii) files and returns a list of dictionaries
    describing mesh objects which description has to include "name", "uid" and "positions"

    Args:
        file_path(str): The path of the example file from which we want to get mesh objects

    Returns:
         Returns a list of mesh objects

    Examples:
        This is example of output from 'example_file_1.ma' file

        >>> parse_file('./example_files/example_file_1.ma')
        
        [{'position': ('1', '1', '-6'), 'name': 'SphereShape', 'uid': '"94071E8E-4E72-008C-F8FD-62B8E4EF57DA'},
        {'position': ('-3', '2', '2'), 'name': 'CubeShape', 'uid': '"47C059BB-4D70-AC70-532B-38A9A7C92F68'},
        {'position': ('0', '0', '5'), 'name': 'CylinderShape', 'uid': '"9BC8DE79-468E-8469-0D05-C19729563BCC'}]

    """
    my_file=open(file_path, 'r')

    lines=my_file.readlines()
    list_of_dict=[]
    number_of_lines=len(lines)
    
    #listing the file by line number
    for line in range (number_of_lines):
        dict_of_object = dict()
        text = lines[line]
        if("createNode mesh" in text):
            position = lines[line-1].split()[::-1]
            name = lines[line].split()
            uid = lines[line+1].split()

            #getting name from object
            name_index = name.index('-n')
            object_name = name[name_index+1].replace('"' , "")
            dict_of_object['name'] = str(object_name)
            
            #getting position from object
            if('"double3"'in position):
                x = position[3]
                y = position[2]
                z = position[1]
            else:
                x,y,z = 0,0,0
            dict_of_object['position'] = (x,y,z)
            
            #getting uid from object
            uid_index = uid.index('-uid')
            object_uid = uid[uid_index+1].replace('";' , "")
            dict_of_object['uid'] = str(object_uid)
            
            #adding object in list of objects
            list_of_dict.append(dict_of_object)
    my_file.close()
    return list_of_dict
