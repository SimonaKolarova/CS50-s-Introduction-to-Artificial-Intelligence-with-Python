
A programme employing the Natural language toolkit (nltk) to determine the structure of a sentence (<i>i.e.</i>, a setence parser). Example sentences are provided in `Example sentences`.

#

Example: 
```
Input (sentence): She never said a word until we were at the door here.
```
```
Output (parsed sentence):

                                  S                                     
            ______________________|_____________                         
           |                      |             S                       
           |                      |     ________|_______                 
           S                      |    |                VP              
  _________|____                  |    |             ___|____________    
 |              VP                |    |            VP               |  
 |     _________|___              |    |    ________|___             |   
 |    |             VP            |    |   |            PP           |  
 |    |     ________|___          |    |   |     _______|___         |   
 NP   |    |            NP        |    NP  |    |           NP       |  
 |    |    |         ___|___      |    |   |    |        ___|___     |   
 N   Adv   V       Det      N    Conj  N   V    P      Det      N   Adv 
 |    |    |        |       |     |    |   |    |       |       |    |   
she never said      a      word until  we were  at     the     door here
```