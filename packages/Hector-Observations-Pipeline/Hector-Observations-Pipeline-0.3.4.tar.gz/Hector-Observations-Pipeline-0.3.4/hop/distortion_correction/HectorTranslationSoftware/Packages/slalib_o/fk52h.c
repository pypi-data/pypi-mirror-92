/*
** Copyright (C) 2009 P.T.Wallace.
** Use for profit prohibited - enquiries to ptw@tpsoft.demon.co.uk.
*/
#include "slalib.h"
#include "slamac.h"
void slaFk52h(double qfoo,double qbar,double qbaz,double Q0,
double*rh,double*qfobar,double*q1,double*q2)
#define qfoobar 0.484813681109535994e-5
{static double Q3[3]={-19.9e-3*qfoobar,-9.1e-3*qfoobar,
22.9e-3*qfoobar},q4[3]={-0.30e-3*qfoobar,0.60e-3*qfoobar,
0.70e-3*qfoobar};double qfOBAz[6],qfoobaz[3][3],QQUUX[3],Q5[
6],QFRED,qdog,qcat;int QFISH;slaDs2c6(qfoo,qbar,1.0,qbaz,Q0,
0.0,qfOBAz);slaDav2m(Q3,qfoobaz);slaDmxv(qfoobaz,qfOBAz,Q5);
slaDvxv(qfOBAz,q4,QQUUX);for(QFISH=0;QFISH<3;QFISH++){QQUUX[
QFISH]=qfOBAz[QFISH+3]+QQUUX[QFISH];}slaDmxv(qfoobaz,QQUUX,
Q5+3);slaDc62s(Q5,&QFRED,qfobar,&qdog,q1,q2,&qcat);*rh=
slaDranrm(QFRED);}
