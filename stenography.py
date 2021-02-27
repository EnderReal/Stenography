import cv2
import sys
import numpy as np
import os

def binary(data):
	if type(data) == str:
		return ''.join([ format(ord(i), "08b") for i in data ])
	else:
		return format(data, "08b")

def char(data):
	bin_chunks = [data[8*i:8*(i+1)] for i in range(len(data)//8)]
	ints = [int(x, 2) for x in bin_chunks]
	chars = [chr(x) for x in ints]
	return ''.join(chars)

def test(data):
	if char(data)[-4:] == "####":
		print("Message:",char(data)[:-4])
		os.system("pause")
		sys.exit()

def encode():
	message=input("Message:")
	message=message+'####'
	bin=binary(message)
	ii=input("Image:")
	img = cv2.imread(ii)
	height, length, c = img.shape
	imax=height*length*3
	if(len(bin)>imax):
		print("Message too big.")
		sys.exit()
	index=0
	for i in img:
		for j in i:
			rr,gg,bb=j
			r=binary(rr)
			g=binary(gg)
			b=binary(bb)
			if index < len(bin):
				j[0] = int(r[:-1] + bin[index], 2)
				index += 1
			if index < len(bin):
				j[1] = int(g[:-1] + bin[index], 2)
				index += 1
			if index < len(bin):
				j[2] = int(b[:-1] + bin[index], 2)
				index += 1
			if index >= len(bin):
				break
	cv2.imwrite('steno.png', img)

def decode():
	ii=input("Image:")
	img=cv2.imread(ii)
	msg=''
	try:
		for i in img:
			for j in i:
				rr,gg,bb=j
				r=binary(rr)
				g=binary(gg)
				b=binary(bb)
				msg=msg+r[-1:]
				test(msg)
				msg=msg+g[-1:]
				test(msg)
				msg=msg+b[-1:]
				test(msg)
		print("No valid message detected.")
		sys.exit()
	except Exception as err:
		print("Invalid file name or format")			
	
ac=input(" 1.Encode: \n 2.Decode: \n 1/2:")
if int(ac)==1:
	encode()
else:
	decode()