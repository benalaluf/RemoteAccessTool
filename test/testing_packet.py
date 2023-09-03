import sys
from io import StringIO

old_stdout = sys.stdout # Memorize the default stdout stream
buffer = StringIO()
sys.stdout = buffer

print('123')
a = 'HeLLo WorLd!'
print(a)
# Call your algorithm function.
# etc...
print("nigga")
sys.stdout = old_stdout # Put the old stream back in place

whatWasPrinted = buffer.getvalue() # Return a str containing the entire contents of the   buffer.
print(whatWasPrinted) # Why not to print it?
print("po")
buffer.close()