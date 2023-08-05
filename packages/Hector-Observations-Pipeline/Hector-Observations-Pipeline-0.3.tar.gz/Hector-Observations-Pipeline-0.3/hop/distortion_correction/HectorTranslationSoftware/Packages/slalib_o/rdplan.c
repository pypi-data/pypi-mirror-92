/*
** Copyright (C) 2009 P.T.Wallace.
** Use for profit prohibited - enquiries to ptw@tpsoft.demon.co.uk.
*/
#include "slalib.h"
#include "slamac.h"
void slaRdplan(double qfoo,int qbar,double qbaz,double phi,
double*Q0,double*qfobar,double*q1)
#define q2 1.49597870e8
#define qfoobar 499.004782
{int Q3,q4,qfOBAz;double qfoobaz,QQUUX[6],Q5[6],QFRED[3][3],
qdog[6],qcat[6],QFISH[6],QgASp[6],Q6,q7,q8,QBAD,qBuG;static 
double qsilly[]={696000.0,2439.7,6051.9,1738.0,3397.0,
71492.0,60268.0,25559.0,24764.0,1151.0};Q3=(qbar>=1&&qbar<=9
)?qbar:0;qfoobaz=slaGmst(qfoo-slaDt(slaEpj(qfoo))/86400.0)+
qbaz;slaDmoon(qfoo,Q5);slaNut(qfoo,QFRED);slaDmxv(QFRED,&Q5[
0],&QQUUX[0]);slaDmxv(QFRED,&Q5[3],&QQUUX[3]);if(Q3==3){for(
qfOBAz=0;qfOBAz<=5;qfOBAz++)Q5[qfOBAz]=QQUUX[qfOBAz];}else{
slaPrenut(2000.0,qfoo,QFRED);slaPlanet(qfoo,3,Q5,&q4);
slaDmxv(QFRED,&Q5[0],&qdog[0]);slaDmxv(QFRED,&Q5[3],&qdog[3]
);for(qfOBAz=0;qfOBAz<=5;qfOBAz++)qcat[qfOBAz]=qdog[qfOBAz]-
0.012150581*QQUUX[qfOBAz];if(Q3==0){for(qfOBAz=0;qfOBAz<=5;
qfOBAz++)Q5[qfOBAz]=-qcat[qfOBAz];}else{slaPlanet(qfoo,Q3,Q5
,&q4);slaDmxv(QFRED,&Q5[0],&QFISH[0]);slaDmxv(QFRED,&Q5[3],&
QFISH[3]);for(qfOBAz=0;qfOBAz<=5;qfOBAz++)Q5[qfOBAz]=QFISH[
qfOBAz]-qcat[qfOBAz];}}slaPvobs(phi,0.0,qfoobaz,QgASp);for(
qfOBAz=0;qfOBAz<=5;qfOBAz++)Q5[qfOBAz]-=QgASp[qfOBAz];Q6=Q5[
0];q7=Q5[1];q8=Q5[2];QBAD=sqrt(Q6*Q6+q7*q7+q8*q8);qBuG=
qfoobar*QBAD;for(qfOBAz=0;qfOBAz<=2;qfOBAz++)Q5[qfOBAz]-=
qBuG*Q5[qfOBAz+3];slaDcc2s(Q5,Q0,qfobar);*Q0=slaDranrm(*Q0);
*q1=2.0*asin(qsilly[Q3]/(QBAD*q2));}
