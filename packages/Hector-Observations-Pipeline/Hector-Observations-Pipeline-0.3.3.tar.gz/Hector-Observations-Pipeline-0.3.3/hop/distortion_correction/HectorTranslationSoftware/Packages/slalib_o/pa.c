/*
** Copyright (C) 2009 P.T.Wallace.
** Use for profit prohibited - enquiries to ptw@tpsoft.demon.co.uk.
*/
#include "slalib.h"
#include "slamac.h"
double slaPa(double qfoo,double qbar,double phi){double qbaz
,Q0,qfobar;qbaz=cos(phi);qfobar=qbaz*sin(qfoo);Q0=sin(phi)*
cos(qbar)-qbaz*sin(qbar)*cos(qfoo);return((qfobar!=0.0||Q0!=
0.0)?atan2(qfobar,Q0):0.0);}
