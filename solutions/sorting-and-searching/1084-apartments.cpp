#include <bits/stdc++.h>
using namespace std;
 
int main(){
    ios::sync_with_stdio(0);
    cin.tie(0);
 
    long n;
    long m;
    long k;
 
    cin>> n >> m>> k;
 
    vector<long> per_req;
    vector<long> asize;
    long x;
    long y;
    long count = 0;
    for(long i = 0; i<n; i++){
        cin>>x;
        per_req.push_back(x);
    }
    for( long i = 0; i<m; i++){
        cin>>y;
        asize.push_back(y);
    }
    sort(per_req.begin(), per_req.end());
    sort(asize.begin(), asize.end());
    long i=0;
    long j=0;
    while(i<n && j<m){
        if(asize[j]< per_req[i]-k){
            j++;
        }
        else if(asize[j]>per_req[i] + k){
            i++;
        }
        else{
            count++;
            i++;
            j++;
        }
    }
 
 
 
    cout<< count;
 
 
 
    return 0;
