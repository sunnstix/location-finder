from matplotlib import pyplot as plt

SPLITS = ["Train", "Validation"]
METRICS = ["Accuracy", "Loss"]

def config(attr):
    """
    Retrieves quries from config file. 
    """
    if not hasattr(config, "config"):
        with open("config.json") as f:
            config.config = eval(f.read())
    node = config.config
    for part in attr.split("."):
        node = node[part]
    return node

class TwitterPlotter():
    #Class that manages my matplotlib implementation
    def __init__(self,name):
        plt.ion()
        fig, self.axes = plt.subplots(1, 2, figsize=(20, 5))
        plt.suptitle(name)
        self.axes[0].set_xlabel("Epoch")
        self.axes[0].set_ylabel("Accuracy")
        self.axes[1].set_xlabel("Epoch")
        self.axes[1].set_ylabel("Loss")
        self.name = name

    def update(self, epoch, stats):
        colors = ["r", "b"]
        for i in range(len(METRICS)):
            for j in range(len(SPLITS)):
                idx = len(METRICS) * j + i
                if idx >= len(stats[-1]):
                    print('skipping')
                    continue
                self.axes[i].plot(
                    range(epoch - len(stats) + 1, epoch + 1),
                    [stat[idx] for stat in stats],
                    linestyle="--",
                    marker="o",
                    color=colors[j],
                )
            self.axes[i].legend(SPLITS[: int(len(stats[-1]) / len(METRICS))])
        plt.pause(0.00001)

    def save(self):
        plt.savefig("{}.png".format(self.name), dpi=200)

    def hold(self):
        plt.ioff()
        plt.show()

def logger(epoch, stats):
    """Print the train, validation, test accuracy/loss/auroc.

    Each epoch in `stats` should have order
        [val_acc, val_loss, val_auc, train_acc, ...]
    Test accuracy is optional and will only be logged if stats is length 9.
    """
    print("Epoch {}".format(epoch))
    for j, split in enumerate(SPLITS):
        for i, metric in enumerate(METRICS):
            idx = len(METRICS) * j + i
            if idx >= len(stats[-1]):
                continue
            print(f"\t{split} {metric}:{round(stats[-1][idx],4)}")