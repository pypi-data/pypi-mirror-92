/*
** Copyright (C) 2009 P.T.Wallace.
** Use for profit prohibited - enquiries to ptw@tpsoft.demon.co.uk.
*/
#include "slalib.h"
#include "slamac.h"
double slaGmsta(double qfoo,double qbar){double qbaz,Q0,
qfobar;if(qfoo<qbar){qbaz=qfoo;Q0=qbar;}else{qbaz=qbar;Q0=
qfoo;}qfobar=(qbaz+(Q0-51544.5))/36525.0;return slaDranrm(
DS2R*(24110.54841+(8640184.812866+(0.093104-6.2e-6*qfobar)*
qfobar)*qfobar+86400.0*(dmod(qbaz,1.0)+dmod(Q0,1.0))));}
