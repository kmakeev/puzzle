from turple_repl import turple_repl

import numpy as np

def find_index(arr,value):
    #print ('In find_index')
    index = -1;
    #print(arr, value)
    for i in range(len(arr)):
        #print(arr[i])
        if np.array_equal(arr[i],value):
            index = i
    return index

def check_values(isFrom, isTo, sizeH, sizeV):

    #print('In check_values')
    #print('isFrom -', isFrom)
    #print('isTo -', isTo)
    graphs = np.array([])
    allgraphs = np.array([])
    train_y = 0
    best = False
    
    if np.array_equal(isFrom, isTo):
        #print('No go to itself')
        train_y = 0
        graphs = np.concatenate((isFrom, isTo))
        #print(graphs)
        #graphs.shape = (-1,16,2)
        allgraphs = np.append(allgraphs,[graphs,train_y])
        #print(allgraphs)
        #print(allgraphs[0],allgraphs[1])
    else:
        positionIsFrom = isFrom[sizeH*sizeV-1]
        positionIsTo = isTo[sizeH*sizeV-1]
        #print('Positions  ', positionIsFrom, positionIsTo)
        
        tmp = [positionIsFrom[0]-1,positionIsFrom[1]]
        #print('tmp Position', tmp, 'To - ', positionIsTo)
        if np.array_equal(tmp, positionIsTo):
            #print('Best position')
            train_y = 1
            isToTmp = np.array(isTo)
            i = find_index(isToTmp,tmp)
            if (i >=0):
                isToTmp[i] = isToTmp[sizeH*sizeV-1]
            isToTmp[sizeH*sizeV-1] = tmp
            #print('isToTMP - ', isToTmp)
            graphs = np.concatenate((isFrom, isToTmp))
            #print(graphs)
            #graphs.shape = (-1,16,2)
            allgraphs = np.append(allgraphs,[graphs,train_y])
            #print(allgraphs)
        
        tmp = [positionIsFrom[0]+1,positionIsFrom[1]]
        #print('tmp Position', tmp, 'To - ', positionIsTo)
        if np.array_equal(tmp, positionIsTo):
            #print('Best position')
            train_y = 1
            isToTmp = np.array(isTo)
            i = find_index(isToTmp,tmp)
            if (i >=0):
                isToTmp[i] = isToTmp[sizeH*sizeV-1]
            isToTmp[sizeH*sizeV-1] = tmp
            #print('isToTMP - ', isToTmp) 
            graphs = np.concatenate((isFrom, isToTmp))
            #print(graphs)
            #graphs.shape = (-1,16,2)
            allgraphs = np.append(allgraphs,[graphs,train_y])
            #print(allgraphs)

        tmp = [positionIsFrom[0],positionIsFrom[1]-1]
        #print('tmp Position', tmp, 'To - ', positionIsTo)
        if np.array_equal(tmp, positionIsTo):
            #print('Best position')
            train_y = 1
            isToTmp = np.array(isTo)
            i = find_index(isToTmp,tmp)
            if (i >=0):
                isToTmp[i] = isToTmp[sizeH*sizeV-1]
            isToTmp[sizeH*sizeV-1] = tmp
            #print('isToTMP - ', isToTmp) 
            graphs = np.concatenate((isFrom, isToTmp))
            #print(graphs)
            #graphs.shape = (-1,16,2)
            allgraphs = np.append(allgraphs,[graphs,train_y])
            #print(allgraphs)

        tmp = [positionIsFrom[0],positionIsFrom[1]+1]
        #print('tmp Position', tmp, 'To - ', positionIsTo)
        if np.array_equal(tmp, positionIsTo):
            #print('Best position')
            train_y = 1
            isToTmp = np.array(isTo)
            i = find_index(isToTmp,tmp)
            if (i >=0):
                isToTmp[i] = isToTmp[sizeH*sizeV-1]
            isToTmp[sizeH*sizeV-1] = tmp
            #print('isToTMP - ', isToTmp) 
            graphs = np.concatenate((isFrom, isToTmp))
            #print(graphs)
            #graphs.shape = (-1,16,2)
            allgraphs = np.append(allgraphs,[graphs,train_y])
        #print(allgraphs)
       
    return allgraphs
