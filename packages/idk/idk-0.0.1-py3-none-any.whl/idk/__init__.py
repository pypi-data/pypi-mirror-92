def foo(a,b):
  return a+b
  
  
def fib(n,n1:int,n2:int):    # write Fibonacci series up to n
    a, b = n1, n2
    while a < n:
      print(a, end=' ')
      a, b = b, a+b