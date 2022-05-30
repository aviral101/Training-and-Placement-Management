#include <bits/stdc++.h>
using namespace std;

int main()
{
	int n,c,d,ans = 0;
	string s;
	cin>>n;
	cin>>s;
	vector<vector<int>> a;
	vector<int> b(26,0);
	for(int i = 0;i<n;i++)
	{
		b[s[i] - 'a']++;
		a.push_back(b);
	}
	for(int i =0;i<n;i++)
	{
		b[s[i]-'a']--;
		int c=0;
		for(int j=9;j<26;j++)
			c+=min(b[j],a[i][j]);
		ans = max(ans,c);
	}
	cout<<ans;
	return 0;
}


