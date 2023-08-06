def fibonacci():
  a=int(input('Enter the number of times you want the sequence to repeat'))
  b=0
  c=1
  for x in range(a):
    c+=b
    b+=c
    print(c)
    print(b)
print(fibonacci())