import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

import numpy as np

'''
#this line already exists in fit method of Model class
loss_history=[]
# add this line to fit method of Model class
plt.ion()
#input is updated loss_history after each loss calculation in fit method of Model class
'''
def visualization(loss_history, batches_loss_history=None):
    fig, ax1 = plt.subplots()
    plt.gca().cla()  # optionally clear axes
    if(batches_loss_history is not None):
        x=range(len(batches_loss_history))
        X=(np.array(x)+1)
        X=X/max(X)*len(loss_history) +0.5
        
        batches_loss_history=np.array(batches_loss_history)/max(batches_loss_history)*max(loss_history)
        plt.plot(X, batches_loss_history,'-', color='orange', linewidth=min(600/len(X),0.5))
        lines = [Line2D([0], [0], color=c, linewidth=3) for c in ['C0','orange']]
        plt.legend(lines, ['epoch loss', 'mini-batches loss'])#, bbox_to_anchor =(1, 1))
    
    # ax1.set_ylabel('epoch loss', color='C0')
    # ax1.plot(t, data1, color='C0')
    # ax1.tick_params(axis='y', labelcolor='C0')
    x=range(len(loss_history))
    X=np.array(x)+1
    plt.plot(X, loss_history, 'o-', color='C0', linewidth=3)
    
    plt.title("losses from epoch 1 to epoch " + str(len(loss_history)) + "")
    
    plt.draw()
    plt.pause(1)
    
'''
#add this line to fit method of Model class
plt.show(block=True)#to block closing the figure "optional", maintains reopenning the graph if closed
'''

# test
# for i in range(50):
#     loss_history+=[i**2-5-i]
#     visualization(loss_history)


# test 2
# loss_history=[1]*5 + [0.5]*5
# batches_loss_history=[2.5]*10+[2]*10+[1.5]*10+[1]*10+[0.5]*600
# visualization(loss_history, batches_loss_history)