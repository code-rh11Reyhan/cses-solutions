#include <bits/stdc++.h>
using namespace std;
int main(){
 
    ios:: sync_with_stdio(0);
    cin.tie(0);
    multiset<int> tickets;
    int n;
    int m;
    cin >> n;
    cin >> m;
    for(int i = 0; i < n; i++){
        int x;
        cin >> x;
        tickets.insert(x);
    }
 
    for(int i = 0; i < m; i++){
        int x;
        cin >> x;
 
        auto it = tickets.upper_bound(x);
 
        if(it == tickets.begin()){
            cout << -1 << '\n';
        }
        else{
            --it;
            cout << *it << '\n';
            tickets.erase(it);
        }
    }
}
