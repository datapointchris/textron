import functools
import time

import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.colors import LogNorm
from sklearn.metrics import confusion_matrix


def function_timer(func):
    """Prints runtime of the decorated function."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        value = func(*args, **kwargs)
        elapsed_time = time.time() - start_time
        print(
            f"Elapsed time: {round(elapsed_time/60,2)} minutes for function {repr(func.__name__)}")
        return value
    return wrapper


def plot_confusion_matrix(model, y_true, y_pred, classes, cmap='Blues'):
    '''
    Plots confusion matrix for fitted model, better than scikit-learn version
    '''
    cm = confusion_matrix(y_true, y_pred)
    fontdict = {'fontsize': 16}
    fig, ax = plt.subplots(figsize=(2.2 * len(classes), 2.2 * len(classes)))

    sns.heatmap(cm,
                annot=True,
                annot_kws=fontdict,
                fmt="d",
                square=True,
                cbar=False,
                cmap=cmap,
                ax=ax,
                norm=LogNorm(),  # to get color diff on small values
                vmin=0.00001  # to avoid non-positive error for '0' cells
                )

    ax.set_xlabel('Predicted labels', fontdict=fontdict)
    ax.set_ylabel('True labels', fontdict=fontdict)
    ax.set_yticklabels(
        labels=classes, rotation='horizontal', fontdict=fontdict)
    ax.set_xticklabels(labels=classes, rotation=20, fontdict=fontdict)
    ax.xaxis.set_ticks_position('top')
    ax.xaxis.set_label_position('top')
