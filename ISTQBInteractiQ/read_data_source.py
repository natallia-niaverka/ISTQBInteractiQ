import os


def read_data_source():
    survey_list = []
    path = "data_source"
    for file in os.listdir(path):
        if file.endswith(".xlsx"):
            # Prints only text file present in My Folder
            survey_list.append(file)
    print(survey_list)
    return survey_list


