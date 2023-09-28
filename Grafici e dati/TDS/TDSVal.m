clc
close all 
clear all

COMS=load('TDS_aggiornato_Final.txt');
fest=load("TDS_W.txt");
figure (2)

bb=readtable("Exp_OgorodnikovaJNM2003_fluence_1e23.csv");
cc=load("exp_T.txt");
dd=load("exp_flux.txt");
%plot((a(:,1)-a(1,1))*8+300,a(:,2))
plot(COMS(1:10:end,1),COMS(1:10:end,2),'b',LineWidth=1)
hold on
plot(fest(:,1),fest(:,2),'r',LineWidth=1)
%title('H flux on the other side of a slab with constant concentration interface')
xlabel('Temperature [K]')
ylabel('Flux [atoms/m^2/s]')
%legend('analytical','COMSOLfeatFestim',"steepest curve COMSOL", "steepest analytical",Location="northwest")
hold on 

plot(cc,dd,LineWidth=1)
plot(bb.Var1,bb.Var2*1E19,'--')
legend('mHIT','Festim','MHIMS', 'experiment')
xlim([301,900])
ylim([0,1E19])
% figure (3)
% plot(COMS(:,1),COMS(:,2))
% plot(fest(1:10:end,1),fest(1:10:end,2)*2,'xr')
% hold on
% e=load('TDS_VolSource_aggiornato.txt');
% plot(e(:,1),e(:,2))
% figure(4)
% plot(e(:,1),abs((e(:,2)-COMS(:,2))./e(:,2).*100))