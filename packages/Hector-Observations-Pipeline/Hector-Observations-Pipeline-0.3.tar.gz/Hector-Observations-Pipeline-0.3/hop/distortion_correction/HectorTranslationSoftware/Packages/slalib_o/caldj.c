/*
** Copyright (C) 2009 P.T.Wallace.
** Use for profit prohibited - enquiries to ptw@tpsoft.demon.co.uk.
*/
#include "slalib.h"
#include "slamac.h"
void slaCaldj(int qfoo,int qbar,int qbaz,double*Q0,int*
qfobar){int q1;if((qfoo>=0)&&(qfoo<=49))q1=qfoo+2000;else if
((qfoo>=50)&&(qfoo<=99))q1=qfoo+1900;else q1=qfoo;slaCldj(q1
,qbar,qbaz,Q0,qfobar);}
