import string,py_compile,inspect,re,itertools
from Tkinter import *
from tkFileDialog   import askopenfilename
from time import sleep

LOOPIF={re.compile('\s*from [\W\w]+ import [\w\W]+ ;'):1,re.compile('\s*import [\w\W]+ ;'):2,re.compile('\s*[if]*[elif]*[while]* [\w\W]+ :'):3,re.compile('\s*for \w+ in [\w\W]+ :'):4}

DATA={
'KEYWORDS':['False', 'class', 'finally', 'is', 'return', 'None', 'continue', 'for', 'lambda', 'try', 'True', 'from', 'nonlocal', 'while', 'and', 'del', 'global', 'not', 'with', 'as', 'elif', 'if', 'or', 'yield', 'assert', 'else', 'import', 'pass', 'break', 'except', 'in', 'raise']
,
'DELIMITER':{'(':'PRNTHSTRT',')':'PRNTHEND','{':'DICTSTRT','}':'DICTEND','[':'SQRSTR',']':'SQREND',';':'END',':':'CONT',"'":'STR','"':'STR'}
,
'OPERATORS':{'=':'ASSIGN','+':'ADD','-':'SUBTRACT','/':'DIVIDE','*':'MULTIPLY','%':'MOD','+=':'INCREMENT','-=':'DECREMENT','/=':'DECDIV','*=':'INCMUL','%=':'DECMOD','<=':'LESSEQ','>=':'GRTEQ','==':'ISEQ','<':'LESSTHN','>':'GRTRTHN'}
}   

    
def check():
    '''
    This functions check for if the feeded source code compiles correctly

    Input - File
    Output - Boolean
    '''
    return bool(py_compile.compile("code.py"))  

def loopif(x):
    '''
    This functions tokenizes the special cases with looping and conditional constructs. The function takes in a list tokenizes the possible feeds and returns a list 

    Input - List
    Output - List
    '''
    for i in range(len(x)):
        for y in LOOPIF :
            if re.match(y,x[i]):
                case=LOOPIF[y]
                if case == 1 :
                    #This to match a python statement importing module
                    a=x[i].split()
                    x[i] =  [{'KEYWORD':a[0]},{'MODULE':a[1]},{'KEYWORD':a[2]},{'FUNCTIONS':' '.join(a[3:-1])},{'END':';'}]
                if case == 2 :
                    #This to match a python statement importing module
                    a=x[i].split()
                    x[i] = [{'KEYWORD':a[0]},{'MODULE':' '.join(a[1:-1])},{'END':';'}]
                if case == 3 :
                    #This to match a while loop or conditional constructs
                    a=x[i].split()
                    x[i] = [{'KEYWORD':a[0]},{'CONDITION':' '.join(a[1:-1])},{'CONT':':'}]
                if case == 4 :
                    #This to match a python for loop
                    a=x[i].split()
                    x[i] = [{'KEYWORD':a[0]},{'TARGET':a[1]},{'KEYWORD':a[2]},{'EXPRESSION':' '.join(a[3:-1]  )},{'CONT':':'}]
                break
    return x

def toklex(l):
    '''
    This functions does the final tokenization of general cases. The function takes in a list tokenizes the possible feeds and returns a list 

    Input - List
    Output - List
    '''
    funcStream=list()
    userD=False
    for x in range(len(l)):
        if str(type(l[x]))==str("<type 'str'>"):
            stream=list()
            l[x]=l[x].split()
            for i in l[x]:
                if i == 'def':
                    userD=True
                elif userD:
                    userD=False
                    stream.append({"USER-DEFINED":i}) 
                elif inspect.isroutine(i):
                    stream.append({"FUNCTION":i})
                elif i in DATA['KEYWORDS']:
                    stream.append({"KEYWORD":i})
                elif DATA['DELIMITER'].has_key(i):
                    stream.append({DATA["DELIMITER"][i]:i})
                elif DATA['OPERATORS'].has_key(i):
                    stream.append({DATA["OPERATORS"][i]:i})
                else:
                    stream.append({"VARIABLE":i})
            l[x]=stream    
    return l

                 
 
def seperate(x):
    '''
    This functions maniuplates the whitespaces for easy understanding of code.

    Input - String
    Output - String
    '''
    x=x.replace('\n\n','\n')
    x=x.replace('\n',' ;\n')
    x=x.replace(': ;\n',':\n')
    x=x.replace('    ',' ')
    x=x.split('\n')
    return x


def sourceCode():
    '''
    This functions takes in a python source code file and returns the tokenized list for the given python source code. Tokens returned are of the form { TOKEN : LEXEME }.

    Input - File
    Output - List
    '''
    sCode=open("code.py",'r')
    sCode=sCode.read()
    sCode=seperate(sCode)
    sCode=loopif(sCode)
    sCode=toklex(sCode)   
    sCode=sum(sCode,[])
    return sCode


def main():
    root=Tk()
    root.iconbitmap('icon.ico')
    root.state('zoomed')
    root.configure(background='White')
    root.title('pyCode Tokenizer')
    l1=Label(text='pyCode Tokenizer',pady='20m',font=('Nexa Light', 48),fg='#1E2847',bg='White').pack()
    lm1=Label(text='Welcome User !!\n\nThis "pyTokenizer" is a program to tokenize any good scripted python source code given by you.\nTo do this locate the desired file in the current directory with the name of code.py.\n\nEfforts by\nShubh Bansal and Harshit Jain\nClass XI - A',font=('Nexa Light', 18),fg='#1E2847',bg='White').pack()
    
    l2=Label(text='Close And Go To Your Shell',pady='30m',font=('Nexa Light', 24),fg='#1E2847',bg='White').pack()
    
    root.mainloop()
    check()
    pairs=sourceCode()
    a=raw_input("Press 'Y' and then 'Enter'  :       ")
    for i in pairs :
        for y in i:
            print y ,'  :  ',i[y]
            sleep(0.01)
    print '\n\nCode in file "code.py" TOKENIZED !!\nThank You !!'

main()
