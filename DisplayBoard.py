import numpy as np

def display(board,u_or_ai):
    print("   A B C D E F G H I J ")
    for i in range(board.shape[0]):
        row_str=str(i)+' ['
        for j in board[i,:]:
            if u_or_ai=='a' and j<2:
                row_str+='+'
            elif u_or_ai=='a' and j==2:
                row_str+='M'
            elif u_or_ai=='a' and j==3:
                row_str+='H'
            elif u_or_ai=='u' and j==0:
                row_str+='~'
            elif u_or_ai=='u' and j==1:
                row_str+='O'
            elif u_or_ai=='u' and j==2:
                row_str+='M'
            elif u_or_ai=='u' and j==3:
                row_str+='H'                
            else:
                row_str+=str(int(j))
            row_str+=' '
        row_str+=']'
        print(row_str)