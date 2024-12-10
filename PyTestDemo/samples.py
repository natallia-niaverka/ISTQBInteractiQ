d = {}
d[1] = 1
d['1'] = 2
d[1] += 1

sum = 0
print("D: ", d)

for k in d:
    sum += d[k]

print(sum)

#-------------------------------sample 2
print("-------Sample 2")
dictionary = {"one": "two", "three": "one", "two": "three"}
v = dictionary["one"]

for k in range(len(dictionary)):
    print(k)
    v = dictionary[v]

print(v)

#-----------------sample 3
print("Sample 3")
str = "Gdansk"
str  = "Bo" + str
print("New string: ", str)
