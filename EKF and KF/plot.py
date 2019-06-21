import matplotlib.pyplot as plt


def Plot_compare(data_1,data_2,string_1='',string_2=''):
    #plt.plot(list(range(0,len(data))),data,'-',linewidth=2,color='b')
    line_up, = plt.plot(list(range(0,len(data_1))),data_1,'-',linewidth=1, color='r')
    line_down, = plt.plot(list(range(0,len(data_2))),data_2,'--',linewidth=1, color='k')
    plt.legend([line_up,line_down],[f'{string_1}',f'{string_2}'])
    plt.xlabel('k')
    #plt.ylabel('')
    #plt.title()
    plt.show()
    pass