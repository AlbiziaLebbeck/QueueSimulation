import matplotlib.pyplot as plt

records = open("traffic_record", "r") 

Q1 = []
Q2 = []
for line in records:
    rec = line.split(",")
    src = rec[0][8]
    start_time = float(rec[0].split(":")[1])
    end_time = float(rec[-2].split(":")[1])
    wating_time = end_time - start_time
    if src == '1':
        Q1.append(wating_time)
    else:
        Q2.append(wating_time)

print(sum(Q1)/len(Q1),sum(Q2)/len(Q2))
print(len(Q1),len(Q2))

plt.figure()
plt.subplot(2,1,1)
plt.hist(Q1,range(0,250,2))
plt.xlim([0,230])
# plt.ylim([0,45])
plt.ylabel("users",size=12)
plt.xlabel("waiting time",size=12)
plt.subplot(2,1,2)
plt.hist(Q2,range(0,250,2))
plt.xlim([0,230])
# plt.ylim([0,45])
plt.ylabel("users",size=12)
plt.xlabel("waiting time",size=12)
plt.show()