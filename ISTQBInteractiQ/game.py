import time
import readxls


def main():
    survey = readxls.read_survey("data_source/istqb_exam_sample_paper_3.xlsx")
    question_quantity = len(survey) -1
    print("Quantity of questions:", question_quantity)
    keys = ["Question", "title", "a)", "b)", "c)", "d)"]
    score = 0
    start_time = time.time()

    for question in survey:
        if question["id"] == "id":
            continue
        for key in keys:
            if key == "title":
                print(question[key])
            else:
                print(key, question[key])
        user_answer = input("Enter your answer: ")
        if user_answer.upper() == question["correct_answer"]:
            print("You are right! Correct answer is:", question["correct_answer"], "\n")
            score += 1
        else:
            print("No! Correct answer is: ", question["correct_answer"], "\n")
    end_time = time.time()
    elapsed_time = end_time - start_time
    score_percentage = (score / question_quantity) * 100
    print("Your score is: %s, percentage: %s, Time spent (min): " % (score, round(score_percentage)))
    print(round(elapsed_time/60))
    return survey, score


main()
