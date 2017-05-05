clc
Vt=25*10^(-3);
Is=2.044*10^(-13);
Ksol=0.3662;
Aref=23.895*10^(-6);
Ef=linspace(0,1600,161);
k=ones(161,1)*Ef;
Il=Ksol.*Aref.*k;
Id=Il';
Ipom=triu(Il-Id);
Vd=Vt.*log(((Ipom)./Is)+1);
P=Id.*Vd;
Iz=Ksol.*Aref.*Ef;
%save pizlaz1.txt P;
%save iulaz1.txt Iz;
eta=P./(k.*Aref);
mesh(Ef, Iz, eta);
xlabel "Solar flux [W/m^2]";
ylabel "Current draw [A]";
zlabel "Power efficiency";
figure
plot(Ef,eta(20, :),Ef,eta(40, :),Ef,eta(60, :),Ef,eta(80, :),Ef,eta(100, :));
xlabel "Solar flux [W/m^2]";
ylabel "Power efficiency";
figure
plot(Iz,eta'(20 , :),Iz,eta'(40, :),Iz,eta'(60, :),Iz,eta'(80, :),Iz,eta'(100, :));
xlabel "Current draw [A]";
ylabel "Power efficiency";