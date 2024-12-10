import openpyxl as xl


def read_survey(filename):
    workbook = xl.load_workbook(filename)
    sheet = workbook["Sheet1"]

    # survey - is a list of tupples to store all questions
    survey = list()
    keys = ["id", "Question", "correct_answer", "title","a)", "b)", "c)", "d)"]

    for raw in sheet:
        cell_quantity = len(raw)
        question = {}
        for cell in raw:
            keys_index= cell.column - 1
            question[keys[keys_index]] = cell.value
        survey.append(question)
    return(survey)


