import matplotlib.pyplot as plt

model = open('./model2.dat')

depth, vp, vs, rho = [], [], [], []

layer = model.readline()
while layer:
    para = layer.split()
    depth.append(float(para[1]))
    vp.append(float(para[2]))
    vs.append(float(para[3]))
    rho.append(float(para[4]))
    layer = model.readline()
model.close()

depth = [i*1000 for i in depth]
depth.insert(0, 0)
depth.append(depth[-1]+20)
vp.insert(0, 0)
vp.append(vp[-1])
vs.insert(0, 0)
vs.append(vs[-1])
rho.insert(0, 1)
rho.append(rho[-1])

p1 = plt.subplot(1, 2, 1)
p1.plot(vp, depth, lw=2)
p1.plot(vs, depth, lw=2)
p1.xaxis.set_ticks_position('top')
p1.invert_yaxis()
p1.set_ylabel('Depth(m)', fontsize=15)
p1.set_xlabel('Velocity(km/s)', fontsize=15)
plt.xticks(fontsize=15)
plt.yticks(fontsize=15)

p2 = plt.subplot(1, 2, 2)
p2.plot(rho, depth, lw=2)
p2.xaxis.set_ticks_position('top')
p2.invert_yaxis()
p2.set_xlabel('Density(kg/m^3)', fontsize=15)
plt.xticks(fontsize=15)
plt.yticks(fontsize=15)
plt.show()
