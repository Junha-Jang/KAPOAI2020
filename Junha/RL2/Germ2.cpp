#include <stdio.h>
#include <algorithm>
using namespace std;

int player;
int B[7][7];
int p[4];

int hash_(int typ){
	int s1=0,s2=0,s3=0;
	int e2=0,e3=0;
	int shape=0;

	for(int dx=-3;dx<=3;dx++){
		for(int dy=-3;dy<=3;dy++){
			if(!dx && !dy) continue;
			if(p[0]+dx<0 || p[0]+dx>=7 || p[1]+dy<0 || p[1]+dy>=7) continue;

			if(B[p[0]+dx][p[1]+dy]!=3-player) continue;
			if(max(abs(dx),abs(dy))==1) s1=1;
			if(max(abs(dx),abs(dy))==2) s2=1;
			if(max(abs(dx),abs(dy))==3) s3=1;
		}
	}

	for(int dx=-3;dx<=3;dx++){
		for(int dy=-3;dy<=3;dy++){
			if(abs(dx)<=1 && abs(dy)<=1) continue;
			if(p[2]+dx<0 || p[2]+dx>=7 || p[3]+dy<0 || p[3]+dy>=7) continue;

			if(B[p[2]+dx][p[3]+dy]!=3-player) continue;
			if(max(abs(dx),abs(dy))==2) e2=1;
			if(max(abs(dx),abs(dy))==3) e3=1;
		}
	}

	for(int dx=-1;dx<=1;dx++){
		for(int dy=-1;dy<=1;dy++){
			if(!dx && !dy) continue;
			
			shape<<=1;
			if(p[2]+dx<0 || p[2]+dx>=7 || p[3]+dy<0 || p[3]+dy>=7) shape|=1;
			else if(B[p[2]+dx][p[3]+dy]) shape|=1;
		}
	}

	if(typ<2) return (typ<<12)+((s1|s2)<<11)+(s3<<10)+(e2<<9)+(e3<<8)+shape+1;
	return (typ<<12)+(s1<<11)+(s2<<10)+(e2<<9)+(e3<<8)+shape+1;
}

int main(){
	scanf("%d",&player);
	for(int i=0;i<7;i++){
		for(int j=0;j<7;j++) scanf("%d",&B[i][j]);
	}
	for(int i=0;i<4;i++) scanf("%d",&p[i]);

	if(p[0]==-1){
		printf("0");
		return 0;
	}


	if(p[2]-p[0]<0){
		for(int i=0;i<3;i++){
			for(int j=0;j<7;j++) swap(B[i][j],B[6-i][j]);
		}
		p[0]=6-p[0];
		p[2]=6-p[2];
	}

	if(p[3]-p[1]<0){
		for(int i=0;i<7;i++){
			for(int j=0;j<3;j++) swap(B[i][j],B[i][6-j]);
		}
		p[1]=6-p[1];
		p[3]=6-p[3];
	}

	if(p[2]-p[0]<p[3]-p[1]){
		for(int i=0;i<7;i++){
			for(int j=i+1;j<7;j++) swap(B[i][j],B[j][i]);
		}
		swap(p[0],p[1]);
		swap(p[2],p[3]);
	}

	int idx;
	if(p[2]-p[0]==1) idx=hash_(p[3]-p[1]);
	else idx=hash_(p[3]-p[1]+2);

	printf("%d",idx);

	return 0;
}