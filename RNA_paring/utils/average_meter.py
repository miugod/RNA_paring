class AverageMeter(object):
    """Computes and stores the average and current value"""

    def __init__(self):
        self.val = 0
        self.avg = 0
        self.sum = 0
        self.max = 0
        self.min = 2147483647
        self.count = 0

    def update(self, val, n=1):
        self.val = val
        self.sum += val * n
        self.max = max(self.max, val)
        self.min = min(self.min, val)
        self.count += n
        self.avg = self.sum / self.count
