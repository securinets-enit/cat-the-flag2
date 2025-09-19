# A minimal Solver Writeup 
### author: h1dr1

We are starting to confirm first that we have SSTI , we know 
the application is built with flask . so we proceed at 
constructing the payload.

By playing with the different fields in the form we can easily 
confirm that the application is vulnerable to SSTI 
by providing  ```{{7*7}}``` as a payload .

In the generation certificate feature we get 49 as a replacement 
of our first name field

As stated in the challenge description
the flag is in an environment variable called FLAG.

To know we have an arbitary attribute access we try to call in the length of the 
subclasses List : ```{{ ''.__class__.__mro__[1].__subclasses__()|length }}``` 

and this is proves the code execution 

This is minimal payload to get the flag (since the application
is flask we can get it using wapplyzer extension)

```{{ config.__init__.__globals__['os'].environ['FLAG'] }}```

I hope you enjoyed this challenge ;) always happy to have your feedbacks


