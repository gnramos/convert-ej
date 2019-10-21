#include <bits/stdc++.h>

using namespace std;


int main(){
   string s;
   getline(cin,s);
   int veiculo = 0;
   int busao = 0;
   for(int i=1;i<=s.size();i++){
      if(s[i-1]=='O'){
         busao++;
      }
      veiculo++;
      if(veiculo == 3 && busao==5){
         cout << "fizzbusao" << endl;
         busao = 0;
         veiculo = 0;
      }
      else if(veiculo == 3){
         cout << "fizz" << endl;
         veiculo = 0;
      }
      else if(busao == 5){
         cout << "busao" << endl;
         busao = 0;
      }
      else{
         cout << i << endl;
      }
   }
   return 0;
}
