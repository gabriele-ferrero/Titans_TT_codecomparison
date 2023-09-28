clc

%c0m= 5.25E-6;
l=1E-3;
n_t=1E-3;
E_1=2;
rhow=6.3382E28;
N_Tis=6*rhow;
T=1000;
k_B=8.617333E-5;
a=load('Flux2EvTrap.txt');
b=load("Medium_flux_festim.txt")
time=a(:,1);
%time=(1:1E3:1E6)';
D=1.9E-7*exp(-0.2/k_B/T);
S=2.9E-5*exp(-1/k_B/T);
N_A_const=6.02214076E23;
c0m= (1E5)^0.5*S*1.0525E5;
%%
%zeta=lambda^2/(D*n1)*n_solute*nu0*exp(-E1/(k_b*T));
%zeta=0.0090489;
zeta=(N_Tis*exp((0.2-E_1)/(k_B*T))+c0m*N_A_const)/(rhow*1E-3);
Deff=D/(1+1/zeta);
steepest_an=l^2/(2*pi^2*Deff);
flux=ones(length(time),1);
strong_breaktrough=l^2*n_t/2/c0m/6/D;
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
figure (1)
plot(time(2:end),flux(2:end)*6.02214076E23/2,'--')

hold on
plot(fluxbulk3.times,fluxbulk3.N_conf_recfl,Color='b')
plot(a(1:25:end,1),a(1:25:end,2),'x',Color='r')
plot(b(1:250:end,1),b(1:250:end,2),'o',Color='g')
%plot(time(breakthrough(1):end),steepest(breakthrough(1):end),"--r")
%plot(steepest_an*ones(length(a(:,2)),1),a(:,2),"--b")

title('H flux on the other side of a slab with constant concentration interface - strong trap [2eV]')
xlabel('time [s]')
ylabel('Flux [D_2m^-^2s^-^1]')
legend('analytical','MHIMS','mHIT','Festim',Location="southeast")
ylim([1E-15,flux(end)*1.1*6.02214076E23/2])

figure(2)
plot(time,flux-a(:,2))
xlabel('time [s]')
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
figure (5)
%plot(time(2:end),flux(2:end)*6.022E23/2,'--r')

hold on
%plot(fluxbulk3.times,fluxbulk3.N_conf_recfl,Color='b')
%plot(a(1:50:end,1),a(1:50:end,2)*6.022E23/2,'x',Color='r')

a=load('Flux25EvV32Trap.txt');
b=load("Strong_flux_festim.txt");
plot(a(:,1),a(:,2))

E_1=2.5;
zeta=(N_Tis*exp((0.2-E_1)/(k_B*T))+c0m*N_A_const)/(rhow*1E-3);
Deff=D/(1+1/zeta);
flux=ones(length(time),1);
strong_breaktrough=l^2*n_t*rhow/2/c0m/N_Tis/D;
for m=1:1:10000
    add=2*(-1)^m*exp(-m^2*pi^2*Deff.*time./l^2);
    flux=flux+add;
end
index=find(a(:,2)>0.99*fluxbulk4.N_conf_recfl(end));
time_br_comsol=a(index(1),1)
flux=flux*c0m*D/l;
plot(time(2:end),flux(2:end)*6.022E23/2,'--b')
stronganalytical=l^2*n_t/2/c0m/D*rhow/6.02214076E23;
plot(fluxbulk4.times,fluxbulk4.N_conf_recfl,Color='g')
xline([stronganalytical])
plot(b(:,1),b(:,2),'o',Color='b')
% legend("Analytical Deff trap 2", "MHIMS trap 2", "mHIT trap 2","mHIT trap 3", "Analytical Deff trap 3","MHIMS trap 3", "breakthrough trap 3",'festim')
legend("mHIT trap 3", "Analytical Deff trap 3","MHIMS trap 3", "breakthrough trap 3",'festim',Location="southeast" )
error_br=abs(stronganalytical-time_br_comsol)/stronganalytical*100