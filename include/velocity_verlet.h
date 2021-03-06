#ifndef VELOCITY_VERLET_H
#define VELOCITY_VERLET_H

#include <stdio.h>
#include <data.h>

/*the list of functions.*/
void velverlet1(mdsys_t *sys);
void velverlet2(mdsys_t *sys);
void force(mdsys_t *sys);
int get_a_line(FILE *fp, char *buf);
void output(mdsys_t *sys, FILE *erg, FILE *traj);
void azzero(double *d, const int n);
void ekin(mdsys_t *sys);
double cclock();
double SignR(double v,double x); /*AAA*/
void Putinthebox(mdsys_t *sys); /*AAA*/


#endif
