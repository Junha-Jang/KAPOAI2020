#include <stdio.h>
#include <vector>
#include <algorithm>
#define pii pair<int,int>
#define pi4 pair<pii,pii>
#define ff first
#define ss second
#define INF 1e9
#define n 7
using namespace std;

vector<vector<int> > B(n,vector<int>(n,0));

vector<vector<int> > next_board(vector<vector<int> > A,pi4 p,int typ){
	vector<vector<int> > AA(n,vector<int>(n,0));
	for(int i=0;i<n;i++){
		for(int j=0;j<n;j++) AA[i][j]=A[i][j];
	}
	
	if(p.ff.ff==-1){
		for(int i=0;i<=n;i++){
			for(int j=0;j<n;j++){
				if(!AA[i][j]) AA[i][j]=-typ;
			}
		}
		return AA;
	}

	int x1=p.ff.ff,y1=p.ff.ss;
	int x2=p.ss.ff,y2=p.ss.ss;
	
	AA[x2][y2]=typ;
	if(max(abs(x2-x1),abs(y2-y1))==2) AA[x1][y1]=0;
	for(int dx=-1;dx<=1;dx++){
		for(int dy=-1;dy<=1;dy++){
			if(x2+dx<0 || x2+dx>=n || y2+dy<0 || y2+dy>=n) continue;
			if(AA[x2+dx][y2+dy]==-typ) AA[x2+dx][y2+dy]=typ;
		}
	}

	return AA;
}

int score(vector<vector<int> > A,int typ){
	int res=0;
	for(int i=0;i<n;i++){
		for(int j=0;j<n;j++){
			if(A[i][j]==typ) res++;
			if(A[i][j]==-typ) res--;
		}
	}
	return res;
}

bool game_end(vector<vector<int> > A){
	for(int i=0;i<n;i++){
		for(int j=0;j<n;j++){
			if(!A[i][j]) return false;
		}
	}
	return true;
}

vector<pi4> all_move(vector<vector<int> > A,int typ){
	vector<pi4> vc;
	for(int x=0;x<n;x++){
		for(int y=0;y<n;y++){
			if(A[x][y]!=typ) continue;

			for(int dx=-2;dx<=2;dx++){
				for(int dy=-2;dy<=2;dy++){
					if(x+dx<0 || x+dx>=n || y+dy<0 || y+dy>=n) continue;
					if(!A[x+dx][y+dy]) vc.push_back({{x,y},{x+dx,y+dy}});
				}
			}
		}
	}
	return vc;
}

pi4 rand_move(){
	vector<pi4> vc=all_move(B,1);

	if(vc.empty()) return {{-1,-1},{-1,-1}};
	return vc[rand()%vc.size()];
}

int get_phase(){
	int cnt=0;
	for(int x=0;x<n;x++){
		for(int y=0;y<n;y++){
			if(B[x][y]) cnt++;
		}
	}
	if(cnt>=n*n-10) return 3;

	for(int x1=0;x1<n;x1++){
		for(int y1=0;y1<n;y1++){
			if(B[x1][y1]!=1) continue;

			for(int x2=x1-3;x2<=x1+3;x2++){
				for(int y2=y1-3;y2<=y1+3;y2++){
					if(x2<0 || x2>=n || y2<0 || y2>=n) continue;
					if(B[x2][y2]==-1) return 2;
				}
			}
		}
	}

	return 1;
}

pi4 phase1(){
	int cntu=0,cntd=0,cntl=0,cntr=0;

	for(int x=0;x<n;x++){
		for(int y=0;y<n;y++){
			if(B[x][y]!=-1) continue;
			
			if(x>y){
				if(6-x>y) cntl++;
				if(6-x<y) cntd++;
			}
			if(x<y){
				if(6-x>y) cntu++;
				if(6-x<y) cntr++;
			}
		}
	}

	pi4 p;
	int mx=max(max(cntu,cntd),max(cntl,cntr));
	if(mx==cntu){
		if(!B[1][5]) p={{0,6},{1,5}};
		else if(!B[2][4]) p={{1,5},{2,4}};
		else if(!B[1][4]) p={{2,4},{1,4}};
		else if(!B[2][5]) p={{2,4},{2,5}};
		else if(!B[5][1]) p={{6,0},{5,1}};
		else if(!B[4][2]) p={{5,1},{4,2}};
		else if(!B[4][1]) p={{4,2},{4,1}};
		else if(!B[5][2]) p={{4,2},{5,2}};
		else p=rand_move();
	}
	else if(mx==cntd){
		if(!B[5][1]) p={{6,0},{5,1}};
		else if(!B[4][2]) p={{5,1},{4,2}};
		else if(!B[5][2]) p={{4,2},{5,2}};
		else if(!B[4][1]) p={{4,2},{4,1}};
		else if(!B[1][5]) p={{0,6},{1,5}};
		else if(!B[2][4]) p={{1,5},{2,4}};
		else if(!B[2][5]) p={{2,4},{2,5}};
		else if(!B[1][4]) p={{2,4},{1,4}};
		else p=rand_move();
	}
	else if(mx==cntl){
		if(!B[5][1]) p={{6,0},{5,1}};
		else if(!B[4][2]) p={{5,1},{4,2}};
		else if(!B[4][1]) p={{4,2},{4,1}};
		else if(!B[5][2]) p={{4,2},{5,2}};
		else if(!B[1][5]) p={{0,6},{1,5}};
		else if(!B[2][4]) p={{1,5},{2,4}};
		else if(!B[1][4]) p={{2,4},{1,4}};
		else if(!B[2][5]) p={{2,4},{2,5}};
		else p=rand_move();
	}
	else if(mx==cntr){
		if(!B[1][5]) p={{0,6},{1,5}};
		else if(!B[2][4]) p={{1,5},{2,4}};
		else if(!B[2][5]) p={{2,4},{2,5}};
		else if(!B[1][4]) p={{2,4},{1,4}};
		else if(!B[5][1]) p={{6,0},{5,1}};
		else if(!B[4][2]) p={{5,1},{4,2}};
		else if(!B[5][2]) p={{4,2},{5,2}};
		else if(!B[4][1]) p={{4,2},{4,1}};
		else p=rand_move();
	}

	return p;
}

pair<pi4,int> phase23(vector<vector<int> > A,int dep){
	if(!dep) return {{{-1,-1},{-1,-1}},score(A,1)};

	int mx1=-INF; pi4 mxp1;
	vector<pi4> vc1=all_move(A,1);
	if(vc1.empty()){
		pi4 p1={{-1,-1},{-1,-1}};
		vector<vector<int> > AA=next_board(A,p1,1);
		return {p1,score(AA,1)};
	}
	for(pi4 p1:vc1){
		vector<vector<int> > AA=next_board(A,p1,1);

		int mn2=INF;
		vector<pi4> vc2=all_move(AA,-1);
		if(vc2.empty()){
			pi4 p2={{-1,-1},{-1,-1}};
			vector<vector<int> > AAA=next_board(AA,p2,-1);
			mn2=score(AAA,1);
		}
		for(pi4 p2:vc2){
			vector<vector<int> > AAA=next_board(AA,p2,-1);

			pair<pi4,int> res=phase23(AAA,dep-1);
			mn2=min(mn2,res.ss);
		}

		if(mx1<mn2) mx1=mn2,mxp1=p1;
	}

	return {mxp1,mx1};
}

void print(){
	for(int i=0;i<n;i++){
		for(int j=0;j<n;j++) printf("%2d ",B[i][j]);
		printf("\n");
	}
	printf("\n");
}

int main(){
	B[0][0]=B[n-1][n-1]=-1;
	B[0][n-1]=B[n-1][0]=1;

	printf("First action?\n");
	int a,b,c,d; scanf("%d %d %d %d",&a,&b,&c,&d);
	if(a>=0) B=next_board(B,{{a,b},{c,d}},-1);

	while(!game_end(B)){
		int idx=get_phase();
		pi4 p;

		switch(idx){
			case 1:
				p=phase1();
				break;
			case 2:
				p=phase23(B,1).ff;
				break;
			case 3:
				p=phase23(B,2).ff;
				break;
		}
		printf("K: (%2d, %2d, %2d, %2d)\n",p.ff.ff,p.ff.ss,p.ss.ff,p.ss.ss);

		B=next_board(B,p,1);
		print();

		printf("Next action?\n");
		int a,b,c,d;
		if(scanf("%d %d %d %d",&a,&b,&c,&d)==EOF) return 0;
		printf("P: (%2d, %2d, %2d, %2d)\n",a,b,c,d);

		B=next_board(B,{{a,b},{c,d}},-1);
		print();
	}

	return 0;
}
