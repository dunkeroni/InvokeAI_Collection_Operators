# Collection Math
Some basic list math operators for InvokeAI collection data.  
If both inputs are scalars, they will be converted to singleton lists.  
If one input is scalar and the other is a list, the scalar will become a list of that scalar with the same length as the other input.  
If both inputs are lists of different sizes, and the operation computes across both lists, then the result will be truncated based on the length of the shorter list.  
![image](https://github.com/dunkeroni/InvokeAI_Collection_Operators/assets/3298737/7dc80f7c-404f-4945-bbc0-75e0830b695a)  

![image](https://github.com/dunkeroni/InvokeAI_Collection_Operators/assets/3298737/4b26b3ad-dd96-44ea-8155-bdfcb1809836)  

