from __future__ import print_function, unicode_literals

from PyInquirer import style_from_dict, Token, prompt, Separator
from pprint import pprint

def present_menu(suggestions):

    style = style_from_dict({
        Token.Separator: '#cc5454',
        Token.QuestionMark: '#673ab7 bold',
        Token.Selected: '#cc5454',  # default
        Token.Pointer: '#673ab7 bold',
        Token.Instruction: '',  # default
        Token.Answer: '#f44336 bold',
        Token.Question: '',
    })

    questions = [
        {
            'type': 'checkbox',
            'message': 'Select which jobs to share on LinkedIn:',
            'name': 'posts',
            'choices': [],
            'validate': lambda answer: 'You must choose at least one option.' \
                if len(answer) == 0 else True
        }
    ]

    # Load menu options.
    questions[0]['choices'].append(Separator("{:=^40}".format("OPTIONS")))
    for job in suggestions:
        questions[0]['choices'].append({'name': "{:<32}: {:>32}".format(job['title'], job['guid'])})
    questions[0]['choices'].append({'name': 'None'})

    answers = prompt(questions, style=style)
    if 'None' in answers['posts']:
        return None
    return answers
