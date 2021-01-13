

# =============================================================================
#流程
#确定base（结束条件）情况
# for 选择 in 选择列表:
    # 做选择
    # 将该选择从选择列表移除
    # 路径.add(选择)
    # backtrack(路径, 选择列表)
    # 撤销选择
    # 路径.remove(选择)
    # 将该选择再加入选择列表
# =============================================================================
# In[Leetcode 46 全排序]
class Solution:
    def permute(self, nums):
        results = []

        def backward(res, nums):
            if len(res) == len(nums):
                #注意这里必修保存的是res的副本，因为事实上就一个res
                #这些结过都是递归产生，他们是共享同一片存储空间
                results.append(res[::1])
                return

            for i in (set(nums) - set(res)):
                res.append(i)
                backward(res, nums)
                res.pop()

        backward([], nums)
        return results


print(Solution().permute([1,2,3,4,5,6,7]))

# =============================================================================
# In[八皇后]
class Solution:
    def solveNQueens(self, n: int):
        results = []
        board = [['.' for i in range(n)] for i in range(n)]


        def backward(board, row):
            if row == n:
                results.append(list([''.join(i) for i in board]))
                return
            
            for col in range(n):
                if  isvalid(board, row, col):
                    board[row][col] = 'Q'
                    backward(board, row+1) #下次决策
                    board[row][col] = '.'
            
        def isvalid(board, row, col):
            #判断每lie
            if 'Q' in [board[i][col] for i in range(n)]:
                return False
            #判断每行
            # if 'Q' in [board[row][i] for i in range(n)]:
            #     return False
            #判断左上角
            if 'Q' in [board[i][j] for i,j in zip(range(row-1, -1, -1), range(col-1, -1, -1))]:
                return False               
            #判断右上角
            if 'Q' in [board[i][j] for i,j in zip(range(row-1, -1, -1), range(col+1 ,n))]:
                return False
            return True
        
        backward(board, 0)
        return results
    

print(Solution().solveNQueens(14))
# =============================================================================
# In[双指针 #leetcode--76]
## 
from collections import Counter
class Solution:
    def minWindow(self, s: str, t: str) -> str:
        left, right = 0, 0
        min_len = float('Inf')
        need = Counter(t)
        window = dict()
        start, match =0, 0


        while right < len(s):
            char = s[right]
            right += 1
            if need.get(char):
                window[char]  = 1 + window.get(char, 0)
                if window[char] == need[char]:
                    match += 1
            
            while match == len(need):
                if right - left < min_len:
                    min_len = right - left
                    start = left
                char = s[left]
                if need[char]>0:
                    window[char] -= 1
                    if window[char] < need[char]:
                        match -= 1
                left += 1

        return s[start:start+min_len] if min_len != float('Inf') else ''
    

print(Solution().minWindow("ADOBECODEBANC", 'ABC'))

# In[双指针 #leetcode--567]
import collections
class Solution:
    def checkInclusion(self, s1: str, s2: str) -> bool:
        left, right = 0, 0
        need = collections.Counter(s1)
        window = {}
        match = 0


        while right < len(s2):
            char = s2[right]
            if need[char]:
                window[char] = 1 + window.get(char, 0)
                if window[char] == need[char]:
                    match += 1
            right += 1

            while match == len(need):
                if right - left == len(s1):
                    return True
                char = s2[left]
                if need[char] > 0:
                    window[char] -= 1
                    if window[char] < need[char]:
                        match -= 1
                left += 1
            
        return False
                
print(Solution().checkInclusion("ab","eidbaooo"))

# In[双指针 #leetcode--438]
class Solution:
    def findAnagrams(self, s: str, p: str):
        left, right = 0,0
        need = collections.Counter(p)
        window = {}
        match = 0
        results = []
        start = 0

        while right < len(s):
            char = s[right]
            if need[char]:
                window[char] = 1 + window.get(char, 0)
                if window[char] == need[char]:
                    match+=1
            right += 1

            while match == len(need):
                if right - left == len(p):
                    start = left
                    results.append(start)
                char = s[left]
                if need[char] > 0:
                    window[char] -= 1
                    if window[char] < need[char]:
                        match -= 1
                left += 1
        
        return results
    
# In[]

class Solution:
    def lengthOfLongestSubstring(self, s: str) -> int:
        left, right = 0, 0
        window = []
        match = 0
        res = 0

        while  right < len(s):
            char = s[right]
            window.append(char)
            if char in window:
                match = 1
            right += 1
            
            while match:
                if len(window) == len(set(window)):
                    match = 0
                else:
                    char = s[left]
                    if char in window:
                        window = window[1:]
                    left += 1
                
            res = max(res, right-left)
        return  res
    
    def lengthOfLongestSubstring2(self, s: str) -> int:
        left, right = 0, 0
        window = collections.Counter()
        res = 0

        while  right < len(s):
            ch = s[right]
            window[ch] += 1
            right += 1
            
            while window[ch]>1:
                char = s[left]
                window[char] -= 1
                left += 1

            res = max(res, right-left) #区间是左开右闭的
        return  res
    
print(Solution().lengthOfLongestSubstring2("abcabcbb"))

# In[]