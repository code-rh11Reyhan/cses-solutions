#include <bits/stdc++.h>
 
using namespace std;
 
void dfs(int sr, int sc, vector<vector<char>>&grid, vector<vector<bool>>&visited){
    visited[sr][sc] = true;
    vector<int> del_row = {-1, 0, 1, 0};
    vector<int> del_col = {0, -1, 0, 1};
    int rooms = 0;
    for(int i = 0; i<4; i++){
        int nrow = sr+del_row[i];
        int ncol = sc+del_col[i];
        if(nrow>=0 && nrow<grid.size() && ncol>=0 && ncol<grid[0].size() && grid[nrow][ncol] == '.' && !visited[nrow][ncol]){
            dfs(nrow, ncol, grid, visited);
            
        }
    }
    
}
 
int main(){
    ios::sync_with_stdio(0);
    cin.tie(0);
    int n;
    int m;
    cin>> n;
    cin>> m;
 
    vector<vector<char>> grid(n, vector<char>(m));
    for(int i = 0; i< n; i++){
        for(int j = 0; j<m; j++){
            cin>> grid[i][j];
        }
    }
    
    vector<vector<bool>> visited(n, vector<bool>(m, false));
 
    int rooms = 0;
 
    for(int i = 0; i<grid.size(); i++){
        for(int j = 0; j<grid[0].size(); j++){
            if(grid[i][j] == '.' && !visited[i][j]){
                dfs(i, j, grid, visited);
                rooms++;
            }
        }
    }
    cout<< rooms;
 
 
    return 0;
}
