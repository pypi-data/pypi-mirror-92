/*
** Copyright (C) 2009 P.T.Wallace.
** Use for profit prohibited - enquiries to ptw@tpsoft.demon.co.uk.
*/
#include "slalib.h"
#include "slamac.h"
void slaTp2s(float qfoo,float qbar,float qbaz,float Q0,float
*qfobar,float*q1){float q2,qfoobar,Q3,q4;q2=(float)sin(Q0);
qfoobar=(float)cos(Q0);Q3=qfoobar-qbar*q2;q4=(float)atan2(
qfoo,Q3);*qfobar=slaRanorm(q4+qbaz);*q1=(float)atan2(q2+qbar
*qfoobar,sqrt(qfoo*qfoo+Q3*Q3));}
