#!/usr/local/bin/python3
from PIL import Image
import random
import xlsxwriter
import requests
import os


name = '{}.xlsx'.format(input('Give a name to your spreadsheet!\n> '))
print("Your spreadsheet will be named",name)
workbook = xlsxwriter.Workbook(name)
worksheet = workbook.add_worksheet()



prefill = (input('Prefill answers? [y/n]\n> ')+"n").lower()[0] == 'y'

if (input('Use equation file? [y/n]\n> ')+"n").lower()[0] == 'y':
	filename = input("Filename:\n> Desktop"+os.sep)
	operations = "n/a"
else:
	filename = ""
	operations = input('Which operations should I use? + or - or +-:\n> ')

while True:
	if filename != "":
		break
	try:
		questions = abs(int(input('How many questions should there be? (~20 reccomended, must be more than 3)\n> ')))
		assert questions > 3
		break
	except:
		print('Please provide a number!')

while True:
	if filename != "":
		break
	try:
		max_answer = abs(int(input('What should the highest answer be?\n> ')))
		break
	except:
		print('Please provide a number!')

offset = 3

if filename != "":
	eqs = open(os.path.expanduser("~"+os.sep+'Desktop'+os.sep+filename)).read().split('\n')
	questions = len(eqs)

# data = image pixels
img = Image.open(requests.get(input('URL to the image:\n> '), stream=True).raw)
result = img.resize((78,78),resample=Image.BILINEAR)
width,height = result.size
result = result.convert('P', palette=Image.ADAPTIVE, colors=questions)
result = result.convert('RGB', palette=Image.ADAPTIVE, colors=questions)
data = list(result.getdata())
colors = set(data)



key = {}
keyRGB = {}
answers = []
count = 0
for color in colors:
	if filename != "":
		num = int(eqs[count].split('|=>|')[1].replace(' ',''))
		count += 1
	else:
		num = random.randint(0,max_answer)
	key[num] = '#%02x%02x%02x' % color
	keyRGB[color] = num
	answers.append(num)

newdata = []
for color in data:
	newdata.append(keyRGB[color])
data = newdata
white = workbook.add_format({'font_color':"#ffffff"})
for index, answer in enumerate(answers):
	hexcode = key[answer]
	forma = workbook.add_format({'font_color':hexcode})
	forma.set_pattern(1)
	forma.set_bg_color(hexcode)
	worksheet.conditional_format(index,1,index,1, {'type':     'cell',
		'criteria': '=',
		'value':     answer,
		'format':    forma
	})
	worksheet.conditional_format(index,1,index,1, {'type':     'cell',
		'criteria': '=',
		'value':     answer,
		'format':    forma
	})
	
	if filename == "":
		operation = random.choice(operations)
		if operation == "+":
			p1 = random.randint(0, answer)
			p2 = answer - p1
		elif operation == "-":
			p1 = random.randint(0, answer)
			p2 = answer + p1
		equation = "{} {} {} =".format(p1,operation,p2)
	else:
		equation = eqs[index].split('|=>|')[0]
	worksheet.write(index,0, equation)
	if prefill:
		worksheet.write(index,1, answer)

count = 0
for row in range(height):
	for col in range(width):
		num_for = data[count]
		forma = workbook.add_format({'font_color':key[num_for]})
		forma.set_pattern(1)
		forma.set_bg_color(key[num_for])
		worksheet.write(row, col+offset, "=B"+str(answers.index(num_for)+1))
		worksheet.conditional_format(row,col+offset,row,col+offset, {'type':     'cell',
			'criteria': '=',
			'value':     num_for,
			'format':    forma
		})
		worksheet.conditional_format(row,col+offset,row,col+offset, {'type':     'cell',
			'criteria': '!=',
			'value':     num_for,
			'format':    white
		})
		

		count += 1
worksheet.ignore_errors({'number_stored_as_text': 'A1:XFD1048576'})
worksheet.ignore_errors({'empty_cell_reference': 'A1:XFD1048576'})
worksheet.ignore_errors({'formula_differs': 'A1:XFD1048576'})
worksheet.set_zoom(10)
worksheet.set_column(offset,offset+width,1.5)
workbook.close()