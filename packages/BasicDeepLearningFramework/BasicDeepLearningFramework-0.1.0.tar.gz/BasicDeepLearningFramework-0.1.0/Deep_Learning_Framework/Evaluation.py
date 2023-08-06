#confusion matrix, accuracy , precision, recall, F1 score
epsilon = 0.000001


def calc_tn_forClass(class_no, classes):
    """calc tn for certain class number"""
    tn =0

    for i in range(len(classes)):
        if i == class_no:
            continue
        for j in range(len(classes[i])):
            if(j == class_no):
                continue
            tn += classes[i][j]
    return tn


def init_classes(num_classes):
    classes =[]
    for i in range(num_classes):
        classes.append([])

    for i in range(num_classes):
        for j in range (num_classes):
            classes[i].append(0)
    return classes



def confusion_matrix (label, predicted_value, num_class):
    """ takes label, predicted_value as vectors
        returns confusion matrix , tp, fp, tn, fn """
    # classes = list(range(num_class)) #0,1,2,3,4..

    classes = init_classes(num_class)

    # #initialize key,values  2d array
    # for i in classes:
    #     classes[i] = list(range(num_class))
    #
    #Build confusion matrix
    for i in range(len(label)):
        classes[label[i]][predicted_value[i]] += 1

    #compute tp
    tps = []
    for i in range(len(classes)):
        tp = classes[i][i]
        tps.append(tp)

    #compute tn
    tns = []
    for i in range(len(classes)):
        tn = calc_tn_forClass(i, classes)
        tns.append(tn)


    #compute fp
    fps = []
    fp =0
    for i in range(len(classes)):
        for j in range(len(classes)):
            if(i == j):
                continue
            fp += classes[j][i]
        fps.append(fp)

    #compute fn
    fns =[]
    fn = 0
    for i in range(len(classes)):
        for j in range(len(classes)):
            if(i == j):
                continue
            fn += classes[i][j]
        fns.append(fn)


    return classes, tps, fps, tns, fns

    


def accuracy (label, predicted_value, num_classes):
    """takes label , predicted_value as vectors
        return accuracy """

    _, tp, fp, tn, fn = confusion_matrix(label, predicted_value, num_classes)

    acc = 0
    for i in range(num_classes):
        acc += (tp[i]+tn[i]) / (tp[i]+fp[i]+tn[i]+fn[i])
    Accuracy = acc / num_classes
    return Accuracy


def precision (label, predicted_value, num_classes):
    """takes label , predicted_value as vectors
        return precision """

    _, tp, fp, tn, fn = confusion_matrix(label, predicted_value, num_classes)
    print(tp)
    print(fp)
    per = 0
    for i in range(num_classes):
        per += (tp[i] ) / (tp[i] + fp[i] + epsilon)
    Precision = per / num_classes
    return Precision


def recall (label, predicted_value, num_classes):
    """takes label , predicted_value as vectors
        return recall """

    _, tp, fp, tn, fn = confusion_matrix(label, predicted_value, num_classes)

    rec = 0
    for i in range(num_classes):
        rec += (tp[i]) / (tp[i]+fn[i])
    Recall = rec / num_classes
    return Recall


def F1_score(label, predicted_value, num_classes):
    """takes label , predicted_value as vectors
        return F1_score """

    Precision = precision(label, predicted_value, num_classes)
    Recall = recall(label, predicted_value, num_classes)
    F1 = 2 * (Precision * Recall)/(Precision + Recall)
    return F1


def print_2dlist(arr):

    idx = 0
    l = list(range(len(arr)))

    print(str('    ') + str(l))
    for i in arr:
        print(str(idx) +'-->' + str(i))
        idx +=1


if __name__ == '__main__':

    label =           [0,1,2,1,0]
    predicted_value = [0,1,1,1,2]

    out, tp, fp, tn, fn = confusion_matrix(label, predicted_value, 3)
    print_2dlist(out)
    print('tp: '+str(tp))
    print('tn: '+str(tn))
    print('fp: '+str(fp))
    print('fn: '+str(fn))
