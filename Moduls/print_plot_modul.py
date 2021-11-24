"""print Module
"""
import matplotlib.pyplot as plt


def print_plot(result):
    """ Method to print Result
    :param Dataframe result
    """
    data1 = result.loc[:, ['Stock_Close']]
    data2 = result.loc[:, ['vix_Close']]
    fig, ax1 = plt.subplots()
    data1["SMA1"] = data1['Stock_Close'].rolling(window=20).mean()
    data1["SMA2"] = data1['Stock_Close'].rolling(window=60).mean()

    color = 'tab:blue'
    ax1.set_xlabel('time')
    ax1.plot(data1['Stock_Close'], color=color)
    ax1.plot(data1['SMA1'], 'g--', label="SMA1", alpha=0.7)
    ax1.plot(data1['SMA2'], 'r--', label="SMA2", alpha=0.7)
    ax1.legend()
    ax1.set_ylabel('index', color=color)

    ax2 = ax1.twinx()
    color = 'tab:grey'
    # we already handled the x-label with ax1
    ax2.set_ylabel('volatility', color=color)
    ax2.plot(data2, color=color)
    ax2.tick_params(axis='y', labelcolor=color)
    ax2.axhline(y=20, color='b', linestyle='-')
    fig.tight_layout()
    plt.show()
