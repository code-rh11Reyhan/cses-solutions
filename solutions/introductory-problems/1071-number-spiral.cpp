#include <bits/stdc++.h>

using namespace std;




int main(){
    ios::sync_with_stdio(0);
    cin.tie(0);
    
    int t;
    cin>> t ;


    while(t--){
        long y;
        long x;
        cin>> y>> x;
        long long n = max(y, x);
        long long diagonal = (n*n) - (n-1);
        
        if(n&1){
            if(y == max(y, x)){
                int diff = n - x;
                cout<<  diagonal - diff<<"\n";
            }
            else{
                int diff = n-y;
                cout<<  diagonal + diff<<"\n";
            }
        }
        else{
            if(y == max(y, x)){
                int diff = n-x;
                cout<<  diagonal +diff<<"\n";

            }
            else{
                int diff = n-y;
                cout<< diagonal - diff<< "\n";
            }
        }


        

    }
    

    return 0;
}