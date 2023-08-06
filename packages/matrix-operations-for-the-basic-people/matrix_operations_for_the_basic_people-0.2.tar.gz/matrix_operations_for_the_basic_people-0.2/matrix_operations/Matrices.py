
class Matrix:
    
    def __init__(self,X,Y):
        
        """ Generic matrix class for basic matrix operations such as addition, subtraction and multiplication.
    
        Attributes:
        X - A matrice in the form of nested list.
        Y - Another matrice in the form of nested list. 
        """
        self.X = X
        self.Y = Y
    
    def add(self):
        
        """Function to perform addition of the matrices.
                
        Args:
            None
        
        Returns:
            Addition of the two matrices
        """
        
        if (len(self.X) == len(self.Y)) & (len(self.X[0]) == len(self.Y[0])):
            
            result = []
            for row in range(len(self.X)):
                result.append([x+y for x,y in zip(self.X[row], self.Y[row])])

            return result 
        else:
            print ("Input matrices have different dimensions, addition cannot be performed.")
            
    def subtract(self):
        
        """Function to perform subtraction of the matrices.
                
        Args:
            None
        
        Returns:
            Subtraction of the two matrices
        """
        if (len(self.X) == len(self.Y)) & (len(self.X[0]) == len(self.Y[0])):
            
            result = []
            for row in range(len(self.X)):
                result.append([x-y for x,y in zip(self.X[row], self.Y[row])])

            return result
        
        else:
            print ("Input matrices have different dimensions, subtraction cannot be performed.")
            
    def multiply(self):
        
        """Function to perform multiplication of the matrices.
                
        Args:
            None
        
        Returns:
            Multiplication of the two matrices
        """
        
        rows_dim = len(self.X)
        cols_dim = len(self.Y[0])
        
        #check if the number of columns of the first matrix is equal to the rows of the second matrice
        if len(self.X[0]) == len(self.Y):
            # Creating an empty nested list with zeros
            result = []
            for i in range(rows_dim): 

                # Append an empty sublist inside the list 
                result.append([]) 

                for j in range(cols_dim): 
                    result[i].append(0) 

            # Populating the nested list with product of matrices       
            for i in range(len(self.X)):
               # iterate through columns of Y
               for j in range(len(self.Y[0])):
                   # iterate through rows of Y
                   for k in range(len(self.Y)):
                       result[i][j] += self.X[i][k] * self.Y[k][j]

            return result

        else:
            print ("Input matrices have inconsistent dimensions, multiplication cannot be performed.")