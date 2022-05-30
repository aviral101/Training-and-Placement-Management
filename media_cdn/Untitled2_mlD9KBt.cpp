#include<bits/stdc++.h>
using namespace std;

string StringChallenge(string str)
{
	int n = str.length();
	string s;
	for(int i = n-1;i>=-1;i--)
	{
		if(str[i] == ' ' || i==-1)
		{
			int j = i+1;
			while(str[j]!=' ' && j<n)
			{
				s.push_back(str[j]) ;
				j++;
			}
			s.push_back(' ');
		}
	}
	return s;
}

int main()
{
	string s;
	getline(cin,s);
	
	cout<<StringChallenge(s);
}
