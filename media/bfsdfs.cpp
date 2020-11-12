#include<bits/stdc++.h>
using namespace std;
#define MAX 10
typedef struct graph{
	int a[MAX][MAX];
	int i, j, n;
}graph;
void initg(graph *g, char *ch){
	int i, j, d, x;
	FILE *fp = fopen(ch, "r");
	if(fp == NULL) {
		perror(" Open failed");
		//return errno;	
	}
	for (i = 0; i < MAX; i++) {
		for (j = 0; j < MAX; j++) 
			g->a[i][j] = 0;
	}
	
	fscanf(fp,"%d",&g->n);
	for (i = 0; i < g->n; i++) {
		for (j = 0; j < g->n; j++) {
			fscanf(fp,"%d",&(g->a[i][j]));
		}
	} 
}
void printg(graph *g){
	for(int i = 0; i < g->n; i++){
		for(int j = 0; j < g->n; j++){
			cout<<g->a[i][j]<<" ";
		}	
		cout<<"\n";
	}
}

void bfs(graph *g, int s, int goal){
	queue<int> q;
	
	int x, i;
	int *visited = (int*)malloc(sizeof(int) * g->n);
	for( i = 0;i < g->n; i++)
		visited[i]=0;
	q.push(s);
	visited[s] =1;
	
	while(!q.empty()){
		x = q.front();
		q.pop();
		if(x == goal){
			cout<<goal;
			return;
		}
		cout<<x<<"-->";
		for(int i = 0; i < g->n; i++){
			
				
			if(g->a[x][i] !=0 && !visited[i]){
				
				q.push(i);
 				visited[i] =1;
				//v.push_back(i);	
			}	
		}
	}
	cout<<"\n";
	
}
void dfs(graph *g, int s, int goal){
	stack<int> st;
	int x, i;
	int *visited = (int*)malloc(sizeof(int) * g->n);
	for( i = 0;i < g->n; i++)
		visited[i]=0;
	st.push(s);
	visited[s] =1;
	while(!st.empty()){
		x = st.top();
		st.pop();
		if(x == goal){
			cout<<goal;
			return;
		}
			
		cout<<x<<"-->";
		for(int i = 0; i < g->n; i++){
			if(g->a[x][i] !=0 && !visited[i]){
				st.push(i);
 				visited[i] =1;
			}	
		}
	}
	cout<<"\n";
	
}
int main(int argc, char *argv[]){
	graph g;
	initg(&g, argv[1]);
	printg(&g);
	cout<<"\n";
	cout<<"BFS\n";
	bfs(&g, 0, 3);
	cout<<"\nDFS\n";
	dfs(&g, 0, 3);
	return 0;
}
