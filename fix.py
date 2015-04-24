import os
smallIndex = 1659
startIndex = 2477

i = startIndex
j = smallIndex

# infile = open("inputs/gilt.dat", "r")
# outfile = open("inputs/gilt2.dat", "w")

for s in range(1659, 1969):
  # ignore = False
  # isTop = True 

  # line = infile.readline()
  # if len(line) == 0: break
  os.rename("img/1238/lg-" + str(j) + ".jpg", "img/1238/lg-" + str(i) +".jpg")
  


  # outfile.write(str(i) + line[4:])
  i += 1
  j += 1


# infile.close()
# outfile.close()
