/*
** Copyright (C) 2009 P.T.Wallace.
** Use for profit prohibited - enquiries to ptw@tpsoft.demon.co.uk.
*/
#include "slalib.h"
#include "slamac.h"
double slaAirmas(double qfoo){double qbar,qbaz;qbar=fabs(
qfoo);qbaz=1.0/(cos(gmin(1.52,qbar)))-1.0;return 1.0+qbaz*(
0.9981833-qbaz*(0.002875+0.0008083*qbaz));}
