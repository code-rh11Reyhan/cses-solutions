#include <bits/stdc++.h>
using namespace std; 
 
 
int main(){
    ios::sync_with_stdio(0);
    cin.tie(0);
 
    vector<long long> v;
    long long n;
    cin >> n;
 
    v.push_back(n);
 
    while(n!=1){
        if (n%2 == 0){
            n/=2;
        }
        else{
            n*=3;
            n+=1;
        }
        v.push_back(n);
 
    }
 
    for(int i = 0; i<v.size(); i++){
        cout << v[i]<< " ";
    }
    return 0;
}
