from matplotlib import pyplot as plt
STATE_ID = {
    'alabama': 1,
    'alaska': 2,
    'arizona': 3,
    'arkansas': 4,
    'california': 5,
    'colorado': 6,
    'connecticut': 7,
    'delaware': 8,
    'district of columbia': 9,
    'florida': 10,
    'georgia': 11,
    'hawaii': 12,
    'idaho': 13,
    'illinois': 14,
    'indiana': 15,
    'iowa': 16,
    'kansas': 17,
    'kentucky': 18,
    'louisiana': 19,
    'maine': 20,
    'maryland': 21,
    'massachusetts': 22,
    'michigan': 23,
    'minnesota': 24,
    'mississippi': 25,
    'missouri': 26,
    'montana': 27,
    'nebraska': 28,
    'nevada': 29,
    'new hampshire': 30,
    'new jersey': 31,
    'new mexico': 32,
    'new york': 33,
    'north carolina': 34,
    'north dakota': 35,
    'ohio': 36,
    'oklahoma': 37,
    'oregon': 38,
    'pennsylvania': 39,
    'rhode island': 40,
    'south carolina': 41,
    'south dakota': 42,
    'tennessee': 43,
    'texas': 44,
    'utah': 45,
    'vermont': 46,
    'virginia': 47,
    'washington': 48,
    'west virginia': 49,
    'wisconsin': 50,
    'wyoming': 51
}

SPLITS = ["Train", "Validation"]
METRICS = ["Accuracy", "Loss"]

def config(attr):
    """
    Retrieves the queried attribute value from the config file. Loads the
    config file on first call.
    """
    if not hasattr(config, "config"):
        with open("config.json") as f:
            config.config = eval(f.read())
    node = config.config
    for part in attr.split("."):
        node = node[part]
    return node

class TwitterPlotter():
    def __init__(self,name):
        plt.ion()
        fig, self.axes = plt.subplots(1, 3, figsize=(20, 5))
        plt.suptitle(name)
        self.axes[0].set_xlabel("Epoch")
        self.axes[0].set_ylabel("Accuracy")
        self.axes[1].set_xlabel("Epoch")
        self.axes[1].set_ylabel("Loss")
        #self.axes[2].set_xlabel("Epoch")
        #self.axes[2].set_ylabel("AUROC")
        self.name = name

    def update(self, epoch, stats):
        colors = ["r", "b"]
        for i, metric in enumerate(METRICS):
            for j, split in enumerate(SPLITS):
                idx = len(METRICS) * j + i
                if idx >= len(stats[-1]):
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