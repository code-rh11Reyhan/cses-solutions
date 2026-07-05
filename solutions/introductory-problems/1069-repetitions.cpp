#include <bits/stdc++.h>
using namespace std;
 
int main(){
    ios::sync_with_stdio(0);
    cin.tie(0);
    typedef long long l;
    string s;
    cin>> s;
    l MaxLen = 1;
    l count = 1;
    
    for(l i = 0; i<s.size(); i++){
        if(s[i] == s[i-1]){
            count++;
        }
        else{
            count = 1;
        }
        MaxLen = max(MaxLen, count);
    }
 
    cout << MaxLen;
 
    return 0;
}
