def main():
    candidate_first_name = input('Enter your first name: ').upper()
    candidate_last_name = input('Enter your last name: ').upper()

    question_attempt_count = 0
    total_number_of_questions = 10
    incorrect_count = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    correct_count = 0
    score = 0
    grades = ['A', 'B', 'C', 'D', 'F']

    candidate_end_test_input = ''
    end_test_input = str('SUBMIT')
    incorrect_candidate_end_test_input = 0

    questions = ['Question 1: what is the capital of france?',
                 'Question 2: How many local government areas are in Delta State Nigeria?',
                 'Question 3: Who is the CEO of Nazaprime Realty?',
                 'Question 4: Which of these companies is a subsidiary of Naza Holding?',
                 'Question 5: When did Nigeria become a Republic?',
                 "Question 6: Who was the 44th president of the United States of America?",
                 'Question 7: What is the legislative capital of South Africa?',
                 'Question 8: Which of these countries is the Eiffel Tower located?',
                 'Question 9: Which of these counties won the 2013 Africa Cup of Nations?',
                 'Question 10: Which year was Nazaprime Realty founded?'
                 ]

    options = ['A: Abuja B: Lyon C: Paris D: Cape Town',
               'A: 24  B: 36  C: 18  D: 25',
               'A: Elon Musk B: Mike Blomberg C: Naza James E: Jeff Bezos',
               'A: Telsa B: Xpance C: Edge D: Bolt',
               'A: 1963 B: 1971 C: 1914 D: 1960',
               'A: George Bush B: Donald Trump C: Barrack Obama D: Joe Biden',
               "A: Pretoria B: Cape Towm C: Johannesburg D: Bloemfontein",
               'A: England B: Uganda C: Canada D: France',
               'A: Algeria B: Egypt C: Ghana D: Nigeria',
               'A: 2023 B: 2013 C: 2017 D: 2021'
               ]

    question_answer = ['C', 'D', 'C', 'C', 'A', 'C', 'B', 'D', 'D', 'A']

    feedback = ['Congratulations! You are correct!',
                'Incorrect! You have one attempt left.',
                'Incorrect!',
                'Score = ',
                '/10',
                'Questions attempted = ',
                'Hi ' + candidate_first_name + ' ' + candidate_last_name + '!' ' You have completed your test.',
                'Congratulations on test! you scored ',
                'Your grade is: ',
                'You may have entered one or more incorrect value.',
                'If you wish to submit and end the test please enter "SUBMIT" ',
                'Please enter "SUBMIT" to end test: ',
                'Sorry your test was not successfully submitted but do not worry it will be submitted automatically by our server.'
                ]

    while question_attempt_count <= 1:
        # question 1
        if question_attempt_count == 0:
            print(questions[0])
            print(options[0])
            candidate_answer = input('Answer: ').upper()
            question_attempt_count += 1
            if candidate_answer == (question_answer[0]):
                print(feedback[0])
                if candidate_answer == (question_answer[0]):
                    score += 1
                    correct_count += 1
                    print(feedback[5] + str(question_attempt_count) + feedback[4])
                    print(feedback[3] + str(score) + feedback[4])

                else:
                    incorrect_count[0] += 1
                    if incorrect_count[0] == 1 and question_attempt_count == 1:
                        print(feedback[1])
                        print(questions[0])
                        print(options[0])
                        candidate_answer = input('Answer: ').upper()
                        if candidate_answer == (question_answer[0]):
                            print(feedback[0])
                            score += 1
                            correct_count += 1
                            print(feedback[5] + str(question_attempt_count) + feedback[4])
                            print(feedback[3] + str(score) + feedback[4])

                        else:
                            incorrect_count[0] += 1
                            if incorrect_count[0] == 2 and question_attempt_count == 1:
                                print(feedback[2])
                                score += 0
                                print(feedback[5] + str(question_attempt_count) + feedback[4])
                                print(feedback[3] + str(score) + feedback[4])

        # question 2
        if question_attempt_count == 1:
            print(questions[1])
            print(options[1])
            candidate_answer = input('Answer: ').upper()
            question_attempt_count += 1
            if candidate_answer == (question_answer[1]):
                print(feedback[0])
                score += 1
                correct_count += 1
                print(feedback[5] + str(question_attempt_count) + feedback[4])
                print(feedback[3] + str(score) + feedback[4])


            else:
               incorrect_count[1] += 1
               if incorrect_count[1] == 1 and question_attempt_count == 2:
                   print(feedback[1])
                   print(questions[1])
                   print(options[1])
                   candidate_answer = input('Answer: ').upper()
                   if candidate_answer == (question_answer[1]):
                       print(feedback[0])
                       score += 1
                       correct_count += 1
                       print(feedback[5] + str(question_attempt_count) + feedback[4])
                       print(feedback[3] + str(score) + feedback[4])

                   else:
                       incorrect_count[1] += 1
                       if incorrect_count[1] == 2 and question_attempt_count == 2:
                           print(feedback[2])
                           score += 0
                           print(feedback[5] + str(question_attempt_count) + feedback[4])
                           print(feedback[3] + str(score) + feedback[4])

        # question 3
        if question_attempt_count == 2:
           print(questions[2])
           print(options[2])
           candidate_answer = input('Answer: ').upper()
           question_attempt_count += 1
           if candidate_answer == (question_answer[2]):
               print(feedback[0])
               score += 1
               correct_count += 1
               print(feedback[5] + str(question_attempt_count) + feedback[4])
               print(feedback[3] + str(score) + feedback[4])

           else:
               incorrect_count[2] += 1
               if incorrect_count[2] == 1 and question_attempt_count == 3:
                   print(feedback[1])
                   print(questions[2])
                   print(options[2])
                   candidate_answer = input('Answer: ').upper()
                   if candidate_answer == (question_answer[2]):
                       print(feedback[0])
                       score += 1
                       correct_count += 1
                       print(feedback[5] + str(question_attempt_count) + feedback[4])
                       print(feedback[3] + str(score) + feedback[4])

                   else:
                       incorrect_count[2] += 1
                       if incorrect_count[2] == 2 and question_attempt_count == 3:
                           print(feedback[2])
                           score += 0
                           print(feedback[5] + str(question_attempt_count) + feedback[4])
                           print(feedback[3] + str(score) + feedback[4])

        # question 4
        if question_attempt_count == 3:
           print(questions[3])
           print(options[3])
           candidate_answer = input('Answer: ').upper()
           question_attempt_count += 1
           if candidate_answer == (question_answer[3]):
               print(feedback[0])
               score += 1
               correct_count += 1
               print(feedback[5] + str(question_attempt_count) + feedback[4])
               print(feedback[3] + str(score) + feedback[4])

           else:
               incorrect_count[3] += 1
               if incorrect_count[3] == 1 and question_attempt_count == 4:
                   print(feedback[1])
                   print(questions[3])
                   print(options[3])
                   candidate_answer = input('Answer: ').upper()
                   if candidate_answer == (question_answer[3]):
                       print(feedback[0])
                       score += 1
                       correct_count += 1
                       print(feedback[5] + str(question_attempt_count) + feedback[4])
                       print(feedback[3] + str(score) + feedback[4])

                   else:
                       incorrect_count[3] += 1
                       if incorrect_count[3] == 2 and question_attempt_count == 4:
                           print(feedback[2])
                           score += 0
                           print(feedback[5] + str(question_attempt_count) + feedback[4])
                           print(feedback[3] + str(score) + feedback[4])

        # question 5
        if question_attempt_count == 4:
           print(questions[4])
           print(options[4])
           candidate_answer = input('Answer: ').upper()
           question_attempt_count += 1
           if candidate_answer == (question_answer[4]):
               print(feedback[0])
               score += 1
               correct_count += 1
               print(feedback[5] + str(question_attempt_count) + feedback[4])
               print(feedback[3] + str(score) + feedback[4])

           else:
               incorrect_count[4] += 1
               if incorrect_count[4] == 1 and question_attempt_count == 5:
                   print(feedback[1])
                   print(questions[4])
                   print(options[4])
                   candidate_answer = input('Answer: ').upper()
                   if candidate_answer == (question_answer[4]):
                       print(feedback[0])
                       score += 1
                       correct_count += 1
                       print(feedback[5] + str(question_attempt_count) + feedback[4])
                       print(feedback[3] + str(score) + feedback[4])

                   else:
                       incorrect_count[4] += 1
                       if incorrect_count[4] == 2 and question_attempt_count == 5:
                           print(feedback[2])
                           score += 0
                           print(feedback[5] + str(question_attempt_count) + feedback[4])
                           print(feedback[3] + str(score) + feedback[4])

        # question 6
        if question_attempt_count == 5:
           print(questions[5])
           print(options[5])
           candidate_answer = input('Answer: ').upper()
           question_attempt_count += 1
           if candidate_answer == (question_answer[5]):
               print(feedback[0])
               score += 1
               correct_count += 1
               print(feedback[5] + str(question_attempt_count) + feedback[4])
               print(feedback[3] + str(score) + feedback[4])

           else:
               incorrect_count[5] += 1
               if incorrect_count[5] == 1 and question_attempt_count == 6:
                   print(feedback[1])
                   print(questions[5])
                   print(options[5])
                   candidate_answer = input('Answer: ').upper()
                   if candidate_answer == (question_answer[5]):
                       print(feedback[0])
                       score += 1
                       correct_count += 1
                       print(feedback[5] + str(question_attempt_count) + feedback[4])
                       print(feedback[3] + str(score) + feedback[4])

                   else:
                       incorrect_count[5] += 1
                       if incorrect_count[5] == 2 and question_attempt_count == 6:
                           print(feedback[2])
                           score += 0
                           print(feedback[5] + str(question_attempt_count) + feedback[4])
                           print(feedback[3] + str(score) + feedback[4])

        # question 7
        if question_attempt_count == 6:
           print(questions[6])
           print(options[6])
           candidate_answer = input('Answer: ').upper()
           question_attempt_count += 1
           if candidate_answer == (question_answer[6]):
               print(feedback[0])
               score += 1
               correct_count += 1
               print(feedback[5] + str(question_attempt_count) + feedback[4])
               print(feedback[3] + str(score) + feedback[4])

           else:
               incorrect_count[6] += 1
               if incorrect_count[6] == 1 and question_attempt_count == 7:
                   print(feedback[1])
                   print(questions[6])
                   print(options[6])
                   candidate_answer = input('Answer: ').upper()
                   if candidate_answer == (question_answer[6]):
                       print(feedback[0])
                       score += 1
                       correct_count += 1
                       print(feedback[5] + str(question_attempt_count) + feedback[4])
                       print(feedback[3] + str(score) + feedback[4])

                   else:
                       incorrect_count[6] += 1
                       if incorrect_count[6] == 2 and question_attempt_count == 7:
                           print(feedback[2])
                           score += 0
                           print(feedback[5] + str(question_attempt_count) + feedback[4])
                           print(feedback[3] + str(score) + feedback[4])

        # question 8
        if question_attempt_count == 7:
           print(questions[7])
           print(options[7])
           candidate_answer = input('Answer: ').upper()
           question_attempt_count += 1
           if candidate_answer == (question_answer[7]):
               print(feedback[0])
               score += 1
               correct_count += 1
               print(feedback[5] + str(question_attempt_count) + feedback[4])
               print(feedback[3] + str(score) + feedback[4])

           else:
               incorrect_count[7] += 1
               if incorrect_count[7] == 1 and question_attempt_count == 8:
                   print(feedback[1])
                   print(questions[7])
                   print(options[7])
                   candidate_answer = input('Answer: ').upper()
                   if candidate_answer == (question_answer[7]):
                       print(feedback[0])
                       score += 1
                       correct_count += 1
                       print(feedback[5] + str(question_attempt_count) + feedback[4])
                       print(feedback[3] + str(score) + feedback[4])

                   else:
                       incorrect_count[7] += 1
                       if incorrect_count[7] == 2 and question_attempt_count == 8:
                           print(feedback[2])
                           score += 0
                           print(feedback[5] + str(question_attempt_count) + feedback[4])
                           print(feedback[3] + str(score) + feedback[4])

        # question 9
        if question_attempt_count == 8:
           print(questions[8])
           print(options[8])
           candidate_answer = input('Answer: ').upper()
           question_attempt_count += 1
           if candidate_answer == (question_answer[8]):
               print(feedback[0])
               score += 1
               correct_count += 1
               print(feedback[5] + str(question_attempt_count) + feedback[4])
               print(feedback[3] + str(score) + feedback[4])

           else:
               incorrect_count[8] += 1
               if incorrect_count[8] == 1 and question_attempt_count == 9:
                   print(feedback[1])
                   print(questions[8])
                   print(options[8])
                   candidate_answer = input('Answer: ').upper()
                   if candidate_answer == (question_answer[8]):
                       print(feedback[0])
                       score += 1
                       correct_count += 1
                       print(feedback[5] + str(question_attempt_count) + feedback[4])
                       print(feedback[3] + str(score) + feedback[4])

                   else:
                       incorrect_count[8] += 1
                       if incorrect_count[8] == 2 and question_attempt_count == 9:
                           print(feedback[2])
                           score += 0
                           print(feedback[5] + str(question_attempt_count) + feedback[4])
                           print(feedback[3] + str(score) + feedback[4])

        # question 10
        if question_attempt_count == 9:
           print(questions[9])
           print(options[9])
           candidate_answer = input('Answer: ').upper()
           question_attempt_count += 1
           if candidate_answer == (question_answer[9]):
               print(feedback[0])
               score += 1
               correct_count += 1
               print(feedback[5] + str(question_attempt_count) + feedback[4])
               print(feedback[3] + str(score) + feedback[4])
               break

           else:
               incorrect_count[9] += 1
               if incorrect_count[9] == 1 and question_attempt_count == 10:
                   print(feedback[1])
                   print(questions[9])
                   print(options[9])
                   candidate_answer = input('Answer: ').upper()
                   if candidate_answer == (question_answer[9]):
                       print(feedback[0])
                       score += 1
                       correct_count += 1
                       print(feedback[5] + str(question_attempt_count) + feedback[4])
                       print(feedback[3] + str(score) + feedback[4])
                       break

                   else:
                       incorrect_count[9] += 1
                       if incorrect_count[9] == 2 and question_attempt_count == 10:
                           print(feedback[2])
                           score += 0
                           print(feedback[5] + str(question_attempt_count) + feedback[4])
                           print(feedback[3] + str(score) + feedback[4])
                           break

    while candidate_end_test_input != end_test_input:
        if incorrect_candidate_end_test_input == 0:
            print(feedback[6])
            candidate_end_test_input = input(feedback[10]).upper()
        if candidate_end_test_input == end_test_input:
            print(feedback[7] + str(score) + feedback[4])
            score_percent = (score / total_number_of_questions) * (100)
            if score_percent >= 0 and score_percent <= 44:
                print(feedback[8] + grades[4])
            if score_percent >= 45 and score_percent <= 49:
                print(feedback[8] + grades[3])
            if score_percent >= 50 and score_percent <= 59:
                print(feedback[8] + grades[2])
            if score_percent >= 60 and score_percent <= 69:
                print(feedback[8] + grades[1])
            if score_percent >= 70 and score_percent <= 100:
                print(feedback[8] + grades[0])

        else:
            incorrect_candidate_end_test_input += 1
            print(feedback[9])
            candidate_end_test_input = input(feedback[11]).upper()
            if candidate_end_test_input == end_test_input:
                print(feedback[7] + str(score) + feedback[4])
                score_percent = (score / total_number_of_questions) * (100)
                if score_percent >= 0 and score_percent <= 44:
                    print(feedback[8] + grades[4])
                if score_percent >= 45 and score_percent <= 49:
                    print(feedback[8] + grades[3])
                if score_percent >= 50 and score_percent <= 59:
                    print(feedback[8] + grades[2])
                if score_percent >= 60 and score_percent <= 69:
                    print(feedback[8] + grades[1])
                if score_percent >= 70 and score_percent <= 100:
                    print(feedback[8] + grades[0])

            elif incorrect_candidate_end_test_input == 2:
                print(feedback[12])
                break


if __name__ == "__main__":
    main()
