/*
** Copyright (C) 2009 P.T.Wallace.
** Use for profit prohibited - enquiries to ptw@tpsoft.demon.co.uk.
*/
#include "slalib.h"
#include "slamac.h"
double slaSp(double qfoo)
#define qbar 36525.0
#define qbaz 51544.5
{double Q0;Q0=(qfoo-qbaz)/qbar;return-47e-6*Q0*DAS2R;}
