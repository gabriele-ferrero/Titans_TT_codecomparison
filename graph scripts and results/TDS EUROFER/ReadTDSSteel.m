clc
close all


a=load('TDS_Eurofer_Part1.txt');
a2=load('TDS_Eurofer_Part2.txt');
festim=readtable('derived_quantities.csv');
%index=find(a(:,1)-5000>0)
%plot(300+(a(index(1,1):end,1)-5000),a(index(1,1):end,2)*2)
plot(a(:,1),a(:,2),'r')

b=load('simTDS1.txt');
c=load("simTDS2.txt");
bb=readtable("tds_mars21_873K.csv");
cc=readtable("tds_mars21_1273K.csv");
hold on
x = festim{:, 6}; % Replace 1 with the column index you want to plot on the x-axis
y = festim{:, 7}; % Replace 2 with the column index you want to plot on the y-axis
plot(y,-x,'y')
plot(b(:,1),b(:,2),'b');
plot(bb.T, bb.flux,'g')
plot(a2(:,1),a2(:,2),'r')
plot(c(:,1),c(:,2),'b');

plot(cc.T, cc.flux,'g')
xlabel('Temperature [K]')
ylabel('Flux [H_2/m^2/s]')
legend('festim','mHIT','MHIMS', 'experiment',Location='north')
xlim([290,1300])
ylim([0,3E18])
