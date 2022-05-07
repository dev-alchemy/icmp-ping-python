

def write_to_file(file_name, path="./data/", write_data=None):

    file_name = file_name + ".txt"
    full_path = path + file_name

    file_obj = open(full_path, "a")
    file_obj.write(write_data)
    file_obj.close()

    return
