def factorial(): 
  a=int(input('Enter Number'))
  b=1
  for x in range(1,a+1):
    b*=x
  return b
print(factorial())