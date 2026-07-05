#include <bits/stdc++.h>
using namespace std;
 
void bfs(int sr, int sc, vector<vector<char>>& grid,
         vector<vector<bool>>& visited) {
 
    int n = grid.size();
    int m = grid[0].size();
 
    vector<int> del_row = {-1, 0, 1, 0};
    vector<int> del_col = {0, -1, 0, 1};
    vector<char> Letters = {'U', 'L', 'D', 'R'};
 
    vector<vector<pair<int,int>>> parent(n,
        vector<pair<int,int>>(m, {-1,-1}));
 
    vector<vector<char>> moveTaken(n,
        vector<char>(m));
 
    queue<pair<int,int>> q;
 
    q.push({sr, sc});
    visited[sr][sc] = true;
 
    while(!q.empty()){
 
        int row = q.front().first;
        int col = q.front().second;
        q.pop();
 
        if(grid[row][col] == 'B'){
 
            string ans;
 
            while(!(row == sr && col == sc)){
                ans.push_back(moveTaken[row][col]);
 
                pair<int,int> p = parent[row][col];
                row = p.first;
                col = p.second;
            }
 
            reverse(ans.begin(), ans.end());
 
            cout << "YES\n";
            cout << ans.size() << "\n";
            cout << ans << "\n";
            return;
        }
 
        for(int i = 0; i < 4; i++){
 
            int nrow = row + del_row[i];
            int ncol = col + del_col[i];
 
            if(nrow >= 0 && nrow < n &&
               ncol >= 0 && ncol < m &&
               !visited[nrow][ncol] &&
               grid[nrow][ncol] != '#'){
 
                visited[nrow][ncol] = true;
 
                parent[nrow][ncol] = {row, col};
                moveTaken[nrow][ncol] = Letters[i];
 
                q.push({nrow, ncol});
            }
        }
    }
 
    cout << "NO\n";
}
 
int main(){
 
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
 
    int n, m;
    cin >> n >> m;
 
    vector<vector<char>> grid(n, vector<char>(m));
    vector<vector<bool>> visited(n, vector<bool>(m, false));
 
    int sr, sc;
 
    for(int i = 0; i < n; i++){
        for(int j = 0; j < m; j++){
            cin >> grid[i][j];
 
            if(grid[i][j] == 'A'){
                sr = i;
                sc = j;
            }
        }
    }
 
    bfs(sr, sc, grid, visited);
 
    return 0;
}
