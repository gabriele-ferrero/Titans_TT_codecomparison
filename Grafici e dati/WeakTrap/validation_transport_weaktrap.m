clc

%c0m= 5.25E-6;
l=1E-3;
n_t=1000;
E_1=1;
rhow=6.3382E28;
N_Tis=6*rhow;
T=1000;
k_B=8.617333E-5;
a=load('Flux1EvTrap1.txt');
b=load('Weak_flux_festim.txt');
time=a(:,1);
D=1.9E-7*exp(-0.2/k_B/T);
S=2.9E-5*exp(-1/k_B/T);
N_A_const=6.022E23;
c0m= (1E5)^0.5*S*1.0525E5;
%%
%zeta=lambda^2/(D*n1)*n_solute*nu0*exp(-E1/(k_b*T));
%zeta=0.0090489;
zeta=(N_Tis*exp((0.2-1)/(k_B*T))+c0m*N_A_const)/(rhow*1E-3);
Deff=D/(1+1/zeta);
steepest_an=l^2/(2*pi^2*Deff);
flux=ones(length(time),1);
for m=1:1:10000
    add=2*(-1)^m*exp(-m^2*pi^2*Deff.*time./l^2);
    flux=flux+add;
end
flux=flux*c0m*D/l;
% flux(1)=flux(2);
for i=1:length(flux)-1
    gradflux(i)=flux(i+1)-flux(i);
end
m=max(gradflux);
i=find(gradflux==m);
ti=time(i);
steepest=flux(i)+m/time(1).*(time(1:end)-ti);
breakthrough=find(steepest>=0);
res=time(breakthrough(1));
figure (10)
plot(time,flux*6.022E23/2)
hold on
plot(a(:,1),a(:,2),'b')
plot(b(1:250:end,1),b(1:250:end,2),'ro')

plot(fluxbulk2.times,fluxbulk2.N_conf_recflux_bulkmoleculem2s1)
figure (1)
plot(time,flux*6.022E23/2)

hold on

plot(a(1:50:end,1),a(1:50:end,2)*6.022E23/2,'x')
plot(b(1:50:end,1),b(1:50:end,2)*6.022E23/2,'o')
plot(time(breakthrough(1):end),steepest(breakthrough(1):end)*6.022E23/2,"--r")
% plot(steepest_an*ones(length(a(:,2)),1),a(:,2)*6.022E23/2,"--b")
% plot(fluxbulk2.times(1:50:end),fluxbulk2.N_conf_recflux_bulkmoleculem2s1(1:50:end),'o')
title('H flux on the other side of a slab with constant concentration interface - weak trap')
xlabel('time [s]')
ylabel('Flux [D_2m^-^2s^-^1]')
legend('analytical','COMSOLfeatFestim',"steepest curve COMSOL", "steepest analytical",'MHIMS',Location="southeast")
ylim([1E-15,flux(end)*1.1*6.022E23/2])
figure(2)
plot(time,flux-a(:,2))
xlabel('time [dimensionless]')
%title('Difference between analytical solution and COMSOLfeatFestim ')
ylabel('Difference [atoms/m^2/s]')
figure(3)
plot(time(100:1:end),(flux(100:1:end)-a(100:1:end,2))./a(100:1:end,2))
xlabel('time [dimensionless]')
%title('Difference % between analytical solution and COMSOLfeatFestim ')
ylabel('Difference [%]')
err_steepest_perc=abs(steepest_an-res)/steepest_an*100;

figure (4)
semilogy(time,flux)

hold on

semilogy(a(:,1),a(:,2))
ylim([1E-15,flux(end)*1.1])