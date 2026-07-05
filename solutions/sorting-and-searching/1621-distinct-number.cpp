#include <bits/stdc++.h>
using namespace std;
 
int main(){
    ios::sync_with_stdio(0);
    cin.tie(0);
 
    long long n;
    cin>>n;
 
 
    vector<long long> v;
    long long x;
    for(int i=0; i<n; i++){
        cin >> x;
        v.push_back(x);
    }
 
    sort(v.begin(), v.end());
 
    long long count = 1;
 
    for(int i = 0; i<v.size()-1; i++){
        if(v[i]!=v[i+1]){
            count ++;
        }
    }
    cout<<count;
    return 0;
}
